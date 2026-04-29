import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class WeatherDiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary - Дневник погоды")
        self.root.geometry("600x500")

        # Файл для хранения данных
        self.data_file = "weather_data.json"
        
        # Список записей
        self.records = []

        # Загрузка данных при старте
        self.load_data()

        # --- Интерфейс ---

        # Фрейм ввода данных
        input_frame = tk.LabelFrame(root, text="Новая запись", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        # Дата
        tk.Label(input_frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, sticky="w", pady=2)
        self.date_entry = tk.Entry(input_frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        # Установка текущей даты по умолчанию
        self.date_entry.insert(0, datetime.now().strftime("%d.%m.%Y"))

        # Температура
        tk.Label(input_frame, text="Температура (°C):").grid(row=1, column=0, sticky="w", pady=2)
        self.temp_entry = tk.Entry(input_frame)
        self.temp_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

        # Описание
        tk.Label(input_frame, text="Описание:").grid(row=2, column=0, sticky="w", pady=2)
        self.desc_entry = tk.Entry(input_frame)
        self.desc_entry.grid(row=2, column=1, padx=5, pady=2, sticky="ew")

        # Осадки
        tk.Label(input_frame, text="Осадки:").grid(row=3, column=0, sticky="w", pady=2)
        self.precipitation_var = tk.BooleanVar(value=False)
        self.precip_check = tk.Checkbutton(input_frame, variable=self.precipitation_var, text="Да")
        self.precip_check.grid(row=3, column=1, sticky="w", padx=5, pady=2)

        # Кнопка добавления
        add_btn = tk.Button(input_frame, text="Добавить запись", command=self.add_record, bg="#4CAF50", fg="white")
        add_btn.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

        input_frame.columnconfigure(1, weight=1)

        # Фрейм фильтрации
        filter_frame = tk.LabelFrame(root, text="Фильтр", padx=10, pady=5)
        filter_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(filter_frame, text="Фильтр по дате (ДД.ММ.ГГГГ):").grid(row=0, column=0, sticky="w")
        self.filter_date_entry = tk.Entry(filter_frame)
        self.filter_date_entry.grid(row=0, column=1, padx=5)
        self.filter_date_entry.bind('<KeyRelease>', self.apply_filters)

        tk.Label(filter_frame, text="Мин. температура (°C):").grid(row=0, column=2, sticky="w", padx=(10, 0))
        self.filter_temp_entry = tk.Entry(filter_frame, width=10)
        self.filter_temp_entry.grid(row=0, column=3, padx=5)
        self.filter_temp_entry.bind('<KeyRelease>', self.apply_filters)

        tk.Button(filter_frame, text="Сброс", command=self.reset_filters).grid(row=0, column=4, padx=5)

        # Таблица записей
        table_frame = tk.Frame(root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("date", "temp", "desc", "precip")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        self.tree.heading("date", text="Дата")
        self.tree.heading("temp", text="Темп.")
        self.tree.heading("desc", text="Описание")
        self.tree.heading("precip", text="Осадки")

        self.tree.column("date", width=100)
        self.tree.column("temp", width=60)
        self.tree.column("desc", width=250)
        self.tree.column("precip", width=80)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        # Кнопка удаления
        del_btn = tk.Button(root, text="Удалить выбранную запись", command=self.delete_record, bg="#f44336", fg="white")
        del_btn.pack(pady=5, padx=10, fill="x")

        # Обновление таблицы при запуске
        self.update_table()

    def load_data(self):
        """Загружает данные из JSON файла."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.records = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.records = []
        else:
            self.records = []

    def save_data(self):
        """Сохраняет данные в JSON файл."""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.records, f, ensure_ascii=False, indent=4)
        except IOError:
            messagebox.showerror("Ошибка", "Не удалось сохранить данные.")

    def validate_input(self):
        """Проверяет корректность введенных данных."""
        date_str = self.date_entry.get().strip()
        temp_str = self.temp_entry.get().strip()
        desc = self.desc_entry.get().strip()

        # Проверка даты
        try:
            datetime.strptime(date_str, "%d.%m.%Y")
        except ValueError:
            messagebox.showwarning("Ошибка ввода", "Неверный формат даты. Используйте ДД.ММ.ГГГГ.")
            return None

        # Проверка температуры
        try:
            temp = float(temp_str)
        except ValueError:
            messagebox.showwarning("Ошибка ввода", "Температура должна быть числом.")
            return None

        # Проверка описания
        if not desc:
            messagebox.showwarning("Ошибка ввода", "Описание погоды не может быть пустым.")
            return None

        return {
            "date": date_str,
            "temperature": temp,
            "description": desc,
            "precipitation": "Да" if self.precipitation_var.get() else "Нет"
        }

    def add_record(self):
        """Добавляет новую запись."""
        record = self.validate_input()
        if record:
            self.records.append(record)
            self.save_data()
            self.update_table()
            self.clear_input_fields()
            messagebox.showinfo("Успех", "Запись добавлена!")

    def delete_record(self):
        """Удаляет выбранную запись."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Внимание", "Выберите запись для удаления.")
            return
        
        # Получаем индекс выбранного элемента в отображаемом списке
        # Примечание: так как у нас есть фильтрация, нужно быть осторожным с индексами.
        # Лучше искать по содержимому или использовать ID дерева, но для простоты 
        # мы будем удалять из основного списка, сопоставляя данные.
        
        item = self.tree.item(selected_item[0])
        values = item['values']
        
        # Находим запись в основном списке и удаляем её
        # (удаляем первое совпадение, чтобы не удалить дубликаты неправильно, если они есть)
        for i, rec in enumerate(self.records):
            if (rec['date'] == values[0] and 
                float(rec['temperature']) == float(values[1]) and 
                rec['description'] == values[2]):
                self.records.pop(i)
                break
        
        self.save_data()
        self.apply_filters() # Обновляем таблицу с учетом текущих фильтров

    def clear_input_fields(self):
        """Очищает поля ввода."""
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%d.%m.%Y"))
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precipitation_var.set(False)

    def reset_filters(self):
        """Сбрасывает фильтры."""
        self.filter_date_entry.delete(0, tk.END)
        self.filter_temp_entry.delete(0, tk.END)
        self.update_table()

    def apply_filters(self, event=None):
        """Фильтрует и отображает записи."""
        self.update_table()

    def update_table(self):
        """Обновляет таблицу, применяя фильтры."""
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Получаем значения фильтров
        filter_date = self.filter_date_entry.get().strip()
        filter_temp_str = self.filter_temp_entry.get().strip()
        
        filter_temp = None
        if filter_temp_str:
            try:
                filter_temp = float(filter_temp_str)
            except ValueError:
                pass # Игнорируем некорректный ввод в фильтре

        # Фильтрация данных
        filtered_records = []
        for rec in self.records:
            match_date = True
            match_temp = True

            if filter_date:
                if rec['date'] != filter_date:
                    match_date = False
            
            if filter_temp is not None:
                if rec['temperature'] < filter_temp:
                    match_temp = False

            if match_date and match_temp:
                filtered_records.append(rec)

        # Вставка отфильтрованных данных в таблицу
        for rec in filtered_records:
            self.tree.insert("", tk.END, values=(
                rec['date'],
                rec['temperature'],
                rec['description'],
                rec['precipitation']
            ))

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiaryApp(root)
    root.mainloop()