import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import pandas as pd

def make_table_wholetable(name, master, column_names, index_names):
    """
    Функция вывода справочника в окно приложения

    Args:
        name (pd.DataFrame): справочник, который нужно вывести
        master (Tk): окно или фрейм, в который выводится справочник
        column_names (list): список с названиями столбцов
        index_names (list): список с названиями строк
    
    Автор: Сальник Максим
    """
    name = name.copy()  #Копирование, чтобы избежать изменение исходных данных
    name.columns = column_names 
    name.index = index_names

    height = name.shape[0]
    width = name.shape[1]

    # Создание виджета Canvas
    canvas = tk.Canvas(master)
    canvas.pack(side="left", fill="both", expand=True)

    # Создание Scrollbar по вертикали
    y_scrollbar = ttk.Scrollbar(master, orient="vertical", command=canvas.yview)
    y_scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=y_scrollbar.set)

    # Создание Scrollbar по горизонтали
    x_scrollbar = ttk.Scrollbar(master, orient="horizontal", command=canvas.xview)
    x_scrollbar.pack(side="bottom", fill="x")
    canvas.configure(xscrollcommand=x_scrollbar.set)

    # Создание вложенного фрейма для размещения таблицы
    table_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=table_frame, anchor="nw")

    # Добавление заголовков столбцов
    for j, col_name in enumerate(column_names):
        label = ttk.Label(table_frame, text=col_name)
        label.grid(row=0, column=j+1, sticky="nsew")

    # Добавление заголовков строк
    for i, ind_name in enumerate(index_names):
        label = ttk.Label(table_frame, text=ind_name)
        label.grid(column=0, row=i+1, sticky="nsew")

    # Создание и заполнение таблицы Entry
    entry_widgets = [] 
    for i in range(height):
        row_widgets = []
        for j in range(width):
            entry = ttk.Entry(table_frame)
            entry.grid(row=i+1, column=j+1, sticky="nsew")

            value = name.iloc[i, j]
            entry.insert(0, value)

            row_widgets.append(entry)
        entry_widgets.append(row_widgets)
    
    # Растягивание ячеек таблицы при изменении размеров окна
    for i in range(height + 1):
        table_frame.rowconfigure(i, weight=1)
    for j in range(width):
        table_frame.columnconfigure(j, weight=1)

    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))