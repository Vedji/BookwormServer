"""
Модуль отвечает за ORM-модели отвечающие за работу с книгами.
"""

# Импорт модулей
from . import genres

# Импорт классов
from .book import Book # Модель для с книг
from .book_preview_images import BookPreviewImage # Модель для отображения превью изображений книги
from .book_translations import BookTranslation # Модель для работы с переводами книги
