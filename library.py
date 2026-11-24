from datetime import datetime, timedelta


class Book:
    """Книга."""

    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_available = True
        self.borrowed_by = None
        self.borrow_date = None

    def __str__(self):
        status = "доступна" if self.is_available else f"выдана {self.borrowed_by}"
        return f"'{self.title}' ({self.author}) — {status}"


class Reader:
    """Читатель."""

    def __init__(self, name):
        self.name = name
        self.borrowed_books = []

    def __str__(self):
        return f"{self.name} (книг на руках: {len(self.borrowed_books)})"


class Library:
    """Библиотека."""

    LOAN_DAYS = 14
    FINE_PER_DAY = 10

    def __init__(self):
        self.books = []
        self.readers = []

    def add_book(self, title, author):
        """Добавляет книгу в фонд."""
        book = Book(title, author)
        self.books.append(book)
        return book

    def add_reader(self, name):
        """Регистрирует читателя."""
        reader = Reader(name)
        self.readers.append(reader)
        return reader

    def find_book(self, title):
        """Ищет книгу по названию."""
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def find_reader(self, name):
        """Ищет читателя по имени."""
        for reader in self.readers:
            if reader.name.lower() == name.lower():
                return reader
        return None

    def lend_book(self, title, reader_name):
        """Выдаёт книгу читателю."""
        book = self.find_book(title)
        reader = self.find_reader(reader_name)

        if book is None:
            return "Книга не найдена"
        if reader is None:
            return "Читатель не найден"
        if not book.is_available:
            return "Книга уже выдана"

        book.is_available = False
        book.borrowed_by = reader_name
        book.borrow_date = datetime.now()
        reader.borrowed_books.append(book)
        return "Книга выдана"

    def return_book(self, title):
        """Возвращает книгу и рассчитывает штраф."""
        book = self.find_book(title)

        if book is None:
            return "Книга не найдена"
        if book.is_available:
            return "Книга не была выдана"

        days = (datetime.now() - book.borrow_date).days
        fine = max(0, (days - self.LOAN_DAYS) * self.FINE_PER_DAY)

        book.is_available = True
        reader = self.find_reader(book.borrowed_by)
        if reader and book in reader.borrowed_books:
            reader.borrowed_books.remove(book)

        book.borrowed_by = None
        book.borrow_date = None

        if fine > 0:
            return f"Книга возвращена. Штраф: {fine} руб."
        return "Книга возвращена. Штрафа нет."