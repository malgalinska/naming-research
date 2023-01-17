#!/usr/bin/python3
# coding: utf-8

from logging import error
import os
import sys

import pandas as pd

from plots_maker import make_plots


def main (path:str):
    # Sprawdzenie poprawności ścieżki
    if not os.path.isdir(path):
        error("That is not dir path.")
        return 1

    # Przechodzenie po katalogu
    for path, subfiles, files in os.walk(path):
        dfs = {"repo_name": path.split("/")[-1]}
        for file_name in files:
            if file_name.endswith("_stats.csv"):
                timestamp = file_name[:-10]
                dfs[timestamp] = pd.read_csv(path + "/" + file_name)
                dfs[timestamp]['len'] = dfs[timestamp]['name'].apply(lambda x: len(str(x)))
        if files:
            make_plots(dfs)

    # Zakończenie progamu
    return 0


# Start programu
if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args):
        sys.exit(main(args[0]))
    else:
        sys.exit(main("."))  
