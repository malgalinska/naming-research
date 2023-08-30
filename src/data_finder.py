#!/usr/local/bin/python3.11
# coding: utf-8

from logging import error
import os
import sys
import pandas as pd

from plots_maker import make_plots

DATA_NAME_ENDING = "_stats.csv"

def main (input_path: str, output_path: str):
    # Sprawdzenie poprawności ścieżek
    if not os.path.isdir(input_path):
        error(f"{input_path} is not a valid directory.")
        return 1
    
    if not os.path.isdir(output_path):
        error(f"{output_path} is not a valid directory.")
        return 1

    # Przechodzenie po katalogu
    for path, _, files in os.walk(input_path):
        dfs = {}
        for file_name in files:
            if not file_name.endswith(DATA_NAME_ENDING):
                continue

            timestamp = file_name[:-10]
            dfs[timestamp] = pd.read_csv(os.path.join(path, file_name))
            dfs[timestamp]["len"] = dfs[timestamp]["name"].apply(lambda x: len(str(x)))
        
        # Tworzenie wykresów na podstawie danych z pojedynczego katalogu
        if len(dfs) > 0:
            make_plots(dfs, os.path.basename(path), output_path)

    return 0


# Start programu
if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 2:
        sys.exit(main(args[0], args[1]))
    else:
        print("Usage: " + sys.argv[0] + " input_path output_path\n")
        print("Arguments:\n")
        print("input_path \t:Path to directory containing data to be analysed\n")
        print("output_path \t:Path to directory to save plots in\n")
