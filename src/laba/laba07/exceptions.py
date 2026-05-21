"""
Собственные исключения для предметной области
"""


class AccountNotFoundError(Exception):
    """Счёт не найден в коллекции."""
    pass


class DuplicateAccountError(Exception):
    """Счёт с таким номером или владельцем уже существует."""
    pass


class InvalidAccountDataError(Exception):
    """Некорректные данные для создания/изменения счёта."""
    pass


class StorageError(Exception):
    """Ошибка при работе с файлом хранилища."""
    pass