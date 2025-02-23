"""
Описание ORM модели базы данных с использованием SQLAlchemy.
"""

# import modules
from . import users     # Импортирование модуля пользователей
from . import books     # Импортирование модуля книг
from . import reviews   # Импортирование модуля пользовательских отзывов

# import classes
from .files import File             # Импортирование модели для хранения файлов
from .languages import Language     # Импортирование модели для хранения языков
