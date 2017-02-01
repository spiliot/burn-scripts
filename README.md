# A (python3) script for burning cd/dvd copies on multiple drives in linux

These scripts help automate the process of burning copies of different discs on multiple drives for a project I received. It doesn't seem like there are any linux tools in recent distro versions to do this (as civilization is past burnable media nowadays) and manually doing it was out of the question.

Not much effort (euphemism for _no effort_) has been given to make these scripts robust for any other use case.

## Requirements

- Linux (tested on Ubuntu 16.04)
- Python 3
- At least one optical drive showing up as `/dev/srX`
- `wodim` for the actual disc burning (or any alternative that can be run from the CLI)
- [`checkmedia`](https://github.com/spiliot/checkmedia) to let us know if media is loaded
- `sg_map` tool from `sg3-utils` package (and super user authority to run it) to map `/dev/srX` to `/dev/sgX`. It seems `wodim` somehow works much faster when accessing `sgX` devices. Can be skipped if not the case.
- (optional but very handy) `tmux` to run different burning instances in the same window.

## How to burn

Call `burn.py` adding the number of required copies needed and the complete path to the ISO that is to be burned. It will scan the system and create X shell files called `burn-instance-X`, where X is the number of available cd/dvd writer drives (assuming readonly drives are extinct since at least a decade this will do fine). Example of use:
`python3 burn.py 100 /home/user/ubuntu.iso`

Now you can call each `burn-instance-X` individually in a terminal session, or use `tmux-start.sh` to open up 16 panes in a new tmux session/window and call the respective script in each pane.

## License

Freeware, public domain