#!/usr/bin/python3
# coding: utf-8

from logging import error
import os
import string
import sys
import tokenize
import csv

statsDictionary = {}

def main (path:string):
    if not os.path.isdir(path):
        error("That is not dir path.")
        return 1
    
    n_of_py = 0
    n_of_others = 0

    with open('StatsFile.csv', 'w', -1, 'utf-8') as statsFile:
        for path, subfiles, files in os.walk(path):
            for fileName in files:
                x  = fileName.split(".", 1)
                if len(x) > 1 and x[1] == "py":
                    add_to_statistics(path + "/" + fileName)
                    n_of_py += 1 
                else:
                    n_of_others += 1
        n = n_of_others + n_of_py
        print("There is " + str(n_of_py) + " Python files of " + str(n) + " of all files.\n\n")
        csvwriter = csv.writer(statsFile)
        for key, value in statsDictionary.items():
            csvwriter.writerow([key, value])
    return 0

def add_to_statistics(fileName:string):
    with tokenize.open(fileName) as file:
        tokens = tokenize.generate_tokens(file.readline)
        for tokenType, tokenString, _, _, _ in tokens:
            if tokenType == 1:
                if tokenString in statsDictionary:
                    statsDictionary[tokenString] += 1
                else:
                    statsDictionary[tokenString] = 1


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args):
        sys.exit(main(args[0]))
    else:
        sys.exit(main("."))  
