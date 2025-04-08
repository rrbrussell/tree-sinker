#!/usr/bin/env python3
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

import configparser
import sys

config = configparser.ConfigParser()
config['fetch.from'] = {'server': 'http://server.example.com',
                        'path': '/directory1/directory2'}
config['store.into'] = {'repos_dir': '/var/db/repos'}
config.write(sys.stdout);

def main_cli():
    print("Hello you have called tree-sinker");

