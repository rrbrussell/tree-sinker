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
