import argparse
import sys

ap_description = '''
%(prog)s is a program for syncronizing compressed read only Portage
trees from a central server.
'''

ap_epilog = '''
For more information about using tree-sinker please see the github at
https://github.com/rrbrussell/tree-sinker/.
'''

def main_cli(argv=sys.argv):
    print(argv)
    parser = argparse.ArgumentParser(
        description = ap_description,
        epilog = ap_epilog)
    parser.add_argument("repository_name",
        help="The repository name that you want to syncronize.")
    args = parser.parse_args()
    print(args)
    print(args.repository_name)
# End of File
