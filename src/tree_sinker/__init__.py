import argparse
import sys

def main_cli(argv=sys.argv):
    print(argv)
    parser = argparse.ArgumentParser()
    parser.add_argument("repository_name", help="The repository name that you want me to syncronize.")
    args = parser.parse_args()
    print(args)
    print(args.repository_name)
# End of File
