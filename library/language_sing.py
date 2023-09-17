import os
os.chdir("D:\work")
import numpy as np
import pandas as pd


def language_singer (ITOG, genre, language): #Получаем исполнителей и их любимый трек
    """
    Функция создания текстого отчёта в виде базы данных,
    содержащей сведения об исполнителях и их песнях,
    в данном жанре и на данном языке

    Args:
        ITOG (pd.DataFrame): общий справочник
        genre (string): жанр, по которому следует искать совпадения
        language (string): язык, по которому следует искать совпадения

    Returns:
        pd.DataFrame: итоговый отчёт

    Автор: Кучерявая Элина
    """
    SEL = (ITOG["Жанр любимого исполнителя"] == genre) & (ITOG["Язык любимого исполнителя"] == language)
    W1 = ITOG.loc[SEL, ["Любимый исполнитель", "Самый популярный трек любимого исполнителя"]]
    return W1