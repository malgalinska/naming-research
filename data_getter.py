#!/usr/bin/python3
# coding: utf-8

from logging import error
import os
# import string
import sys
import ast
import csv

stats_dictionary = {}
field_names = ["name", "all", "function def", "class def", "import", "exception", "param", "keyword", "alias", "object decl", "object", "case_convention", "words"]


def get_data(path: str, output: str):
    # Sprawdzenie poprawności ścieżki
    if not os.path.isdir(path):
        error("That is not dir path.")
        return 1
    
    n_of_py = 0
    n_of_others = 0

    # Przechodzenie po katalogu
    for path, subfiles, files in os.walk(path):
        for file_name in files:
            x  = file_name.split(".", 1)
            if len(x) > 1 and x[1] == "py":
                add_to_statistics(path + "/" + file_name)
                n_of_py += 1 
            else:
                n_of_others += 1

    # Zapisanie danych do pliku
    with open(output, 'w', -1, 'utf-8') as stats_file:
        csvwriter = csv.DictWriter(stats_file, fieldnames=field_names)
        csvwriter.writeheader()
        for key, value in stats_dictionary.items():
            value["name"] = key
            csvwriter.writerow(value)
    
    # Zakończenie progamu
    n = n_of_others + n_of_py
    print("There is " + str(n_of_py) + " Python files of " + str(n) + " of all files.\n\n")
    return 0


# Wyłuskanie danych z pojedynczego pliku pythonowego
def add_to_statistics(file_name: str):
    with open(file_name, encoding='utf-8') as f:
        code = f.read()
        tree = ast.parse(code)
        NamesCounter().visit(tree)


class NamesCounter(ast.NodeVisitor):
    def visit_FunctionDef(self, node: ast.FunctionDef):
        add_name_with_kind(node.name, "function def")
        return self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        add_name_with_kind(node.name, "function def")
        return self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        add_name_with_kind(node.name, "class def")
        return self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module:
            add_name_with_kind(node.module, "import")
        return self.generic_visit(node)

    def visit_Global(self, node: ast.Global):
        for name in node.names:
            add_name_with_kind(name, "object decl")
        return self.generic_visit(node)

    def visit_Nonlocal(self, node: ast.Nonlocal):
        for name in node.names:
            add_name_with_kind(name, "object decl")
        return self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        add_name_with_kind(node.attr, "object")
        return self.generic_visit(node)

    def visit_Name(self, node: ast.Name):
        add_name_with_kind(node.id, "object")
        return self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        if node.name:
            add_name_with_kind(node.name, "exception")
        return self.generic_visit(node)

    def visit_arg(self, node: ast.arg):
        add_name_with_kind(node.arg, "param")
        return self.generic_visit(node)

    def visit_keyword (self, node: ast.keyword):
        if node.arg:
            add_name_with_kind(node.arg, "keyword")
        return self.generic_visit(node)

    def visit_alias (self, node: ast.alias):
        add_name_with_kind(node.name, "import")

        if node.asname:
            add_name_with_kind(node.asname, "alias")

        return self.generic_visit(node)


# Dodanie wystąpienia nazwy
def add_name_with_kind(name: str, kind: str):
    if name == "self" or (name[:2] == "__" and name[-2:] == "__") or name == "":
        return

    if "." in name:
        for module in name.split("."):
            add_name_with_kind(module, kind)
        return

    if name not in stats_dictionary:
        stats_dictionary[name] = {"all": 0}
        add_new_name_with_case_convention_and_words(name)
    stats_dictionary[name]["all"] += 1

    if kind not in stats_dictionary[name]:
        stats_dictionary[name][kind] = 1
    else:
        stats_dictionary[name][kind] += 1


def add_new_name_with_case_convention_and_words(name: str):
    stats_dictionary[name]["case_convention"] = convention(name)
    stats_dictionary[name]["words"] = split_to_words(name)


# Based on: https://peps.python.org/pep-0008/#descriptive-naming-styles
def convention(name: str):
    name = name.strip("_")
    if len(name) == 0:
        return "ugly"

    if len(name) == 1:
        if name.islower():
            return "b" # single lowercase letter
        if name.isupper():
            return "B" # single uppercase letter
    
    if '_' in name:
        if name.islower():
            return "lower_case_with_underscores"
        if name.isupper():
            return "UPPER_CASE_WITH_UNDERSCORES"
    else:
        if name.islower():
            return "lowercase"
        if name.isupper():
            return "UPPERCASE"
        if name[0].isupper():
            return "CapitalizedWords"
        return "mixedCase"
    return "ugly"
    

def split_to_words(name: str):
    name = name.strip("_")
    if len(name) == 0:
        return []
        
    if '_' in name:
        return name.lower().split("_")

    ret = []
    start_of_word = 0
    for i in range(1, len(name) - 1):
        if name[i].isupper() and (name[i + 1].islower() or name[i - 1].islower()):
            ret.append(name[start_of_word:i].lower())
            start_of_word = i

    if name[-1].isupper():
        ret.append(name[start_of_word:-1].lower())
        ret.append(name[-1].lower())
    else:
        ret.append(name[start_of_word:].lower())

    return ret
            



# Start programu
if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) >= 2:
        sys.exit(get_data(args[0], args[1]))
    elif len(args) == 1:
        sys.exit(get_data(args[0], "Stats.csv"))
    else:
        sys.exit(get_data(".", "Stats.csv"))
