#
#Copyright (C) 2025 Robert R. Russell
#
#This program is free software; you can redistribute it and/or modify it under
#the terms of the GNU General Public License as published by the Free Software
#Foundation; version 2.
#
#This program is distributed in the hope that it will be useful, but WITHOUT ANY
#WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
#PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License along with
#this program; if not, write to the Free Software Foundation, Inc., 51 Franklin
#Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
import argparse
import os
import sys
import typing
from configparser import ConfigParser
from hashlib import blake2b

import requests

import tree_sinker.support

ap_description = '''
%(prog)s is a program for syncronizing compressed read only Portage
trees from a central server.
'''

ap_epilog = '''
For more information about using tree-sinker please see the github at
https://github.com/rrbrussell/tree-sinker/.
'''

permission_error_message = 'Unable to read from or write to a file or\
 directory that I should be able to.'

def main_cli(argv=sys.argv):
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description = ap_description,
        epilog = ap_epilog);
    parser.add_argument("repository_name",
                        help="The repository name that you want to syncronize.");
    args = parser.parse_args();
#    response = requests.head(
#        'http://mars.private.rrbrussell.com/portage_trees/gentoo-latest.sqfs');
    blake_hash = blake2b();
    try:
        config = ConfigParser();
        with open('/etc/tree-sinker.ini','r') as etc_config:
            config.read_file(etc_config);
        print(config);
        print(_check_configuration(config));
    except PermissionError as e:
        print(permission_error_message);
        print(e);
    except FileNotFoundError as e:
        print('Unable to open an expected file.');
        print(e);
        sys.exit(1);
    finally:
        sys.exit(0);

# Nested if statements aren't the friendliest way to do this.
def _check_configuration(config: ConfigParser) -> bool:
    if config == None:
        print('''/etc/tree_sinker.ini exists but it doesn't contain any \
configuration
data. Please fix. See the man page for more information about the configuration
file.''');
        return False;
    else:
        if 'server' in config['fetch from'] and 'path' in config['fetch from']:
            if 'repos_dir' in config['store into']:
                # There is an entry in the configuration file.
                # Does it exist in the directory tree and is it writeable for
                # me.
                if _check_directory(config['store into']['repos_dir']):
                    return True;
                else:
                    print('''The repos_dir entry in /etc/tree_sinker.ini either \
does not exist or is not
writable. Please fix. See the man page for more information about the
configuration file.''');
                    return False;
            else:
                # There is no entry in the configuration file. The configuration
                # file has an issue.
                print('''/etc/tree_sinker.ini is missing the [store into] \
section or the 'repos_dir'
key is not set correctly. Please fix. See the man page for more information about
the configuration file.''');
                return False;
        else:
            # The configuration file is missing the [fetch from] section or the
            # correct keys in that section.
            print('''/etc/tree_sinker.ini is missing the correct [fetch from]\
 section or the
'server' and 'path' keys are not set correctly in it. Please fix. See the man
page for more information about the configuration file.''');
            return False;
    return True;

# Confirms that a directory exists and we can write into it.
# 
# Okay python's file system library is not ergonomic. I don't see the
# reason to create an entire library for decoding file system permissions.
# We will do this the easy way. Can I create a hidden test
# file under the provided path. If yes then we are good to go if not then
# return false.

def _check_directory(name: str) -> bool:
    if os.path.isdir(name):
        try:
            handle = open(os.path.join(name, '.hidden'), 'x')
            handle.close();
            os.remove(os.path.join(name, '.hidden'));
            return True;
        except:
            return False;
    else:
        return False;


'''
[fetch from]
server = http://server.example.com
#The path on the server to the directory containing the compressed repos.
#The repos are expected to be named <repo>-latest.sqfs and <repo>-latest.b2sum
path = /directory/directory2

[store into]
#The local directory where the compressed repos are stored.
#This is assumed to be /var/db/repos by default. If you change this
#you will need to modify the .mount units to use the correct path.
repos_dir = /var/db/repos
'''
# End of buffer
