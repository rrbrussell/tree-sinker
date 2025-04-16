#
# Copyright (C) 2025 Robert R. Russell
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
import argparse
from configparser import ConfigParser
import hashlib
import os
import requests
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import urlparse
from urllib.parse import ParseResult

ap_description: str = '''
%(prog)s is a program for syncronizing compressed read only Portage
trees from a central server.
'''

ap_epilog: str = '''
For more information about using tree-sinker please see the github at
https://github.com/rrbrussell/tree-sinker/.
'''

http_status_error_message: str = '''
Oops I got a 400 or 500 series status code from the server. The error is
printed out next to help your troubleshooting.
'''

permission_error_message: str = 'Unable to read from or write to a file or\
 directory that I should be able to.'


def main_cli(argv=sys.argv) -> int:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description=ap_description, epilog=ap_epilog)
    parser.add_argument("repository_name",
                        help="The repository name that you want to syncronize.")
    args = parser.parse_args()
    try:
        config: ConfigParser = ConfigParser()
        with open('/etc/tree-sinker.ini', 'r') as etc_config:
            config.read_file(etc_config)
        if _check_configuration(config):
            url: ParseResult = urlparse(config['fetch from']['server'])
            url = url._replace(path=config['fetch from']['path'])
            local_sqfs_name: str = \
                os.path.join(config['store into']['repos_dir'],
                             f'{args.repository_name}.sqfs')
            with open(local_sqfs_name, 'rb') as sqfs:
                local_hash: str = hashlib.file_digest(sqfs, 'blake2b') \
                  .hexdigest()
            blake2_url = \
                ''.join([url.geturl(),
                         f'/{args.repository_name}-latest.blake2b'])
            squashfs_url = \
                ''.join([url.geturl(),
                         f'/{args.repository_name}-latest.sqfs'])
            blake2_response = requests.get(blake2_url)
            # Raise any exceptions for error handling.
            blake2_response.raise_for_status()
            # Okay no errors
            blake2_hash, blake2_sqfs_name = blake2_response.text.split()
            blake2_sqfs_name = blake2_sqfs_name.lstrip('*')
            if local_hash == blake2_hash:
                # We have the latest file.
                # cleanup and then leave:
                blake2_response.close()
                return 0
            # We don't have the latest file.
            with tempfile.TemporaryDirectory(prefix='tree-sinker.') as temp_dir:
                os.chdir(temp_dir)
                squashfs_response = requests.get(squashfs_url)
                # Raise any exceptions for error handling.
                squashfs_response.raise_for_status()
                # Okay, no errors
                new_squashfile = open(blake2_sqfs_name, 'wb+')
                new_squashfile.write(squashfs_response.content)
                new_squashfile.flush()
                new_squashfile.seek(0)
                new_hash: str = hashlib.file_digest(new_squashfile, 'blake2b')\
                    .hexdigest()
                if not new_squashfile.closed:
                    new_squashfile.close()
                if blake2_hash != new_hash:
                    print("The new file does not match the expected hash sum.")
                    return 1
                unmount = subprocess.run(['umount'], local_sqfs_name)
                if unmount.returncode != 0:
                    print("Failed to unmount the current squashfs.")
                    return 1
                old_sqfs_name: str = \
                    os.path.join(config['store into']['repos_dir'],
                                 f'{args.repository_name}-old.sqfs')
                try:
                    os.remove(old_sqfs_name)
                except FileNotFoundError as _:
                    pass
                shutil.move(local_sqfs_name, old_sqfs_name)
                shutil.move(blake2_sqfs_name, local_sqfs_name)
                mount = subprocess.run(['mount'], local_sqfs_name)
                return mount.returncode
        else:
            print('Configuration file has errors.')
            sys.exit(1)
        print('stuff')
    except requests.HTTPError as e:
        print(http_status_error_message)
        print(e)
        return 1
    except PermissionError as e:
        print(permission_error_message)
        print(e)
        sys.exit(1)
    except FileNotFoundError as e:
        print('Unable to open an expected file.')
        print(e)
        sys.exit(1)
    finally:
        return 0


# Nested if statements aren't the friendliest way to do this.
#
# The point of this monstrosity is to check that the configuration file was
# read and has a probably usable configuration.
def _check_configuration(config: ConfigParser) -> bool:
    return True
    if config is None:
        print('''/etc/tree_sinker.ini exists but it doesn't contain any \
configuration
data. Please fix. See the man page for more information about the configuration
file.''')
        return False
    else:
        if 'server' in config['fetch from'] and 'path' in config['fetch from']:
            if 'repos_dir' in config['store into']:
                # There is an entry in the configuration file.
                # Does it exist in the directory tree and is it writeable for
                # me.
                if _check_directory(config['store into']['repos_dir']):
                    return True
                else:
                    print('''The repos_dir entry in /etc/tree_sinker.ini \
either does not exist or is not
writable. Please fix. See the man page for more information about the
configuration file.''')
                    return False
            else:
                # There is no entry in the configuration file. The
                # configuration file has an issue.
                print('''/etc/tree_sinker.ini is missing the [store into] \
section or the 'repos_dir'
key is not set correctly. Please fix. See the man page for more information
about the configuration file.''')
                return False
        else:
            # The configuration file is missing the [fetch from] section or the
            # correct keys in that section.
            print('''/etc/tree_sinker.ini is missing the correct [fetch from] \
section or the
'server' and 'path' keys are not set correctly in it. Please fix. See the man
page for more information about the configuration file.''')
            return False
    return True


# Confirms that a directory exists and we can write into it.
#
# Okay python's file system library is not ergonomic. I don't see the
# reason to create an entire library for decoding file system permissions.
# We will do this the easy way. Can I create a hidden test file under the
# provided path. If yes then we are good to go if not then return false.
def _check_directory(name: str) -> bool:
    if os.path.isdir(name):
        try:
            handle = open(os.path.join(name, '.hidden'), 'x')
            handle.close()
            os.remove(os.path.join(name, '.hidden'))
            return True
        except Exception:
            return False
    else:
        return False


# End of buffer
