import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random
from datetime import datetime

class RandomTaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("550x600")

        self.data_file = "data.json"
        self.tasks_pool = []
        self.history = []

        self.load_data()
        if not self.tasks_pool:
            self.init_predefined_tasks()

        self.setup_ui()
        self.update_history_view()

    def init_predefined_tasks(self):
        """Инициализация начального набора задач."""
        self.tasks_pool = [
            {"text": "Прочитать статью по программированию", "type": "учёба"},
            {"text": "Сделать зарядку на 15 минут", "type": "спорт"},
            {"text": "Завершить отчёт по проекту", "type": "работа"},
            {"text": "Изучить новую тему в учебнике", "type": "учёба"},
            {"text": "Пробежка 3 км", "type": "спорт"},
            {"text": "Ответить на рабочие письма", "type": "работа"},
            {"text": "Выучить 10 новых слов", "type": "учёба"},
            {"text": "Растяжка после тренировки", "type": "спорт"}
        ]

    def setup_ui(self):
        # --- Блок добавления пользовательской задачи ---
        add_frame = tk.LabelFrame(self.root, text="Добавить новую задачу", padx=10, pady=5)
        add_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(add_frame, text="Текст:").grid(row=0, column=0, sticky="w")
        self.task_entry = tk.Entry(add_frame, width=45)
        self.task_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(add_frame, text="Тип:").grid(row=0, column=2, sticky="w", padx=(10, 0))
        self.type_var = tk.StringVar(value="другое")
        ttk.Combobox(add_frame, textvariable=self.type_var, 
                     values=["учёба", "спорт", "работа", "другое"], state="readonly", width=10).grid(row=0, column=3, padx=5)

        tk.Button(add_frame, text="Добавить", command=self.add_custom_task, bg="#2196F3", fg="white").grid(row=0, column=4, padx=5)

        # --- Блок генерации и фильтрации ---
        gen_frame = tk.Frame(self.root)
        gen_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(gen_frame, text="Фильтр генерации:").pack(side=tk.LEFT)
        self.gen_filter_var = tk.StringVar(value="все")
        ttk.Combobox(gen_frame, textvariable=self.gen_filter_var, 
                     values=["все", "учёба", "спорт", "работа", "другое"], state="readonly", width=10).pack(side=tk.LEFT, padx=5)

        tk.Button(gen_frame, text="🎲 Сгенерировать задачу", command=self.generate_task, 
                  bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(side=tk.RIGHT, padx=5)

        # Отображение сгенерированной задачи
        self.result_label = tk.Label(self.root, text="Нажмите кнопку для генерации задачи!", 
                                     font=("Arial", 14, "bold"), fg="#333", height=2, relief="groove", bd=2)
        self.result_label.pack(pady=5)

        # --- Блок истории и фильтрации истории ---
        hist_frame = tk.LabelFrame(self.root, text="История задач", padx=10, pady=5)
        hist_frame.pack(fill="both", expand=True, padx=10, pady=5)

        hist_ctrl_frame = tk.Frame(hist_frame)
        hist_ctrl_frame.pack(fill="x", pady=5)

        tk.Label(hist_ctrl_frame, text="Фильтр истории:").pack(side=tk.LEFT)
        self.hist_filter_var = tk.StringVar(value="все")
        hist_combo = ttk.Combobox(hist_ctrl_frame, textvariable=self.hist_filter_var, 
                                  values=["все", "учёба", "спорт", "работа", "другое"], state="readonly", width=10)
        hist_combo.pack(side=tk.LEFT, padx=5)
        hist_combo.bind("<<ComboboxSelected>>", lambda e: self.update_history_view())

        tk.Button(hist_ctrl_frame, text="Очистить историю", command=self.clear_history, bg="#f44336", fg="white").pack(side=tk.RIGHT)

        # Список истории
        list_container = tk.Frame(hist_frame)
        list_container.pack(fill="both", expand=True, pady=5)

        self.history_listbox = tk.Listbox(list_container, font=("Arial", 11), bg="#fafafa")
        self.history_listbox.pack(side=tk.LEFT, fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.history_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.history_listbox.config(yscrollcommand=scrollbar.set)

    def add_custom_task(self):
        """Добавляет пользовательскую задачу с проверкой ввода."""
        text = self.task_entry.get().strip()
        if not text:
            messagebox.showwarning("Ошибка ввода", "Текст задачи не может быть пустым!")
            return
        
        task_type = self.type_var.get()
        new_task = {"text": text, "type": task_type}
        self.tasks_pool.append(new_task)
        self.save_data()
        self.task_entry.delete(0, tk.END)
        messagebox.showinfo("Успех", f"Задача добавлена: [{task_type}] {text}")

    def generate_task(self):
        """Выбирает случайную задачу и сохраняет её в историю."""
        filter_type = self.gen_filter_var.get()
        pool = [t for t in self.tasks_pool if filter_type == "все" or t["type"] == filter_type]

        if not pool:
            messagebox.showwarning("Внимание", "Нет задач выбранного типа для генерации.")
            return

        selected_task = random.choice(pool)
        history_entry = {
            "text": selected_task["text"],
            "type": selected_task["type"],
            "time": datetime.now().strftime("%H:%M:%S")
        }
        self.history.append(history_entry)
        self.save_data()
        self.update_history_view()

        self.result_label.config(text=f"{selected_task['text']} ({selected_task['type']})", fg="#1976D2")

    def update_history_view(self):
        """Обновляет отображение списка истории с учётом фильтра."""
        self.history_listbox.delete(0, tk.END)
        filter_type = self.hist_filter_var.get()

        for item in reversed(self.history):
            if filter_type == "все" or item["type"] == filter_type:
                display_str = f"[{item['time']}] {item['type'].upper()}: {item['text']}"
                self.history_listbox.insert(tk.END, display_str)

    def clear_history(self):
        """Очищает историю с подтверждением."""
        if messagebox.askyesno("Подтверждение", "Очистить всю историю задач?"):
            self.history = []
            self.save_data()
            self.update_history_view()
            self.result_label.config(text="Нажмите кнопку для генерации задачи!", fg="#333")

    def save_data(self):
        """Сохраняет пул задач и историю в JSON."""
        data = {"tasks_pool": self.tasks_pool, "history": self.history}
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except IOError:
            messagebox.showerror("Ошибка", "Не удалось сохранить данные в файл.")

    def load_data(self):
        """Загружает данные из JSON при старте."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks_pool = data.get("tasks_pool", [])
                    self.history = data.get("history", [])
            except (json.JSONDecodeError, IOError):
                messagebox.showwarning("Внимание", "Файл данных повреждён. Загружены данные по умолчанию.")
                self.tasks_pool = []
                self.history = []

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGeneratorApp(root)
    root.mainloop()
