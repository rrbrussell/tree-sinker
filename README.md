# Tree-Sinker

This is a small program that I am using to manage compressed readonly copies of
the Gentoo Portage tree and the various overalys that I use. I am opening this
program up under the terms of the GPL-2.0 only license so other people can use
it.

## Current status.

- [x] I can make a Python Wheel out of the package.
- [x] Default Systemd timers, mounts, and service files are provided.
- [x] Basic command line argument parsing. I mean basic.
- [ ] Correctly setup an installer for those files.
- [ ] Download a squashfs.
  - [ ] Integrity checking of the downloaded squashfs.
     - [ ] Check if we actually need to download the squashfs in the first
     place. This now has a hard dependecy on the integrity checking operation.
- [ ] Read a configuration file properly.
  - [x] I have a working test for the basic configparser api that I use.
  - [ ] Check if the file exists
    - [ ] The support function to do the existance checking has been written and
    tested but it needs to be integrated into the main executable.
  - [ ] Correctly handle the appropriate errors.
- [ ] Tests.
  - [x] ConfigParser

### Currently working on:

I have expanded the documentation strings for main_cli. The next task I expect to
work on is using requests to handle the file fetching.

## Dependencies

[argparse](https://docs.python.org/3/library/argparse.html)
[configparser](https://docs.python.org/3/library/configparser.html)
[requests](https://requests.readthedocs.io/en/latest/)


## Notes and Brain downloads

This is where I stash notes about parts of the program including algorithm
snippets or other ideas.

### What is the best way of checksumming the squashfs files.

Two options. First a `gpg` signed checksum file probably using `b2sum`. Second is
to use `gpg` to create a signature file for the squashed file anyway.