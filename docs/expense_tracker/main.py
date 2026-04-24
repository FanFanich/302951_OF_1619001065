import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = "expenses.json"

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("850x550")
        self.expenses = []
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        # ─── Поля ввода ───
        input_frame = ttk.Frame(self.root, padding=10)
        input_frame.pack(fill=tk.X)

        ttk.Label(input_frame, text="Сумма:").grid(row=0, column=0, padx=5, sticky="e")
        self.amount_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.amount_var, width=10).grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="Категория:").grid(row=0, column=2, padx=5, sticky="e")
        self.category_var = tk.StringVar(value="Еда")
        categories = ["Еда", "Транспорт", "Развлечения", "Жильё", "Здоровье", "Другое"]
        ttk.Combobox(input_frame, textvariable=self.category_var, values=categories, width=15).grid(row=0, column=3, padx=5)

        ttk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=4, padx=5, sticky="e")
        self.date_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.date_var, width=12).grid(row=0, column=5, padx=5)

        ttk.Button(input_frame, text="➕ Добавить расход", command=self._add_expense).grid(row=0, column=6, padx=5)

        # ─── Таблица ───
        columns = ("amount", "category", "date")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=12)
        self.tree.heading("amount", text="Сумма (₽)")
        self.tree.heading("category", text="Категория")
        self.tree.heading("date", text="Дата")
        self.tree.column("amount", width=120, anchor="e")
        self.tree.column("category", width=180, anchor="w")
        self.tree.column("date", width=120, anchor="center")
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        # ─── Фильтры и итого ───
        filter_frame = ttk.Frame(self.root, padding=10)
        filter_frame.pack(fill=tk.X, padx=10)

        ttk.Label(filter_frame, text="Категория:").pack(side=tk.LEFT, padx=5)
        self.filter_cat = tk.StringVar(value="Все")
        ttk.Combobox(filter_frame, textvariable=self.filter_cat, values=["Все"] + categories, width=12, state="readonly").pack(side=tk.LEFT, padx=5)

        ttk.Label(filter_frame, text="Период с:").pack(side=tk.LEFT, padx=5)
        self.filter_start = tk.StringVar()
        ttk.Entry(filter_frame, textvariable=self.filter_start, width=10).pack(side=tk.LEFT)

        ttk.Label(filter_frame, text="по:").pack(side=tk.LEFT, padx=5)
        self.filter_end = tk.StringVar()
        ttk.Entry(filter_frame, textvariable=self.filter_end, width=10).pack(side=tk.LEFT)

        ttk.Button(filter_frame, text="🔍 Применить", command=self._refresh_table).pack(side=tk.LEFT, padx=10)
        ttk.Button(filter_frame, text="🗑 Сбросить", command=self._reset_filter).pack(side=tk.LEFT, padx=5)

        self.total_label = ttk.Label(filter_frame, text="💰 Итого за период: 0.00 ₽", font=("Arial", 12, "bold"))
        self.total_label.pack(side=tk.RIGHT, padx=5)

        # ─── Сохранение/Загрузка ───
        io_frame = ttk.Frame(self.root, padding=10)
        io_frame.pack(fill=tk.X, padx=10)
        ttk.Button(io_frame, text="💾 Сохранить JSON", command=self._save_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(io_frame, text="📂 Загрузить JSON", command=self._load_data).pack(side=tk.LEFT, padx=5)

    # ─── Валидация ───
    def _validate_input(self):
        amount_str = self.amount_var.get().strip()
        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Ошибка ввода", "Сумма должна быть положительным числом.")
                return False
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Сумма должна быть числом.")
            return False

        date_str = self.date_var.get().strip()
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Некорректный формат даты. Используйте ГГГГ-ММ-ДД.")
            return False
        return True

    # ─── Добавление ───
    def _add_expense(self):
        if not self._validate_input():
            return
        self.expenses.append({
            "amount": float(self.amount_var.get()),
            "category": self.category_var.get(),
            "date": self.date_var.get().strip()
        })
        self.amount_var.set("")
        self.date_var.set("")
        self._refresh_table()

    # ─── Фильтрация и подсчёт ───
    def _get_filtered(self):
        filtered = self.expenses[:]
        cat = self.filter_cat.get()
        if cat != "Все":
            filtered = [e for e in filtered if e["category"] == cat]

        start = self.filter_start.get().strip()
        end = self.filter_end.get().strip()

        if start:
            try:
                start_dt = datetime.strptime(start, "%Y-%m-%d")
                filtered = [e for e in filtered if datetime.strptime(e["date"], "%Y-%m-%d") >= start_dt]
            except ValueError:
                messagebox.showwarning("Фильтр", "Некорректная дата начала")
        if end:
            try:
                end_dt = datetime.strptime(end, "%Y-%m-%d")
                filtered = [e for e in filtered if datetime.strptime(e["date"], "%Y-%m-%d") <= end_dt]
            except ValueError:
                messagebox.showwarning("Фильтр", "Некорректная дата конца")
        return filtered

    def _refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        filtered = self._get_filtered()
        total = sum(e["amount"] for e in filtered)
        for e in filtered:
            self.tree.insert("", tk.END, values=(f"{e['amount']:.2f}", e["category"], e["date"]))
        self.total_label.config(text=f"💰 Итого за период: {total:.2f} ₽")

    def _reset_filter(self):
        self.filter_cat.set("Все")
        self.filter_start.set("")
        self.filter_end.set("")
        self._refresh_table()

    # ─── JSON ───
    def _save_data(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.expenses, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Успех", "Данные сохранены в expenses.json")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")

    def _load_data(self):
        if not os.path.exists(DATA_FILE):
            return
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.expenses = json.load(f)
            self._refresh_table()
            messagebox.showinfo("Успех", "Данные загружены из expenses.json")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
