import tkinter as tk
from tkinter import messagebox, Frame, Grid
from MainWindow import MainWindow
from project import pinning_of_fermi_level as fp


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
    # window.geometry("{}x{}".format(1366, 768))
    # window.geometry("{}x{}".format(1920, 1080))
    window.geometry("{}x{}".format(w - 10, h - 1))

    # icon = tk.PhotoImage(file='icon.png')
    # window.iconphoto(False, icon)
    return window


if __name__ == '__main__':

    win = create_window()

    Grid.rowconfigure(win, 0, weight=1)
    Grid.columnconfigure(win, 0, weight=1)
    frame=Frame(win)
    frame.grid(row=0, column=0, sticky="news")
        
    """
    При закрытии всплывает окно, уточняющее намерение пользователя
    """
    win.protocol('WM_DELETE_WINDOW', on_closing)

    main_window = MainWindow(frame)
    main_window.draw_window()

    Grid.rowconfigure(frame, tuple(range(21)), weight=1)
    Grid.columnconfigure(frame, tuple(range(1, 5)), weight=1)
    Grid.columnconfigure(frame, 0, weight=15)


    win.mainloop()

    # fp.run()
