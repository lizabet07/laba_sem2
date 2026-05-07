"""
Модуль стратегий для ЛР-5
"""
# ========== ФУНКЦИИ ДЛЯ СОРТИРОВКИ (используются как key в sort/sorted) ==========

def by_balance(account):
    """Ключ сортировки: по балансу (от меньшего к большему)"""
    return account.balance  # Просто возвращаем число


def by_owner_name(account):
    """Ключ сортировки: по имени владельца (алфавитный порядок)"""
    return account.owner  # Возвращаем строку


def by_balance_desc(account):
    """Ключ сортировки: по балансу (от большего к меньшему)"""
    return -account.balance  # Минус - чем больше баланс, тем меньше число


def by_multiple_criteria(account):
    """
    Ключ сортировки: по нескольким критериям
    Сначала статус, потом баланс (по убыванию)
    Кортеж сравнивается поэлементно
    """
    status_order = {"активен": 0, "заблокирован": 1, "закрыт": 2}
    return (status_order.get(account.status, 3), -account.balance)
    # Возвращаем кортеж: (статус_число, -баланс)


# ========== ФУНКЦИИ-ФИЛЬТРЫ (используются в filter, возвращают True/False) ==========

def is_active(account):
    """Предикат: счёт активен?"""
    return account.status == "активен"  # True если активен, False если нет


def is_not_closed(account):
    """Предикат: счёт не закрыт?"""
    return account.status != "закрыт"  # True если не закрыт


# ========== ФАБРИКИ ФУНКЦИЙ (возвращают новые функции) ==========

def make_balance_filter(min_balance, max_balance=float('inf')):
    """
    Фабрика: создаёт фильтр для баланса в заданном диапазоне
    Использует замыкание - min_balance и max_balance запоминаются
    """
    def filter_fn(account):
        # Эта внутренняя функция "запоминает" min_balance и max_balance
        return min_balance <= account.balance <= max_balance
    return filter_fn  # Возвращаем функцию, а НЕ результат её вызова


def make_discount_applier(percent):
    """
    Фабрика: создаёт функцию для применения скидки
    Возвращает функцию, которая преобразует счёт в словарь со скидкой
    """
    def apply_discount(account):
        # Внутренняя функция "запоминает" percent
        return {
            "account": account.number,  # Номер счёта
            "original": account.balance,  # Исходный баланс
            "discounted": account.balance * (1 - percent / 100)  # Баланс со скидкой
        }
    return apply_discount


# ========== ФУНКЦИИ ДЛЯ map() (преобразуют один счёт во что-то другое) ==========

def to_short_string(account):
    """Преобразует счёт в короткую строку для вывода"""
    return f"{account.number}: {account.owner} ({account.balance:.0f}₽)"


def to_dict(account):
    """Преобразует счёт в словарь со всеми полями"""
    return {
        "number": account.number,
        "owner": account.owner,
        "balance": account.balance,
        "status": account.status,
        "type": account.get_type()
    }


def extract_name_balance(account):
    """Извлекает пару (имя, баланс)"""
    return (account.owner, account.balance)


# ========== CALLABLE-ОБЪЕКТЫ (классы, экземпляры которых можно вызывать как функции) ==========

class SimpleInterestStrategy:
    """
    Простая стратегия начисления процентов
    Проценты = баланс × ставка (только для активных счетов)
    """
    def __call__(self, account):
        # Этот метод позволяет вызывать объект как функцию: strategy(account)
        if account.status != "активен":
            return 0.0
        return account.balance * account.rate


class AggressiveInterestStrategy:
    """
    Агрессивная стратегия начисления процентов
    Базовая ставка + бонус если баланс выше порога
    """
    def __init__(self, threshold=50000, bonus=0.01):
        # Сохраняем настройки внутри объекта
        self.threshold = threshold  # Порог для бонуса
        self.bonus = bonus          # Дополнительный процент
    
    def __call__(self, account):
        if account.status != "активен":
            return 0.0
        base = account.balance * account.rate  # Базовые проценты
        if account.balance > self.threshold:   # Если баланс больше порога
            return base + account.balance * self.bonus  # Добавляем бонус
        return base


class ConservativeInterestStrategy:
    """
    Консервативная стратегия начисления процентов
    Начисляет только 70% от ставки, и только если баланс не слишком большой
    """
    def __call__(self, account):
        # Не начисляем если счёт не активен ИЛИ баланс больше 500 000
        if account.status != "активен" or account.balance > 500000:
            return 0.0
        return account.balance * account.rate * 0.7  # Только 70% от ставки
