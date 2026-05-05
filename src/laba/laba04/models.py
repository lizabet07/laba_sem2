"""
Модели счетов с интерфейсами для ЛР-4
"""

import sys
import os
from typing import List, Any

sys.path.insert(0, r"C:\Users\HONOR\laba_prog\laba_sem2\src\laba\labа03")
sys.path.insert(0, r"C:\Users\HONOR\laba_prog\laba_sem2")

from base import BankAccount as BaseBankAccount
from base import AccountCollection as BaseCollection
from interfaces import Printable, Comparable


# ========== БАЗОВЫЙ КЛАСС С ИНТЕРФЕЙСАМИ ==========
class BankAccount(BaseBankAccount, Printable, Comparable):
    
    # --- Интерфейс Printable ---
    def to_string(self) -> str:
        """Выводит тип, номер, владельца и баланс"""
        return f"[{self.get_type()}] {self.number}: {self.owner} | {self._balance:.2f}₽"
    
    # --- Интерфейс Comparable ---
    def compare_to(self, other: Any) -> int:
        """Сравнивает по балансу: -1 (меньше), 0 (равно), 1 (больше)"""
        if self._balance < other._balance:
            return -1
        elif self._balance > other._balance:
            return 1
        else:
            return 0


class SavingsAccount(BankAccount):
    """Добавляет бонусную ставку и лимит снятий"""
    def __init__(self, owner, balance=0.0, rate=0.05, bonus=0.01, limit=3):
        super().__init__(owner, balance, rate)  
        self.bonus = bonus      
        self.limit = limit      
        self.withdrawals = 0    
    
    # общая ставка = базовая + бонус 
    @property
    def total_rate(self):
        return self.rate + self.bonus

    def add_bonus(self):
        """Бонус начисляется если счёт активен и баланс >= 10000"""
        if self.status == "активен" and self._balance >= 10000:
            bonus = self._balance * self.bonus
            self._balance += bonus
            return bonus
        return 0.0
    
    # --- Снятие с проверкой лимита ---
    def withdraw(self, amount):
        if self.withdrawals >= self.limit:
            raise PermissionError(f"Лимит снятий ({self.limit}) исчерпан")
        result = super().withdraw(amount)
        self.withdrawals += 1
        return result
    
    # --- Расчёт процентов ---
    def calculate_interest(self):
        if self.status != "активен":
            return 0.0
        return self._balance * self.total_rate  
    
    # --- Ежемесячная обработка ---
    def process_monthly(self):
        result = super().process_monthly()  # Родительская обработка
        if "error" not in result:
            result["bonus"] = self.add_bonus()      
            result["balance"] = self._balance       
            self.withdrawals = 0                    
        return result
  
    def get_type(self):
        return "Накопительный"
    
    # --- Годовая комиссия ---
    def annual_fee(self):
        return max(500, self._balance * 0.005)  
    

class CreditAccount(BankAccount):
    """Позволяет уходить в минус в пределах кредитного лимита"""

    def __init__(self, owner, balance=0.0, rate=0.02, credit_limit=50000, credit_rate=0.18):
        initial_balance = max(0, balance)
        super().__init__(owner, initial_balance, rate)
        
        self.credit_limit = credit_limit    # Кредитный лимит
        self.credit_rate = credit_rate      # Ставка на долг
        
        # Если был минус - устанавливаем его вручную
        if balance < 0:
            self._balance = balance
            self._credit_used = abs(balance)  # Сколько использовано кредита
        else:
            self._credit_used = 0
    
    # --- Доступный остаток кредита ---
    @property
    def credit_available(self):
        return self.credit_limit - self._credit_used
    
    # --- Снятие (можно уходить в минус) ---
    def withdraw(self, amount):
        import lib.validate as validate
        ok, err = validate.validate_status_for_operation(self.status, "снять")
        if not ok:
            raise PermissionError(err)
        
        max_amount = self._balance + self.credit_available  # Максимум для снятия
        if amount > max_amount:
            raise ValueError(f"Максимум: {max_amount:.2f}")
        
        self._balance -= amount
        self._credit_used = abs(self._balance) if self._balance < 0 else 0
        return self._balance
    
    # --- Расчёт процентов ---
    def calculate_interest(self):
        if self.status != "активен":
            return 0.0
        if self._balance >= 0:
            return self._balance * self.rate   
        else:
            return self._balance * self.credit_rate  
    
    # --- Ежемесячная обработка ---
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
    
    # --- Тип счёта ---
    def get_type(self):
        return "Кредитный"
    
    # --- Годовая комиссия ---
    def annual_fee(self):
        return 1200 + self.credit_limit * 0.01  # 1200₽ + 1% от лимита
    
    # --- Интерфейс Printable ---
    def to_string(self) -> str:
        base = super().to_string()
        if self._balance < 0:
            return f"{base} | долг: {-self._balance:.2f}₽ | лимит: {self.credit_limit:.0f}₽"
        else:
            return f"{base} | кредит доступен: {self.credit_available:.0f}₽"


class PremiumAccount(SavingsAccount):
    """Премиум счёт с VIP-уровнем и консьерж-сервисом"""

    def __init__(self, owner, balance=100000.0, rate=0.06, bonus=0.02, limit=10):
        if balance < 100000:
            raise ValueError("Минимум 100000₽ для премиум счёта")
        super().__init__(owner, balance, rate, bonus, limit)
        self.concierge = True       # Доступ к консьерж-сервису
        self.vip_level = "Gold"     # VIP-уровень
    
    # --- Расчёт процентов с VIP-бонусом ---
    def calculate_interest(self):
        base = super().calculate_interest()
        if self._balance > 500000:
            self.vip_level = "Platinum"
            return base + self._balance * 0.005   
        elif self._balance > 250000:
            self.vip_level = "Gold"
            return base + self._balance * 0.002 
        return base
    
    # --- Тип счёта ---
    def get_type(self):
        return "Премиум"
    
    # --- Годовая комиссия ---
    def annual_fee(self):
        return 5000 
    
    # --- Интерфейс Printable ---
    def to_string(self) -> str:
        base = super().to_string()
        return f"{base} | VIP {self.vip_level} | консьерж: {'да' if self.concierge else 'нет'}"
    
    # --- Интерфейс Comparable ---
    def compare_to(self, other: Any) -> int:
        # Сначала сравниваем по VIP-уровню
        if hasattr(other, 'vip_level'):
            levels = {"Platinum": 3, "Gold": 2, "Silver": 1}
            my_lvl = levels.get(self.vip_level, 0)
            other_lvl = levels.get(other.vip_level, 0)
            
            if my_lvl < other_lvl:
                return -1
            elif my_lvl > other_lvl:
                return 1
        # Если уровни равны - сравниваем по балансу (родительский метод)
        return super().compare_to(other)


# ========== КОЛЛЕКЦИЯ С ПОДДЕРЖКОЙ ИНТЕРФЕЙСОВ ==========
class AccountCollection(BaseCollection):
    """Наследует коллекцию из ЛР-2 и добавляет работу с интерфейсами"""
    
    # --- Фильтрация: получить все Printable ---
    def get_printable(self) -> List[Printable]:
        return [item for item in self._items if isinstance(item, Printable)]
    
    # --- Фильтрация: получить все Comparable ---
    def get_comparable(self) -> List[Comparable]:
        return [item for item in self._items if isinstance(item, Comparable)]
    
    # --- Вывод всех через to_string() ---
    def print_all(self):
        for item in self.get_printable():
            print(f"  {item.to_string()}")
    
    # --- Сортировка через compare_to() ---
    def sort_using_comparable(self, reverse: bool = False):
        items = self.get_comparable()
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                if (items[i].compare_to(items[j]) > 0) != reverse:
                    items[i], items[j] = items[j], items[i]
        self._items = items
        return self
    
    # --- Поиск лучшего через compare_to() ---
    def find_best(self):
        items = self.get_comparable()
        if not items:
            return None
        best = items[0]
        for item in items[1:]:
            if item.compare_to(best) > 0:
                best = item
        return best
