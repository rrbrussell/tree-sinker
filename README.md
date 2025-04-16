# Tree-Sinker

This is a small program that I am using to manage compressed readonly copies of
the Gentoo Portage tree and the various overalys that I use. I am opening this
program up under the terms of the GPL-2.0 only license so other people can use
it.

## Current status.

Stage 1 of testing is now being worked on.

## Dependencies

- [argparse](https://docs.python.org/3/library/argparse.html)
- [configparser](https://docs.python.org/3/library/configparser.html)
- [requests](https://requests.readthedocs.io/en/latest/)
- [shutil](https://docs.python.org/3/library/shutil.html)
- [subprocess](https://docs.python.org/3/library/subprocess.html)
- [tempfile](https://docs.python.org/3/library/tempfile.html)
- [urllib](https://docs.python.org/3/library/urllib.html)

## Notes and Brain downloads

This is where I stash notes about parts of the program including algorithm
snippets or other ideas.

### Areas for improvement

- The error handling definitely needs some work. Python is not the most
ergonomic programming language to work with in my opinion.
