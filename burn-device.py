import subprocess, sys, os, time
from colorama import Fore, Back, Style


def eject_tray(srdev):
    return subprocess.call(["eject", srdev])

def check_media_loaded(srdev):
    trashcan = open(os.devnull, 'w')
    return subprocess.call(["./checkmedialoaded", srdev], stdout = trashcan)

def burn(sgdev, file_to_burn):
    return subprocess.Popen("wodim -v -eject -data -gracetime=2 speed=16 dev='{0}' {1}".format(sgdev, file_to_burn), shell = True)

def main():
    if len(sys.argv) != 5:
        print("Usage: {0} srdev sgdev copies file_to_burn".format(sys.argv[0]))
        print("i.e. {0} /dev/sr0 /dev/sg0 100 /home/burn/dvd.iso".format(sys.argv[0]))
        print("sgdev is used for burning as it is faster, make sure srdev and sgdev correspond to the same optical drive!")
        return 1

    srdev = str(sys.argv[1])
    sgdev = str(sys.argv[2])
    copies_requested = int(sys.argv[3])
    file_to_burn = str(sys.argv[4])
    copies_finished = 0

    if check_media_loaded(srdev) != 0:
        eject_tray(srdev)

    burning = copies_finished < copies_requested

    while burning:
        print(Fore.YELLOW, "Copy {0}/{1}: Waiting for media to be loaded in drive {2} ({3})".format(copies_finished + 1, copies_requested, srdev, sgdev), Style.RESET_ALL, sep='')
        while check_media_loaded(srdev) != 0:
            print('.', end = '')
            time.sleep(2)

        print(Fore.GREEN, "Copy {0}/{1}: Starting on drive {2} ({3})".format(copies_finished + 1, copies_requested, srdev, sgdev), Style.RESET_ALL, sep='')

        burn_process = burn(sgdev, file_to_burn)

        if burn_process.wait() == 0:
            copies_finished += 1

            print(Fore.WHITE, Back.GREEN, "Copy {0}/{1}: Burn complete".format(copies_finished, copies_requested), Style.RESET_ALL, sep='')
            if copies_finished >= copies_requested:
                print(Fore.GREEN, sep = '', end = '')
                burning = bool(input("All copies completed, do you want to burn one more? (y/n)") == "y")
                print(Style.RESET_ALL, sep = '', end = '')
            time.sleep(2)
    
    return 0

if __name__ == "__main__":
    main()
