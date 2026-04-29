import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os

DATA_FILE = "history.json"
MIN_LENGTH = 4
MAX_LENGTH = 32

# --- Работа с данными (JSON) ---
def load_history():
    """Загружает историю паролей из файла."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    """Сохраняет историю в файл."""
    with open(DATA_FILE, "w") as f:
        json.dump(history, f, indent=2)

# --- Генерация пароля ---
def generate_password():
    """Генерирует пароль на основе выбранных настроек."""
    length = int(scale_length.get())
    use_digits = var_digits.get()
    use_letters = var_letters.get()
    use_symbols = var_symbols.get()

    # Проверка: выбран хотя бы один тип символов
    if not (use_digits or use_letters or use_symbols):
        messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов!")
        return

    # Сбор набора символов
    chars = ""
    if use_letters:
        chars += string.ascii_letters  # a-zA-Z
    if use_digits:
        chars += string.digits         # 0-9
    if use_symbols:
        chars += string.punctuation    # Спецсимволы

    # Генерация пароля
    password = ''.join(random.choices(chars, k=length))
    
    # Отображение и сохранение в историю
    entry_password.delete(0, tk.END)
    entry_password.insert(0, password)
    
    history = load_history()
    history.append(password)
    save_history(history)
    
    update_history_list()

# --- Валидация длины ---
def validate_length(val):
    """Валидация значения ползунка."""
    try:
        v = int(val)
        if v < MIN_LENGTH:
            scale_length.set(MIN_LENGTH)
            return False
        if v > MAX_LENGTH:
            scale_length.set(MAX_LENGTH)
            return False
        return True
    except ValueError:
        return False

# --- Обновление истории ---
def update_history_list():
    """Обновляет виджет списка истории."""
    history_list.delete(0, tk.END)
    for pwd in load_history():
        history_list.insert(tk.END, pwd)

# --- Создание GUI ---
root = tk.Tk()
root.title("Random Password Generator")
root.geometry("500x500")
root.resizable(False, False)

# --- Настройки генерации ---
frame_settings = tk.LabelFrame(root, text="Настройки", padx=10, pady=10)
frame_settings.pack(pady=10, padx=10, fill="x")

tk.Label(frame_settings, text="Длина пароля:").grid(row=0, column=0, sticky="e")
scale_length = tk.Scale(frame_settings, from_=MIN_LENGTH, to=MAX_LENGTH, orient=tk.HORIZONTAL,
                        command=validate_length)
scale_length.set(12)
scale_length.grid(row=0, column=1, pady=5)
tk.Label(frame_settings, text=f"(от {MIN_LENGTH} до {MAX_LENGTH})").grid(row=0, column=2)

var_digits = tk.BooleanVar(value=True)
var_letters = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=True)

tk.Checkbutton(frame_settings, text="Цифры (0-9)", variable=var_digits).grid(row=1, column=0, columnspan=2, sticky="w")
tk.Checkbutton(frame_settings, text="Буквы (a-zA-Z)", variable=var_letters).grid(row=2, column=0, columnspan=2, sticky="w")
tk.Checkbutton(frame_settings, text="Спецсимволы (!@#)", variable=var_symbols).grid(row=3, column=0, columnspan=2, sticky="w")

btn_generate = tk.Button(root, text="Сгенерировать пароль", command=generate_password)
btn_generate.pack(pady=15)

# --- Результат ---
frame_result = tk.LabelFrame(root, text="Ваш пароль", padx=10, pady=10)
frame_result.pack(pady=5, padx=10, fill="x")
entry_password = tk.Entry(frame_result, width=40)
entry_password.pack(pady=5)

# --- История ---
frame_history = tk.LabelFrame(root, text="История сгенерированных паролей", padx=10, pady=10)
frame_history.pack(pady=10, padx=10, fill="both", expand=True)
history_list = tk.Listbox(frame_history)
history_list.pack(fill="both", expand=True)

# Загрузка истории при старте
update_history_list()
root.mainloop()
