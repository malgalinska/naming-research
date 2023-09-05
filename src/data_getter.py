#!/usr/local/bin/python3.11
# coding: utf-8

import os
import sys
import ast
import csv
from logging import error
from datetime import datetime

from utils import *


FIELD_NAMES = ["name", "all", "function_def", "class_def", "import_module_or_alias", "exception", "param", "keyword",
               "alias", "object_decl", "object", "naming_style"]
PYTHON_EXTENSION = ".py"
LOG_FILE_NAME = "./log.txt"


def get_data(input_path: str, output_path: str):
    try:
        start_time = datetime.now()

        # Sprawdzenie poprawności ścieżki
        if not os.path.isdir(input_path):
            error(f"{input_path} is not a valid directory.")
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
                with open(file_path, encoding="utf-8") as file:
                    code = file.read()
                    tree = ast.parse(code, file_path)
                    NamesCounter(stats_dictionary).visit(tree)

        # Zapisanie danych do pliku
        with open(output_path, "w", -1, "utf-8") as stats_file:
            csvwriter = csv.DictWriter(stats_file, fieldnames=FIELD_NAMES)
            csvwriter.writeheader()
            for key, value in stats_dictionary.items():
                value["name"] = key
                csvwriter.writerow(value)

        end_time = datetime.now()

    except Exception as e:
        with open(LOG_FILE_NAME, "a", -1, "utf-8") as log:
            log_and_print(f"{output_path} (by Python 3.11):", log, True)
            log_and_print(f"{repr(e)}\n", log)

        return 1

    else:
        # Zakończenie progamu
        duration = end_time - start_time
        with open(LOG_FILE_NAME, "a", -1, "utf-8") as log:
            log_and_print(f"{output_path} (by Python 3.11):", log)
            log_and_print(f"    Started at {start_time:%H:%M:%S}, ended at {end_time:%H:%M:%S} (duration {duration})\n",
                          log)

    return 0


class NamesCounter(ast.NodeVisitor):
    def __init__(self, stats_dictionary: dict) -> None:
        self.stats_dictionary = stats_dictionary
        super().__init__()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        add_name_with_kind_to_stats(node.name, "function_def", self.stats_dictionary)
        return self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        add_name_with_kind_to_stats(node.name, "function_def", self.stats_dictionary)
        return self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        add_name_with_kind_to_stats(node.name, "class_def", self.stats_dictionary)
        return self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module:
            add_name_with_kind_to_stats(node.module, "import_module_or_alias", self.stats_dictionary)
        return self.generic_visit(node)

    def visit_Global(self, node: ast.Global):
        for name in node.names:
            add_name_with_kind_to_stats(name, "object_decl", self.stats_dictionary)
        return self.generic_visit(node)

    def visit_Nonlocal(self, node: ast.Nonlocal):
        for name in node.names:
            add_name_with_kind_to_stats(name, "object_decl", self.stats_dictionary)
        return self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        add_name_with_kind_to_stats(node.attr, "object", self.stats_dictionary)
        return self.generic_visit(node)

    def visit_Name(self, node: ast.Name):
        add_name_with_kind_to_stats(node.id, "object", self.stats_dictionary)
        return self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        if node.name:
            add_name_with_kind_to_stats(node.name, "exception", self.stats_dictionary)
        return self.generic_visit(node)

    def visit_arg(self, node: ast.arg):
        add_name_with_kind_to_stats(node.arg, "param", self.stats_dictionary)
        return self.generic_visit(node)

    def visit_keyword(self, node: ast.keyword):
        if node.arg:
            add_name_with_kind_to_stats(node.arg, "keyword", self.stats_dictionary)
        return self.generic_visit(node)

    def visit_alias (self, node: ast.alias):
        add_name_with_kind_to_stats(node.name, "import_module_or_alias", self.stats_dictionary)
        if node.asname:
            add_name_with_kind_to_stats(node.asname, "alias", self.stats_dictionary)
        return self.generic_visit(node)

    def visit_MatchMapping(self, node: ast.MatchMapping):
        if node.rest:
            add_name_with_kind_to_stats(node.rest, "object_decl", self.stats_dictionary)
        return self.generic_visit(node)

    def visit_MatchClass(self, node: ast.MatchClass):
        for name in node.kwd_attrs:
            add_name_with_kind_to_stats(name, "object", self.stats_dictionary)
        return self.generic_visit(node)

    def visit_MatchStar(self, node: ast.MatchStar):
        if node.name:
            add_name_with_kind_to_stats(node.name, "object_decl", self.stats_dictionary)
        return self.generic_visit(node)

    def visit_MatchAs(self, node: ast.MatchAs):
        if node.name:
            add_name_with_kind_to_stats(node.name, "object_decl", self.stats_dictionary)
        return self.generic_visit(node)


# Start programu
if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) >= 2:
        sys.exit(get_data(args[0], args[1]))
    else:
        print(f"Usage: {sys.argv[0]} input_path output_path\n")
        print("Arguments:\n")
        print("input_path \t:Path to project\n")
        print("output_path \t:Path to file, in which statistics will be saved\n")
