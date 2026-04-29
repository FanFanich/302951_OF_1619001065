import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "movies.json"

# --- Работа с данными (JSON) ---
def load_movies():
    """Загружает фильмы из файла JSON. Возвращает пустой список, если файла нет."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_movies(movies):
    """Сохраняет список фильмов в файл JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(movies, f, indent=2)

# --- Валидация ввода ---
def validate_input():
    """Проверяет корректность введенных данных."""
    title = entry_title.get().strip()
    genre = entry_genre.get().strip()
    year = entry_year.get().strip()
    rating = entry_rating.get().strip()

    if not title or not genre or not year or not rating:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
        return False

    if not year.isdigit() or len(year) != 4:
        messagebox.showerror("Ошибка", "Год должен быть числом из 4 цифр (например, 2020)!")
        return False

    if not rating.replace('.', '', 1).isdigit():
        messagebox.showerror("Ошибка", "Рейтинг должен быть числом!")
        return False

    rating_num = float(rating)
    if not (0 <= rating_num <= 10):
        messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10!")
        return False

    return True

# --- Логика приложения ---
movies = load_movies()

def add_movie():
    """Добавляет фильм в список и обновляет таблицу."""
    if validate_input():
        movie = {
            "title": entry_title.get(),
            "genre": entry_genre.get(),
            "year": int(entry_year.get()),
            "rating": float(entry_rating.get())
        }
        movies.append(movie)
        save_movies(movies)
        update_treeview()
        clear_entries()

def clear_entries():
    """Очищает поля ввода."""
    entry_title.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
    entry_year.delete(0, tk.END)
    entry_rating.delete(0, tk.END)

def update_treeview(filtered_list=None):
    """Обновляет данные в таблице (Treeview)."""
    for i in tree.get_children():
        tree.delete(i)
    
    data_source = filtered_list if filtered_list is not None else movies

    for movie in data_source:
        tree.insert("", tk.END, values=(
            movie["title"],
            movie["genre"],
            movie["year"],
            f"{movie['rating']:.1f}"
        ))

def filter_by_genre():
    """Фильтрует фильмы по жанру."""
    genre = entry_genre_filter.get().strip().lower()
    filtered = [m for m in movies if genre in m["genre"].lower()]
    update_treeview(filtered)

def filter_by_year():
    """Фильтрует фильмы по году выпуска."""
    year = entry_year_filter.get().strip()
    
    if not year.isdigit() or len(year) != 4:
        messagebox.showerror("Ошибка", "Введите год из 4 цифр для фильтрации!")
        update_treeview() # Сбросить фильтр и показать все
        return

    filtered = [m for m in movies if str(m["year"]) == year]
    update_treeview(filtered)

# --- Создание GUI ---
root = tk.Tk()
root.title("Movie Library")
root.geometry("900x600")
root.resizable(False, False)

# --- Форма добавления ---
frame_add = tk.LabelFrame(root, text="Добавить новый фильм", padx=10, pady=10)
frame_add.pack(pady=10, padx=10, fill="x")

tk.Label(frame_add, text="Название:").grid(row=0, column=0, sticky="e", pady=2)
entry_title = tk.Entry(frame_add, width=40)
entry_title.grid(row=0, column=1, pady=2)

tk.Label(frame_add, text="Жанр:").grid(row=1, column=0, sticky="e", pady=2)
entry_genre = tk.Entry(frame_add, width=40)
entry_genre.grid(row=1, column=1, pady=2)

tk.Label(frame_add, text="Год:").grid(row=2, column=0, sticky="e", pady=2)
entry_year = tk.Entry(frame_add, width=15)
entry_year.grid(row=2, column=1, sticky="w", pady=2)

tk.Label(frame_add, text="Рейтинг (0-10):").grid(row=3, column=0, sticky="e", pady=2)
entry_rating = tk.Entry(frame_add, width=15)
entry_rating.grid(row=3, column=1, sticky="w", pady=2)

btn_add = tk.Button(frame_add, text="Добавить фильм", command=add_movie)
btn_add.grid(row=4, column=0, columnspan=2, pady=15)

# --- Фильтрация ---
frame_filter = tk.LabelFrame(root, text="Фильтрация", padx=10, pady=5)
frame_filter.pack(pady=5, padx=10, fill="x")

tk.Label(frame_filter, text="Жанр:").grid(row=0, column=0, sticky="e")
entry_genre_filter = tk.Entry(frame_filter, width=30)
entry_genre_filter.grid(row=0, column=1, pady=2)
btn_filter_genre = tk.Button(frame_filter, text="Фильтровать по жанру", command=filter_by_genre)
btn_filter_genre.grid(row=0, column=2, padx=5)

tk.Label(frame_filter, text="Год:").grid(row=1, column=0, sticky="e")
entry_year_filter = tk.Entry(frame_filter, width=15)
entry_year_filter.grid(row=1, column=1, sticky="w", pady=2)
btn_filter_year = tk.Button(frame_filter, text="Фильтровать по году", command=filter_by_year)
btn_filter_year.grid(row=1, column=2, padx=5)

# --- Таблица фильмов ---
frame_table = tk.Frame(root)
frame_table.pack(pady=10, padx=10, fill="both", expand=True)

columns = ("Название", "Жанр", "Год", "Рейтинг")
tree = ttk.Treeview(frame_table, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
tree.column("Рейтинг", width=80) # Фиксируем ширину колонки рейтинга

tree.pack(side="left", fill="both", expand=True)

# Скроллбар
scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Первоначальная загрузка данных в таблицу
update_treeview()

root.mainloop()
