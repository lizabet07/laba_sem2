"""
Расширенная коллекция с функциональными методами для ЛР-5
"""

from typing import Callable  # Для указания типа "функция"


class BankAccountCollection:
    """Коллекция банковских счетов"""
    
    def __init__(self, items=None):
        self._items = list(items) if items else []  # Внутренний список для хранения счетов
    
    def add(self, item):
        """Добавить счёт"""
        if not hasattr(item, 'owner') or not hasattr(item, 'balance'):
            raise TypeError("Объект должен иметь атрибуты owner и balance")
        if any(acc.owner == item.owner for acc in self._items):
            raise ValueError(f"Счёт для {item.owner} уже есть")
        self._items.append(item)
        return self  # Возвращаем self для цепочек вызовов
    
    def remove(self, item):
        self._items.remove(item)
        return self
    
    def get_all(self):
        return self._items.copy()  # Возвращаем копию, чтобы нельзя было изменить внутренний список извне
    
    def sort_by(self, key_func: Callable, reverse: bool = False):
        """Сортировка по ключу - функция передаётся как аргумент"""
        self._items.sort(key=key_func, reverse=reverse)
        return self  # Возвращаем self для цепочек
    
    def filter_by(self, predicate: Callable):
        """Фильтрация по предикату - функция передаётся как аргумент"""
        filtered = [item for item in self._items if predicate(item)]
        return BankAccountCollection(filtered)  # Возвращаем НОВУЮ коллекцию
    
    def apply(self, func: Callable):
        """Применить функцию ко всем элементам"""
        return [func(item) for item in self._items]  # Возвращаем список результатов
    
    def __len__(self):
        return len(self._items)
    
    def __getitem__(self, index):
        if isinstance(index, slice):
            return BankAccountCollection(self._items[index])  # Для срезов возвращаем коллекцию
        return self._items[index]  # Для индекса возвращаем один счёт
    
    def __iter__(self):
        return iter(self._items)  # Чтобы можно было писать for acc in collection
    
    def __str__(self):
        if not self._items:
            return "Коллекция пуста"
        return "\n".join(str(acc) for acc in self._items)
    
    def __repr__(self):
        return f"BankAccountCollection({len(self._items)} счетов)"