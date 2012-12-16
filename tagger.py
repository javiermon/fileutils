#!/usr/bin/python                                                                                                                                                         
import sys, os
import logging
import optparse

FULLFORMAT = "%(asctime)s  [%(levelname)s]  [%(module)s] %(message)s"
BASICFORMAT = "%(message)s"
logger = logging.getLogger()
extensions = (".mp3", ".ogg")

def filetagger(directory, simulate=False):
    root = os.path.abspath(directory)
    for filename in os.listdir(root):
        if os.path.isfile(os.path.join(directory, filename)):
            name, extension = os.path.splitext(filename)
            if extension in extensions:
                logger.debug("tagging %s%s" % name, extension)
                song = name[3:]
                number = name[:2]
                path = os.getcwd().split('/')
                artist = path[-2]
                album = path[-1]
                cmd = "id3v2 -a %s -A %s -t '%s' -T %s '%s'" % (artist, album, song, number, filename)
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
    
    loglevel = logging.DEBUG if opts.verbose else logging.INFO
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
