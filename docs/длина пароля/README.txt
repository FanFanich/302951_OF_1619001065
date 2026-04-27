Вот пошаговая инструкция и готовый код для создания приложения «Random Password Generator» на Python с использованием библиотеки Tkinter.

1. Структура проекта
Создайте папку для проекта (например, PasswordGenerator) и добавьте в неё следующие файлы:

main.py — основной файл с кодом приложения.
history.json — файл для хранения истории (создастся автоматически при первом запуске).
README.md — файл с описанием проекта.
2. Код приложения (main.py)
Скопируйте этот код в файл main.py. Он реализует все требования: интерфейс, генерацию, сохранение истории и проверку ввода.

import tkinter as tk
from tkinter import messagebox, ttk
import random
import string
import json
import os

# --- Настройки ---
HISTORY_FILE = "history.json"
MIN_LENGTH = 4
MAX_LENGTH = 32

# --- Логика генерации пароля ---
def generate_password(length, use_digits, use_letters, use_special):
    """Генерирует пароль на основе выбранных параметров."""
    if length < 1:
        raise ValueError("Длина пароля должна быть больше 0.")

    chars = ''
    if use_digits:
        chars += string.digits
    if use_letters:
        chars += string.ascii_letters
    if use_special:
        chars += string.punctuation

    if not chars:
        raise ValueError("Необходимо выбрать хотя бы один тип символов.")
    
    return ''.join(random.choices(chars, k=length))

# --- Работа с историей (JSON) ---
def load_history():
    """Загружает историю из файла."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_history(history):
    """Сохраняет историю в файл."""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# --- Основная логика приложения ---
def on_generate():
    """Обработчик нажатия кнопки 'Сгенерировать'."""
    try:
        length = int(scale_length.get())
        
        # Проверка длины (валидация)
        if length < MIN_LENGTH or length > MAX_LENGTH:
            messagebox.showwarning(
                "Недопустимая длина",
                f"Длина пароля должна быть от {MIN_LENGTH} до {MAX_LENGTH} символов."
            )
            return

        # Получение флагов выбора символов
        use_digits = var_digits.get()
        use_letters = var_letters.get()
        use_special = var_special.get()
        
        # Генерация пароля
        password = generate_password(length, use_digits, use_letters, use_special)
        
        # Вывод в интерфейс
        entry_password.delete(0, tk.END)
        entry_password.insert(0, password)

        # Сохранение в историю и обновление таблицы
        history = load_history()
        history.append(password)
        save_history(history)
        update_history_table()

    except ValueError as e:
        messagebox.showerror("Ошибка ввода", str(e))
    except Exception as e:
        messagebox.showerror("Критическая ошибка", "Произошла непредвиденная ошибка.")

def update_history_table():
    """Обновляет виджет таблицы с историей."""
    for item in tree.get_children():
        tree.delete(item)
    for pwd in load_history():
        tree.insert('', 'end', values=(pwd,))

# --- Создание графического интерфейса ---
root = tk.Tk()
root.title("Генератор случайных паролей")
root.geometry("500x450")
root.resizable(False, False)
root.configure(bg='#f0f0f0')

# Фрейм настроек (Длина и флажки)
frame_settings = tk.Frame(root, bg='#f0f0f0', padx=10, pady=10)
frame_settings.pack(pady=10)

tk.Label(frame_settings, text="Длина пароля:", bg='#f0f0f0').grid(row=0, column=0)
scale_length = tk.Scale(frame_settings, from_=MIN_LENGTH, to=MAX_LENGTH, orient=tk.HORIZONTAL, length=250)
scale_length.set(12)  # Значение по умолчанию
scale_length.grid(row=0, column=1, columnspan=2)

var_digits = tk.BooleanVar(value=True)
var_letters = tk.BooleanVar(value=True)
var_special = tk.BooleanVar(value=True)

tk.Checkbutton(frame_settings, text="Цифры", variable=var_digits, bg='#f0f0f0').grid(row=1, column=0)
tk.Checkbutton(frame_settings, text="Буквы", variable=var_letters, bg='#f0f0f0').grid(row=1, column=1)
tk.Checkbutton(frame_settings, text="Спецсимволы", variable=var_special, bg='#f0f0f0').grid(row=1, column=2)

btn_generate = tk.Button(root, text="Сгенерировать", command=on_generate, bg='#4CAF50', fg='white')
btn_generate.pack(pady=5)

# Фрейм вывода пароля и кнопки копирования
frame_output = tk.Frame(root, bg='#f0f0f0')
frame_output.pack(pady=10)

tk.Label(frame_output, text="Ваш пароль:", bg='#f0f0f0').pack(side=tk.LEFT)
entry_password = tk.Entry(frame_output, width=40, font=('Arial', 12))
entry_password.pack(side=tk.LEFT, padx=5)
btn_copy = tk.Button(frame_output, text="Копировать", 
                     command=lambda: root.clipboard_clear() or root.clipboard_append(entry_password.get()))
btn_copy.pack(side=tk.LEFT)

# Таблица истории (Treeview)
frame_history = tk.Frame(root)
frame_history.pack(fill='both', expand=True, padx=20, pady=10)

tree = ttk.Treeview(frame_history, columns=('password',), show='headings')
tree.heading('password', text='История паролей')
tree.column('password', width=450)
tree.pack(fill='both', expand=True)

scrollbar = ttk.Scrollbar(frame_history, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Загрузка истории при запуске приложения
update_history_table()
root.mainloop()
3. Работа с Git и публикация
Чтобы выложить проект на GitHub или GitLab:

Инициализация репозитория:
Откройте терминал в папке PasswordGenerator и выполните команды:
git init             # Создаем локальный репозиторий
git add .            # Добавляем все файлы в отслеживание
git commit -m "Initial commit: Random Password Generator"
Создание репозитория на хостинге:
Зайдите на GitHub или GitLab и создайте новый пустой репозиторий (например, PasswordGenerator). Не создавайте файлы README или .gitignore там, они у вас уже есть локально.
Связь с удаленным репозиторием и загрузка:
В терминале выполните (замените ссылку на свою):
git remote add origin https://github.com/ВАШ_ЛОГИН/PasswordGenerator.git 
git branch -M main   # Переименовываем ветку в main (если требуется хостингом)
git push -u origin main # Отправляем код на сервер
README.md:
Создайте файл README.md в папке проекта. Вот готовый шаблон для заполнения:
# Random Password Generator

**Автор:** [Ваше Имя Фамилия]
**Версия:** 1.0

## Описание

Кроссплатформенное приложение с графическим интерфейсом для генерации надежных случайных паролей. Позволяет настраивать сложность (длина и типы символов) и сохраняет историю сгенерированных паролей.
*   **Язык:** Python 3.x+
*   **Библиотеки:** Tkinter (стандартная), Random (стандартная), JSON.
*   **Контроль версий:** Git.
