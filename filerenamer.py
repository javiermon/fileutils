#!/usr/bin/python

import sys, os, shutil
import re
import optparse
import logging

FULLFORMAT = "%(asctime)s  [%(levelname)s]  [%(module)s] %(message)s"
BASICFORMAT = "%(message)s"
logger = logging.getLogger()
delimiters = " _"
seasonre = re.compile("season (\d)", re.IGNORECASE)

def filerename(directory, new, original="Episode", simulate=False):
    root = os.path.abspath(directory)
    logger.debug("walking %s" % root)
    
    for filename in os.listdir(root):
        if os.path.isfile(os.path.join(directory, filename)):
            fullfile = os.path.join(root, filename)
            basedir = os.path.basename(directory)
            logger.debug("parsing %s from %s" % (fullfile, basedir))

            name, extension = os.path.splitext(filename)

            # extract season from directory:
            season = 1
            try:
                season = seasonre.match(basedir).group(1)
            except IndexError, AttributeError:
                print >> sys.stderr, "could not determine season, assuming it's the first"

            for delimiter in delimiters:
                name = name.replace(delimiter, ".")
            # renaming quirks:
            name = name.replace(":.", ":")
            name = name.replace(".-.", "-")     
            name = name.replace("%s." % original, '%s.S%sE0' % (new, season))
            # renaming quirks: remove 0 for double digits episodes
            name = re.sub(r'(E)0(\d{2})', r'\1\2', name)
            
            newfile = "%s/%s%s" % (directory, name, extension)
            logger.info("mv %s %s" % (fullfile, newfile))
            if not simulate:
                shutil.move(fullfile, newfile)

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

    optp.add_option("-o", "--origin", dest="origin",
                    help="origin naming.")

    optp.add_option("-n", "--new", dest="new",
                    help="new naming.")

    opts, args = optp.parse_args()

    loglevel = logging.DEBUG if opts.verbose else logging.INFO
    logformat = FULLFORMAT if opts.verbose else BASICFORMAT
    # log to stderr in fg
    logging.basicConfig(level=loglevel,
                        format=logformat)

    if opts.directory is None:
        print >> sys.stderr, "please specify a valid directory"
        optp.print_help()
        sys.exit(-1)

    elif opts.origin is None:
        print >> sys.stderr, "please specify an origin naming scheme"
        optp.print_help()
        sys.exit(-1)

    elif opts.new is None:
        print >> sys.stderr, "please specify a new naming scheme"
        optp.print_help()
        sys.exit(-1)

    elif not os.path.isdir(opts.directory):
        print >> sys.stderr, "%s is not a valid directory" % opts.directory
        sys.exit(-1)

    for root, _, _ in os.walk(opts.directory):
        filerename(root, opts.new, opts.origin, opts.simulate)

if __name__ == "__main__":    
    main()
