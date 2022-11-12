import tkinter as tk
from tkinter import messagebox
from MainWindow import MainWindow


def clear_window(window: tk.Tk):
    """
    Очищаем все виджеты установленные при помощи 'place'
    """
    array = window.place_slaves()
    for index in array:
        index.destroy()


def on_closing():
    """
    обрабатываем закрытие программы
    запрашиваем подтверждение о закрытии
    """
    if messagebox.askokcancel('Выход из приложения', 'Хотите выйти?'):
        win.destroy()


def create_window():
    """
    Создаем главное окно
    :return: window
    """

    window = tk.Tk()
    window.title("Science Software")
    w = window.winfo_screenwidth()
    h = window.winfo_screenheight()
    window.geometry("{}x{}".format(w-10, h-1))
    # icon = tk.PhotoImage(file='icon.png')
    # window.iconphoto(False, icon)
    return window


if __name__ == '__main__':

    win = create_window()

    """
    При закрытии всплывает окно, уточняющее намерение пользователя
    """
    win.protocol('WM_DELETE_WINDOW', on_closing)

    main_window = MainWindow(win)
    main_window.draw_window()

    win.mainloop()
