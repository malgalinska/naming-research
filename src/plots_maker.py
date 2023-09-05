#!/usr/local/bin/python3.11
# coding: utf-8

import os
from datetime import datetime
\
import nltk # TEST
import numpy as np
import matplotlib.pyplot as plt

from statisctics_library import log_and_print, has_part_of_speech


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

    # make_mean_len_plot(data, path_out)
    # make_procent_of_classes_with_noun_plot(data, path_out)
    # make_number_of_classes_with_noun_plot(data, path_out)
    # make_procent_of_functions_with_verb_plot(data, path_out)
    # make_number_of_functions_with_verb_plot(data, path_out)
    # make_words_to_avoid_in_procents_plot(data, path_out)
    # make_number_of_words_to_avoid_plot(data, path_out)


    plt.close("all")

    end_time = datetime.now()
    duration = end_time - start_time

    with open(LOG_FILE_NAME, "a", -1, "utf-8") as log:
        log_and_print(f"{repo_name}:", log)
        log_and_print(f"    Started at {start_time:%H:%M:%S}, ended at {end_time:%H:%M:%S} (duration {duration})\n",
                      log)

    return 0


def make_project_size_plot(data: dict, path_out: str):
    fig, ax1 = plt.subplots()
    ax1.set_xlabel("Czas")
    ax1.set_ylabel("Liczba")

    df1 = data.copy()
    for timestamp in df1:
        df1[timestamp] = len(df1[timestamp])

    ax1.plot(df1.keys(), df1.values(), color="red", label="Liczba identyfikatorów")

    ax2 = ax1.twinx()
    ax2.set_ylabel("Suma")

    df2 = data.copy()
    for timestamp in df2:
        df2[timestamp] = df2[timestamp]["all"].sum()

    ax2.plot(df2.keys(), df2.values(), label="Suma wystąpień identyfikatorów")

    fig.legend(loc="upper left")
    fig.savefig(os.path.join(path_out, "project_size_plot.jpg"))


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
            if not np.isnan(row[4]):
                n_of_classes += 1
                if row[12] in good_notations:
                    good_notations[row[12]][-1] += 1
                else:
                    bad_notations[row[12]][-1] += 1
        
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
        axs[0].bar_label(p, label_type='center', fmt=lambda x: f"{x:.2f}%" if(x > 0) else "")

    axs[1].set_ylabel("Liczba")
    axs[1].set_title("Identyfikatory klas poza dobrą notacją")
    # axs[1].yaxis.set_major_locator(plt.MultipleLocator(1))

    bottom = np.zeros(len(df.keys()))
    for notation, numbers in bad_notations.items():
        p = axs[1].bar(df.keys(), numbers, width_of_bars, label=notation, bottom=bottom, color=colours[notation])
        bottom += numbers
        axs[1].bar_label(p, label_type='center', fmt=lambda x: f"{x:.0f}" if(x > 0) else "")

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
            if not np.isnan(row[3]):
                n_of_functions += 1
                if row[12] in good_notations:
                    good_notations[row[12]][-1] += 1
                else:
                    bad_notations[row[12]][-1] += 1
        
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
        axs[0].bar_label(p, label_type='center', fmt=lambda x: f"{x:.2f}%" if(x > 0) else "")

    axs[1].set_ylabel("Liczba")
    axs[1].set_title("Identyfikatory funkcji poza dobrą notacją")
    # axs[1].yaxis.set_major_locator(plt.MultipleLocator(1))

    bottom = np.zeros(len(df.keys()))
    for notation, numbers in bad_notations.items():
        p = axs[1].bar(df.keys(), numbers, width_of_bars, label=notation, bottom=bottom, color=colours[notation])
        bottom += numbers
        axs[1].bar_label(p, label_type='center', fmt=lambda x: f"{x:.0f}" if(x > 0) else "")

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
            if not np.isnan(row[4]):
                n_of_classes += 1
                if has_part_of_speech(row[13], "n"):
                    n_of_classes_with_noun += 1
        
        classes_with_noun_in_procents.append(n_of_classes_with_noun * 100 / n_of_classes)
        classes_without_noun_in_numbers.append(n_of_classes - n_of_classes_with_noun)

    width_of_bars = 0.7

    fig, axs = plt.subplots(1, 2, layout="constrained", figsize=(9, 4.5))

    axs[0].set_ylabel("Procent")
    axs[0].set_title("Identyfikatory klas zawierające rzeczownik")

    p = axs[0].bar(df.keys(), classes_with_noun_in_procents, width_of_bars)
    axs[0].bar_label(p, label_type='center', fmt=lambda x: f"{x:.2f}%")

    axs[1].set_ylabel("Liczba")
    axs[1].set_title("Identyfikatory klas nie zawierające rzeczownika")

    p = axs[1].bar(df.keys(), classes_without_noun_in_numbers, width_of_bars)
    axs[1].bar_label(p, label_type='center', fmt=lambda x: f"{x:.0f}")

    fig.savefig(os.path.join(path_out, "classes_with_noun_plot.png"), dpi=300, format="png")


def make_mean_len_plot(data: dict, path_out: str):
    fig,ax = plt.subplots()
    ax.set_xlabel("Czas")
    ax.set_ylabel("Liczba liter")

    df1 = data.copy()
    for x in df1:
        df1[x] = df1[x]["len"].mean()

    ax.plot(df1.keys(), df1.values(), color="red", label="Średnia długość identyfikatora")
    
    ax2 = ax.twinx()
    ax2.set_ylabel("Liczba członów")

    df2 = data.copy()
    for x in df2:
        df2[x]["n_of_words"] = df2[x]["words"].apply(lambda x: str(x).count(",") + 1)
        df2[x] = df2[x]["n_of_words"].mean()

    ax2.plot(df2.keys(), df2.values(), label="Średnia liczba członów w identyfikatorze")
    
    fig.legend()
    fig.savefig(os.path.join(path_out, "maen_len_plot.jpg"))


def make_procent_of_functions_with_verb_plot(data: dict, path_out: str):
    fig,ax = plt.subplots()
    ax.set_xlabel("Czas")
    ax.set_ylabel("Procent")

    df = data.copy()
    for x in df:
        n_of_function = 0
        n_of_function_with_verb = 0
        for row in df[x].itertuples():
            if not np.isnan(row[3]):
                n_of_function += 1
                # print(str(row))
                for word in str(row[13]).strip("[']").split("', '"):
                    tag = nltk.pos_tag([word])[0][1]
                    if tag.startswith("VB"):
                        # print(word + " - " + tag)
                        n_of_function_with_verb += 1
                        break
                    # else:
                        # print("Nie: " + word + " - " + tag)
            # if n_of_class_with_noun >= 10:
            #     return
                # print (str(str(row[13]).split(", ")))
        df[x] = n_of_function_with_verb * 100 / n_of_function

    ax.plot(df.keys(), df.values(), label="Procent identyfikatorów funkcji zawierających czasownik")
    
    fig.legend()
    fig.savefig(os.path.join(path_out, "procent_of_functions_with_verb_plot.jpg"))


def make_number_of_functions_with_verb_plot(data: dict, path_out: str):
    fig,ax = plt.subplots()
    ax.set_xlabel("Czas")
    ax.set_ylabel("Liczba")

    df = data.copy()
    for x in df:
        n_of_function_with_verb = 0
        for row in df[x].itertuples():
            if not np.isnan(row[3]):
                # print(str(row))
                for word in str(row[13]).strip("[']").split("', '"):
                    tag = nltk.pos_tag([word])[0][1]
                    if tag.startswith("VB"):
                        # print(word + " - " + tag)
                        n_of_function_with_verb += 1
                        break
                    # else:
                        # print("Nie: " + word + " - " + tag)
            # if n_of_class_with_noun >= 10:
            #     return
                # print (str(str(row[13]).split(", ")))
        df[x] = n_of_function_with_verb

    ax.plot(df.keys(), df.values(), label="Liczba identyfikatorów funkcji zawierających czasownik")
    
    fig.legend()
    fig.savefig(os.path.join(path_out, "number_of_functions_with_verb_plot.jpg"))


def make_words_to_avoid_in_procents_plot(data: dict, path_out: str):
    words_to_avoid = ["klass", "clss"]

    fig,ax = plt.subplots()
    ax.set_xlabel("Czas")
    ax.set_ylabel("Procent")

    df = data.copy()
    for x in df:
        n_of_bad_names = 0
        for row in df[x].itertuples():
            for word in str(row[13]).strip("[']").split("', '"):
                if word in words_to_avoid:
                    n_of_bad_names += 1
                    break

        df[x] = n_of_bad_names * 100 / len(df[x])

    ax.plot(df.keys(), df.values(), label="Procent identyfikatorów ze słowami do omijania")
    
    fig.legend()
    fig.savefig(os.path.join(path_out, "words_to_avoid_in_procents_plot.jpg"))


def make_number_of_words_to_avoid_plot(data: dict, path_out: str):
    words_to_avoid = ["klass", "clss"]

    fig,ax = plt.subplots()
    ax.set_xlabel("Czas")
    ax.set_ylabel("Liczba")

    df = data.copy()
    for x in df:
        n_of_bad_names = 0
        for row in df[x].itertuples():
            for word in str(row[13]).strip("[']").split("', '"):
                if word in words_to_avoid:
                    n_of_bad_names += 1
                    break

        df[x] = n_of_bad_names

    ax.plot(df.keys(), df.values(), label="Liczba identyfikatorów ze słowami do omijania")
    
    fig.legend()
    fig.savefig(os.path.join(path_out, "number_of_words_to_avoid_plot.jpg"))

    

