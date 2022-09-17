#!/usr/bin/env python
# coding: utf-8

from logging import error
import os
import string
import sys

def main (path:string):
    if not os.path.isdir(path):
        error("That is not dir path.")
        return 1

    f = open('FileData.txt', 'w', -1, 'utf-8')

    n_of_py = 0
    n_of_others = 0

    for path, subfiles, files in os.walk(path):
        # f.write('=' * 70 + '\n')
        # f.write(path + '\n')
        # if len(subfiles):
            # f.write('=' * 70 + '\n')
            # f.write('Podkatalogi:\n' + '=' * 70 + '\n')
            # for i in subfiles:
            #     f.write('\n' + i)
            # f.write('\n')
        if len(files):
            f.write('=' * 70 + '\n')
            f.write('Pliki:\n' + '=' * 70 + '\n')
            for i in files:
                a  = i.split(".", 1)
                if len(a) > 1 and a[1] == "py":
                    f.write('\n' + i)
                    n_of_py += 1
                else:
                    f.write('\n' + "No Python file!")
                    n_of_others += 1
            f.write('\n')

    n = n_of_others + n_of_py
    f.write("\n\nThere is " + str(n_of_py) + " Python files of " + str(n) + " of all files.\n" )
    f.close()
    return 0


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args):
        sys.exit(main(args[0]))
    else:
        sys.exit(main("."))  
