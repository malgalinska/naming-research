#!/usr/bin/python3
# coding: utf-8

from logging import error
import os
import string
import sys
import ast
import csv

statsDictionary = {}
field_names = ["name", "all", "function def", "class def", "import", "exception", "param", "keyword", "alias", "object decl", "object"]

def get_data(path:string, output:string):
    # Sprawdzenie poprawności ścieżki
    if not os.path.isdir(path):
        error("That is not dir path.")
        return 1
    
    n_of_py = 0
    n_of_others = 0

    # Przechodzenie po katalogu
    for path, subfiles, files in os.walk(path):
        for fileName in files:
            x  = fileName.split(".", 1)
            if len(x) > 1 and x[1] == "py":
                add_to_statistics(path + "/" + fileName)
                n_of_py += 1 
            else:
                n_of_others += 1

    # Zapisanie danych do pliku
    with open(output, 'w', -1, 'utf-8') as statsFile:
        csvwriter = csv.DictWriter(statsFile, fieldnames=field_names)
        csvwriter.writeheader()
        for key, value in statsDictionary.items():
            value["name"] = key
            csvwriter.writerow(value)
    
    # Zakończenie progamu
    n = n_of_others + n_of_py
    print("There is " + str(n_of_py) + " Python files of " + str(n) + " of all files.\n\n")
    return 0

# Wyłuskanie danych z pojedynczego pliku pythonowego
def add_to_statistics(fileName:string):
    with open(fileName, encoding='utf-8') as f:
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
def add_name_with_kind(name:string, kind:string):
    if name == "self" or (name[:2] == "__" and name[-2:] == "__") or name == "":
        return

    if "." in name:
        for module in name.split("."):
            add_name_with_kind(module, kind)
        return

    if name not in statsDictionary:
        statsDictionary[name] = {"all": 0}
    statsDictionary[name]["all"] += 1

    if kind not in statsDictionary[name]:
        statsDictionary[name][kind] = 1
    else:
        statsDictionary[name][kind] += 1  

# Start programu
if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) >= 2:
        sys.exit(get_data(args[0], args[1]))
    elif len(args) == 1:
        sys.exit(get_data(args[0], "Stats.csv"))
    else:
        sys.exit(get_data(".", "Stats.csv"))