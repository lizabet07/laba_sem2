"""
Модуль с классом BankAccountCollection для лабораторной работы №2
"""

from ..laba03.base import BankAccount

class BankAccountCollection:
    """Контейнер для хранения банковских счетов"""

    def __init__(self, items=None):
        """Конструктор коллекции"""
        self._items = items if items is not None else []

    def add(self, item):
        """Добавить банковский счёт в коллекцию"""
        if not isinstance(item, BankAccount):
            raise TypeError("Можно добавлять только объекты типа BankAccount")
        
        # ПРОВЕРКА ДУБЛИКАТОВ ПО ИМЕНИ ВЛАДЕЛЬЦА
        if any(acc.owner_name == item.owner_name for acc in self._items):
            raise ValueError(f"Счёт для владельца '{item.owner_name}' уже существует в коллекции")
        
        self._items.append(item)

    def remove(self, item):
        """Удалить банковский счёт из коллекции"""
        try:
            self._items.remove(item)
        except ValueError:
            raise ValueError(f"Счёт {item.account_number} не найден в коллекции")

    def remove_at(self, index):
        """Удалить счёт по индексу"""
        if 0 <= index < len(self._items):
            return self._items.pop(index)
        raise IndexError("Индекс выходит за границы коллекции")

    def get_all(self):
        """Вернуть список всех счетов"""
        return self._items.copy()

    def find_by_owner_name(self, name):
        """Поиск счетов по имени владельца"""
        return BankAccountCollection([acc for acc in self._items if acc.owner_name == name])

    def find_by_status(self, status):
        """Поиск счетов по статусу"""
        return BankAccountCollection([acc for acc in self._items if acc.status == status])

    def find_by_balance_range(self, min_balance, max_balance):
        """Поиск счетов в диапазоне балансов"""
        return BankAccountCollection([
            acc for acc in self._items
            if min_balance <= acc.balance <= max_balance
        ])

    def get_active(self):
        """Получить коллекцию активных счетов"""
        return BankAccountCollection([acc for acc in self._items if acc.status == "активен"])

    def get_blocked(self):
        """Получить коллекцию заблокированных счетов"""
        return BankAccountCollection([acc for acc in self._items if acc.status == "заблокирован"])

    def get_high_balance(self, threshold=100000):
        """Получить счета с балансом выше порога"""
        return BankAccountCollection([acc for acc in self._items if acc.balance > threshold])

    def sort_by_balance(self, reverse=False):
        """Сортировка по балансу"""
        self._items.sort(key=lambda acc: acc.balance, reverse=reverse)

    def sort_by_owner_name(self, reverse=False):
        """Сортировка по имени владельца"""
        self._items.sort(key=lambda acc: acc.owner_name, reverse=reverse)
    
    def sort(self, key, reverse=False):
        """Универсальная сортировка по ключу"""
        self._items.sort(key=key, reverse=reverse)

    def __len__(self):
        """Возвращает количество счетов в коллекции"""
        return len(self._items)

    def __getitem__(self, index):
        """Доступ к счёту по индексу"""
        if isinstance(index, slice):
            return BankAccountCollection(self._items[index])
        return self._items[index]

    def __iter__(self):
        """Итератор по коллекции"""
        return iter(self._items)

    def __str__(self):
        """Строковое представление коллекции"""
        if not self._items:
            return "Коллекция пуста"
        accounts_str = "\n".join(str(acc) for acc in self._items)
        return f"Коллекция банковских счетов ({len(self)} счетов):\n{accounts_str}"

    def __repr__(self):
        """Представление для разработчиков"""
        return f"BankAccountCollection({len(self._items)} счетов)"