from tkinter import filedialog
import pandas as pd

def save_file(name):
    """
    Функция сохранения файла отчёта или справоника на компьютер

    Args:
        name (pd.DataFrame): справочник или отчёт, который нужно сохранить

    Автор: Муратов Айнур
    """
    filetypes = [
        ("CSV файл", "*.csv"),
        ("Текстовый файл", "*.txt"),
        ("Эксель файл", "*.xlsx"),
        ("Все файлы", "*.*")]
    file_path = filedialog.asksaveasfilename(filetypes=filetypes)
    if file_path:
        name.to_csv(file_path, encoding = 'cp1251')
    elif file_path.endswith(".xlsx"):
        name.to_excel(file_path, delimiter = ';', encoding = 'cp1251') 