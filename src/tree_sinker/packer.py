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
import typing

tp_description: str = '''
%(prog)s packages a portage tree into a squashfs for later consumption by
tree-sinker. See /usr/share/doc/tree-sinker/example-tree-packer.ini for
an example configuration file.
'''

tp_epilog: str = '''
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
    cfg: dict[str, str] = dict([]);
    cfg['htdocs'] = config['store_into']['htdocs'];
    cfg['squashfs_name'] = f'{args.repository_name}.sqfs';
    cfg['squashfs_date'] = time.strftime(f'{args.repository_name}-%Y-%m-%d.sqfs');
    cfg['squashfs_latest'] = f'{args.repository_name}-latest.sqfs';
    cfg['b2sum_date'] = time.strftime(f'{args.repository_name}-%Y-%m-%d.blake2b');
    cfg['b2sum_latest'] = f'{args.repository_name}-latest.blake2b';
    with tempfile.TemporaryDirectory(prefix='tree-packer.') as temp_dir:
        os.chdir(temp_dir);
        egencache = subprocess.run(['egencache', '--update', '--update-manifests',
        '--update-pkg-desc-index', '--sign-manifests', 'n', '--jobs=4',
        f'--repo={args.repository_name}']);
        if egencache.returncode == 0:
            mksquashfs = subprocess.run(['mksquashfs',
                args.repository_path, cfg['squashfs_name'], '-e', '.git',
                '-comp', 'xz', '-all-time', 'now', '-force-uid', 'portage',
                '-force-gid', 'portage', '-no-exports', '-tailends',
                '-no-xattrs', '-noappend'], stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL);
            if mksquashfs.returncode == 0:
                with open(cfg['squashfs_name'], 'rb') as squashfile:
                    cfg['squashfs_digest'] = hashlib.file_digest(squashfile,
                        'blake2b').hexdigest();
                    _move_to_htdocs_and_fix_symlinks(cfg);
            else:
                # Mksquashfs failed go boom so the administator gets the error
                # messages.
                sys.exit(1);
    #Done exit the program and trigger the magic cleanup.
    sys.exit(0);

def _move_to_htdocs_and_fix_symlinks(cfg: dict[str, str]):
    digest_line = f"{cfg['squashfs_digest']} *{cfg['squashfs_date']}";
    with open(cfg['b2sum_date'],'w') as digest_file:
        digest_file.writelines(digest_line);
    shutil.move(cfg['squashfs_name'], os.path.join(cfg['htdocs'],
                                                   cfg['squashfs_date']));
    shutil.move(cfg['b2sum_date'], os.path.join(cfg['htdocs'], cfg['b2sum_date']));
    os.chdir(cfg['htdocs']);
    try:
        os.remove(cfg['b2sum_latest']);
    except FileNotFoundError as error:
        pass
    os.symlink(src=cfg['b2sum_date'], dst=cfg['b2sum_latest']);
    try:
        os.remove(cfg['squashfs_latest']);
    except FileNotFoundError as error:
        pass
    os.symlink(src=cfg['squashfs_date'], dst=cfg['squashfs_latest']);
