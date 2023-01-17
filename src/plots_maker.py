#!/usr/bin/python3
# coding: utf-8

import matplotlib.pyplot as plt
# import pandas as pd

def make_plots (dfs: dict):
    make_sample_plot(dfs)
    project_size_plot(dfs)


def make_sample_plot(dfs):
    print(str(dfs))
    df = dfs['2022']
    df2 = dfs['2023']

    plt.figure(figsize=(15, 15))

    plt.xlabel("Liczba liter")
    plt.ylabel("Liczba wystąpień")

    x = df['len']
    y = df['all']
    plt.scatter(x, y, marker = '.', color="blue", alpha=0.5, label="Pierwsza wersja")

    x2 = df2['len']
    y2 = df2['all']
    plt.scatter(x2, y2, marker = '.', color="red", alpha=0.5, label="Druga wersja")

    plt.legend()
    plt.savefig(dfs['repo_name'] + "_sample_plot.jpg")


def project_size_plot(dfs):
    pass
