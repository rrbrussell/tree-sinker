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
import os

def clean_string(str):
    return str.lower().strip()

def clean_hostname(hostname):
    hostname = clean_string(hostname)
    hostname = hostname.rstrip('/')
    if not hostname.startswith(('http://', 'https://')):
        return 'http://{0}'.format(hostname)
    return hostname

def clean_intermediate_path(directory):
    return clean_string(directory).strip('/')

def clean_repo_name(repo):
    return clean_string(repo).strip('/')

def build_full_url(hostname, directory, repo):
    hostname = clean_hostname(hostname)
    directory = clean_intermediate_path(directory)
    repo = clean_string(repo)
    return '{0}/{1}/{2}.sqfs'.format(hostname, directory, repo)

def confirm_and_open_file(path, read_write=False):
    """
    Hello no documentation.

    :param path: The path of the file you want to open.
    :type path: str
    :returns: Either NONE or a useable file object
    :rtype: object
    """
    flags = os.O_NOFOLLOW
    if read_write:
        flags = os.O_RDWR | flags
    else:
        flags = os.O_RDONLY | flags
    try:
        descriptor = os.open(path, flags)
        return open(descriptor)
    except FileNotFoundError:
        return None
    except PermissionError:
        return None

#End of buffer
