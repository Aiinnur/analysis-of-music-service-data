import os
os.chdir("D:\work")
import numpy as np
import pandas as pd

def text_describe(ITOG, how):
    """
    Функция создания текстого отчёта в виде базы данных,
    содержащей сведения о возрасте людей

    Args:
        ITOG (pd.DataFrame): общий справочник
        how (string): указатель на то, по каким данным делать отчёт

    Returns:
        pd.DataFrame: итоговый отчёт

    Автор: Сальник Максим
    """
    if how == 'Жанрам':
        DES = ITOG.groupby(["Любимый жанр музыки"]).describe()
        DES = DES.loc[:,"Возраст"]
        DES = DES.drop(columns = ['std', '25%', '75%'])
        DES.columns = ['Количество людей', 'Средний возраст', 'Минимальный возраст','Медиана возраста', 'Максимальный возраст']
    elif how == 'Всей таблице':
        DES = ITOG[["Возраст"]].describe()
        DES = DES.drop(labels = ['std', '25%', '75%'])
        DES.index = ['Количество людей', 'Средний возраст', 'Минимальный возраст','Медиана возраста', 'Максимальный возраст']
    return DES