"""
Импорт классов предметной области из предыдущих лабораторных
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from laba.laba03.base import BankAccount
from laba.laba03.model import SavingsAccount, CreditAccount, PremiumAccount

# Для удобства создаём словарь типов счетов
ACCOUNT_TYPES = {
    "1": ("Обычный", BankAccount),
    "2": ("Накопительный", SavingsAccount),
    "3": ("Кредитный", CreditAccount),
    "4": ("Премиум", PremiumAccount),
}

__all__ = ['BankAccount', 'SavingsAccount', 'CreditAccount', 'PremiumAccount', 'ACCOUNT_TYPES']