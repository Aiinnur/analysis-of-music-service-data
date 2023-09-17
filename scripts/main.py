"""
Cамостоятельная работа по курсу —
«Проектный семинар «Python в науке о данных»

Авторы:
    Муратов Айнур
    Кучерявая Элина
    Сальник Максим
"""
from tkinter import ttk
from tkinter import messagebox
from tkinter.messagebox import askyesno
from tkinter.ttk import Combobox
import os
import sys
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
os.chdir("D:\work")
sys.path.append("D:\work")
from library.read_table import make_table
from library.save_file import save_file
from scripts.genre_match import genre_matches
from scripts.singer_match import singers_listeners
from scripts.language_sing import language_singer
from scripts.describing import text_describe
from library.made_table_whole import make_table_wholetable
from scripts.piv_t import piv_table



BACKGR = '#745e8a'

def change_color(color):
    """
    Изменение фонового цвета

    Args:
        color (string): Цвет нового фона

    Автор: Сальник Максим
    """
    result = askyesno(title='Подтверждение операции',
                      message='Для выполнения операции'+
                      ' необходимо закрыть все окна и'+
                      ' несохраненные изменения пропадут.\nПродолжить?')
    if result:
        for widget in root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()
        button1.config(state='normal')
        button2.config(state='normal')
        button3.config(state='normal')
        root["bg"] = color
        global BACKGR
        BACKGR = color
        style.configure("Custom.TLabel", background=color, foreground="black")

def update_data():
    """
    Функция обновления справочников

    Автор: Муратов Айнур
    """
    global TABLE_ONE
    TABLE_ONE = pd.read_csv('./data/Tab1.csv', delimiter=';', encoding='cp1251')
    global TABLE_TWO
    TABLE_TWO = pd.read_csv('./data/Tab2.csv', delimiter=';', encoding='cp1251')
    global ITOG
    ITOG = pd.merge(TABLE_ONE, TABLE_TWO, on="Любимый исполнитель")

#Прогрузка справочников
update_data()

def add_entity():
    """
    Функция добавления сущности в справочник

    Автор: Муратов Айнур
    """
    add_window = tk.Toplevel(root)
    add_window.title("Добавить сущность")

    labels = ["ID пользователя:", "Имя:", "Фамилия:",
              "Возраст:", "Любимый исполнитель:", "Любимый жанр музыки:",
              "Число слушателей за месяц:", "Жанр любимого исполнителя:",
              "Самый популярный трек:", "Язык исполнителя:"]
    entries = []

    for i, label in enumerate(labels):
        lbl = tk.Label(add_window, text=label)
        lbl.grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(add_window)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    def save_entity():
        """
        Функция сохранения новых данных

        Автор: Муратов Айнур
        """
        new_entity = {}
        for i, entry in enumerate(entries):
            new_entity[labels[i]] = entry.get()

        table1_path = './data/Tab1.csv'
        table2_path = './data/Tab2.csv'

        # Сохранение данных в Table1
        table1_data = [new_entity[label] for label in labels[:6]]
        table1 = pd.DataFrame([table1_data], columns=labels[:6])
        file_exists = os.path.isfile(table1_path)
        table1.to_csv(table1_path, index=False, mode='a',
                      header=not file_exists, sep=';', encoding='cp1251')

        # Проверка наличия Любимого исполнителя в Table2.csv
        favorite_artist = new_entity["Любимый исполнитель:"]
        table2_exists = os.path.isfile(table2_path)
        if table2_exists:
            table2 = pd.read_csv(table2_path, delimiter=';', encoding='cp1251')
            if not table2['Любимый исполнитель'].str.contains(favorite_artist).any():
                table2_data = [new_entity[label] for label in (labels[4:5] + labels[6:10])]
                table2_data = pd.DataFrame([table2_data],
                                           columns=(labels[4:5] + labels[6:10]))
                table2_data.to_csv(table2_path, index=False,
                                   mode='a', header=False, sep=';',
                                   encoding='cp1251')
        else:
            table2_data = pd.DataFrame(
                [new_entity[label] for label in (labels[4:5] + labels[6:10])],
                                       columns=(labels[4:5] + labels[6:10])
                                       )
            table2_data.to_csv(table2_path, index=False, sep=';', encoding='cp1251')
        update_data()
        add_window.destroy()
        messagebox.showinfo("Отлично", "Сущность успешно добавлена!")

    save_button = tk.Button(add_window, text="Сохранить", command=save_entity)
    save_button.grid(row=len(labels), columnspan=2, padx=10, pady=5)
# Функция-обработчик для кнопки со справочником с пользователями
def show_table_one(bgr):
    """
    Функция показа окна с первым справочниклм

    Args:
        bgr (string): Цвет фона

    Автор: Муратов Айнур
    """

    # Блокировка кнопки повторного вызова таблицы
    button1.config(state='disabled')

    # Ф-я разблокирования кнопки и закртыия окна
    def on_button():
        """
        Функция разблокирования кнопки после закрытия окна

        Автор: Муратов Айнур
        """
        window.destroy()
        button1.config(state='')

    window = tk.Toplevel(root)
    window.title("Справочник с пользователями")
    window.configure(bg=BACKGR)
    window.minsize(800, 520)
    window.focus()
    colum_names = ["ID пользователя", "Имя", "Фамилия",
                   "Возраст", "Любимый исполнитель", "Любимый жанр музыки"]

    menubar = tk.Menu(window)
    # Создание меню "Файл"
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Сохранить", command = lambda:save_file(TABLE_ONE))
    file_menu.add_separator()
    file_menu.add_command(label="Выход", command=on_button)
    menubar.add_cascade(label="Файл", menu=file_menu)
    window.config(menu=menubar)

    top = tk.LabelFrame(window, text="Справочник с пользователями", bg=bgr)
    top.pack(expand=True, fill="both")

    make_table(TABLE_ONE, top, colum_names)

    # Создание протокла действий при попытке пользователя закрыть окно
    window.protocol("WM_DELETE_WINDOW", on_button)



def show_itog(bgr):
    """
    Функция показа окна с общим справочником

    Args:
        bgr (string): Цвет фона

    Автор: Муратов Айнур
    """

    # Блокировка кнопки повторного вызова таблицы
    button2.config(state='disabled')

    # Ф-я разблокирования кнопки и закртыия окна
    def on_button():
        """
        Функция разблокирования кнопки после закрытия окна

        Автор: Муратов Айнур
        """
        window.destroy()
        button2.config(state='normal')


    window = tk.Toplevel(root)
    window.title("Общий справочник")
    window.focus()
    window.minsize(800, 520)
    window.configure(bg=BACKGR)
    colum_names = ["ID пользователя", "Имя", "Фамилия", "Возраст",
                   "Любимый исполнитель", "Любимый жанр музыки",
                   "Число слушателей за месяц", "Жанр любимого исполнителя",
                   "Самый популярный трек", "Язык исполнителя"]
    menubar = tk.Menu(window)
    # Создание меню Файл
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Добавить сущность", command= add_entity)
    file_menu.add_command(label="Сохранить", command = lambda:save_file(ITOG))
    file_menu.add_separator()
    file_menu.add_command(label="Выход", command=on_button)
    # Создание меню Графические отчеты
    graph_reports_menu = tk.Menu(menubar, tearoff=0)
    graph_reports_menu.add_command(label="Гистограмма жанровых совпадений",
                                   command= lambda: create_genre_histogram(menubar))
    graph_reports_menu.add_command(label="Популярность артистов",
                                   command= lambda: create_popularity_chart(menubar))
    graph_reports_menu.add_command(label="Диаграмма Бокс-Вискера",
                                   command= lambda: create_boxplot(menubar))
    graph_reports_menu.add_command(label="Диаграмма рассеивания",
                                   command= lambda: create_scatterplot(menubar))
    graph_reports_menu.add_command(label='Кластерная гистограмма',
                                   command= lambda: create_clastar(menubar))
    # Создание меню Сводная таблица
    pivot_table_menu = tk.Menu(menubar, tearoff=0)
    pivot_table_menu.add_command(label="Генерировать сводную таблицу возрастов",
                                 command= lambda: text_pivot(menubar, BACKGR))
    # Создание меню смены цыета фона
    color_menu = tk.Menu(menubar, tearoff=0)
    color_menu.add_command(label="По умолчанию", command= lambda: change_color('#745e8a'))
    color_menu.add_command(label="Зеленый", command= lambda: change_color('#598a34') )
    color_menu.add_command(label="Синий", command= lambda:change_color('#4b5c99') )


    text_reports_menu = tk.Menu(menubar, tearoff=0)

    menubar.add_cascade(label="Файл", menu=file_menu)
    menubar.add_cascade(label="Текстовые отчеты", menu=text_reports_menu)
    menubar.add_cascade(label="Графические отчеты", menu=graph_reports_menu)
    menubar.add_cascade(label="Сводная таблица", menu=pivot_table_menu)
    menubar.add_cascade(label="Смена фона", menu= color_menu )
    # Создание меню Текстовые отчеты
    text_reports_menu.add_command(label="Возрастные сведения",
                                  command = lambda: text_describer(menubar, BACKGR))
    text_reports_menu.add_command(label="Соответствие жанров",
                                  command= lambda: text_genre(menubar, BACKGR))
    text_reports_menu.add_command(label="Поиск по языку и жанру",
                                  command= lambda: text_lang(menubar, BACKGR))
    text_reports_menu.add_command(label="Посик слушателей нужного исполнителя",
                                  command= lambda: text_singer(menubar, BACKGR))

    window.config(menu=menubar)
    top = tk.LabelFrame(window, text="Общий справочник", bg=bgr)
    top.pack(expand=True, fill="both")

    make_table(ITOG, top, colum_names)
    # Создание протокла действий при попытке пользователя закрыть окно
    window.protocol("WM_DELETE_WINDOW", on_button)

    window.mainloop()
def show_table_two(bgr):
    """
    Функция показа окна со вторым справочником

    Args:
        bgr (string): Цвет фона

    Автор: Муратов Айнур
    """

    # Блокировка кнопки повторного вызова таблицы
    button3.config(state='disabled')

    # Ф-я разблокирования кнопки и закртыия окна
    def on_button():
        """
        Функция разблокирования кнопки после закрытия окна

        Автор: Муратов Айнур
        """
        window.destroy()
        button3.config(state='')

    window = tk.Toplevel(root)
    window.title("Справочник с исполнителями")
    window.minsize(800, 520)
    window.focus()
    window.configure(bg=BACKGR)
    colum_names = ["Любимый исполнитель", "Число слушателей за месяц",
                   "Жанр любимого исполнителя", "Самый популярный трек",
                   "Язык исполнителя"]
    menubar = tk.Menu(window)
    # Создание меню "Файл"
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Сохранить", command = lambda:save_file(TABLE_TWO))
    file_menu.add_separator()
    file_menu.add_command(label="Выход", command=on_button)
    menubar.add_cascade(label="Файл", menu=file_menu)
    window.config(menu=menubar)
    top = tk.LabelFrame(window, text="Справочник с исполнителями", bg=bgr)
    top.pack(expand=True, fill="both")

    make_table(TABLE_TWO, top, colum_names)

    # Создание протокла действий при попытке пользователя закрыть окно
    window.protocol("WM_DELETE_WINDOW", on_button)

def text_describer(men, bgr):
    """
    Функция составяления текстового отчёта в виде возрастной статистике

    Args:
        men (tk.Menu): меню, из которого вызвалась функция
        bgr (string): цвет фона

    Автор: Сальник Максим
    """
    def generate_second():
        """
        Функция формирования отчёта
        Автор: Сальник Максим
        """
        for widgets in frame_rep.winfo_children():
            widgets.destroy()
        txt = text_describe(ITOG, entry.get())
        if entry.get() == 'Жанрам':
            colum_names = ['Количество людей', 'Средний возраст',
                           'Минимальный возраст','Медиана возраста',
                           'Максимальный возраст']
            index_names = txt.index
            make_table_wholetable(txt, frame_rep, colum_names, index_names)
        elif entry.get() == 'Всей таблице':
            colum_names = ["Значение"]
            index_names = ['Количество людей', 'Средний возраст',
                           'Минимальный возраст','Медиана возраста',
                           'Максимальный возраст']
            make_table_wholetable(txt, frame_rep, colum_names, index_names)
    def on_button():
        """
        Функция закрытия окна и разблокировки кнопки
        Автор: Сальник Максим
        """
        window.destroy()
        men.entryconfig("Текстовые отчеты", state='normal')

    window = tk.Toplevel(root)
    window.configure(bg=bgr)
    window.minsize(800, 520)
    window.title("Возрастные сведения")
    frame_rep = tk.Frame(window)
    frame_rep.pack(side='left')
    frame_panel = tk.Frame(window, background=bgr)
    frame_panel.pack(expand=1)
    lbl = tk.Label(frame_panel, text='Возрастная статистика по:', bg= bgr, font=("Times", 20))
    lbl.pack(padx=10, pady=10)
    entry = Combobox(frame_panel, state='readonly', font=("Times", 20))
    entry['values'] = ('Всей таблице', 'Жанрам')
    entry.current(0)
    entry.pack(padx=10, pady=10)
    button_create = ttk.Button(frame_panel, text="Сгенерировать",
                               style="Custom.TButton", command= generate_second)
    button_create.pack(padx=10, pady=10)
    button_save = ttk.Button(frame_panel, text="Сохранить",
                             style="Custom.TButton",
                             command= lambda: save_file(text_describe(ITOG, entry.get())))
    button_save.pack(padx=10, pady=10)
    men.entryconfig("Текстовые отчеты", state='disabled')
    # Создание протокла действий при попытке пользователя закрыть окно
    window.protocol("WM_DELETE_WINDOW", on_button)

# Функция текстового отчёта для сопоставления жанра
def text_genre(men, bgr):
    """
    Функция составяления текстового отчёта о пользователе и рекомендованной для него песне,
    если его любимый жанр совпал с жанром исполнителя

    Args:
        men (tk.Menu): меню, из которого вызвалась функция
        bgr (string): цвет фона

    Автор: Сальник Максим
    """
    def on_button():
        """
        Функция закрытия окна и разблокировки кнопки
        Автор: Сальник Максим
        """
        window.destroy()
        men.entryconfig("Текстовые отчеты", state='normal')
    def generate_second():
        """
        Функция формирования отчёта
        Автор: Сальник Максим
        """
        for widgets in frame_rep.winfo_children():
            widgets.destroy()
        txt = genre_matches(ITOG, entry.get())
        if txt.empty:
            lbl = tk.Label(frame_rep, text='Совпадений нет', font=("Times", 25))
            lbl.pack(padx=10, pady=10)
        else:
            make_table(txt, frame_rep, colum_names)

    colum_names = ["Идентификатор пользователя","Имя","Фамилия",
                   "Самый популярный трек любимого исполнителя"]
    window = tk.Toplevel(root)
    window.minsize(800, 520)
    window.title("Соответствие жанров")
    window.configure(bg=bgr)
    frame_rep = tk.Frame(window)
    frame_rep.pack(side='left')
    #make_table(TABLE_TWO, frame_rep)
    frame_panel = tk.Frame(window, bg=bgr)
    frame_panel.pack(expand=1)
    lbl = tk.Label(frame_panel, text='Совпадения по жанру:', bg= bgr, font=("Times", 20))
    lbl.pack(padx=10, pady=10)
    entry = Combobox(frame_panel, values = list(TABLE_ONE['Любимый жанр музыки'].unique())[:-1],
                     state='readonly', font=("Times", 20))
    entry['values'] = (list(TABLE_ONE['Любимый жанр музыки'].unique())[:-1])
    entry.current(0)
    entry.pack(padx=10, pady=10)
    button_create = ttk.Button(frame_panel, text="Сгенерировать",
                               style="Custom.TButton", command= generate_second)
    button_create.pack(padx=10, pady=10)
    button_save = ttk.Button(frame_panel, text="Сохранить",
                             style="Custom.TButton",
                             command= lambda: save_file(genre_matches(ITOG, entry.get())))
    button_save.pack(padx=10, pady=10)
    men.entryconfig("Текстовые отчеты", state='disabled')
    # Создание протокла действий при попытке пользователя закрыть окно
    window.protocol("WM_DELETE_WINDOW", on_button)


# Функция текстового отчёта для поиска слушателей исполнителя
def text_singer(men, bgr):
    """
    Функция составяления текстового отчёта о пользователях и их любимом жанре музыки,
    если они слушают данного исполнителя
    Args:
        men (tk.Menu): меню, из которого вызвалась функция
        bgr (string): цвет фона

    Автор: Сальник Максим
    """
    def on_button():
        """
        Функция закрытия окна и разблокировки кнопки
        Автор: Сальник Максим
        """
        window.destroy()
        men.entryconfig("Текстовые отчеты", state='normal')
    def generate_second():
        """
        Функция формирования отчёта
        Автор: Сальник Максим
        """
        for widgets in frame_rep.winfo_children():
            widgets.destroy()
        txt = singers_listeners(ITOG, entry.get())
        if txt.empty:
            lbl = tk.Label(frame_rep, text='Совпадений нет', font=("Times", 25))
            lbl.pack(padx=10, pady=10)
        else:
            make_table(txt, frame_rep, colum_names)
    colum_names = ["Идентификатор пользователя","Имя","Фамилия", "Любимый жанр музыки"]
    window = tk.Toplevel(root)
    window.minsize(800, 520)
    window.title("Поиск слушателей нужного исполнителя")
    window.configure(bg=bgr)
    frame_rep = tk.Frame(window)
    frame_rep.pack(side='left')
    frame_panel = tk.Frame(window, bg=bgr)
    frame_panel.pack(expand=1)
    lbl = tk.Label(frame_panel, text='Введите исполнителя:', bg= bgr, font=("Times", 20))
    lbl.pack(padx=10, pady=10)
    entry = Combobox(frame_panel, values = list(TABLE_TWO['Любимый исполнитель'].unique())[:-1],
                     state='readonly', font=("Times", 20))
    entry['values']=(list(TABLE_TWO['Любимый исполнитель'].unique())[:-1])
    entry.current(0)
    entry.pack(padx=10, pady=10)
    button_create = ttk.Button(frame_panel, text="Сгенерировать", style="Custom.TButton",
                               command= generate_second)
    button_create.pack(padx=10, pady=10)
    button_save = ttk.Button(frame_panel, text="Сохранить", style="Custom.TButton",
                             command= lambda: save_file(singers_listeners(ITOG, entry.get())))
    button_save.pack(padx=10, pady=10)
    men.entryconfig("Текстовые отчеты", state='disabled')
    # Создание протокла действий при попытке пользователя закрыть окно
    window.protocol("WM_DELETE_WINDOW", on_button)

# Функция текстового отчёта для поиска певца по языку
def text_lang(men, bgr):
    """
    Функция составяления текстового отчёта об исполнителе,
    если он делает музыку в данном жанре и на данном языке
    Args:
        men (tk.Menu): меню, из которого вызвалась функция
        bgr (string): цвет фона

    Автор: Сальник Максим
    """
    def on_button():
        """
        Функция закрытия окна и разблокировки кнопки
        Автор: Сальник Максим
        """
        window.destroy()
        men.entryconfig("Текстовые отчеты", state='normal')
    def generate_second():
        """
        Функция формирования отчёта
        Автор: Сальник Максим
        """
        for widgets in frame_rep.winfo_children():
            widgets.destroy()
        txt = language_singer(TABLE_TWO, entry.get(), entry2.get())
        if txt.empty:
            lbl = tk.Label(frame_rep, text='Совпадений нет', font=("Times", 25))
            lbl.pack(padx=10, pady=10)
        else:
            make_table(txt, frame_rep, colum_names)
    colum_names = ["Исполнитель", "Самый популярный трек"]
    window = tk.Toplevel(root)
    window.minsize(800, 520)
    window.title("Поиск по языку и жанру")
    window.configure(bg=bgr)
    frame_rep = tk.Frame(window)
    frame_rep.pack(side='left')
    frame_panel = tk.Frame(window, bg=bgr)
    frame_panel.pack(expand=1)
    lbl = tk.Label(frame_panel, text='Введите жанр исполнителя:', bg= bgr, font=("Times", 20))
    lbl.pack(padx=10, pady=10)
    entry = Combobox(frame_panel, values = list(TABLE_ONE['Любимый жанр музыки'].unique())[:-1],
                     state='readonly', font=("Times", 20))
    entry['values']= (list(TABLE_ONE['Любимый жанр музыки'].unique())[:-1])
    entry.current(0)
    entry.pack(padx=10, pady=10)
    lbl2 = tk.Label(frame_panel, text='Введите язык исполнителя:', bg= bgr, font=("Times", 20))
    lbl2.pack(padx=10, pady=10)
    entry2 = Combobox(frame_panel,
                      values = list(TABLE_TWO['Язык любимого исполнителя'].unique())[:-1],
                      state='readonly', font=("Times", 20))
    entry2['values']=(list(TABLE_TWO['Язык любимого исполнителя'].unique())[:-1])
    entry2.current(0)
    entry2.pack(padx=10, pady=10)
    button_create = ttk.Button(frame_panel, text="Сгенерировать", style="Custom.TButton",
                               command= generate_second)
    button_create.pack(padx=10, pady=10)
    button_save = ttk.Button(frame_panel, text="Сохранить", style="Custom.TButton",
                             command= lambda: save_file(
                                 language_singer(TABLE_TWO, entry.get(), entry2.get()))
                             )
    button_save.pack(padx=10, pady=10)
    men.entryconfig("Текстовые отчеты", state='disabled')
    # Создание протокла действий при попытке пользователя закрыть окно
    window.protocol("WM_DELETE_WINDOW", on_button)

def text_pivot(men, bgr):
    """
    Функция составяления текстового отчёта в виде сводной таблице возрастов
    слушателей для рассмотрения зависимости от жанра и языка музыки
    Args:
        men (tk.Menu): меню, из которого вызвалась функция
        bgr (string): цвет фона

    Автор: Сальник Максим
    """
    def on_button():
        """
        Функция закрытия окна и разблокировки кнопки
        Автор: Сальник Максим
        """
        window.destroy()
        men.entryconfig("Сводная таблица", state='normal')
    window = tk.Toplevel(root)
    window.minsize(800, 520)
    window.title("Сводная таблица возрастов")
    window.configure(bg=bgr)
    window.columnconfigure(0, weight=1)
    frame_rep = tk.Frame(window)
    frame_rep.grid(row=0, column=0, sticky='nsew')
    frame_panel = tk.Frame(window, bg =bgr)
    frame_panel.grid(row=1, column=0, sticky='nsew')
    button_save = ttk.Button(frame_panel, text="Сохранить", style="Custom.TButton",
                             command= lambda: save_file(piv_table(ITOG)))
    button_save.pack(padx=10, pady=10)
    piv = piv_table(ITOG)
    colum_names = piv.columns
    ind_names = piv.index
    make_table_wholetable(piv, frame_rep, colum_names, ind_names)
    men.entryconfig("Сводная таблица", state='disabled')
    # Создание протокла действий при попытке пользователя закрыть окно
    window.protocol("WM_DELETE_WINDOW", on_button)

def create_genre_histogram(men):
    """
    Функция составления графического отчёта в виде гистограммы, показывающей,
    как много пользователей слушают преимущественно один жанр.
    Args:
        men (tk.Menu): меню, из которого вызвалась функцияа

    Автор: Кучерявая Элина
    """
    men.entryconfig("Графические отчеты", state='disabled')
    # Загрузка данных из таблицы 1 и таблицы 2
    table1 = TABLE_ONE
    table2 = TABLE_TWO
    # Создание словаря для хранения количества соответствующих пользователей
    genre_counts = {}
    # Подсчет количества соответствующих пользователей для каждой категории и столбца
    for index, row in table2.iterrows():
        genre = row['Жанр любимого исполнителя']
        favorite_artist = row['Любимый исполнитель']
        matching_users = table1[
            (table1['Любимый жанр музыки'] == genre) & (table1['Любимый исполнитель'] == favorite_artist)]
        count = len(matching_users)
        if genre in genre_counts:
            genre_counts[genre].append(count)
        else:
            genre_counts[genre] = [count]
    # Создание списков для категорий и соответствующих столбцов
    categories = []
    columns = []
    # Суммирование количества пользователей в каждой категории
    for genre, counts in genre_counts.items():
        categories.append(genre)
        columns.append(sum(counts))
    # Построение гистограммы
    plt.bar(categories, columns)
    plt.xlabel('Категория жанра')
    plt.ylabel('Количество пользователей')
    plt.title('Гистограмма жанров')
    plt.xticks(rotation=90)
    plt.show()
    try:
        men.entryconfig("Графические отчеты", state='normal')
    except:
        pass

def create_popularity_chart(men):
    """
    Функция составления графического отчёта, показывающего количество людей,
    слушающих конкретных исполнителей
    Args:
        men (tk.Menu): меню, из которого вызвалась функцияа

    Автор: Кучерявая Элина
    """
    men.entryconfig("Графические отчеты", state='disabled')
    # Считываем данные из CSV-файла в DataFrame
    data = TABLE_ONE

    # Группируем данные по исполнителю и подсчитываем количество пользователей
    artist_counts = data['Любимый исполнитель'].value_counts()

    # Получаем список исполнителей и соответствующие им количество слушателей
    artists = artist_counts.index
    listeners = artist_counts.values

    # Создаем фигуру и оси для диаграммы
    fig, ax = plt.subplots()

    # Строим столбчатую диаграмму
    ax.bar(artists, listeners)

    # Настраиваем подписи осей и заголовок диаграммы
    ax.set_xlabel('Исполнитель')
    ax.set_ylabel('Количество слушателей')
    ax.set_title('Популярность исполнителей')

    # Поворачиваем подписи на оси X для лучшей читаемости
    plt.xticks(rotation=90)

    # Отображаем диаграмму
    plt.show()

    try:
        men.entryconfig("Графические отчеты", state='normal')
    except:
        pass

def create_boxplot(men):
    """
    Функция составления графического отчёта в виде Бокса-Вискера.
    Args:
        men (tk.Menu): меню, из которого вызвалась функцияа

    Автор: Кучерявая Элина
    """
    men.entryconfig("Графические отчеты", state='disabled')

    table1 = TABLE_ONE
    table2 = TABLE_TWO
    # Объединение таблиц по общему столбцу 'Любимый исполнитель'
    ITOG = pd.merge(table1, table2, on='Любимый исполнитель')
    ITOG['Число слушателей за месяц'] = ITOG['Число слушателей за месяц'].map(lambda x: x.replace(" ", ""))
    data_types_dict = {'Число слушателей за месяц': int}
    ITOG = ITOG.astype(data_types_dict)
    # Объединение таблиц по общему столбцу 'Любимый исполнитель'
    merged_data = ITOG

    # Категоризация данных по столбцу 'Любимый жанр музыки'
    categories = merged_data['Любимый жанр музыки'].unique()
    data_by_category = []
    for category in categories:
        data_by_category.append(merged_data.loc[merged_data['Любимый жанр музыки'] == category, 'Число слушателей за месяц'])

    # Построение категоризированной диаграммы Бокса-Вискера
    plt.boxplot(data_by_category, labels=categories)
    plt.xlabel('Любимый жанр музыки')
    plt.ylabel('Число слушателей за месяц')
    plt.title('Категоризированная диаграмма Бокса-Вискера')
    plt.xticks(rotation=90)
    # Отображение диаграммы
    plt.show()
    try:
        men.entryconfig("Графические отчеты", state='normal')
    except:
        pass

def create_scatterplot(men):
    """
    Функция составления графического отчёта в виде Диаграммы рассеивания.
    Args:
        men (tk.Menu): меню, из которого вызвалась функцияа

    Автор: Кучерявая Элина
    """
    men.entryconfig("Графические отчеты", state='disabled')
    # Загрузка данных из таблицы 1 и таблицы 2
    table1 = TABLE_ONE
    table2 = TABLE_TWO

    # Атрибуты для диаграммы рассеивания
    x_attribute = 'Возраст'  # Количественный атрибут 1
    y_attribute = 'Число слушателей за месяц'  # Количественный атрибут 2
    category_attribute = 'Любимый жанр музыки'  # Качественный атрибут

    # Объединение таблиц по общему столбцу 'Любимый исполнитель'
    merged_data = pd.merge(table1, table2, on='Любимый исполнитель')

    # Сортировка данных по возрастанию значения столбца 'Число слушателей за месяц'
    merged_data_sorted = merged_data.sort_values(by=y_attribute)

    # Получение уникальных значений категорий
    categories = merged_data_sorted[category_attribute].unique()

    # Создание цветовой палитры для категорий
    color_palette = plt.cm.get_cmap('tab10', len(categories))

    # Построение категоризированной диаграммы рассеивания
    for i, category in enumerate(categories):
        category_data = merged_data_sorted[merged_data_sorted[category_attribute] == category]
        x = category_data[x_attribute]
        y = category_data[y_attribute]
        plt.scatter(x, y, color=color_palette(i), label=category)

    # Настройка подписей осей и легенды
    plt.xlabel(x_attribute)
    plt.ylabel(y_attribute)
    plt.title('Категоризированная диаграмма рассеивания')
    plt.legend()

    # Отображение диаграммы рассеивания
    plt.show()
    try:
        men.entryconfig("Графические отчеты", state='normal')
    except:
        pass

def create_clastar(men):
    """
    Функция составления графического отчёта в виде Кластерной гистограммы.
    Args:
        men (tk.Menu): меню, из которого вызвалась функцияа

    Автор: Кучерявая Элина
    """
    men.entryconfig("Графические отчеты", state='disabled')
     # Объединение таблиц по общему столбцу 'Любимый исполнитель'
    merged_data = pd.merge(TABLE_ONE, TABLE_TWO, on='Любимый исполнитель')

    # Группировка данных по категориям 'Жанр любимого исполнителя' и 'Язык любимого исполнителя'
    grouped_data = merged_data.groupby(['Жанр любимого исполнителя', 'Язык любимого исполнителя']).size().unstack().fillna(0)

    # Построение кластеризованной столбчатой диаграммы
    grouped_data.plot(kind='bar', stacked=True)

    # Настройка подписей осей и заголовка
    plt.xlabel('Жанр любимого исполнителя')
    plt.ylabel('Количество исполнителей')
    plt.title('Кластеризованная столбчатая диаграмма')

    # Отображение диаграммы
    plt.show()
    try:
        men.entryconfig("Графические отчеты", state='normal')
    except:
        pass

# Создание главного окна
root = tk.Tk()
root.title("Мое приложение")
root.configure(bg=BACKGR)  # Задний фон окна

root.minsize(800, 520)

def closing():
    """
    Функция закрытия графических отчётов вместе с закрытием главного окна
    Автор: Кучерявая Элина
    """
    plt.close()
    root.destroy()
# Создание кнопки "Закрыть"
close_button = ttk.Button(root, text="Закрыть", style="Custom.TButton", command=closing)
close_button.place(relx=0.5, rely=0.7, anchor="center")

# Создание стиля для метки
style = ttk.Style()
style.configure("Custom.TLabel", background=BACKGR, foreground="black")

# Создание метки с текстом "Выберите справочник"
label = ttk.Label(root, text="Выберите справочник", font=("Times", 30), style="Custom.TLabel")
label.pack(pady=50)

# Создание кнопок
button1 = ttk.Button(root, text="Справочник с пользователями", style="Custom.TButton",
                     command=lambda: show_table_one(BACKGR))
button2 = ttk.Button(root, text="Общий справочник", style="Custom.TButton",
                     command=lambda: show_itog(BACKGR))
button3 = ttk.Button(root, text="Справочник с исполнителями", style="Custom.TButton",
                     command=lambda: show_table_two(BACKGR))

# Расстановка кнопок
button2.place(relx=0.5, rely=0.3, anchor="center")
button1.place(relx=0.3, rely=0.5, anchor="center")
button3.place(relx=0.7, rely=0.5, anchor="center")

# Создание стиля для кнопок
style.configure("Custom.TButton", background=BACKGR, padding=(10, 20), font=("Times", 14))

root.protocol("WM_DELETE_WINDOW", closing)

root.mainloop()
