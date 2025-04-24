from enum import Enum


class AllowedFileFormats(str, Enum):
    FB2 = "application/x-fictionbook+xml"
    EPUB = "application/epub+zip"
    PDF = "application/pdf"
    MARKDOWN = "text/markdown"
    PNG = "image/png"
    JPEG = "image/jpeg"
    GIF = "image/gif"
    ZIP = "application/zip"
    TXT = "text/plain"
    INCORRECT_FILE_FORMAT = "application/octet-stream"
