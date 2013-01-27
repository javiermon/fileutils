#!/usr/bin/python
import sys, os
import logging
import optparse

FULLFORMAT = "%(asctime)s  [%(levelname)s]  [%(module)s] %(message)s"
BASICFORMAT = "%(message)s"
extensions = (".mp3", ".ogg")
logger = logging.getLogger()

def filetagger(directory, simulate=False):
    root = os.path.abspath(directory)
    for filename in os.listdir(root):
        if not os.path.isfile(os.path.join(directory, filename)):
            continue
        name, extension = os.path.splitext(filename)
        if not extension in extensions:
            continue
        logger.debug("tagging %s%s" % (name, extension))
        song = name[3:]
        number = name[:2]
        path = os.getcwd().split('/')
        artist = path[-2]
        album = path[-1]
        cmd = "id3v2 -a '%s' -A '%s' -t '%s' -T '%s' '%s'" % (artist, album, song, number, filename)
        logger.debug(cmd)
        if not simulate:
            os.system(cmd)

def main():
    # Setup the command line arguments.
    optp = optparse.OptionParser()
    # options.
    optp.add_option("-v", "--verbose", dest="verbose",
                    help="log verbosity.", action="store_true", default=False)

    optp.add_option("-s", "--simulate", dest="simulate",
                    help="do nothing, just simulate.", action="store_true", default=False)

    opts, args = optp.parse_args()

    loglevel = logging.DEBUG if opts.simulate or opts.verbose else logging.INFO
    logformat = FULLFORMAT if opts.verbose else BASICFORMAT
    # log to stderr in fg
    logging.basicConfig(level=loglevel,
                        format=logformat)

    if len(args) < 1:
        print >> sys.stderr, "please specify a valid directory"
        optp.print_help()
        sys.exit(-1)

    if not os.path.isdir(args[0]):
        print >> sys.stderr, "%s is not a valid directory" % opts.directory
        sys.exit(-1)

    for root, _, _ in os.walk(args[0]):
        filetagger(root, opts.simulate)

if __name__ == "__main__":
    main()
