#!/usr/bin/python                                                                                                                                                         
                                                                                                                                                                          
import sys, os                                                                                                                                                            
import re
import optparse
import logging

FULLFORMAT = "%(asctime)s  [%(levelname)s]  [%(module)s] %(message)s"
BASICFORMAT = "%(message)s"
logger = logging.getLogger()
delimiters = " _"
seasonre = re.compile("season\s*(\d)", re.IGNORECASE)
prefixre = re.compile("(\w+)[%s]." % delimiters)

def filerename(directory):
    root = os.path.abspath(directory)

    for filename in os.listdir(root):
        if os.path.isfile(os.path.join(directory, filename)):
            name, extension = os.path.splitext(filename)
            print name, extension
            if extension in (".mp3"):
                song = name[3:]
                number = name[:2]
                cmd = "id3v2 -t '%s' -T %s '%s'" % (song, number, filename)
                print cmd
                os.system(cmd)

def main():
    # Setup the command line arguments.                                                                                                                                   
    optp = optparse.OptionParser()
    # options.                                                                                                                                                            
    optp.add_option("-d", "--directory", dest="directory",
                    help="directory to parse.")

    optp.add_option("-v", "--verbose", dest="verbose",
                    help="log verbosity.", action="store_true", default=False)

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
        filerename(root)

if __name__ == "__main__":
    main()
