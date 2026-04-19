"""
Интерфейсы для ЛР-4
"""

from abc import ABC, abstractmethod


class Printable(ABC):
    """Интерфейс для вывода информации"""
    
    @abstractmethod
    def to_string(self) -> str:
        """Возвращает строковое представление объекта"""
        pass


class Comparable(ABC):
    """Интерфейс для сравнения объектов"""
    
    @abstractmethod
    def compare_to(self, other) -> int:
        """
        Сравнивает текущий объект с другим.
        Возвращает: -1 (меньше), 0 (равно), 1 (больше)
        """
        pass