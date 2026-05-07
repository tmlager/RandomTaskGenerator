import unittest
import os
import json
from task_manager import TaskManager

class TestTaskManager(unittest.TestCase):
    
    def setUp(self):
        """Создаём временный файл для тестов"""
        self.test_filename = "test_data.json"
        self.manager = TaskManager(self.test_filename)
    
    def tearDown(self):
        """Удаляем тестовый файл после тестов"""
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)
    
    # ===== ПОЗИТИВНЫЕ ТЕСТЫ =====
    def test_add_task_positive(self):
        """Позитивный тест: добавление корректной задачи"""
        result = self.manager.add_task("Пойти в спортзал", "спорт")
        self.assertTrue(result)
        
        # Проверяем, что задача добавилась
        tasks = self.manager.get_all_tasks_list()
        self.assertTrue(any("Пойти в спортзал" in task for task in tasks))
    
    def test_generate_random_task(self):
        """Позитивный тест: генерация задачи возвращает словарь с ключами text и category"""
        task = self.manager.get_random_task()
        self.assertIn("text", task)
        self.assertIn("category", task)
        self.assertIsInstance(task["text"], str)
    
    def test_save_and_load_json(self):
        """Позитивный тест: сохранение и загрузка JSON"""
        self.manager.add_task("Тестовая задача", "учёба")
        self.manager.generate_and_add_to_history()
        
        # Создаём новый менеджер, который загрузит те же данные
        new_manager = TaskManager(self.test_filename)
        
        # Проверяем, что задачи сохранились
        tasks = new_manager.get_all_tasks_list()
        self.assertTrue(any("Тестовая задача" in task for task in tasks))
    
    def test_filter_history_by_category(self):
        """Позитивный тест: фильтрация истории по категории"""
        self.manager.history = [
            {"text": "Учить Python", "category": "учёба"},
            {"text": "Бег", "category": "спорт"},
            {"text": "Отчёт", "category": "работа"}
        ]
        
        filtered = self.manager.filter_history_by_category("учёба")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["text"], "Учить Python")
    
    # ===== НЕГАТИВНЫЕ ТЕСТЫ =====
    def test_add_task_empty_string(self):
        """Негативный тест: добавление пустой строки"""
        result = self.manager.add_task("", "учёба")
        self.assertFalse(result)
        
        result = self.manager.add_task("   ", "учёба")
        self.assertFalse(result)
    
    def test_generate_from_empty_list(self):
        """Негативный тест: генерация при пустом списке задач"""
        self.manager.all_tasks = []
        task = self.manager.get_random_task()
        self.assertEqual(task["text"], "Нет задач! Добавьте новую.")
    
    # ===== ГРАНИЧНЫЕ ТЕСТЫ =====
    def test_boundary_long_text(self):
        """Граничный тест: очень длинное название задачи"""
        long_text = "А" * 1000
        result = self.manager.add_task(long_text, "учёба")
        self.assertTrue(result)
    
    def test_boundary_single_character(self):
        """Граничный тест: задача из одного символа"""
        result = self.manager.add_task("X", "работа")
        self.assertTrue(result)
    
    def test_boundary_clear_history(self):
        """Граничный тест: очистка истории"""
        self.manager.generate_and_add_to_history()
        self.manager.generate_and_add_to_history()
        self.assertEqual(len(self.manager.history), 2)
        
        self.manager.clear_history()
        self.assertEqual(len(self.manager.history), 0)
    
    def test_boundary_invalid_category(self):
        """Граничный тест: неверная категория (должна стать учёбой)"""
        result = self.manager.add_task("Задача", "несуществующая")
        self.assertTrue(result)
        
        # Проверяем, что категория изменилась на "учёба"
        tasks = self.manager.all_tasks
        found = False
        for task in tasks:
            if task["text"] == "Задача":
                self.assertEqual(task["category"], "учёба")
                found = True
        self.assertTrue(found)

if __name__ == "__main__":
    unittest.main()