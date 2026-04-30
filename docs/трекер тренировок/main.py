import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# Константы
DATA_FILE = "workouts.json"

class TrainingPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.root.geometry("800x600")

        # Список тренировок
        self.workouts = []

        # --- Фрейм ввода данных ---
        input_frame = ttk.LabelFrame(root, text="Добавить тренировку", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        # Дата
        ttk.Label(input_frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.date_entry = ttk.Entry(input_frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%d.%m.%Y"))

        # Тип тренировки
        ttk.Label(input_frame, text="Тип тренировки:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.type_combobox = ttk.Combobox(input_frame, values=["Бег", "Плавание", "Силовая", "Йога", "Велосипед"])
        self.type_combobox.grid(row=0, column=3, padx=5, pady=5)
        self.type_combobox.set("Бег")

        # Длительность (минуты)
        ttk.Label(input_frame, text="Длительность (мин):").grid(row=0, column=4, sticky="w", padx=5, pady=5)
        self.duration_entry = ttk.Entry(input_frame)
        self.duration_entry.grid(row=0, column=5, padx=5, pady=5)

        # Кнопка добавления
        add_btn = ttk.Button(input_frame, text="Добавить тренировку", command=self.add_workout)
        add_btn.grid(row=0, column=6, padx=10, pady=5)

        # --- Фрейм фильтрации ---
        filter_frame = ttk.LabelFrame(root, text="Фильтрация", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(filter_frame, text="Фильтр по типу:").grid(row=0, column=0, sticky="w", padx=5)
        self.filter_type_var = tk.StringVar()
        self.filter_type_combo = ttk.Combobox(filter_frame, textvariable=self.filter_type_var, values=["Все", "Бег", "Плавание", "Силовая", "Йога", "Велосипед"])
        self.filter_type_combo.set("Все")
        self.filter_type_combo.grid(row=0, column=1, padx=5)
        self.filter_type_combo.bind("<<ComboboxSelected>>", self.apply_filters)

        ttk.Label(filter_frame, text="Фильтр по дате (ДД.ММ.ГГГГ):").grid(row=0, column=2, sticky="w", padx=5)
        self.filter_date_entry = ttk.Entry(filter_frame)
        self.filter_date_entry.grid(row=0, column=3, padx=5)
        
        filter_btn = ttk.Button(filter_frame, text="Применить фильтр даты", command=self.apply_filters)
        filter_btn.grid(row=0, column=4, padx=5)
        
        clear_filter_btn = ttk.Button(filter_frame, text="Сбросить фильтры", command=self.clear_filters)
        clear_filter_btn.grid(row=0, column=5, padx=5)

        # --- Таблица данных ---
        table_frame = ttk.Frame(root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("date", "type", "duration")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип тренировки")
        self.tree.heading("duration", text="Длительность (мин)")

        self.tree.column("date", width=150)
        self.tree.column("type", width=200)
        self.tree.column("duration", width=150)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        # --- Загрузка данных при старте ---
        self.load_data()
        self.refresh_table()

    def validate_input(self, date_str, duration_str):
        """Проверка корректности ввода"""
        # Проверка даты
        try:
            datetime.strptime(date_str, "%d.%m.%Y")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ДД.ММ.ГГГГ.")
            return False

        # Проверка длительности
        try:
            duration = int(duration_str)
            if duration <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным целым числом.")
            return False

        return True

    def add_workout(self):
        date_str = self.date_entry.get().strip()
        workout_type = self.type_combobox.get()
        duration_str = self.duration_entry.get().strip()

        if not self.validate_input(date_str, duration_str):
            return

        new_workout = {
            "date": date_str,
            "type": workout_type,
            "duration": int(duration_str)
        }

        self.workouts.append(new_workout)
        self.save_data()
        self.refresh_table()
        
        # Очистка поля длительности для удобства
        self.duration_entry.delete(0, tk.END)
        messagebox.showinfo("Успех", "Тренировка добавлена!")

    def save_data(self):
        """Сохранение данных в JSON"""
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.workouts, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить данные: {e}")

    def load_data(self):
        """Загрузка данных из JSON"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.workouts = json.load(f)
            except Exception as e:
                messagebox.showerror("Ошибка загрузки", f"Не удалось загрузить данные: {e}")
                self.workouts = []

    def get_filtered_workouts(self):
        """Получение списка тренировок с учетом фильтров"""
        filtered = self.workouts[:]
        
        # Фильтр по типу
        type_filter = self.filter_type_var.get()
        if type_filter and type_filter != "Все":
            filtered = [w for w in filtered if w["type"] == type_filter]

        # Фильтр по дате
        date_filter = self.filter_date_entry.get().strip()
        if date_filter:
            try:
                # Проверяем формат даты в фильтре
                datetime.strptime(date_filter, "%d.%m.%Y")
                filtered = [w for w in filtered if w["date"] == date_filter]
            except ValueError:
                messagebox.showwarning("Предупреждение", "Неверный формат даты в фильтре. Фильтр проигнорирован.")

        return filtered

    def apply_filters(self, event=None):
        """Обновление таблицы с применением фильтров"""
        self.refresh_table()

    def clear_filters(self):
        """Сброс фильтров"""
        self.filter_type_var.set("Все")
        self.filter_date_entry.delete(0, tk.END)
        self.refresh_table()

    def refresh_table(self):
        """Очистка и заполнение таблицы"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        filtered_workouts = self.get_filtered_workouts()

        for workout in filtered_workouts:
            self.tree.insert("", tk.END, values=(
                workout["date"],
                workout["type"],
                workout["duration"]
            ))

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlannerApp(root)
    root.mainloop()
