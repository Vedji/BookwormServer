from enum import Enum

class AllowedBookFileFormats(str, Enum):
    """
    Доступные mime-типы файлов для хранения содержимого книг.
    """
    NONE = None
    FB2 = "application/x-fictionbook+xml"
    EPUB = "application/epub+zip"
    MARKDOWN = "text/markdown"
