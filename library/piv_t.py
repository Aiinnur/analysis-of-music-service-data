import os
import numpy as np
import pandas as pd

def piv_table(ITOG):
    """
    Функция создания текстого отчёта в виде базы данных,
    представляющей собой сводную таблицу, в которой
    видна зависимость возраста слушателя от языка и жанра музыки

    Args:
        ITOG (pd.DataFrame): общий справочник

    Returns:
        pd.DataFrame: итоговый отчёт

    Автор: Сальник Максим
    """
    REP= pd.pivot_table(ITOG, index='Язык любимого исполнителя', columns='Жанр любимого исполнителя', values='Возраст', aggfunc='mean')
    return REP