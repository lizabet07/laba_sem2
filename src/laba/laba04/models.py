"""
Модели счетов с интерфейсами для ЛР-4
"""

import sys
import os
from typing import List, Any

# ========== ФИКСИРОВАННЫЙ ИМПОРТ ==========
sys.path.insert(0, r"C:\Users\HONOR\laba_prog\laba_sem2\src\laba\labа03")
sys.path.insert(0, r"C:\Users\HONOR\laba_prog\laba_sem2")

from base import BankAccount as BaseBankAccount
from base import AccountCollection as BaseCollection
from interfaces import Printable, Comparable


class BankAccount(BaseBankAccount, Printable, Comparable):
    """Базовый класс с интерфейсами"""
    
    def to_string(self) -> str:
        return f"[{self.get_type()}] {self.number}: {self.owner} | {self._balance:.2f}₽"
    
    def compare_to(self, other: Any) -> int:
        if self._balance < other._balance:
            return -1
        elif self._balance > other._balance:
            return 1
        else:
            return 0


class SavingsAccount(BankAccount):
    """Накопительный счёт"""
    
    def __init__(self, owner, balance=0.0, rate=0.05, bonus=0.01, limit=3):
        super().__init__(owner, balance, rate)
        self.bonus = bonus
        self.limit = limit
        self.withdrawals = 0
    
    @property
    def total_rate(self):
        return self.rate + self.bonus
    
    def add_bonus(self):
        if self.status == "активен" and self._balance >= 10000:
            bonus = self._balance * self.bonus
            self._balance += bonus
            return bonus
        return 0.0
    
    def withdraw(self, amount):
        if self.withdrawals >= self.limit:
            raise PermissionError(f"Лимит снятий ({self.limit}) исчерпан")
        result = super().withdraw(amount)
        self.withdrawals += 1
        return result
    
    def calculate_interest(self):
        if self.status != "активен":
            return 0.0
        return self._balance * self.total_rate
    
    def process_monthly(self):
        result = super().process_monthly()
        if "error" not in result:
            result["bonus"] = self.add_bonus()
            result["balance"] = self._balance
            self.withdrawals = 0
        return result
    
    def get_type(self):
        return "Накопительный"
    
    def annual_fee(self):
        return max(500, self._balance * 0.005)
    
    def to_string(self) -> str:
        base = super().to_string()
        return f"{base} | ставка: {self.total_rate*100:.1f}% | снятий: {self.withdrawals}/{self.limit}"
    
    def compare_to(self, other: Any) -> int:
        my_rate = self.total_rate
        other_rate = other.total_rate if hasattr(other, 'total_rate') else other.rate
        
        if my_rate < other_rate:
            return -1
        elif my_rate > other_rate:
            return 1
        else:
            return 0


class CreditAccount(BankAccount):
    """Кредитный счёт"""
    
    def __init__(self, owner, balance=0.0, rate=0.02, credit_limit=50000, credit_rate=0.18):
        # ВАЖНО: вызываем конструктор BankAccount с ПОЛОЖИТЕЛЬНЫМ балансом
        # если передан отрицательный, передаём 0
        initial_balance = max(0, balance)
        super().__init__(owner, initial_balance, rate)
        
        self.credit_limit = credit_limit
        self.credit_rate = credit_rate
        
        # Если был передан отрицательный баланс - эмулируем долг
        if balance < 0:
            self._balance = balance
            self._credit_used = abs(balance)
        else:
            self._credit_used = 0
    
    @property
    def credit_available(self):
        return self.credit_limit - self._credit_used
    
    def withdraw(self, amount):
        import lib.validate as validate
        ok, err = validate.validate_status_for_operation(self.status, "снять")
        if not ok:
            raise PermissionError(err)
        
        max_amount = self._balance + self.credit_available
        if amount > max_amount:
            raise ValueError(f"Максимум: {max_amount:.2f}")
        
        self._balance -= amount
        self._credit_used = abs(self._balance) if self._balance < 0 else 0
        return self._balance
    
    def calculate_interest(self):
        if self.status != "активен":
            return 0.0
        if self._balance >= 0:
            return self._balance * self.rate
        else:
            return self._balance * self.credit_rate
    
    def process_monthly(self):
        if self.status != "активен":
            return {"error": f"Счёт {self.number} не активен"}
        
        interest = self.calculate_interest()
        self._balance += interest
        self._credit_used = abs(self._balance) if self._balance < 0 else 0
        
        return {
            "account": self.number, "type": self.get_type(),
            "interest": interest, "balance": self._balance,
            "credit_used": self._credit_used
        }
    
    def get_type(self):
        return "Кредитный"
    
    def annual_fee(self):
        return 1200 + self.credit_limit * 0.01
    
    def to_string(self) -> str:
        base = super().to_string()
        if self._balance < 0:
            return f"{base} | долг: {-self._balance:.2f}₽ | лимит: {self.credit_limit:.0f}₽"
        else:
            return f"{base} | кредит доступен: {self.credit_available:.0f}₽"


class PremiumAccount(SavingsAccount):
    """Премиум счёт"""
    
    def __init__(self, owner, balance=100000.0, rate=0.06, bonus=0.02, limit=10):
        if balance < 100000:
            raise ValueError("Минимум 100000₽ для премиум счёта")
        super().__init__(owner, balance, rate, bonus, limit)
        self.concierge = True
        self.vip_level = "Gold"
    
    def calculate_interest(self):
        base = super().calculate_interest()
        if self._balance > 500000:
            self.vip_level = "Platinum"
            return base + self._balance * 0.005
        elif self._balance > 250000:
            self.vip_level = "Gold"
            return base + self._balance * 0.002
        return base
    
    def get_type(self):
        return "Премиум"
    
    def annual_fee(self):
        return 5000
    
    def to_string(self) -> str:
        base = super().to_string()
        return f"{base} | VIP {self.vip_level} | консьерж: {'да' if self.concierge else 'нет'}"
    
    def compare_to(self, other: Any) -> int:
        if hasattr(other, 'vip_level'):
            levels = {"Platinum": 3, "Gold": 2, "Silver": 1}
            my_lvl = levels.get(self.vip_level, 0)
            other_lvl = levels.get(other.vip_level, 0)
            
            if my_lvl < other_lvl:
                return -1
            elif my_lvl > other_lvl:
                return 1
        
        return super().compare_to(other)


class AccountCollection(BaseCollection):
    """Расширенная коллекция с поддержкой интерфейсов"""
    
    def get_printable(self) -> List[Printable]:
        return [item for item in self._items if isinstance(item, Printable)]
    
    def get_comparable(self) -> List[Comparable]:
        return [item for item in self._items if isinstance(item, Comparable)]
    
    def print_all(self):
        for item in self.get_printable():
            print(f"  {item.to_string()}")
    
    def sort_using_comparable(self, reverse: bool = False):
        items = self.get_comparable()
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                if (items[i].compare_to(items[j]) > 0) != reverse:
                    items[i], items[j] = items[j], items[i]
        self._items = items
        return self
    
    def find_best(self):
        items = self.get_comparable()
        if not items:
            return None
        best = items[0]
        for item in items[1:]:
            if item.compare_to(best) > 0:
                best = item
        return best