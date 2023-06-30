#!/usr/bin/python2.7
# coding: utf-8

from logging import error
import os
import sys
import ast
import csv
from datetime import datetime
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

from statisctics_library import *

colorama_init()

FIELD_NAMES = ["name", "all", "function def", "class def", "import", "exception", "param", "keyword", "alias", "object decl", "object", "naming_style", "words"]


def get_data(input, output):
    try:
        start_time = datetime.now()

        # Sprawdzenie poprawności ścieżki
        if not os.path.isdir(input):
            error("That is not a dir path.")
            return 1

        # Przechodzenie po katalogu
        stats_dictionary = {}
        for path, _, files in os.walk(input):
            for file_name in files:
                ext  = os.path.splitext(file_name)[1]
                if ext != "py":
                    continue

                # Zebranie danych z pojedynczego pliku pythonowego
                file_path = os.path.join(path, file_name)
                with open(file_path) as file:
                    code = file.read()
                    tree = ast.parse(code, file_path)
                    NamesCounter(stats_dictionary).visit(tree)

        # Zapisanie danych do pliku
        with open(output, "w") as stats_file:
            csvwriter = csv.DictWriter(stats_file, fieldnames=FIELD_NAMES)
            csvwriter.writeheader()
            for key, value in stats_dictionary.items():
                value["name"] = key
                csvwriter.writerow(value)
        
        end_time = datetime.now()

    except Exception as e:
        with open("./log.txt", "a") as log:
            log_and_print(output + ':', log, True)
            log_and_print(repr(e), log)
            log_and_print(str(e), log)
            log_and_print('Even Python 2.7 doesn`t work here!\n', log)

    else:
        # Zakończenie progamu
        duration = end_time - start_time
        with open("./log.txt", "a") as log:
            log_and_print(output + ' (by Python 2.7):', log)
            log_and_print('    Duration: ' + str(duration), log)

    return 0


class NamesCounter(ast.NodeVisitor):
    def __init__(self, stats_dictionary) -> None:
        self.stats_dictionary = stats_dictionary
        super().__init__()

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

    def visit_alias (self, node):
        add_name_with_kind_to_stats(node.name, "import", self.stats_dictionary)
        if node.asname:
            add_name_with_kind_to_stats(node.asname, "alias", self.stats_dictionary)
        return self.generic_visit(node)


def log_and_print(text, file, error=False):
    file.write(text + '\n')
    if error:
        print(Fore.RED + text + Style.RESET_ALL)
    else:
        print(text)


# Start programu
if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) >= 2:
        sys.exit(get_data(args[0], args[1]))
    elif len(args) == 1:
        sys.exit(get_data(args[0], "Stats.csv"))
    else:
        sys.exit(get_data(".", "Stats.csv"))
