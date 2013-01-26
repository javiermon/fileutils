#!/usr/bin/python
import sys, os
import logging
import optparse

FULLFORMAT = "%(asctime)s  [%(levelname)s]  [%(module)s] %(message)s"
BASICFORMAT = "%(message)s"
extensions = (".mp3", ".ogg")
logger = logging.getLogger()

def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"

def filetagger(directory, simulate=False):
    root = os.path.abspath(directory)
    for filename in os.listdir(root):
        fullfile = os.path.join(directory, filename)
        if not os.path.isfile(fullfile):
            continue
        name, extension = os.path.splitext(filename)
        if not extension in extensions:
            continue
        logger.debug("v2 tagging %s%s" % (name, extension))
        cmd = "id3v2 -l  %s | grep 'No ID3v2 tag'" % shellquote(fullfile)
        logger.debug(cmd)
        if not simulate:
            ret = os.system(cmd)
            if ret == 0:
                cmd = "id3v2 -C  %s" % shellquote(fullfile)
                logger.debug(cmd)
                if not simulate:
                    os.system(cmd)

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

    if not os.path.isdir(opts.directory):
        print >> sys.stderr, "%s is not a valid directory" % opts.directory
        sys.exit(-1)

    for root, _, _ in os.walk(opts.directory):
        filetagger(root, opts.simulate)

if __name__ == "__main__":
    main()
