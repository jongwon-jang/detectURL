#!/usr/bin/env python3

'''
detectURL v0.1

Detect links within a file and prints whether the link is dead or not
'''

import sys
import re
import requests
from colorama import Fore
import argparse

# https://docs.python.org/2/library/argparse.html
# https://docs.python.org/3/howto/argparse.html
parser = argparse.ArgumentParser()
parser.add_argument("FILE", nargs="?", help="FILE NAME YOU WANT TO CHECK")
parser.add_argument(
    "-v",
    "--version",
    help="VERSION INFO",
    action="version",
    version="detectURL v0.1"
)
args = parser.parse_args()


def initialize():

    with open(sys.argv[1]) as file:
        urls = []

        for line in file:
            url = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', line)
            [urls.append(final) for final in url if final not in urls]

        for link in urls:
            try:
                r = requests.get(link, timeout=1.5)
                if r.status_code == 200:
                    print(Fore.GREEN + "GOOD - " + str(link))
                r.raise_for_status()
            except requests.exceptions.HTTPError as e:
                status_code = e.response.status_code
                if status_code == 400 or 404:
                    print(Fore.RED + "BAD - " + link)
                else:
                    print(Fore.WHITE + "UNKNOWN - " + link)
            except requests.exceptions.ConnectionError:
                print(Fore.WHITE + "UNKNOWN - " + link)
            except requests.exceptions.Timeout:
                print(Fore.RED + "BAD - " + link)

        print(Fore.RESET)


# https://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
if len(sys.argv) < 2:
    parser.print_usage()
    sys.exit(1)

if sys.argv[1]:
    initialize()

if __name__ == "__main__":
    initialize()
