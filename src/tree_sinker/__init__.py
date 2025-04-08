import argparse
from hashlib import blake2b
import os
import requests
import sys
import tree_sinker.support
from tree_sinker.packer import packer_cli


ap_description = '''
%(prog)s is a program for syncronizing compressed read only Portage
trees from a central server.
'''

ap_epilog = '''
For more information about using tree-sinker please see the github at
https://github.com/rrbrussell/tree-sinker/.
'''

def main_cli(argv=sys.argv):
    parser = argparse.ArgumentParser(
        description = ap_description,
        epilog = ap_epilog)
    parser.add_argument("repository_name",
        help="The repository name that you want to syncronize.")
    args = parser.parse_args()
    response = requests.head(
        'http://mars.private.rrbrussell.com/portage_trees/gentoo-latest.sqfs')
    blake_hash = blake2b()
    config = configparser.ConfigParser()
    config['fetch from'] = {'server': 'https://server.example.com',
                            'path': '/directory1/directory2'}
    config['store into'] = {'repos_dir': '/var/db/repos'}
    config.read('./etc/tree-sinker.ini')
    
    
# End of File
