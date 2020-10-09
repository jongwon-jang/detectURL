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

parser.add_argument(
    "--all",
    help="prints all urls",
    nargs="*"
)

parser.add_argument(
    "--good",
    help="prints good urls",
    nargs="*"
)

parser.add_argument(
    "--bad",
    help="prints bad urls",
    nargs="*"
)

args = parser.parse_args()


def initialize():
    with open(sys.argv[1]) as file:
        urls = []
        goodURLs = []
        badURLs = []
        unknownURLs = []

        for line in file:
            url = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', line)
            [urls.append(final) for final in url if final not in urls]

        for link in urls:
            try:
                r = requests.get(link, timeout=1.5)
                if r.status_code == 200:
                    goodURLs.append(link)
                r.raise_for_status()
            except requests.exceptions.HTTPError as e:
                status_code = e.response.status_code
                if status_code == 400 or 404:
                    # print(Fore.RED + "BAD - " + link)
                    badURLs.append(link)
                else:
                    # print(Fore.WHITE + "UNKNOWN - " + link)
                    unknownURLs.append(link)
            except requests.exceptions.ConnectionError:
                # print(Fore.WHITE + "UNKNOWN - " + link)
                unknownURLs.append(link)
            except requests.exceptions.Timeout:
                # print(Fore.RED + "BAD - " + link)
                badURLs.append(link)

        if args.good is not None:
            for goodLinks in goodURLs:
                print(Fore.GREEN + "GOOD - " + str(goodLinks))
            sys.exit(0)
        elif args.bad is not None:
            for badLinks in badURLs:
                print(Fore.RED + "BAD - " + str(badLinks))
            sys.exit(1)
        elif args.all is not None:
            allURLs = goodURLs + badURLs + unknownURLs
            for allLinks in allURLs:
                if allLinks in goodURLs:
                    print(Fore.GREEN + "GOOD - " + str(allLinks))
                elif allLinks in badURLs:
                    print(Fore.RED + "BAD - " + str(allLinks))
                elif allLinks in unknownURLs:
                    print(Fore.WHITE + "UNKONWN - " + str(allLinks))
            sys.exit(2)
        else:
            allURLs = goodURLs + badURLs + unknownURLs
            for allLinks in allURLs:
                if allLinks in goodURLs:
                    print(Fore.GREEN + "GOOD - " + str(allLinks))
                elif allLinks in badURLs:
                    print(Fore.RED + "BAD - " + str(allLinks))
                elif allLinks in unknownURLs:
                    print(Fore.WHITE + "UNKONWN - " + str(allLinks))
            sys.exit(2)


# https://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
if len(sys.argv) < 2:
    parser.print_usage()
    sys.exit(3)

if __name__ == "__main__":
    initialize()
