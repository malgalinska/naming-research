#!/usr/local/bin/python3.11
# coding: utf-8

from nltk.corpus import wordnet as wn


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
def has_part_of_speech(name, pos):
    for word in split_to_words(name):
        if is_part_of_speech(word, pos):
            return True
    return False


# Sprawdzanie, czy dane słowo może być użyte jako dana część mowy
def is_part_of_speech(word, pos):
    if word == "task" and pos == "n":
        return True

    list_of_synsets = list(filter(lambda x: x.name().split(".")[0] == wn.morphy(word), wn.synsets(word)))
    if not list_of_synsets:
        return True

    for synset in list_of_synsets:
        if synset.pos() == pos:
            return True
    return False
