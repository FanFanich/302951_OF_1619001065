import tkinter as tk
from tkinter import messagebox, Listbox, END
import random
import json
import os

QUOTES_FILE = "quotes.json"
HISTORY_FILE = "history.json"

# Загрузка предопределённых цитат
def load_quotes():
    if os.path.exists(QUOTES_FILE):
        with open(QUOTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Загрузка истории
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Сохранение истории
def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

# Генерация случайной цитаты
def generate_quote():
    quotes = load_quotes()
    if not quotes:
        messagebox.showwarning("Предупреждение", "База цитат пуста!")
        return

    quote = random.choice(quotes)
    text_label.config(text=f'"{quote["text"]}"')
    author_label.config(text=f"— {quote['author']}")

    # Добавляем в историю (без дубликатов)
    history = load_history()
    if quote not in history:
        history.append(quote)
        save_history(history)

    update_history_list()

# Обновление списка истории
def update_history_list(filtered=None):
    history_list.delete(0, END)
    history = filtered if filtered is not None else load_history()
    for q in history:
        history_list.insert(END, f'"{q["text"]}" — {q["author"]}')

# Фильтрация по автору
def filter_by_author():
    author = entry_author_filter.get().strip().lower()
    history = load_history()
    filtered = [q for q in history if author in q["author"].lower()]
    update_history_list(filtered)

# Фильтрация по теме
def filter_by_topic():
    topic = entry_topic_filter.get().strip().lower()
    history = load_history()
    filtered = [q for q in history if topic in q["topic"].lower()]
    update_history_list(filtered)

# Создание окна
root = tk.Tk()
root.title("Random Quote Generator")
root.geometry("600x500")

# Текущая цитата
text_label = tk.Label(root, text="", wraplength=500, font=("Arial", 12))
text_label.pack(pady=10)
author_label = tk.Label(root, text="", font=("Arial", 10, "italic"))
author_label.pack(pady=5)

btn_generate = tk.Button(root, text="Сгенерировать цитату", command=generate_quote)
btn_generate.pack(pady=10)

# Фильтрация по автору
tk.Label(root, text="Фильтр по автору").pack()
entry_author_filter = tk.Entry(root, width=40)
entry_author_filter.pack(pady=5)
btn_filter_author = tk.Button(root, text="Фильтровать по автору", command=filter_by_author)
btn_filter_author.pack(pady=5)

# Фильтрация по теме
tk.Label(root, text="Фильтр по теме").pack()
entry_topic_filter = tk.Entry(root, width=40)
entry_topic_filter.pack(pady=5)
btn_filter_topic = tk.Button(root, text="Фильтровать по теме", command=filter_by_topic)
btn_filter_topic.pack(pady=5)

# История цитат
tk.Label(root, text="История сгенерированных цитат").pack()
history_list = Listbox(root, width=70, height=15)
history_list.pack(pady=10)

update_history_list()
root.mainloop()
