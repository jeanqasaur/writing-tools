""" Takes two directories of Latex files and populates an output directory with
    the latexdiff of each of the latex files. Run this from the directory you
    want to use this in.

    Author: Jean Yang
"""
import os
import sys, getopt

def getFullPath(dirName, makeDir=False):
    if not os.path.isdir(dirName):
        dirName = os.path.join(os.getcwd(), dirName)
        if not os.path.isdir(dirName):
            if makeDir:
                print 'mkdir', dirName
                os.system(' '.join(['mkdir', dirName]))
            else:
                print "Directory does not exist: ", dirName
                sys.exit(2)
    return dirName

def latexDiff(oldFile, newFile, outFile):
    diffCmd = ' '.join(['latexdiff', oldFile, newFile, '>', outFile])
    os.system(diffCmd)

def diffDir(prevDir, newDir, outDir):
    def getSubDir(dirName):
        return '/'.join(dirName.split('/')[1:])
    for folder, subs, files in os.walk(prevDir):
        print 'Diff for', folder, '...'
        for f in files:
            if f.endswith(".tex"):
                prev = getFullPath(folder)
                subDir = getSubDir(folder)
                new = getFullPath(os.path.join(newDir, subDir))
                out = getFullPath(os.path.join(outDir, subDir), True)
                latexDiff(os.path.join(prev, f), os.path.join(new, f)
                    , os.path.join(out, f))

def main(argv):
    prevDir = ''
    newDir = ''
    outDir = ''

    # Get directories from the command line.
    usage = 'diff.py -p <old directory> -n <new directory> -o <output directory>'
    try:
        opts, args = getopt.getopt(argv, "hp:n:o:"
            , ["previous=", "new=", "out="])
    except getopt.GetoptError:
        print usage
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print usage
            print "  \\    /\\"
            print "   )  ( ')"
            print "  (  /  )"
            print "   \\(__)|"
            print "* Make sure your previous and new directories have " \
                "identically-named .tex files."
            print "* Note this only operates over your .tex files."
            print "* Run 'python diff.py -p prev -n new -o out' to test."
            sys.exit(1)
        elif opt in ('-p', '--previous'):
            prevDir = getFullPath(arg)
        elif opt in ('-n', '--new'):
            newDir = getFullPath(arg)
        elif opt in ('-o', '--out'):
            outDir = getFullPath(arg)

    diffDir(prevDir, newDir, outDir)

if __name__=="__main__":
    main(sys.argv[1:])
