#!/usr/bin/env python
#main function 

if __name__ == '__main__':
    import sys
    import getopt
from test import process

args, sources = getopt.getopt(sys.argv[1:], '', 'shotdir=')
process(args,sources)