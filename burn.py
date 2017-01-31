import sys, os, glob, stat, subprocess

def main():
    if len(sys.argv) != 3:
        print("Usage: {0} <number_of_copies> <path_to_iso_file>".format(argv[0]))
        return 1

    number_of_copies = int(sys.argv[1])
    path_to_iso = str(sys.argv[2])

    raw_output = subprocess.Popen("ls /dev/sr* -x -1 | wc -l", stdout = subprocess.PIPE, shell = True)

    device_count = int(raw_output.stdout.read())
    copies_per_device = number_of_copies // device_count
    devices_doing_one_more = number_of_copies % device_count

    print("Found", device_count, "devices")
    print("Requested", number_of_copies, "copies")
    print(device_count - devices_doing_one_more, "devices doing", copies_per_device, "copies")
    if devices_doing_one_more:
        print("and", devices_doing_one_more, "devices doing", repr(copies_per_device + 1), "copies")

    raw_output = subprocess.Popen("sudo sg_map -sr", stdout = subprocess.PIPE, shell = True)
    dev_map = raw_output.stdout.read().splitlines()
    count = 0

    print("Removing old burn-instance-* files")
    for file in glob.glob("burn-instance-*"):
        os.remove(file)

    print("Creating new burn-instance-* files:")
    for entry in dev_map:
        mapping = entry.split()
        if len(mapping) == 2:
            mapping[0] = mapping[0].decode()
            mapping[1] = mapping[1].decode()

            filename = "burn-instance-{0}".format(count)
            file = open(filename, "w+")

            needs_extra = 0
            if count < devices_doing_one_more:
                needs_extra = 1

            file.write("#!/bin/bash\n")
            file.write("python3 burn-device.py {1} {2} {3} {4}".format(count, mapping[1], mapping[0], copies_per_device + needs_extra ,path_to_iso))
            file.close()

            filestat = os.stat(filename)
            os.chmod(filename, filestat.st_mode | stat.S_IEXEC)

            print("burn-dev-{0}: python3 burn-device.py {1} {2} {3} {4}".format(count, mapping[1], mapping[0], copies_per_device + needs_extra ,path_to_iso))
            count += 1

    print("Done, happy burning")

if __name__ == "__main__":
    main()
