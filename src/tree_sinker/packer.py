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
import configparser
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import time

tp_description = '''
%(prog)s packages a portage tree into a squashfs for later consumption by
tree-sinker. See /usr/share/doc/tree-sinker/example-tree-packer.ini for
an example configuration file.
'''

tp_epilog = '''
For more information about using tree-packer please see the github at
https://github.com/rrbrussell/tree-sinker/.
'''

def packer_cli(argv=sys.argv):
    parser = argparse.ArgumentParser(
        description = tp_description,
        epilog = tp_epilog);
    parser.add_argument("repository_name",
        help="The repository name that you want to syncronize.");
    parser.add_argument("sync_uri",
        help="The upstream uri for synchronizing the repository.");
    parser.add_argument("repository_path",
        help="The local path the repository was synced into.");
    args = parser.parse_args();
    config = configparser.ConfigParser();
    config['store_into'] = {'htdocs': '/var/www/localhost/htdocs/portage_trees'};
    read_files = config.read('/etc/tree-packer.ini');
    htdocs = config['store_into']['htdocs'];
    squashfs_name = f'{args.repository_name}.sqfs';
    squashfs_date = time.strftime(f'{args.repository_name}-%Y-%m-%d.sqfs');
    squashfs_latest = f'{args.repository_name}-latest.sqfs';
    b2sum_date = time.strftime(f'{args.repository_name}-%Y-%m-%d.blake2b');
    b2sum_latest = f'{args.repository_name}-latest.blake2b';
    with tempfile.TemporaryDirectory(prefix='tree-packer.') as temp_dir:
        os.chdir(temp_dir);
        egencache = subprocess.run(['egencache', '--update', '--update-manifests',
        '--update-pkg-desc-index', '--sign-manifests', 'n', '--jobs=4',
        f'--repo={args.repository_name}']);
        if egencache.returncode == 0:
            mksquashfs = subprocess.run(['mksquashfs',
                args.repository_path, squashfs_name, '-e', '.git',
                '-comp', 'xz', '-all-time', 'now', '-force-uid', 'portage',
                '-force-gid', 'portage', '-no-exports', '-tailends',
                '-no-xattrs', '-noappend'], stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL);
            if mksquashfs.returncode == 0:
                # If this fails we want to go boom so the administator gets
                # error messages.
                with open(squashfs_name, 'rb') as squashfile:
                    digest1 = hashlib.file_digest(squashfile,
                        'blake2b').hexdigest();
                    _move_to_htdocs_and_fix_symlinks(htdocs=htdocs,
                                                     squashfs_digest=digest1,
                                                     squashfs_date=squashfs_date,
                                                     squashfs_latest=squashfs_latest,
                                                     squashfs_name=squashfs_name,
                                                     b2sum_date=b2sum_date,
                                                     b2sum_latest=b2sum_latest);
            else:
                sys.exit(1);
    #Done exit the program and trigger the magic cleanup.
    sys.exit(0);

def _move_to_htdocs_and_fix_symlinks(htdocs, squashfs_digest, squashfs_date,
                                    squashfs_latest, squashfs_name,
                                     b2sum_date, b2sum_latest):
    digest_line = f'{squashfs_digest} *{squashfs_date}';
    with open(b2sum_date,'w') as digest_file:
        digest_file.writelines(digest_line);
    shutil.move(squashfs_name, os.path.join(htdocs, squashfs_date));
    shutil.move(b2sum_date, os.path.join(htdocs, b2sum_date));
    os.chdir(htdocs);
    try:
        os.remove(b2sum_latest);
    except FileNotFoundError as error:
        pass
    os.symlink(src=b2sum_date, dst=b2sum_latest);
    try:
        os.remove(squashfs_latest);
    except FileNotFoundError as error:
        pass
    os.symlink(src=squashfs_date, dst=squashfs_latest);
