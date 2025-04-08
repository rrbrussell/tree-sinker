#!/usr/bin/env python3

import configparser
import sys

config = configparser.ConfigParser()
config['fetch.from'] = {'server': 'http://server.example.com',
                        'path': '/directory1/directory2'}
config['store.into'] = {'repos_dir': '/var/db/repos'}
config.write(sys.stdout);


def main_cli():
    print("Hello you have called tree-sinker");

