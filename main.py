import tkinter as tk

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
    и высылаем отчет.
    """
    if messagebox.askokcancel('Выход из приложения', 'Хотите выйти?'):
        win.destroy()
        #adm.send_ReportForOneday(dbase=dbase)
        dbase.close()

def create_window():
    """
    Создаем главное окно
    :return: window
    """

    window = tk.Tk()
    window.title("RNBCoffee")
    w = window.winfo_screenwidth()
    h = window.winfo_screenheight()
    window.geometry("{}x{}".format(w-10, h-1))
    icon = tk.PhotoImage(file='logo.png')
    window.iconphoto(False, icon)
    return window

if __name__ == '__main__':
    pass