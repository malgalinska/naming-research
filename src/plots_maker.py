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

    make_sample_plot(data, path)
    make_project_size_plot(data, path)
    make_mean_len_plot(data, path)
    make_weighted_mean_len_plot(data, path)
    make_procent_of_class_with_noun_plot(data, path)


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


def make_procent_of_class_with_noun_plot(data, path):
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
                print(str(row))
                for word in str(row[13]).strip("[']").split("', '"):
                    tag = nltk.pos_tag([word])[0][1]
                    if tag.startswith("NN"):
                        print(word + " - " + tag)
                        n_of_class_with_noun += 1
                        break
                    else:
                        print("Nie: " + word + " - " + tag)
            if n_of_class_with_noun >= 10:
                return
                # print (str(str(row[13]).split(", ")))
