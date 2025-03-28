# Tree-Sinker

This is a small program that I am using to manage compressed readonly
copies of the Gentoo Portage tree and the various overalys that I use.
I am opening this program up under the terms of the GPL-2.0 only
license so other people can use it.

## Current status.

- [x] I can make a Python Wheel out of the package.
- [x] Default Systemd timers, mounts, and service files are provided.
- [x] Basic command line argument parsing. I mean basic.
- [ ] Correctly setup an installer for those files.
- [ ] Download a squashfs.
- [ ] Read a configuration file properly.
  - [x] I have a working test for the basic configparser api that I
  use.
  - [ ] Check if the file exists and handle errors.
- [ ] Tests.
  - [x] ConfigParser


## Dependencies

[argparse](https://docs.python.org/3/library/argparse.html)
[configparser](https://docs.python.org/3/library/configparser.html)