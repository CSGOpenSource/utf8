#!/usr/bin/env python

"""
"""
import sys, os, traceback
import re
import getopt
import subprocess


def run(command):
    try:
        print "*** opening subproces with command:"
        print command
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print "***"
        print "Reading output..."
        output = p.stdout.read()
        print "... done"
    except Exception as e:
        print ">>> Caught exception: "
        print e
        print "<<<"
        output = ""                  
    return output    

# Try to determine if the given stream is encoded utf-8. Can only return a
# false positive, negatives are (can be) known to be correct.
#
def guess_utf8(s):
    #ba = bytearray(s)
    #ba = bytearray(s, "cp1252")
    ba = bytearray(s, "iso-8859-1")

    # Believe the windowsish BOM if it's there. Would be more robust to
    # skip over it and anaylize the rest of the file.
    if len(ba) > 2 and ba[0] == 0xef and ba[1] == 0xbb and ba[2] == 0xbf:
        return True

    rval = False
    i = 0
    while i < len(ba):
        if ba[i] < 128: # ascii stands alone
            i = i + 1
        elif ba[i] >= 194 and ba[i] <= 223: # precedes one continuation
            if i + 1 < len(ba) and ba[i+1] >= 128 and ba[i+1] <= 191:
                rval = True
                i = i + 2
            else:
                return False
        elif ba[i] >= 224 and ba[i] <= 239: # precedes two continuations
            if (i + 2 < len(ba) and ba[i+1] >= 128 and ba[i+1] <= 191
                                and ba[i+2] >= 128 and ba[i+2] <= 191):
                rval = True
                i = i + 3
            else:
                return False
        else:
            return False

    return rval


def get_utf8_items(transaction, repository, items):
    utf8_items = []
    svnlook = "C:\\Program Files (x86)\\VisualSVN Server\\bin\\svnlook.exe"
    for item in items:
        for suffix in ('.osql', '.sql'):
            if item.lower().endswith(suffix):
                size = run ([svnlook, "filesize",
                    "-r", transaction, repository, item])
                #"-t", transaction, repository, item])
                if int(size) < 524288:
                    contents = run ([svnlook, "cat", 
                        "-r", transaction, repository, item])
                    #"-t", transaction, repository, item])
                    if (guess_utf8(contents)):
                        utf8_items.append(item)

    return utf8_items


def main ():
    args = sys.argv[1:]

    item = args[0]

    contents = run(['cat', item])

    if (guess_utf8(contents)):
        print "It's UTF8"


if __name__ == '__main__':
    try:
        exit_status = main()
        if exit_status is None:
            sys.exit(0)
        sys.exit(int(exit_status))
    except SystemExit, e:
        raise e
    except Exception, e:
        print >> sys.stderr,'ERROR, UNEXPECTED EXCEPTION'
        print >> sys.stderr, str(e)
        traceback.print_exc()
        os._exit(1)



