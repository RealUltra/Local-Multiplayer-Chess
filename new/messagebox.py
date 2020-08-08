import ctypes

def showinfo(title, message):
    return ctypes.windll.user32.MessageBoxW(0, message, title, 64)

def showerror(title, message):
    return ctypes.windll.user32.MessageBoxW(0, message, title, 16)

def askyesno(title, message):
    return ctypes.windll.user32.MessageBoxW(4, message, title, 32)

def askyesnocancel(title, message):
    return ctypes.windll.user32.MessageBoxW(3, message, title, 32)

def showwarning(title, message):
    return ctypes.windll.user32.MessageBoxW(0, message, title, 48)