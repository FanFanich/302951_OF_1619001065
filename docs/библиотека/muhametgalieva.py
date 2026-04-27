import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


# --- Основной класс приложения ---
class MovieLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Movie Library")
        self.movies = []
        self.load_movies()
        self.create_widgets()
        self.update_table()

    # --- Создание графических элементов ---
    def create_widgets(self):
        # --- Блок 1: Поля ввода ---
        frame_input = tk.LabelFrame(self.root, text="Добавить новый фильм", padx=10, pady=10)
        frame_input.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        tk.Label(frame_input, text="Название:").grid(row=0, column=0, sticky="e")
        self.title_entry = tk.Entry(frame_input, width=35)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Жанр:").grid(row=1, column=0, sticky="e")
        self.genre_entry = tk.Entry(frame_input, width=35)
        self.genre_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Год выпуска:").grid(row=2, column=0, sticky="e")
        self.year_entry = tk.Entry(frame_input, width=35)
        self.year_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Рейтинг (0-10):").grid(row=3, column=0, sticky="e")
        self.rating_entry = tk.Entry(frame_input, width=35)
        self.rating_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления фильма
        self.add_button = tk.Button(frame_input, text="➕ Добавить фильм", command=self.add_movie)
        self.add_button.grid(row=4, columnspan=2, pady=10)

        # --- Блок 2: Фильтрация ---
        frame_filter = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=10)
        frame_filter.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        tk.Label(frame_filter, text="По жанру:").grid(row=0, column=0, sticky="e")
        self.filter_genre_entry = tk.Entry(frame_filter)
        self.filter_genre_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_filter, text="По году:").grid(row=1, column=0, sticky="e")
        self.filter_year_entry = tk.Entry(frame_filter)
        self.filter_year_entry.grid(row=1, column=1, padx=5, pady=5)

        self.filter_button = tk.Button(frame_filter, text="🔎 Применить фильтр", command=self.apply_filter)
        self.filter_button.grid(row=2, columnspan=2, pady=(5, 15))

        # --- Блок 3: Таблица фильмов ---
        columns = ("title", "genre", "year", "rating")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text={"title": "Название", "genre": "Жанр", "year": "Год", "rating": "Рейтинг"}[col])
            self.tree.column(col, width=120)

        self.tree.grid(row=2, columnspan=2, padx=10, pady=(0, 10), sticky="nsew")

    # --- Логика добавления фильма ---
    def add_movie(self):
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year_raw = self.year_entry.get().strip()
        rating_raw = self.rating_entry.get().strip()

        # Валидация полей
        if not all([title, genre, year_raw, rating_raw]):
            messagebox.showerror("Ошибка ввода", "Все поля должны быть заполнены!")
            return

        if not year_raw.isdigit():
            messagebox.showerror("Ошибка ввода", "Год должен быть целым числом!")
            return

        year = int(year_raw)

        try:
            rating = float(rating_raw)
            if not (0 <= rating <= 10):
                raise ValueError("Рейтинг вне диапазона")
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Рейтинг должен быть числом от 0 до 10!")
            return

        # Добавление в список и сохранение
        self.movies.append({"title": title, "genre": genre.lower(), "year": year, "rating": rating})

        self.save_movies()

        # Очистка полей и обновление таблицы
        self.clear_entries()
        self.update_table()

    def clear_entries(self):
        self.title_entry.delete(0, 'end')
        self.genre_entry.delete(0, 'end')
        self.year_entry.delete(0, 'end')
        self.rating_entry.delete(0, 'end')

    # --- Логика фильтрации ---
    def apply_filter(self):
        genre_filter = self.filter_genre_entry.get().strip().lower()
        year_filter_raw = self.filter_year_entry.get().strip()

        filtered_movies = self.movies.copy()

        if genre_filter:
            filtered_movies = [m for m in filtered_movies if genre_filter in m["genre"]]

        if year_filter_raw.isdigit():
            year_filter = int(year_filter_raw)
            filtered_movies = [m for m in filtered_movies if m["year"] == year_filter]

        self.display_movies(filtered_movies)

    # --- Работа с JSON ---
    def save_movies(self):
        with open("movies.json", "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def load_movies(self):
        if os.path.exists("movies.json"):
            with open("movies.json", "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.movies = data
                except json.JSONDecodeError:
                    pass  # Если файл пуст или поврежден

    # --- Отображение данных в таблице ---
    def update_table(self):
        self.display_movies(self.movies)

    def display_movies(self, movie_list):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for movie in movie_list:
            self.tree.insert("", "end", values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))


# --- Запуск приложения ---
if __name__ == "__main__":
    root = tk.Tk()

    # Настройка сетки для растягивания таблицы
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    app = MovieLibraryApp(root)
    root.mainloop()