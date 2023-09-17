import os
import numpy as np
import pandas as pd

def singers_listeners (ITOG, singer): #Пользователи, которые слушают конкретного исполнителя 
    """
    Функция создания текстового отчёта в виде базы данных,
    содержащей информацию о людях, слушающих данного исполнителя

    Args:
        ITOG (pd.DataFrame): общий справочник
        singer (string): имя исполнителя

    Returns:
        pd.DataFrame: итоговый отчёт

    Автор: Муратов Айнур
    """
    SEL = (ITOG["Любимый исполнитель"] == singer)
    W1 = ITOG.loc[SEL, ["Идентификатор пользователя","Имя","Фамилия", "Любимый жанр музыки"]]
    return W1