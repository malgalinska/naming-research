#!/usr/bin/python2.7
# coding: utf-8

import os
import sys
import ast
import csv
from logging import error
from datetime import datetime

from statisctics_library import *


FIELD_NAMES = ["name", "all", "function def", "class def", "import", "exception", "param", "keyword", "alias",
               "object decl", "object", "naming_style", "words"]
PYTHON_EXTENSION = ".py"
LOG_FILE_NAME = "./log.txt"


def get_data(input_path, output_path):
    try:
        start_time = datetime.now()

        # Sprawdzenie poprawności ścieżki
        if not os.path.isdir(input_path):
            error(input_path + " is not a valid directory.")
            return 1

        # Przechodzenie po katalogu
        stats_dictionary = {}
        for path, _, files in os.walk(input_path):
            for file_name in files:
                ext = os.path.splitext(file_name)[1]
                if ext != PYTHON_EXTENSION:
                    continue

                # Zebranie danych z pojedynczego pliku pythonowego
                file_path = os.path.join(path, file_name)
                with open(file_path) as file:
                    code = file.read()
                    tree = ast.parse(code, file_path)
                    NamesCounter(stats_dictionary).visit(tree)

        # Zapisanie danych do pliku
        with open(output_path, "w") as stats_file:
            csvwriter = csv.DictWriter(stats_file, fieldnames=FIELD_NAMES)
            csvwriter.writeheader()
            for key, value in stats_dictionary.items():
                value["name"] = key
                csvwriter.writerow(value)
        
        end_time = datetime.now()

    except Exception as e:
        with open(LOG_FILE_NAME, "a") as log:
            log_and_print(output_path + " (by Python 2.7):", log, True)
            log_and_print(repr(e), log)
            log_and_print(str(e) + "\n", log)
            
        return 1

    # Zakończenie progamu
    duration = end_time - start_time
    with open(LOG_FILE_NAME, "a") as log:
        log_and_print(output_path + " (by Python 2.7):", log)
        log_and_print("    Duration: " + str(duration) + "\n", log)

    return 0


class NamesCounter(ast.NodeVisitor):
    def __init__(self, stats_dictionary):
        self.stats_dictionary = stats_dictionary
        super(NamesCounter, self).__init__()

    def visit_FunctionDef(self, node):
        add_name_with_kind_to_stats(node.name, "function def", self.stats_dictionary)
        return self.generic_visit(node)

    def visit_ClassDef(self, node):
        add_name_with_kind_to_stats(node.name, "class def", self.stats_dictionary)
        return self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            add_name_with_kind_to_stats(node.module, "import", self.stats_dictionary)
        return self.generic_visit(node)

    def visit_Global(self, node):
        for name in node.names:
            add_name_with_kind_to_stats(name, "object decl", self.stats_dictionary)
        return self.generic_visit(node)

    def visit_Attribute(self, node):
        add_name_with_kind_to_stats(node.attr, "object", self.stats_dictionary)
        return self.generic_visit(node)

    def visit_Name(self, node):
        add_name_with_kind_to_stats(node.id, "object", self.stats_dictionary)
        return self.generic_visit(node)

    def visit_arg(self, node):
        if node.vararg:
            add_name_with_kind_to_stats(node.vararg, "param", self.stats_dictionary)
        return self.generic_visit(node)

    def visit_keyword(self, node):
        add_name_with_kind_to_stats(node.arg, "keyword", self.stats_dictionary)
        return self.generic_visit(node)

    def visit_alias(self, node):
        add_name_with_kind_to_stats(node.name, "import", self.stats_dictionary)
        if node.asname:
            add_name_with_kind_to_stats(node.asname, "alias", self.stats_dictionary)
        return self.generic_visit(node)


# Start programu
if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) >= 2:
        sys.exit(get_data(args[0], args[1]))
    else:
        print("Usage: " + sys.argv[0] + " input_path output_path\n")
        print("Arguments:\n")
        print("input_path \t:Path to project\n")
        print("output_path \t:Path to file, in which statistics will be saved\n")
