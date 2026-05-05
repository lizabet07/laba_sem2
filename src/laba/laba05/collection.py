"""
Расширенная коллекция с функциональными методами для ЛР-5
"""

from typing import Callable

# Прямой импорт без сложных путей
try:
    from laba03.base import BankAccount
except ImportError:
    from base import BankAccount


class BankAccountCollection:
    """Коллекция банковских счетов"""
    
    def __init__(self, items=None):
        self._items = list(items) if items else []
    
    def add(self, item):
        """Добавить счёт с проверкой типа"""
        # Временная проверка: разрешаем добавлять любой объект, у которого есть owner и balance
        if not hasattr(item, 'owner') or not hasattr(item, 'balance'):
            raise TypeError("Объект должен иметь атрибуты owner и balance")
        if any(acc.owner == item.owner for acc in self._items):
            raise ValueError(f"Счёт для {item.owner} уже есть")
        self._items.append(item)
        return self
    
    def remove(self, item):
        self._items.remove(item)
        return self
    
    def get_all(self):
        return self._items.copy()
    
    def sort_by(self, key_func: Callable, reverse: bool = False):
        self._items.sort(key=key_func, reverse=reverse)
        return self
    
    def filter_by(self, predicate: Callable):
        filtered = [item for item in self._items if predicate(item)]
        return BankAccountCollection(filtered)
    
    def apply(self, func: Callable):
        return [func(item) for item in self._items]
    
    def __len__(self):
        return len(self._items)
    
    def __getitem__(self, index):
        if isinstance(index, slice):
            return BankAccountCollection(self._items[index])
        return self._items[index]
    
    def __iter__(self):
        return iter(self._items)
    
    def __str__(self):
        if not self._items:
            return "Коллекция пуста"
        return "\n".join(str(acc) for acc in self._items)
    
    def __repr__(self):
        return f"BankAccountCollection({len(self._items)} счетов)"