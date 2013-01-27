#!/usr/bin/python

import sys, os, shutil
import re
import optparse
import logging

FULLFORMAT = "%(asctime)s  [%(levelname)s]  [%(module)s] %(message)s"
BASICFORMAT = "%(message)s"
logger = logging.getLogger()
delimiters = " _"
multicd = re.compile(r".cd\d", re.IGNORECASE)

def file2folder(directory, simulate=False):
    root = os.path.abspath(directory)
    for filename in os.listdir(root):
        if os.path.isfile(os.path.join(directory, filename)):
            fullfile = os.path.join(root, filename)
            name, extension = os.path.splitext(filename)
            for delimiter in delimiters:
                name = name.replace(delimiter, ".")
            # renaming quirks:
            name = name.replace(":.", ":")
            # find multiple cd files and group them
            match = multicd.search(name)
            endname = name.replace(match.group(), "") if match else name
            subdirname = os.path.join(root, endname)
            if not os.path.isdir(subdirname):
                logger.debug("mkdir %s" % subdirname)
                if not simulate:
                    os.mkdir(subdirname)

            # rename the file:
            subdirname = "%s/%s%s" % (subdirname, name, extension)
            logger.debug("mv %s %s" % (fullfile, subdirname))
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

    opts, _ = optp.parse_args()

    loglevel = logging.DEBUG if opts.simulate or opts.verbose else logging.INFO
    logformat = FULLFORMAT if opts.verbose else BASICFORMAT
    # log to stderr in fg
    logging.basicConfig(level=loglevel,
                        format=logformat)

    if opts.directory is None:
        print >> sys.stderr, "please specify a valid directory"
        optp.print_help()
        sys.exit(-1)
    elif not os.path.isdir(opts.directory):
        print >> sys.stderr, "%s is not a valid directory" % opts.directory
        sys.exit(-1)
    file2folder(opts.directory, opts.simulate)

if __name__ == "__main__":
    main()
