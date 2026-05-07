import tkinter as tk
from tkinter import ttk, messagebox
from task_manager import TaskManager

class RandomTaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Инициализация менеджера задач
        self.task_manager = TaskManager()
        
        # Текущий фильтр
        self.current_filter = None
        
        self.setup_ui()
        self.update_history_display()
    
    def setup_ui(self):
        # Основной контейнер
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # ===== Верхняя панель: генерация задачи =====
        generate_frame = ttk.LabelFrame(main_frame, text="Генерация задачи", padding="10")
        generate_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.generate_btn = ttk.Button(
            generate_frame, 
            text="🎲 Сгенерировать задачу", 
            command=self.generate_task,
            width=30
        )
        self.generate_btn.pack()
        
        # Поле для отображения сгенерированной задачи
        self.current_task_label = ttk.Label(
            generate_frame, 
            text="Нажмите кнопку, чтобы получить задачу",
            font=("Arial", 12, "bold"),
            wraplength=500
        )
        self.current_task_label.pack(pady=10)
        
        # ===== Панель добавления новой задачи =====
        add_frame = ttk.LabelFrame(main_frame, text="Добавить свою задачу", padding="10")
        add_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(add_frame, text="Текст задачи:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.new_task_entry = ttk.Entry(add_frame, width=50)
        self.new_task_entry.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        ttk.Label(add_frame, text="Категория:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.category_var = tk.StringVar(value="учёба")
        category_combo = ttk.Combobox(add_frame, textvariable=self.category_var, values=["учёба", "спорт", "работа"], state="readonly", width=20)
        category_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.add_btn = ttk.Button(add_frame, text="➕ Добавить", command=self.add_new_task)
        self.add_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # ===== Левая панель: список всех задач =====
        all_tasks_frame = ttk.LabelFrame(main_frame, text="Все доступные задачи", padding="10")
        all_tasks_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5), pady=5)
        
        all_tasks_scroll = ttk.Scrollbar(all_tasks_frame)
        all_tasks_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.all_tasks_listbox = tk.Listbox(all_tasks_frame, yscrollcommand=all_tasks_scroll.set, height=15)
        self.all_tasks_listbox.pack(fill=tk.BOTH, expand=True)
        all_tasks_scroll.config(command=self.all_tasks_listbox.yview)
        
        # ===== Правая панель: история =====
        history_frame = ttk.LabelFrame(main_frame, text="История сгенерированных задач", padding="10")
        history_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Фильтр
        filter_frame = ttk.Frame(history_frame)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(filter_frame, text="Фильтр:").pack(side=tk.LEFT, padx=5)
        
        self.filter_var = tk.StringVar(value="все")
        filter_all = ttk.Radiobutton(filter_frame, text="Все", variable=self.filter_var, value="все", command=self.apply_filter)
        filter_all.pack(side=tk.LEFT, padx=5)
        
        filter_study = ttk.Radiobutton(filter_frame, text="📚 Учёба", variable=self.filter_var, value="учёба", command=self.apply_filter)
        filter_study.pack(side=tk.LEFT, padx=5)
        
        filter_sport = ttk.Radiobutton(filter_frame, text="🏃 Спорт", variable=self.filter_var, value="спорт", command=self.apply_filter)
        filter_sport.pack(side=tk.LEFT, padx=5)
        
        filter_work = ttk.Radiobutton(filter_frame, text="💼 Работа", variable=self.filter_var, value="работа", command=self.apply_filter)
        filter_work.pack(side=tk.LEFT, padx=5)
        
        # Кнопка очистки истории
        self.clear_btn = ttk.Button(filter_frame, text="🗑 Очистить историю", command=self.clear_history)
        self.clear_btn.pack(side=tk.RIGHT, padx=5)
        
        # Список истории
        history_scroll = ttk.Scrollbar(history_frame)
        history_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(history_frame, yscrollcommand=history_scroll.set, height=15)
        self.history_listbox.pack(fill=tk.BOTH, expand=True)
        history_scroll.config(command=self.history_listbox.yview)
        
        # Обновление списка всех задач
        self.update_all_tasks_display()
    
    def generate_task(self):
        """Генерирует задачу и добавляет в историю"""
        task = self.task_manager.generate_and_add_to_history()
        self.current_task_label.config(text=f"✨ {task['text']} ({task['category']}) ✨")
        self.update_history_display()
        self.update_all_tasks_display()
    
    def add_new_task(self):
        """Добавляет новую задачу"""
        text = self.new_task_entry.get()
        category = self.category_var.get()
        
        if self.task_manager.add_task(text, category):
            messagebox.showinfo("Успех", f"Задача \"{text}\" добавлена!")
            self.new_task_entry.delete(0, tk.END)
            self.update_all_tasks_display()
        else:
            messagebox.showerror("Ошибка", "Текст задачи не может быть пустым!")
    
    def apply_filter(self):
        """Применяет фильтр к истории"""
        filter_value = self.filter_var.get()
        if filter_value == "все":
            self.current_filter = None
        else:
            self.current_filter = filter_value
        self.update_history_display()
    
    def update_history_display(self):
        """Обновляет отображение истории с учётом фильтра"""
        self.history_listbox.delete(0, tk.END)
        
        filtered_history = self.task_manager.filter_history_by_category(self.current_filter)
        
        if not filtered_history:
            self.history_listbox.insert(tk.END, "История пуста")
        else:
            for task in filtered_history:
                self.history_listbox.insert(tk.END, f"{task['text']} ({task['category']})")
    
    def update_all_tasks_display(self):
        """Обновляет список всех доступных задач"""
        self.all_tasks_listbox.delete(0, tk.END)
        
        for task_str in self.task_manager.get_all_tasks_list():
            self.all_tasks_listbox.insert(tk.END, task_str)
    
    def clear_history(self):
        """Очищает историю"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.task_manager.clear_history()
            self.update_history_display()

def main():
    root = tk.Tk()
    app = RandomTaskGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()