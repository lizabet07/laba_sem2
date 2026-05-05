"""Базовый класс BankAccount и коллекция для ЛР-3"""

from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from lib.validate import validate

class BankAccount:
    """Базовый класс банковского счёта"""

    bank_name = "Python Bank"
    _next_id = 1000

    def __init__(self, owner, balance=0.0, rate=0.01):
        # Валидация
        for check in [validate.validate_name(owner), 
                      validate.validate_balance(balance),
                      validate.validate_interest_rate(rate)]:
            if not check[0]:
                raise ValueError(check[1])

        self.owner = owner.strip()
        self._balance = float(balance)
        self.rate = float(rate)
        self.number = f"ACC{BankAccount._next_id}"
        BankAccount._next_id += 1
        self.status = "активен"
        self._opened = datetime.now()

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        ok, err = validate.validate_status_for_operation(self.status, "пополнить")
        if not ok: raise PermissionError(err)
        ok, err = validate.validate_amount(amount, "пополнения")
        if not ok: raise ValueError(err)
        self._balance += amount
        return self._balance

    def withdraw(self, amount):
        ok, err = validate.validate_status_for_operation(self.status, "снять")
        if not ok: raise PermissionError(err)
        ok, err = validate.validate_amount(amount, "снятия")
        if not ok: raise ValueError(err)
        if amount > self._balance:
            raise ValueError(f"Недостаточно средств. Доступно: {self._balance:.2f}")
        self._balance -= amount
        return self._balance

    def calculate_interest(self):
        """Расчёт процентов (полиморфный метод)"""
        return self._balance * self.rate if self.status == "активен" else 0.0

    # === ОБЩИЙ ИНТЕРФЕЙС ===
    def process_monthly(self):
        """Ежемесячная обработка (полиморфный метод)"""
        if self.status != "активен":
            return {"error": f"Счёт {self.number} не активен"}
        interest = self.calculate_interest()
        self._balance += interest
        return {"account": self.number, "type": self.get_type(), 
                "interest": interest, "balance": self._balance}

    def get_type(self):
        return "Базовый"

    def annual_fee(self):
        return 0.0

    def block(self):
        if self.status != "закрыт": self.status = "заблокирован"

    def activate(self):
        if self.status != "закрыт": self.status = "активен"

    def close(self):
        if self._balance != 0:
            raise ValueError(f"Нельзя закрыть счёт с балансом {self._balance:.2f}")
        self.status = "закрыт"

    def __str__(self):
        return f"[{self.get_type()}] {self.number}: {self.owner}, {self._balance:.2f}₽"

    def __lt__(self, other):
        return self._balance < other._balance


class AccountCollection:
    """Коллекция счетов с методами фильтрации"""

    def __init__(self, items=None):
        self._items = items if items else []

    def add(self, acc):
        if not isinstance(acc, BankAccount):
            raise TypeError("Только BankAccount")
        if any(a.owner == acc.owner for a in self._items):
            raise ValueError(f"Счёт для {acc.owner} уже есть")
        self._items.append(acc)

    def get_by_type(self, acc_class):
        """Фильтрация по типу счёта"""
        return AccountCollection([a for a in self._items if isinstance(a, acc_class)])

    def process_all(self):
        """Полиморфная обработка всех счетов"""
        return [acc.process_monthly() for acc in self._items]

    def total_fees(self):
        return sum(acc.annual_fee() for acc in self._items)

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    def __str__(self):
        return "\n".join(str(acc) for acc in self._items)