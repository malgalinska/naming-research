# coding: utf-8

from nltk.corpus import wordnet as wn
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
        stats_dictionary[name]["naming_style"] = style(name)
        stats_dictionary[name]["words"] = split_to_words(name)

    stats_dictionary[name]["all"] += 1

    if kind not in stats_dictionary[name]:
        stats_dictionary[name][kind] = 1
    else:
        stats_dictionary[name][kind] += 1

    return


# Określenie notacji identyfikatora
def style(name):
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


# Podział identyfikatora na człony
def split_to_words(name):
    name = name.strip("_")
    if not name:
        return []

    if "_" in name:
        return name.lower().split("_")

    if "-" in name:
        return name.lower().split("-")

    ret = []
    start_of_word = 0
    for i in range(1, len(name) - 1):
        if name[i].isupper() and (name[i+1].islower() or name[i-1].islower()):
            ret.append(name[start_of_word:i].lower())
            start_of_word = i

    if name[-1].isupper():
        ret.append(name[start_of_word:-1].lower())
        ret.append(name[-1].lower())
    else:
        ret.append(name[start_of_word:].lower())

    return ret


# Sprawdzanie, czy któryś z członów identyfikatora jest podaną częścią mowy
# Przyjmuje wartości pos: v - verb, n - noun, a - adjective, r - adverb, s - adjective satellite
def has_part_of_speech(words, pos):
    for word in str(words).strip("[']").split("', '"):
        if is_part_of_speech(word, pos):
            return True
    return False


# Sprawdzanie, czy dane słowo może być użyte jako dana część mowy
def is_part_of_speech(word, pos):
    list_of_synsets = list(filter(lambda x: x.name().split(".")[0] == wn.morphy(word), wn.synsets(word)))

    if not list_of_synsets:
        return True

    for synset in list_of_synsets:
        if synset.pos() == pos:
            return True
    return False


# Wypisywanie wiadomości diagnostycznej
def log_and_print(text, file, error=False):
    file.write(text + "\n")
    if error:
        print(Fore.RED + text + Style.RESET_ALL)
    else:
        print(text)
