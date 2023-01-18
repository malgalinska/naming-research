#!/usr/bin/python3
# coding: utf-8

from logging import error
import os
import sys
import shutil
import zipfile

from data_getter import get_data


def main (path: str):
    # Sprawdzenie poprawności ścieżki
    if not os.path.isdir(path):
        error("That is not dir path.")
        return 1

    # Przechodzenie po katalogu
    for path, subfiles, files in os.walk(path):
        for file_name in files:
            if zipfile.is_zipfile(path + "/" + file_name):
                os.mkdir(path + "/tmp")
                try:
                    with zipfile.ZipFile(path + "/" + file_name, "r") as zip:
                        zip.extractall(path + "/tmp")

                    name = file_name.split(".", 1)[0]
                    get_data(path + "/tmp", path + "/" + name + "_stats.csv")
                finally:
                    shutil.rmtree(path + "/tmp")
    # Zakończenie progamu
    return 0


# Start programu
if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args):
        sys.exit(main(args[0]))
    else:
        sys.exit(main("."))  
