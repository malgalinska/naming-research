#!/usr/local/bin/python3.11
# coding: utf-8

import os
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt

from statisctics_library import log_and_print, has_part_of_speech, split_to_words


LOG_FILE_NAME = "./plots_log.txt"


def make_plots (data: dict, repo_name: str, path_out: str):
    start_time = datetime.now()

    path_out = os.path.join(path_out, repo_name)
    if not os.path.isdir(path_out):
        os.mkdir(path_out)

    make_project_size_plot(data, path_out)
    make_classes_in_notations_plot(data, path_out)
    make_functions_in_notations_plot(data, path_out)
    make_classes_with_noun_plot(data, path_out)
    make_functions_with_verb_plot(data, path_out)
    make_words_to_avoid_plot(data, path_out)
    make_mean_len_plot(data, path_out)

    plt.close("all")

    end_time = datetime.now()
    duration = end_time - start_time

    with open(LOG_FILE_NAME, "a", -1, "utf-8") as log:
        log_and_print(f"{repo_name}:", log)
        log_and_print(f"    Started at {start_time:%H:%M:%S}, ended at {end_time:%H:%M:%S} (duration {duration})\n",
                      log)

    return 0


def make_project_size_plot(data: dict, path_out: str):
    df = data.copy()

    number_of_names = []
    sum_of_occurences = []

    for timestamp in df:
        number_of_names.append(len(df[timestamp]))
        sum_of_occurences.append(df[timestamp]["all"].sum())

    width_of_bars = 0.7

    fig, axs = plt.subplots(1, 2, layout="constrained", figsize=(9, 4.5))

    axs[0].set_ylabel("Liczba")
    axs[0].set_title("Liczba różnych identyfikatorów")

    p = axs[0].bar(df.keys(), number_of_names, width_of_bars)
    axs[0].bar_label(p, label_type="center", fmt=lambda x: f"{x:.0f}")

    axs[1].set_ylabel("Liczba")
    axs[1].set_title("Suma wystąpień identyfikatorów")

    p = axs[1].bar(df.keys(), sum_of_occurences, width_of_bars)
    axs[1].bar_label(p, label_type="center", fmt=lambda x: f"{x:.0f}")

    fig.savefig(os.path.join(path_out, "project_size_plot.png"), dpi=300, format="png")


def make_classes_in_notations_plot(data: dict, path_out: str):
    df = data.copy()

    good_notations = {"CapitalizedWords": [], "B": []}
    bad_notations = {"ugly": [], "b": [], "lower_case_with_underscores": [], "UPPER_CASE_WITH_UNDERSCORES": [],
                     "Capitalized_Words_With_Underscores": [], "camel_Snake_Case": [], "dash-case": [],
                     "COBOL-CASE": [], "lowercase": [], "UPPERCASE": [], "mixedCase": []}

    for timestamp in df:
        n_of_classes = 0
        for value in good_notations.values():
            value.append(0)
        for value in bad_notations.values():
            value.append(0)

        for row in df[timestamp].itertuples():
            if not np.isnan(row["class_def"]):
                n_of_classes += 1
                if row["naming_style"] in good_notations:
                    good_notations[row["naming_style"]][-1] += 1
                else:
                    bad_notations[row["naming_style"]][-1] += 1

        for value in good_notations.values():
            value[-1] = value[-1] * 100 / n_of_classes

    width_of_bars = 0.7
    colours = {"ugly": "red",
               "b": "sienna",
               "lower_case_with_underscores": "tomato",
               "UPPER_CASE_WITH_UNDERSCORES": "orange",
               "Capitalized_Words_With_Underscores": "yellow",
               "camel_Snake_Case": "pink",
               "dash-case": "fuchsia",
               "COBOL-CASE": "plum",
               "lowercase": "lightblue",
               "UPPERCASE": "aqua",
               "mixedCase": "aquamarine",
               "CapitalizedWords": "green",
               "B": "yellowgreen",
              }

    fig, axs = plt.subplots(1, 2, layout="constrained", figsize=(9, 4.5))

    axs[0].set_ylabel("Procent")
    axs[0].set_title("Identyfikatory klas w dobrej notacji")

    bottom = np.zeros(len(df.keys()))
    for notation, procents in good_notations.items():
        p = axs[0].bar(df.keys(), procents, width_of_bars, label=notation, bottom=bottom, color=colours[notation])
        bottom += procents
        axs[0].bar_label(p, label_type="center", fmt=lambda x: f"{x:.2f}%" if(x > 0) else "")

    axs[1].set_ylabel("Liczba")
    axs[1].set_title("Identyfikatory klas poza dobrą notacją")

    bottom = np.zeros(len(df.keys()))
    for notation, numbers in bad_notations.items():
        p = axs[1].bar(df.keys(), numbers, width_of_bars, label=notation, bottom=bottom, color=colours[notation])
        bottom += numbers
        axs[1].bar_label(p, label_type="center", fmt=lambda x: f"{x:.0f}" if(x > 0) else "")

    fig.legend(loc="outside lower center", reverse=True, ncols=3)
    fig.savefig(os.path.join(path_out, "classes_in_notations_plot.png"), dpi=300, format="png")


def make_functions_in_notations_plot(data: dict, path_out: str):
    df = data.copy()

    good_notations = {"lower_case_with_underscores": [], "lowercase": [], "b": []}
    bad_notations = {"ugly": [], "B": [], "UPPER_CASE_WITH_UNDERSCORES": [],
                     "Capitalized_Words_With_Underscores": [], "camel_Snake_Case": [], "dash-case": [],
                     "COBOL-CASE": [], "UPPERCASE": [], "CapitalizedWords": [], "mixedCase": []}

    for timestamp in df:
        n_of_functions = 0
        for value in good_notations.values():
            value.append(0)
        for value in bad_notations.values():
            value.append(0)

        for row in df[timestamp].itertuples():
            if not np.isnan(row["function_def"]):
                n_of_functions += 1
                if row["naming_style"] in good_notations:
                    good_notations[row["naming_style"]][-1] += 1
                else:
                    bad_notations[row["naming_style"]][-1] += 1

        for value in good_notations.values():
            value[-1] = value[-1] * 100 / n_of_functions

    width_of_bars = 0.7
    colours = {"ugly": "red",
               "B": "sienna",
               "UPPER_CASE_WITH_UNDERSCORES": "orange",
               "Capitalized_Words_With_Underscores": "yellow",
               "camel_Snake_Case": "pink",
               "dash-case": "fuchsia",
               "COBOL-CASE": "plum",
               "UPPERCASE": "aqua",
               "CapitalizedWords": "lightblue",
               "mixedCase": "aquamarine",
               "b": "yellowgreen",
               "lower_case_with_underscores": "green",
               "lowercase": "darkgreen",
              }

    fig, axs = plt.subplots(1, 2, layout="constrained", figsize=(9, 4.5))

    axs[0].set_ylabel("Procent")
    axs[0].set_title("Identyfikatory funkcji w dobrej notacji")

    bottom = np.zeros(len(df.keys()))
    for notation, procents in good_notations.items():
        p = axs[0].bar(df.keys(), procents, width_of_bars, label=notation, bottom=bottom, color=colours[notation])
        bottom += procents
        axs[0].bar_label(p, label_type="center", fmt=lambda x: f"{x:.2f}%" if(x > 0) else "")

    axs[1].set_ylabel("Liczba")
    axs[1].set_title("Identyfikatory funkcji poza dobrą notacją")

    bottom = np.zeros(len(df.keys()))
    for notation, numbers in bad_notations.items():
        p = axs[1].bar(df.keys(), numbers, width_of_bars, label=notation, bottom=bottom, color=colours[notation])
        bottom += numbers
        axs[1].bar_label(p, label_type="center", fmt=lambda x: f"{x:.0f}" if(x > 0) else "")

    fig.legend(loc="outside lower center", reverse=True, ncols=3)
    fig.savefig(os.path.join(path_out, "functions_in_notations_plot.png"), dpi=300, format="png")


def make_classes_with_noun_plot(data: dict, path_out: str):
    df = data.copy()

    classes_with_noun_in_procents = []
    classes_without_noun_in_numbers = []

    for timestamp in df:
        n_of_classes = 0
        n_of_classes_with_noun = 0

        for row in df[timestamp].itertuples():
            if not np.isnan(row["class_def"]):
                n_of_classes += 1
                if has_part_of_speech(row["name"], "n"):
                    n_of_classes_with_noun += 1

        classes_with_noun_in_procents.append(n_of_classes_with_noun * 100 / n_of_classes)
        classes_without_noun_in_numbers.append(n_of_classes - n_of_classes_with_noun)

    width_of_bars = 0.7

    fig, axs = plt.subplots(1, 2, layout="constrained", figsize=(9, 4.5))

    axs[0].set_ylabel("Procent")
    axs[0].set_title("Identyfikatory klas zawierające rzeczownik")

    p = axs[0].bar(df.keys(), classes_with_noun_in_procents, width_of_bars)
    axs[0].bar_label(p, label_type="center", fmt=lambda x: f"{x:.2f}%")

    axs[1].set_ylabel("Liczba")
    axs[1].set_title("Identyfikatory klas nie zawierające rzeczownika")

    p = axs[1].bar(df.keys(), classes_without_noun_in_numbers, width_of_bars)
    axs[1].bar_label(p, label_type="center", fmt=lambda x: f"{x:.0f}")

    fig.savefig(os.path.join(path_out, "classes_with_noun_plot.png"), dpi=300, format="png")


def make_functions_with_verb_plot(data: dict, path_out: str):
    df = data.copy()

    functions_with_verb_in_procents = []
    functions_without_verb_in_numbers = []

    for timestamp in df:
        n_of_functions = 0
        n_of_functions_with_verb = 0

        for row in df[timestamp].itertuples():
            if not np.isnan(row["function_def"]):
                n_of_functions += 1
                if has_part_of_speech(row["name"], "v"):
                    n_of_functions_with_verb += 1

        functions_with_verb_in_procents.append(n_of_functions_with_verb * 100 / n_of_functions)
        functions_without_verb_in_numbers.append(n_of_functions - n_of_functions_with_verb)

    width_of_bars = 0.7

    fig, axs = plt.subplots(1, 2, layout="constrained", figsize=(9, 4.5))

    axs[0].set_ylabel("Procent")
    axs[0].set_title("Identyfikatory funkcji zawierające czasownik")

    p = axs[0].bar(df.keys(), functions_with_verb_in_procents, width_of_bars)
    axs[0].bar_label(p, label_type="center", fmt=lambda x: f"{x:.2f}%")

    axs[1].set_ylabel("Liczba")
    axs[1].set_title("Identyfikatory funkcji nie zawierające czasownika")

    p = axs[1].bar(df.keys(), functions_without_verb_in_numbers, width_of_bars)
    axs[1].bar_label(p, label_type="center", fmt=lambda x: f"{x:.0f}")

    fig.savefig(os.path.join(path_out, "functions_with_verb_plot.png"), dpi=300, format="png")


def make_words_to_avoid_plot(data: dict, path_out: str):
    df = data.copy()

    words_to_avoid = ["klass", "clss", "classs"]
    names_to_avoid = ["l", "O", "I"]

    bad_names_in_procent = []
    bad_names_in_numbers = []


    for timestamp in df:
        n_of_bad_names = 0
        for row in df[timestamp].itertuples():
            if str(row["name"]) in names_to_avoid:
                n_of_bad_names += 1
                continue

            for word in split_to_words(row["name"]):
                if word in words_to_avoid:
                    n_of_bad_names += 1
                    break

        bad_names_in_procent.append(n_of_bad_names * 100 / len(df[timestamp]))
        bad_names_in_numbers.append(n_of_bad_names)

    width_of_bars = 0.7

    fig, axs = plt.subplots(1, 2, layout="constrained", figsize=(9, 4.5))

    axs[0].set_ylabel("Procent")
    axs[0].set_title("Identyfikatory zawierające omijane słowa")

    p = axs[0].bar(df.keys(), bad_names_in_procent, width_of_bars)
    axs[0].bar_label(p, label_type="center", fmt=lambda x: f"{x:.2f}%")

    axs[1].set_ylabel("Liczba")
    axs[1].set_title("Identyfikatory zawierające omijane słowa")

    p = axs[1].bar(df.keys(), bad_names_in_numbers, width_of_bars)
    axs[1].bar_label(p, label_type="center", fmt=lambda x: f"{x:.0f}")

    fig.savefig(os.path.join(path_out, "words_to_avoid_plot.png"), dpi=300, format="png")


def make_mean_len_plot(data: dict, path_out: str):
    df = data.copy()

    mean_len = []
    mean_number_of_words = []

    for timestamp in df:
        mean_len.append(df[timestamp]["len"].mean())
        mean_number_of_words.append(df[timestamp]["words"].apply(lambda x: str(x).count(",") + 1).mean())

    width_of_bars = 0.7

    fig, axs = plt.subplots(1, 2, layout="constrained", figsize=(9, 4.5))

    axs[0].set_ylabel("Liczba liter")
    axs[0].set_title("Średnia długość identyfikatora")

    p = axs[0].bar(df.keys(), mean_len, width_of_bars)
    axs[0].bar_label(p, label_type="center", fmt=lambda x: f"{x:.3f}")

    axs[1].set_ylabel("Liczba członów")
    axs[1].set_title("Średnia liczba członów w identyfikatorze")

    p = axs[1].bar(df.keys(), mean_number_of_words, width_of_bars)
    axs[1].bar_label(p, label_type="center", fmt=lambda x: f"{x:.3f}")

    fig.savefig(os.path.join(path_out, "maen_len_plot.png"), dpi=300, format="png")
