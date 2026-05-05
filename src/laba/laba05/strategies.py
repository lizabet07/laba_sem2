"""
Модуль стратегий для ЛР-5
"""


# ========== ФУНКЦИИ ДЛЯ СОРТИРОВКИ ==========

def by_balance(account):
    return account.balance


def by_owner_name(account):
    return account.owner


def by_balance_desc(account):
    return -account.balance


def by_multiple_criteria(account):
    status_order = {"активен": 0, "заблокирован": 1, "закрыт": 2}
    return (status_order.get(account.status, 3), -account.balance)


# ========== ФУНКЦИИ-ФИЛЬТРЫ ==========

def is_active(account):
    return account.status == "активен"


def is_not_closed(account):
    return account.status != "закрыт"


# ========== ФАБРИКИ ФУНКЦИЙ ==========

def make_balance_filter(min_balance, max_balance=float('inf')):
    def filter_fn(account):
        return min_balance <= account.balance <= max_balance
    return filter_fn


def make_discount_applier(percent):
    def apply_discount(account):
        return {
            "account": account.number,
            "original": account.balance,
            "discounted": account.balance * (1 - percent / 100)
        }
    return apply_discount


# ========== ФУНКЦИИ ДЛЯ map() ==========

def to_short_string(account):
    return f"{account.number}: {account.owner} ({account.balance:.0f}₽)"


def to_dict(account):
    return {
        "number": account.number,
        "owner": account.owner,
        "balance": account.balance,
        "status": account.status,
        "type": account.get_type()
    }


def extract_name_balance(account):
    return (account.owner, account.balance)


# ========== CALLABLE-ОБЪЕКТЫ ==========

class SimpleInterestStrategy:
    def __call__(self, account):
        if account.status != "активен":
            return 0.0
        return account.balance * account.rate


class AggressiveInterestStrategy:
    def __init__(self, threshold=50000, bonus=0.01):
        self.threshold = threshold
        self.bonus = bonus
    
    def __call__(self, account):
        if account.status != "активен":
            return 0.0
        base = account.balance * account.rate
        if account.balance > self.threshold:
            return base + account.balance * self.bonus
        return base


class ConservativeInterestStrategy:
    def __call__(self, account):
        if account.status != "активен" or account.balance > 500000:
            return 0.0
        return account.balance * account.rate * 0.7