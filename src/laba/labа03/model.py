"""Производные классы счетов для ЛР - 3"""

from base import BankAccount
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from lib import validate


class SavingsAccount(BankAccount):
    """Накопительный счёт с бонусной ставкой и лимитом снятий"""

    def __init__(self, owner, balance=0.0, rate=0.05, bonus=0.01, limit=3):
        super().__init__(owner, balance, rate)
        self.bonus = bonus
        self.limit = limit
        self.withdrawals = 0

    @property
    def total_rate(self):
        return self.rate + self.bonus

    def add_bonus(self):
        """Новый метод - начисление бонуса"""
        if self.status == "активен" and self._balance >= 10000:
            bonus = self._balance * self.bonus
            self._balance += bonus
            return bonus
        return 0.0

    def withdraw(self, amount):
        """Переопределение - проверка лимита снятий"""
        if self.withdrawals >= self.limit:
            raise PermissionError(f"Лимит снятий ({self.limit}) исчерпан")
        result = super().withdraw(amount)
        self.withdrawals += 1
        return result

    def calculate_interest(self):
        if self.status != "активен": return 0.0
        return self._balance * self.total_rate

    def process_monthly(self):
        result = super().process_monthly()
        if "error" not in result:
            result["bonus"] = self.add_bonus()
            result["balance"] = self._balance
            self.withdrawals = 0  # сброс счётчика
        return result

    def get_type(self):
        return "Накопительный"

    def annual_fee(self):
        return max(500, self._balance * 0.005)

    def __str__(self):
        return f"{super().__str__()} [ставка:{self.total_rate*100:.1f}%]"


class CreditAccount(BankAccount):
    """Кредитный счёт с возможностью ухода в минус"""

    def __init__(self, owner, balance=0.0, rate=0.02, credit_limit=50000, credit_rate=0.18):
        super().__init__(owner, balance, rate)
        self.credit_limit = credit_limit
        self.credit_rate = credit_rate
        self._credit_used = max(0, -balance)

    @property
    def credit_available(self):
        return self.credit_limit - self._credit_used

    def credit_info(self):
        """Новый метод - информация о кредите"""
        return {"лимит": self.credit_limit, "доступно": self.credit_available}

    def withdraw(self, amount):
        """Переопределение - можно уходить в минус"""
        ok, err = validate.validate_status_for_operation(self.status, "снять")
        if not ok: raise PermissionError(err)
        
        max_amount = self._balance + self.credit_available
        if amount > max_amount:
            raise ValueError(f"Максимум: {max_amount:.2f}")
        
        self._balance -= amount
        self._credit_used = abs(self._balance) if self._balance < 0 else 0
        return self._balance

    def calculate_interest(self):
        if self.status != "активен": return 0.0
        if self._balance >= 0:
            return self._balance * self.rate
        else:
            return self._balance * self.credit_rate  # отрицательные проценты

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

    def __str__(self):
        return f"{super().__str__()} [кредит:{self.credit_available:.0f}₽]"


class PremiumAccount(SavingsAccount):
    """Премиум счёт - наследник накопительного"""

    def __init__(self, owner, balance=100000.0, rate=0.06, bonus=0.02, limit=10):
        if balance < 100000:
            raise ValueError("Минимум 100000₽ для премиум счёта")
        super().__init__(owner, balance, rate, bonus, limit)
        self.concierge = True

    def request_service(self, service):
        """Новый метод - консьерж-сервис"""
        services = {"travel": "Билеты", "hotel": "Отель", "car": "Авто"}
        return f"Запрос '{services.get(service, service)}' принят (приоритет)"

    def calculate_interest(self):
        base = super().calculate_interest()
        if self._balance > 500000:
            return base + self._balance * 0.005  # премиум-бонус
        return base

    def process_monthly(self):
        result = super().process_monthly()
        if "error" not in result:
            result["concierge"] = self.concierge
        return result

    def get_type(self):
        return "Премиум"

    def annual_fee(self):
        return 5000

    def __str__(self):
        return f"{super().__str__()} [VIP]"