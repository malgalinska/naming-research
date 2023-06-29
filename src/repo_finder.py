#!/usr/local/bin/python3.11
# coding: utf-8

from logging import error
import os
import sys
import shutil
import zipfile

from data_getter import get_data


def main (input_path: str):
    # Sprawdzenie poprawności ścieżki
    if not os.path.isdir(input_path):
        error("That is not a dir path.")
        return 1

    # Przechodzenie po wszystkich plikach w drzewie katalogu
    for path, _, files in os.walk(input_path):
        tmp_path = os.path.join(path, "tmp")

        for file_name in files:
            file_path = os.path.join(path, file_name)
            statistic_file_path = os.path.splitext(file_path)[0] + "_stats.csv"
            
            # Sprawdzenie, czy plik jest w formacie zip
            if not zipfile.is_zipfile(file_path):
                continue

            # Tymczasowe rozpakowanie archiwum i przeanalizowanie go funkcją get_data 
            os.mkdir(tmp_path)
            try:
                with zipfile.ZipFile(file_path, "r") as zip:
                    zip.extractall(tmp_path)

                get_data(tmp_path, statistic_file_path)
            finally:
                shutil.rmtree(tmp_path)
    return 0


# Start programu
if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args):
        sys.exit(main(args[0]))
    else:
        sys.exit(main("."))  
