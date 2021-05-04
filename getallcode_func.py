#!/usr/bin/env python3

import os
from pathlib import Path
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '')

# argparse fileinputs
sys.path.append(str(__projectdir__ / Path('submodules/argparse-fileinputs/')))
from argparse_fileinputs import add_fileinputs
from argparse_fileinputs import process_fileinputs

# Excluded Variables:{{{1
fileendingsexclude = []
# general exclude
fileendingsexclude = fileendingsexclude + ['.jpg', '.mat', '.out', '.pdf', '.png', '.pptx', '.pyc', '.tar', '.xls', '.zip']
# latex fileendings exclude
fileendingsexclude = fileendingsexclude + ['.aux', '.bbl', '.blg', '.dvi', 'fdb_latexmk', 'fls', '.log', '.synctex.gz']
# want to avoid calling _escaped.snippets in my commonsectionupdate function
fileendingsexclude = fileendingsexclude + ['_escaped.snippets']

foldernamesexclude = ['.git', 'data', 'graphs', 'old', 'submodules', 'submodules2', 'temp', 'git', 'output']
folderendingsexclude = ['-external',]



def getallcode(parselist, fileendingsexclude = fileendingsexclude, foldernamesexclude = foldernamesexclude):
    if fileendingsexclude is None:
        fileendingsexclude = []
    if foldernamesexclude is None:
        foldernamesexclude = []

    # convert to Paths if not already for consistency
    for i in range(len(parselist)):
        parselist[i] = Path(parselist[i])

    # firstly verify parselist contains unique entries
    for i in range(len(parselist)):
        for j in range(len(parselist)):
            if i != j:
                folder1 = str(parselist[i]) + os.sep
                folder2 = str(parselist[j]) + os.sep
                if folder1.startswith(folder2):
                    raise ValueError('folder list does not contain unique entries. ' + str(folder1) + ' is contained in ' + str(folder2) + '.')
    
    # next verify all folders exist
    for folder in parselist:
        if not os.path.exists(folder):
            raise ValueError(str(folder) + ' does not exist.')

    # now go through folders one by one and get all files and folders in that folder
    files = []
    while len(parselist) > 0:
        element = parselist.pop()

        # skip links
        if os.path.islink(element):
            continue

        if os.path.isfile(element):
            # do not include if file has bad ending
            badending = False
            for ending in fileendingsexclude:
                if str(element).endswith(ending):
                    badending = True
            if badending is True:
                continue

            # add to list of files
            files.append(element)

        else:

            # verify folder does not have bad name
            badname = False
            for name in foldernamesexclude:
                if os.path.basename(str(element)) == name:
                    badname = True
            for name in folderendingsexclude:
                if os.path.basename(str(element)).endswith(name):
                    badname = True

            if badname is True:
                continue

            # add the contents of the folder to parselist
            foldercontents = os.listdir(element) 
            for content in foldercontents:
                fullpathcontent = element / Path(content)
                parselist.append(fullpathcontent)



    # now convert to string
    # wanted to do conversion to string here so I could get correct paths when doing file search
    for i in range(len(files)):
        files[i] = str(files[i])

    # sort files
    files = sorted(files)

    return(files)


def getallcode_test():
    files = getallcode([__projectdir__ / Path('testdir/okdir1/'), __projectdir__ / Path('testdir/okdir3/')])

    print(files)


def getallcode_ap():
    #Argparse:{{{
    import argparse
    
    parser=argparse.ArgumentParser()

    parser = add_fileinputs(parser)
    
    args=parser.parse_args()
    #End argparse:}}}

    filelist = process_fileinputs(args)

    # remove comments and blank lines in parselist
    filelist = [filename for filename in filelist if not filename.startswith('#') and not filename == '']

    # replace ~ in parselist
    filelist = [filename.replace('~', os.path.expanduser('~')) for filename in filelist]

    files = getallcode(filelist)

    print('\n'.join(files))


# Run:{{{1
if __name__ == '__main__':
    getallcode_ap()

