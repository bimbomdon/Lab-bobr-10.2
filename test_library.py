import unittest
from datetime import datetime, timedelta
from library import Library


class TestLibrary(unittest.TestCase):

    def setUp(self):
        """Создаём чистую библиотеку перед каждым тестом."""
        self.lib = Library()
        self.lib.add_book("Мастер и Маргарита", "Булгаков")
        self.lib.add_reader("Иванов")

    # Тест 1
    def test_add_book(self):
        """После добавления книги её можно найти."""
        book = self.lib.find_book("Мастер и Маргарита")
        self.assertIsNotNone(book)
        self.assertEqual(book.author, "Булгаков")

    # Тест 2
    def test_add_reader(self):
        """После регистрации читателя его можно найти."""
        reader = self.lib.find_reader("Иванов")
        self.assertIsNotNone(reader)
        self.assertEqual(reader.name, "Иванов")

    # Тест 3
    def test_lend_book(self):
        """Выдача книги делает её недоступной."""
        result = self.lib.lend_book("Мастер и Маргарита", "Иванов")
        self.assertEqual(result, "Книга выдана")
        book = self.lib.find_book("Мастер и Маргарита")
        self.assertFalse(book.is_available)

    # Тест 4
    def test_lend_already_borrowed(self):
        """Повторная выдача уже выданной книги запрещена."""
        self.lib.lend_book("Мастер и Маргарита", "Иванов")
        result = self.lib.lend_book("Мастер и Маргарита", "Петров")
        self.assertEqual(result, "Книга уже выдана")

    # Тест 5
    def test_return_book(self):
        """Возврат книги делает её снова доступной."""
        self.lib.lend_book("Мастер и Маргарита", "Иванов")
        result = self.lib.return_book("Мастер и Маргарита")
        self.assertIn("возвращена", result)
        book = self.lib.find_book("Мастер и Маргарита")
        self.assertTrue(book.is_available)

    # Тест 6
    def test_return_not_borrowed(self):
        """Нельзя вернуть книгу, которая не была выдана."""
        result = self.lib.return_book("Мастер и Маргарита")
        self.assertEqual(result, "Книга не была выдана")

    # Тест 7
    def test_find_nonexistent_book(self):
        """Поиск несуществующей книги возвращает None."""
        book = self.lib.find_book("Неизвестная книга")
        self.assertIsNone(book)

    # Тест 8
    def test_find_nonexistent_reader(self):
        """Поиск несуществующего читателя возвращает None."""
        reader = self.lib.find_reader("Сидоров")
        self.assertIsNone(reader)

    # Тест 9
    def test_lend_nonexistent_book(self):
        """Выдача несуществующей книги возвращает ошибку."""
        result = self.lib.lend_book("Нет такой книги", "Иванов")
        self.assertEqual(result, "Книга не найдена")

    # Тест 10
    def test_lend_to_nonexistent_reader(self):
        """Выдача книги несуществующему читателю возвращает ошибку."""
        result = self.lib.lend_book("Мастер и Маргарита", "Петров")
        self.assertEqual(result, "Читатель не найден")

    # Тест 11
    def test_fine_no_delay(self):
        """Если книга возвращена вовремя, штрафа нет."""
        self.lib.lend_book("Мастер и Маргарита", "Иванов")
        result = self.lib.return_book("Мастер и Маргарита")
        self.assertIn("Штрафа нет", result)

    # Тест 12
    def test_fine_with_delay(self):
        """При просрочке начисляется штраф."""
        self.lib.lend_book("Мастер и Маргарита", "Иванов")
        book = self.lib.find_book("Мастер и Маргарита")
        # Искусственно сдвигаем дату выдачи на 20 дней назад
        book.borrow_date = datetime.now() - timedelta(days=20)
        result = self.lib.return_book("Мастер и Маргарита")
        # Просрочка: 20 - 14 = 6 дней; штраф: 6 * 10 = 60 руб.
        self.assertIn("60 руб.", result)


if __name__ == "__main__":
    unittest.main()