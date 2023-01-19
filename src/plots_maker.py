#!/usr/bin/python3
# coding: utf-8
import os

import matplotlib.pyplot as plt
import numpy as np
import nltk


def make_plots (data: dict, repo_name: str, path: str):
    path = path + "/" + repo_name
    if not os.path.isdir(path):
        os.mkdir(path)
    path = path + "/"

    # make_sample_plot(data, path)
    # make_project_size_plot(data, path)
    # make_mean_len_plot(data, path)
    # make_weighted_mean_len_plot(data, path)
    # make_procent_of_classes_with_noun_plot(data, path)
    # make_procent_of_functions_with_verb_plot(data, path)
    # make_words_to_avoid_in_procents_plot(data, path)
    make_procent_of_good_convention_plot(data, path)


def make_sample_plot(data, path):
    # plt.figure(figsize=(15, 15))
    fig, ax = plt.subplots()
    ax.set_xlabel("Liczba liter")
    ax.set_ylabel("Liczba wystąpień")

    # plt.hist2d(data["2022"]["len"], data["2022"]["all"], color="blue", alpha=0.5, label="2022")

    ax.hist2d(data["2023"]["len"], data["2023"]["all"], bins=(80, 40000), label="2023")
    ax.set(xlim=(0, 80), ylim=(1, 10))

    # plt.legend()
    plt.savefig(path + "sample_plot.jpg")


def make_project_size_plot(data, path):
    fig,ax = plt.subplots()
    ax.set_xlabel("Czas")
    ax.set_ylabel("Ilość")

    df1 = data.copy()
    for x in df1:
        df1[x] = len(df1[x])

    ax.plot(df1.keys(), df1.values(), color="red", label="Ilość nazw")
    
    ax2 = ax.twinx()
    ax2.set_ylabel("Suma")

    df2 = data.copy()
    for x in df2:
        df2[x] = df2[x]['all'].sum()

    ax2.plot(df2.keys(), df2.values(), label="Suma wystąpień nazw")
    
    fig.legend(loc="upper left")
    fig.savefig(path + "project_size_plot.jpg")


def make_mean_len_plot(data, path):
    fig,ax = plt.subplots()
    ax.set_xlabel("Czas")
    ax.set_ylabel("Ilość liter")

    df1 = data.copy()
    for x in df1:
        df1[x] = df1[x]['len'].mean()

    ax.plot(df1.keys(), df1.values(), color="red", label="Średnia długość nazwy")
    
    ax2 = ax.twinx()
    ax2.set_ylabel("Ilość członów")

    df2 = data.copy()
    for x in df2:
        df2[x]['n_of_words'] = df2[x]['words'].apply(lambda x: str(x).count(",") + 1)
        df2[x] = df2[x]['n_of_words'].mean()

    ax2.plot(df2.keys(), df2.values(), label="Średnia ilość członów w nazwie")
    
    fig.legend()
    fig.savefig(path + "maen_len_plot.jpg")


def make_weighted_mean_len_plot(data, path):
    fig,ax = plt.subplots()
    ax.set_xlabel("Czas")
    ax.set_ylabel("Ilość liter")

    df1 = data.copy()
    for x in df1:
        df1[x] = (df1[x]['len'] * df1[x]['all']).sum() / df1[x]['all'].sum()

    ax.plot(df1.keys(), df1.values(), color="red", label="Średnia długość nazwy")
    
    ax2 = ax.twinx()
    ax2.set_ylabel("Ilość członów")

    df2 = data.copy()
    for x in df2:
        df2[x]['n_of_words'] = df2[x]['words'].apply(lambda x: str(x).count(",") + 1)
        df2[x] = (df2[x]['n_of_words'] * df2[x]['all']).sum() / df2[x]['all'].sum()

    ax2.plot(df2.keys(), df2.values(), label="Średnia ilość członów w nazwie")
    
    fig.legend()
    fig.savefig(path + "weighted_mean_len_plot.jpg")


def make_procent_of_classes_with_noun_plot(data, path):
    fig,ax = plt.subplots()
    ax.set_xlabel("Czas")
    ax.set_ylabel("Procent")

    df = data.copy()
    for x in df:
        n_of_class = 0
        n_of_class_with_noun = 0
        for row in df[x].itertuples():
            if not np.isnan(row[4]):
                n_of_class += 1
                # print(str(row))
                for word in str(row[13]).strip("[']").split("', '"):
                    tag = nltk.pos_tag([word])[0][1]
                    if tag.startswith("NN"):
                        # print(word + " - " + tag)
                        n_of_class_with_noun += 1
                        break
                    # else:
                        # print("Nie: " + word + " - " + tag)
            # if n_of_class_with_noun >= 10:
            #     return
                # print (str(str(row[13]).split(", ")))
        df[x] = n_of_class_with_noun * 100 / n_of_class

    ax.plot(df.keys(), df.values(), label="Procent klas z rzeczownikiem w nazwie")
    
    fig.legend()
    fig.savefig(path + "procent_of_class_with_noun_plot.jpg")


def make_procent_of_functions_with_verb_plot(data, path):
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

    ax.plot(df.keys(), df.values(), label="Procent funkcji z czasownikiem w nazwie")
    
    fig.legend()
    fig.savefig(path + "procent_of_functions_with_verb_plot.jpg")


def make_words_to_avoid_in_procents_plot(data, path):
    words_to_avoid = ["klass", 'clss']

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

    ax.plot(df.keys(), df.values(), label="Procent nazw ze słowami do omijania")
    
    fig.legend()
    fig.savefig(path + "words_to_avoid_in_procents_plot.jpg")


def make_procent_of_good_convention_plot(data, path):
    fig, ax = plt.subplots()

    ax.set_ylabel('Procent')
    ax.set_title('Procent nazw w dobrej konwencji')

    df = data.copy()
    procents_of_classes = []
    procents_of_functions = [] 
    for x in df:
        n_of_classes = 0
        n_of_good_classes = 0
        n_of_functions = 0
        n_of_good_functions = 0
        for row in df[x].itertuples():
            if not np.isnan(row[4]):
                n_of_classes += 1
                if row[12] == "CapitalizedWords" or row[12] == "B":
                    n_of_good_classes += 1
            if not np.isnan(row[3]):
                n_of_functions += 1
                if row[12] == "lower_case_with_underscores" or row[12] == "lowercase" or row[12] == "b":
                    n_of_good_functions += 1
        # df[x] = [n_of_good_classes * 100 / n_of_classes, n_of_good_functions * 100 / n_of_good_functions]
        procents_of_classes.append(n_of_good_classes * 100 / n_of_classes)
        procents_of_functions.append(n_of_good_functions * 100 / n_of_good_functions)

    x = np.arange(len(df.keys()))  # the label locations
    width = 0.35  # the width of the bars
    
    ax.set_xticks(x, df.keys())

    rects1 = ax.bar(x - width/2, procents_of_classes, width, label='Klasy')
    rects2 = ax.bar(x + width/2, procents_of_functions, width, label='Funkcje')

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()

    fig.legend(loc="upper left")
    fig.savefig(path + "procent_of_good_convention_plot.jpg")
