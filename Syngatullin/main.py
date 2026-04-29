import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# --- Настройки ---
DATA_FILE = "data/trainings.json"
DATE_FORMAT = "%d.%m.%Y" # Формат даты: ДД.ММ.ГГГГ

class TrainingPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.root.geometry("700x500")
        
        # Загрузка данных из файла
        self.trainings = self.load_data()
        
        # Создание виджетов
        self.create_widgets()
        
        # Заполнение таблицы начальными данными
        self.update_table()
    
    def create_widgets(self):
        # --- Фрейм для ввода данных ---
        input_frame = tk.LabelFrame(self.root, text="Добавить новую тренировку", padx=10, pady=10)
        input_frame.pack(padx=10, pady=10, fill="x")
        
        # Дата
        tk.Label(input_frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, sticky="e")
        self.date_entry = tk.Entry(input_frame)
        self.date_entry.grid(row=0, column=1, sticky="we", padx=5)
        
        # Тип тренировки
        tk.Label(input_frame, text="Тип тренировки:").grid(row=1, column=0, sticky="e")
        self.type_entry = tk.Entry(input_frame)
        self.type_entry.grid(row=1, column=1, sticky="we", padx=5)
        
        # Длительность
        tk.Label(input_frame, text="Длительность (мин):").grid(row=2, column=0, sticky="e")
        self.duration_entry = tk.Entry(input_frame)
        self.duration_entry.grid(row=2, column=1, sticky="we", padx=5)
        
        # Кнопка добавления
        add_btn = tk.Button(input_frame, text="Добавить тренировку", command=self.add_training)
        add_btn.grid(row=3, column=0, columnspan=2, pady=10)
        
        # --- Фрейм для фильтрации ---
        filter_frame = tk.LabelFrame(self.root, text="Фильтр", padx=10, pady=10)
        filter_frame.pack(padx=10, pady=(0, 10), fill="x")
        
        tk.Label(filter_frame, text="Тип:").grid(row=0, column=0, sticky="e")
        self.filter_type_var = tk.StringVar()
        self.filter_type_entry = tk.Entry(filter_frame, textvariable=self.filter_type_var)
        self.filter_type_entry.grid(row=0, column=1, sticky="we", padx=5)
        
        tk.Label(filter_frame, text="Дата с:").grid(row=1, column=0, sticky="e")
        self.filter_date_from_var = tk.StringVar()
        self.filter_date_from_entry = tk.Entry(filter_frame, textvariable=self.filter_date_from_var)
        self.filter_date_from_entry.grid(row=1, column=1, sticky="we", padx=5)
        
        filter_btn = tk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        filter_btn.grid(row=2, column=0, columnspan=2, pady=5)
        
        clear_btn = tk.Button(filter_frame, text="Очистить фильтр", command=self.clear_filter)
        clear_btn.grid(row=3, column=0, columnspan=2)
        
        # --- Таблица для отображения данных ---
        columns = ("id", "date", "type", "duration")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        
         # Настройка ширины колонок
        self.tree.column("id", width=30)
        self.tree.column("date", width=120)
        self.tree.column("type", width=200)
        self.tree.column("duration", width=80)
        
         # Заголовки колонок
        self.tree.heading("id", text="ID")
        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип тренировки")
        self.tree.heading("duration", text="Длительность")
        
         # Полосы прокрутки
        yscroll = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        xscroll = ttk.Scrollbar(self.root, orient="horizontal", command=self.tree.xview)
        
         self.tree.configure(yscroll=yscroll.set, xscroll=xscroll.set)
         
         self.tree.pack(padx=10, pady=(0, 10), fill="both", expand=True)
         yscroll.pack(side="right", fill="y")
         xscroll.pack(side="bottom", fill="x")
    
    # --- Логика работы с данными ---
    def load_data(self):
         """Загрузка данных из JSON файла."""
         if not os.path.exists(DATA_FILE):
             os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True) # Создаем папку data если её нет
             return []
         
         try:
             with open(DATA_FILE, "r", encoding="utf-8") as f:
                 return json.load(f)
         except (json.JSONDecodeError, FileNotFoundError):
             return []
    
    def save_data(self):
         """Сохранение данных в JSON файл."""
         with open(DATA_FILE, "w", encoding="utf-8") as f:
             json.dump(self.trainings, f, ensure_ascii=False, indent=4)
    
    def validate_input(self):
         """Проверка корректности введенных данных."""
         date = self.date_entry.get().strip()
         tr_type = self.type_entry.get().strip()
         duration = self.duration_entry.get().strip()
         
         if not date or not tr_type or not duration:
             messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
             return False
         
         try:
             datetime.strptime(date, DATE_FORMAT) # Проверка формата даты
         except ValueError:
             messagebox.showerror("Ошибка", f"Неверный формат даты. Используйте {DATE_FORMAT}")
             return False
         
         try:
             duration_num = float(duration)
             if duration_num <= 0:
                 raise ValueError
         except ValueError:
             messagebox.showerror("Ошибка", "Длительность должна быть положительным числом.")
             return False
         
         return True

    def add_training(self):
         """Обработчик кнопки 'Добавить тренировку'."""
         if not self.validate_input():
             return

         new_training = {
             "id": len(self.trainings) + 1,
             "date": self.date_entry.get().strip(),
             "type": self.type_entry.get().strip(),
             "duration": float(self.duration_entry.get().strip())
         }
         
         self.trainings.append(new_training)
         self.save_data()
         self.update_table()
         
         # Очистка полей ввода после добавления
         self.date_entry.delete(0, 'end')
         self.type_entry.delete(0, 'end')
         self.duration_entry.delete(0, 'end')
    
    def update_table(self):
         """Обновление данных в таблице."""
         for i in self.tree.get_children():
              self.tree.delete(i) # Очистка таблицы

          filter_type = self.filter_type_var.get().lower()
          filter_date_from = self.filter_date_var_from.get()
          
          filtered_trainings = self.trainings.copy()
          
          if filter_type:
              filtered_trainings = [t for t in filtered_trainings if filter_type in t["type"].lower()]
          
          if filter_date_from:
              try:
                  date_from_obj = datetime.strptime(filter_date_from, DATE_FORMAT).date()
                  filtered_trainings = [t for t in filtered_trainings if datetime.strptime(t["date"], DATE_FORMAT).date() >= date_from_obj]
              except ValueError:
                  messagebox.showerror("Ошибка", f"Неверный формат даты фильтра. Используйте {DATE_FORMAT}")
                  return

          for t in filtered_trainings:
              self.tree.insert("", "end", values=(t["id"], t["date"], t["type"], t["duration"]))
    
    def apply_filter(self):
         """Применить фильтр."""
          self.update_table()
    
    def clear_filter(self):
         """Очистить фильтр."""
          self.filter_type_var.set("")
          self.filter_date_from_var.set("")
          self.update_table()
    
    def on_closing(self):
          """Сохранение данных при закрытии окна."""
          self.save_data()
          self.root.destroy()

# --- Запуск приложения ---
if __name__ == "__main__":
    from datetime import datetime # Импортируем здесь для избежания циклических зависимостей в классах

    root = tk.Tk()
    app = TrainingPlannerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing) # Перехват закрытия окна для сохранения данных
    root.mainloop()