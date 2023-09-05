# coding: utf-8

from colorama import Fore, Style
from colorama import init as colorama_init


colorama_init()


# Dodanie wystąpienia nazwy
def add_name_with_kind_to_stats(name, kind, stats_dictionary):
    if name is None:
        return

    if name == "self" or (name[:2] == "__" and name[-2:] == "__") or name == "":
        return

    if "." in name:
        for module in name.split("."):
            add_name_with_kind_to_stats(module, kind, stats_dictionary)
        return

    if name not in stats_dictionary:
        stats_dictionary[name] = {"all": 0}
        stats_dictionary[name]["naming_style"] = specify_style(name)

    stats_dictionary[name]["all"] += 1

    if kind not in stats_dictionary[name]:
        stats_dictionary[name][kind] = 1
    else:
        stats_dictionary[name][kind] += 1

    return


# Określenie notacji identyfikatora
def specify_style(name):
    name = name.strip("_")
    if not name:
        return "ugly"

    if len(name) == 1:
        if name.islower():
            return "b" # single lowercase letter
        if name.isupper():
            return "B" # single uppercase letter
        return "ugly"

    if "_" in name:
        if name.islower():
            return "lower_case_with_underscores"
        if name.isupper():
            return "UPPER_CASE_WITH_UNDERSCORES"
        if all(map(lambda word: word != "" and word[0].isupper(), name.split("_"))):
            return "Capitalized_Words_With_Underscores"
        if all(map(lambda word: word != "" and word[0].isupper(), name.split("_")[1:])):
            return "camel_Snake_Case"
        return "ugly"

    if "-" in name:
        if name.islower():
            return "dash-case"
        if name.isupper():
            return "COBOL-CASE"
        return "ugly"

    if name.islower():
        return "lowercase"
    if name.isupper():
        return "UPPERCASE"
    if name[0].isupper():
        return "CapitalizedWords"
    return "mixedCase"


# Wypisywanie wiadomości diagnostycznej
def log_and_print(text, file, error=False):
    file.write(text + "\n")
    if error:
        print(Fore.RED + text + Style.RESET_ALL)
    else:
        print(text)
