#!/usr/local/bin/python3.11
# coding: utf-8

from logging import error
import os
import sys

import pandas as pd

from plots_maker import make_plots


def main (path_in:str, path_out: str):
    # Sprawdzenie poprawności ścieżki
    if not os.path.isdir(path_in):
        error("Input path is not dir path.")
        return 1

    # Przechodzenie po katalogu
    for path, subfiles, files in os.walk(path_in):
        dfs = {}
        for file_name in files:
            if file_name.endswith("_stats.csv"):
                timestamp = file_name[:-10]
                dfs[timestamp] = pd.read_csv(path + "/" + file_name)
                dfs[timestamp]["len"] = dfs[timestamp]["name"].apply(lambda x: len(str(x)))
        if len(dfs) > 0:
            make_plots(dfs, path.split("/")[-1], path_out)

    # Zakończenie progamu
    return 0


# Start programu
if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 2:
        sys.exit(main(args[0], args[1]))
    elif len(args) == 1:
        sys.exit(main(args[0], "."))
    else:
        sys.exit(main("." , ".")) 
