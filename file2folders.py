#!/usr/bin/python

import sys, os
import optparse
import logging
from logging import handlers

FULLFORMAT = "%(asctime)s  [%(levelname)s]  [%(module)s] %(message)s"
logger = logging.getLogger()
delimiters = ". _"

def file2folder(directory, simulate):
    for entry in os.

def main():
    # Setup the command line arguments.
    optp = optparse.OptionParser()
    # options.
    optp.add_option("-d", "--directory", dest="dir",
                    help="directory to parse.")

    optp.add_option("-v", "--verbose", dest="verbose",
                    help="log verbosity.", action="store_true", default=False)

    optp.add_option("-s", "--simulate", dest="simulate",
                    help="do nothing, just simulate.", action="store_true", default=False)

    opts, args = optp.parse_args()

    if opts.verbose in (None, False):
        loglevel = logging.INFO
    else:
        loglevel = logging.DEBUG

    # log to stderr in fg
    logging.basicConfig(level=loglevel,
                        format=FULLFORMAT)

    logger.debug("init")

if __name__ == "__main__":    
    main()
