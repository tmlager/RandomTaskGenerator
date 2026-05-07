import json
import random
from typing import List, Dict

class TaskManager:
    def __init__(self, filename="data.json"):
        self.filename = filename
        self.categories = ["учёба", "спорт", "работа"]
        
        # Предопределённые задачи
        self.default_tasks = [
            {"text": "Прочитать статью", "category": "учёба"},
            {"text": "Сделать зарядку", "category": "спорт"},
            {"text": "Выучить 5 новых слов", "category": "учёба"},
            {"text": "Пробежать 2 км", "category": "спорт"},
            {"text": "Сдать отчёт", "category": "работа"},
            {"text": "Написать план на день", "category": "работа"},
            {"text": "Посмотреть вебинар", "category": "учёба"},
            {"text": "Отжаться 20 раз", "category": "спорт"},
            {"text": "Провести встречу", "category": "работа"},
            {"text": "Почитать книгу", "category": "учёба"}
        ]
        
        self.all_tasks = self.default_tasks.copy()
        self.history = []
        self.load_data()
    
    def get_random_task(self) -> Dict:
        """Возвращает случайную задачу из всех доступных"""
        if not self.all_tasks:
            return {"text": "Нет задач! Добавьте новую.", "category": "учёба"}
        return random.choice(self.all_tasks)
    
    def add_task(self, text: str, category: str) -> bool:
        """Добавляет новую задачу. Возвращает True, если успешно"""
        # Валидация: не пустая строка
        if not text or not text.strip():
            return False
        
        # Проверка категории
        if category not in self.categories:
            category = "учёба"
        
        new_task = {"text": text.strip(), "category": category}
        self.all_tasks.append(new_task)
        self.save_data()
        return True
    
    def generate_and_add_to_history(self):
        """Генерирует задачу и добавляет её в историю"""
        task = self.get_random_task()
        self.history.append(task)
        self.save_data()
        return task
    
    def clear_history(self):
        """Очищает историю"""
        self.history = []
        self.save_data()
    
    def filter_history_by_category(self, category: str = None) -> List[Dict]:
        """Фильтрует историю по категории. Если category=None, возвращает всё"""
        if not category:
            return self.history
        return [task for task in self.history if task["category"] == category]
    
    def save_data(self):
        """Сохраняет all_tasks и history в JSON"""
        data = {
            "all_tasks": self.all_tasks,
            "history": self.history
        }
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
    
    def load_data(self):
        """Загружает данные из JSON"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.all_tasks = data.get("all_tasks", self.default_tasks.copy())
                self.history = data.get("history", [])
        except FileNotFoundError:
            # Файла нет - используем значения по умолчанию
            self.all_tasks = self.default_tasks.copy()
            self.history = []
            self.save_data()
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            self.all_tasks = self.default_tasks.copy()
            self.history = []
    
    def get_all_tasks_list(self) -> List[str]:
        """Возвращает список всех задач (для отображения)"""
        return [f"{task['text']} ({task['category']})" for task in self.all_tasks]