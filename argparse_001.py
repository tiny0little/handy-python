#!/usr/bin/python3

import argparse


parser = argparse.ArgumentParser(description="Python test program")
parser.add_argument("-v", "--verbosity", type=int, default=0,
                    choices=[0, 1, 2], help="level of verbosity")
args = parser.parse_args()
print(f"v = {args.verbosity}")
