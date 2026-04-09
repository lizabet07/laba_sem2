"""
Базовый класс BankAccount и коллекция для ЛР - 3
"""

from datetime import datetime
import sys
import os

# Правильный путь к lib (на два уровня выше: laba03 -> laba -> src)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from lib import validate


class BankAccount:
    """Базовый класс банковского счёта"""

    bank_name = "Python Bank"
    _next_number = 1000

    def __init__(self, owner, balance=0.0, rate=0.01):
        # Валидация
        ok, err = validate.validate_name(owner)
        if not ok:
            raise ValueError(f"имя: {err}")
        ok, err = validate.validate_balance(balance)
        if not ok:
            raise ValueError(f"баланс: {err}")
        ok, err = validate.validate_interest_rate(rate)
        if not ok:
            raise ValueError(f"ставка: {err}")

        self._owner = owner.strip()
        self._balance = float(balance)
        self._rate = float(rate)
        self._number = f"ACC{BankAccount._next_number}"
        BankAccount._next_number += 1
        self._status = "активен"
        self._opened = datetime.now()

    @property
    def number(self): return self._number
    @property
    def owner(self): return self._owner
    @property
    def balance(self): return self._balance
    @property
    def rate(self): return self._rate
    @property
    def status(self): return self._status

    def deposit(self, amount):
        if self._status != "активен":
            raise PermissionError("Счёт не активен")
        ok, err = validate.validate_amount(amount, "пополнения")
        if not ok: raise ValueError(err)
        self._balance += amount
        return self._balance

    def withdraw(self, amount):
        if self._status != "активен":
            raise PermissionError("Счёт не активен")
        ok, err = validate.validate_amount(amount, "снятия")
        if not ok: raise ValueError(err)
        if amount > self._balance:
            raise ValueError(f"Недостаточно средств. Доступно: {self._balance:.2f}")
        self._balance -= amount
        return self._balance

    def calculate_interest(self):
        if self._status == "закрыт":
            return 0.0
        return self._balance * self._rate

    def apply_interest(self):
        if self._status != "активен":
            raise PermissionError("Счёт не активен")
        interest = self.calculate_interest()
        self._balance += interest
        return interest

    def process_monthly(self):
        if self._status != "активен":
            return {"error": f"Счёт {self._number} не активен"}
        interest = self.calculate_interest()
        self._balance += interest
        return {
            "account": self._number,
            "type": self.get_type(),
            "interest": interest,
            "balance": self._balance
        }

    def get_type(self):
        return "Базовый"

    def calculate_fee(self):
        return 0.0

    def block(self):
        if self._status == "закрыт":
            raise PermissionError("Счёт закрыт")
        self._status = "заблокирован"

    def activate(self):
        if self._status == "закрыт":
            raise PermissionError("Счёт закрыт")
        self._status = "активен"

    def __str__(self):
        return f"[{self.get_type()}] {self._number}: {self._owner}, {self._balance:.2f} руб."

    def __repr__(self):
        return f"{self.__class__.__name__}('{self._owner}', {self._balance:.2f})"

    def __lt__(self, other):
        return self._balance < other._balance


class AccountCollection:
    """Коллекция счетов"""

    def __init__(self, items=None):
        self._items = items if items else []

    def add(self, acc):
        if not isinstance(acc, BankAccount):
            raise TypeError("Только BankAccount")
        if any(a.owner == acc.owner for a in self._items):
            raise ValueError(f"Счёт для {acc.owner} уже есть")
        self._items.append(acc)

    def get_all(self):
        return self._items.copy()

    def get_active(self):
        return AccountCollection([a for a in self._items if a.status == "активен"])

    def get_by_type(self, cls):
        return AccountCollection([a for a in self._items if isinstance(a, cls)])

    def process_all(self):
        return [acc.process_monthly() for acc in self._items]

    def total_fees(self):
        return sum(acc.calculate_fee() for acc in self._items)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, idx):
        return self._items[idx]

    def __iter__(self):
        return iter(self._items)

    def __str__(self):
        return "\n".join(str(a) for a in self._items)
    """
Модуль с функциями валидации
"""

def validate_name(name):
    """Проверка имени владельца счета"""
    if not isinstance(name, str):
        return False, "Имя должно быть строкой"
    
    name = name.strip()
    if not name:
        return False, "Имя не может быть пустым"
    
    if len(name) < 5:
        return False, "Имя должно содержать минимум 5 символов"
    
    if len(name) > 50:
        return False, "Имя слишком длинное (макс. 50 символов)"
    
    for c in name:
        if not (c.isalpha() or c.isspace()):
            return False, "Имя может содержать только буквы и пробелы"
    
    return True, "OK"


def validate_balance(balance):
    """Проверка баланса счета"""
    if not isinstance(balance, (int, float)):
        return False, "Баланс должен быть числом"
    
    if balance < 0:
        return False, "Баланс не может быть отрицательным"
    
    if balance > 10000000:
        return False, "Баланс не может превышать 10 миллионов"
    
    return True, "OK"


def validate_interest_rate(rate):
    """Проверка процентной ставки"""
    if not isinstance(rate, (int, float)):
        return False, "Процентная ставка должна быть числом"
    
    if rate < 0:
        return False, "Процентная ставка не может быть отрицательной"
    
    if rate > 1:
        return False, "Процентная ставка не может быть больше 1 (100%)"
    
    return True, "OK"


def validate_amount(amount, operation="операция"):
    """Проверка суммы операции"""
    if not isinstance(amount, (int, float)):
        return False, f"Сумма {operation} должна быть числом"
    
    if amount <= 0:
        return False, f"Сумма {operation} должна быть положительной"
    
    if amount > 10000000:
        return False, f"Сумма {operation} не может превышать 10 миллионов"
    
    return True, "OK"


def validate_transfer_target(target):
    """Проверка получателя перевода"""
    if not hasattr(target, 'number') and not hasattr(target, 'deposit'):
        return False, "Получатель должен быть банковским счетом"
    return True, "OK"


def validate_status_for_operation(status, operation):
    """Проверка статуса счета для выполнения операции"""
    if status == "закрыт":
        return False, f"Нельзя {operation}: счет закрыт"
    if status == "заблокирован":
        return False, f"Нельзя {operation}: счет заблокирован"
    return True, "OK"


def validate_withdrawal(balance, amount):
    """Проверка возможности снятия средств со счета"""
    if amount > balance:
        return False, f"Недостаточно средств. Доступно: {balance:.2f}"
    return True, "OK"


def validate_close(balance):
    """Проверка возможности закрытия счета"""
    if balance != 0:
        return False, f"Нельзя закрыть счет с деньгами. Баланс: {balance:.2f}"
    return True, "OK"