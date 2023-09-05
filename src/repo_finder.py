#!/usr/local/bin/python3.11
# coding: utf-8

import os
import sys
import shutil
import zipfile
from logging import error

from data_getter import get_data
from statisctics_library import log_and_print


DATA_NAME_ENDING = "_stats.csv"
TEMPORARY_DIRECTORY_NAME = "tmp"
ALTERNATIVE_PROGRAM_PATH = os.path.join(os.path.dirname(__file__), "alternative_data_getter.py")
LOG_FILE_NAME = "./log.txt"


def main(input_path: str):
    # Sprawdzenie poprawności ścieżki
    if not os.path.isdir(input_path):
        error(f"{input_path} is not a valid directory.")
        return 1

    # Przechodzenie po wszystkich plikach w drzewie katalogu
    for path, _, files in os.walk(input_path):
        tmp_path = os.path.join(path, TEMPORARY_DIRECTORY_NAME)

        for file_name in files:
            file_path = os.path.join(path, file_name)
            statistic_file_path = os.path.splitext(file_path)[0] + DATA_NAME_ENDING

            # Sprawdzenie, czy plik jest w formacie zip
            if not zipfile.is_zipfile(file_path):
                continue

            # Tymczasowe rozpakowanie archiwum i przeanalizowanie go funkcją get_data
            os.mkdir(tmp_path)
            try:
                with zipfile.ZipFile(file_path, "r") as zip:
                    zip.extractall(tmp_path)

                # Analiza za pomocą Python 3.11
                ret = get_data(tmp_path, statistic_file_path)

                # Analiza za pomocą Pythona 2.7
                if ret:
                    waitstatus = os.system(f"{ALTERNATIVE_PROGRAM_PATH} {tmp_path} {statistic_file_path}")
                    ret = os.waitstatus_to_exitcode(waitstatus)

                # Obie analizy zwracają błędy
                if ret:
                    with open(LOG_FILE_NAME, "a", -1, "utf-8") as log:
                        log_and_print(f"{file_path}: Nothing works here!\n", log, True)

            finally:
                shutil.rmtree(tmp_path)

    return 0


# Start programu
if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 1:
        sys.exit(main(args[0]))
    else:
        print(f"Usage: {sys.argv[0]} input_path\n")
        print("Argument:\n")
        print("input_path \t:Path to location containing zipped projects\n")
