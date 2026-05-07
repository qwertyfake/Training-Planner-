import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.root.geometry("850x600")

        self.trainings = []

        # ===== Поля ввода =====
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Дата (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(input_frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Тип тренировки:").grid(row=1, column=0, padx=5, pady=5)
        self.type_entry = tk.Entry(input_frame)
        self.type_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Длительность (мин):").grid(row=2, column=0, padx=5, pady=5)
        self.duration_entry = tk.Entry(input_frame)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(
            input_frame,
            text="Добавить тренировку",
            command=self.add_training,
            bg="lightgreen"
        ).grid(row=3, column=0, columnspan=2, pady=10)

        # ===== Фильтрация =====
        filter_frame = tk.LabelFrame(root, text="Фильтрация")
        filter_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(filter_frame, text="Тип тренировки:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_type_entry = tk.Entry(filter_frame)
        self.filter_type_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(
            filter_frame,
            text="Фильтр по типу",
            command=self.filter_by_type
        ).grid(row=0, column=2, padx=5)

        tk.Label(filter_frame, text="Дата:").grid(row=1, column=0, padx=5, pady=5)
        self.filter_date_entry = tk.Entry(filter_frame)
        self.filter_date_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(
            filter_frame,
            text="Фильтр по дате",
            command=self.filter_by_date
        ).grid(row=1, column=2, padx=5)

        tk.Button(
            filter_frame,
            text="Показать все",
            command=self.display_trainings
        ).grid(row=2, column=1, pady=5)

        # ===== Таблица =====
        columns = ("date", "type", "duration")

        self.tree = ttk.Treeview(root, columns=columns, show="headings")

        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип тренировки")
        self.tree.heading("duration", text="Длительность (мин)")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # ===== JSON =====
        buttons_frame = tk.Frame(root)
        buttons_frame.pack(pady=10)

        tk.Button(
            buttons_frame,
            text="Сохранить JSON",
            command=self.save_to_json,
            bg="lightblue"
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            buttons_frame,
            text="Загрузить JSON",
            command=self.load_from_json,
            bg="lightyellow"
        ).grid(row=0, column=1, padx=10)

    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def add_training(self):
        date = self.date_entry.get()
        training_type = self.type_entry.get()
        duration = self.duration_entry.get()

        if not self.validate_date(date):
            messagebox.showerror(
                "Ошибка",
                "Дата должна быть в формате YYYY-MM-DD"
            )
            return

        try:
            duration = float(duration)

            if duration <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Ошибка",
                "Длительность должна быть положительным числом"
            )
            return

        if training_type.strip() == "":
            messagebox.showerror(
                "Ошибка",
                "Тип тренировки не должен быть пустым"
            )
            return

        training = {
            "date": date,
            "type": training_type,
            "duration": duration
        }

        self.trainings.append(training)
        self.display_trainings()
        self.clear_inputs()

    def clear_inputs(self):
        self.date_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)

    def display_trainings(self, trainings=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if trainings is None:
            trainings = self.trainings

        for training in trainings:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    training["date"],
                    training["type"],
                    training["duration"]
                )
            )

    def filter_by_type(self):
        training_type = self.filter_type_entry.get()

        filtered = [
            training for training in self.trainings
            if training["type"].lower() == training_type.lower()
        ]

        self.display_trainings(filtered)

    def filter_by_date(self):
        date = self.filter_date_entry.get()

        filtered = [
            training for training in self.trainings
            if training["date"] == date
        ]

        self.display_trainings(filtered)

    def save_to_json(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )

        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(
                    self.trainings,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

            messagebox.showinfo(
                "Успех",
                "Данные успешно сохранены"
            )

    def load_from_json(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")]
        )

        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                self.trainings = json.load(file)

            self.display_trainings()

            messagebox.showinfo(
                "Успех",
                "Данные успешно загружены"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
