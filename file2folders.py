#!/usr/bin/python

import sys, os, shutil
import optparse
import logging

FULLFORMAT = "%(asctime)s  [%(levelname)s]  [%(module)s] %(message)s"
logger = logging.getLogger()
delimiters = ". _"

def file2folder(directory, rename=False, simulate=False):
    for dirname, _, filenames in os.walk(directory):
        for filename in filenames:
            fullfile = os.path.join(dirname, filename)
            name, extension = os.path.splitext(filename)
            for delimiter in delimiters:
                name = name.replace(delimiter, ".")
            subdirname = os.path.join(dirname, name)
            logger.info("mkdir %s" % subdirname)
            if not simulate:
                os.mkdir(subdirname)

            if rename:
                subdirname = "%s/%s" % (subdirname, os.path.join(name, extension))
            logger.info("mv %s %s" % (fullfile, subdirname))
            if not simulate:
                shutil.move(fullfile, subdirname)

def main():
    # Setup the command line arguments.
    optp = optparse.OptionParser()
    # options.
    optp.add_option("-d", "--directory", dest="directory",
                    help="directory to parse.")

    optp.add_option("-v", "--verbose", dest="verbose",
                    help="log verbosity.", action="store_true", default=False)

    optp.add_option("-s", "--simulate", dest="simulate",
                    help="do nothing, just simulate.", action="store_true", default=False)

    optp.add_option("-r", "--rename", dest="rename",
                    help="rename the file changing delimiters.", action="store_true", default=False)

    opts, args = optp.parse_args()

    loglevel = logging.INFO if opts.verbose in (None, False) else logging.DEBUG
    # log to stderr in fg
    logging.basicConfig(level=loglevel,
                        format=FULLFORMAT)

    logger.debug("init")
    if opts.directory is None:
        opts.directory = os.getcwd()
    file2folder(opts.directory, opts.rename, opts.simulate)
        

if __name__ == "__main__":    
    main()
