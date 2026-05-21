"""
Бизнес-логика приложения: управление коллекцией счетов
"""

from typing import List, Optional, Callable, Any
from datetime import datetime

from .exceptions import AccountNotFoundError, DuplicateAccountError, InvalidAccountDataError
from .models import BankAccount, SavingsAccount, CreditAccount, PremiumAccount, ACCOUNT_TYPES
from laba.laba02.collection import BankAccountCollection


class BankApp:
    """
    Основной класс приложения, управляющий коллекцией счетов.
    """
    
    def __init__(self) -> None:
        """Инициализирует пустую коллекцию счетов."""
        self._collection: BankAccountCollection = BankAccountCollection()
    
    @property
    def collection(self) -> BankAccountCollection:
        """Возвращает коллекцию счетов (только для чтения)."""
        return self._collection
    
    def add_account(self, account_type: str, **kwargs) -> BankAccount:
        """
        Добавляет новый счёт в коллекцию.
        
        Args:
            account_type: Тип счёта ("1", "2", "3", "4")
            **kwargs: Параметры для создания счёта
            
        Returns:
            Созданный объект счёта
            
        Raises:
            DuplicateAccountError: Если счёт с таким владельцем уже существует
        """
        type_name, account_class = ACCOUNT_TYPES.get(account_type, ("Обычный", BankAccount))
        
        # Проверяем, нет ли уже счёта с таким владельцем
        for acc in self._collection.get_all():
            if acc.owner == kwargs.get("owner"):
                raise DuplicateAccountError(f"Счёт для {kwargs.get('owner')} уже существует!")
        
        try:
            if account_type == "1":  # Обычный
                account = account_class(kwargs["owner"], kwargs["balance"], kwargs.get("rate", 0.05))
            elif account_type == "2":  # Накопительный
                account = account_class(
                    kwargs["owner"], kwargs["balance"],
                    kwargs.get("rate", 0.06), kwargs.get("bonus_rate", 0.02),
                    kwargs.get("min_term", 3)
                )
            elif account_type == "3":  # Кредитный
                account = account_class(
                    kwargs["owner"], kwargs["balance"],
                    kwargs.get("rate", 0.04), kwargs.get("credit_limit", 50000),
                    kwargs.get("interest_rate", 0.18)
                )
            elif account_type == "4":  # Премиум
                account = account_class(
                    kwargs["owner"], kwargs["balance"],
                    kwargs.get("rate", 0.07), kwargs.get("cashback_rate", 0.025),
                    kwargs.get("service_level", 1)
                )
            else:
                raise InvalidAccountDataError(f"Неизвестный тип счёта: {account_type}")
            
            self._collection.add(account)
            return account
        except Exception as e:
            raise InvalidAccountDataError(f"Ошибка создания счёта: {e}")
    
    def remove_account(self, owner: str) -> BankAccount:
        """
        Удаляет счёт по имени владельца.
        
        Args:
            owner: Имя владельца
            
        Returns:
            Удалённый счёт
            
        Raises:
            AccountNotFoundError: Если счёт не найден
        """
        for acc in self._collection.get_all():
            if acc.owner.lower() == owner.lower():
                self._collection.remove(acc)
                return acc
        
        raise AccountNotFoundError(f"Счёт для {owner} не найден!")
    
    def find_account(self, owner: str) -> Optional[BankAccount]:
        """
        Находит счёт по имени владельца.
        
        Args:
            owner: Имя владельца
            
        Returns:
            Найденный счёт или None
        """
        for acc in self._collection.get_all():
            if acc.owner.lower() == owner.lower():
                return acc
        return None
    
    def find_accounts_by_balance(self, min_balance: float, max_balance: float) -> List[BankAccount]:
        """
        Находит счета в диапазоне балансов.
        
        Args:
            min_balance: Минимальный баланс
            max_balance: Максимальный баланс
            
        Returns:
            Список подходящих счетов
        """
        result = []
        for acc in self._collection.get_all():
            if min_balance <= acc.balance <= max_balance:
                result.append(acc)
        return result
    
    def filter_by_status(self, status: str) -> List[BankAccount]:
        """
        Фильтрует счета по статусу.
        
        Args:
            status: Статус счёта ("активен", "заблокирован", "закрыт")
            
        Returns:
            Список счетов с указанным статусом
        """
        result = []
        for acc in self._collection.get_all():
            if acc.status.lower() == status.lower():
                result.append(acc)
        return result
    
    def sort_collection(self, key_func: Callable[[BankAccount], Any], reverse: bool = False) -> List[BankAccount]:
        """
        Сортирует коллекцию по заданному ключу.
        
        Args:
            key_func: Функция для получения значения для сортировки
            reverse: Сортировать в обратном порядке
            
        Returns:
            Отсортированный список счетов
        """
        items = self._collection.get_all()
        items.sort(key=key_func, reverse=reverse)
        return items
    
    def get_all_accounts(self) -> List[BankAccount]:
        """Возвращает список всех счетов."""
        return self._collection.get_all()
    
    def get_accounts_count(self) -> int:
        """Возвращает количество счетов."""
        return len(self._collection)
    
    def deposit(self, owner: str, amount: float) -> BankAccount:
        """
        Пополняет счёт владельца.
        
        Args:
            owner: Имя владельца
            amount: Сумма пополнения
            
        Returns:
            Обновлённый счёт
            
        Raises:
            AccountNotFoundError: Если счёт не найден
            ValueError: Если сумма некорректна
        """
        account = self.find_account(owner)
        if not account:
            raise AccountNotFoundError(f"Счёт для {owner} не найден!")
        
        account.deposit(amount)
        return account
    
    def withdraw(self, owner: str, amount: float) -> BankAccount:
        """
        Снимает средства со счёта владельца.
        
        Args:
            owner: Имя владельца
            amount: Сумма снятия
            
        Returns:
            Обновлённый счёт
            
        Raises:
            AccountNotFoundError: Если счёт не найден
            ValueError: Если сумма некорректна или недостаточно средств
        """
        account = self.find_account(owner)
        if not account:
            raise AccountNotFoundError(f"Счёт для {owner} не найден!")
        
        account.withdraw(amount)
        return account
    
    def block_account(self, owner: str) -> BankAccount:
        """Блокирует счёт владельца."""
        account = self.find_account(owner)
        if not account:
            raise AccountNotFoundError(f"Счёт для {owner} не найден!")
        
        account.block()
        return account
    
    def close_account(self, owner: str) -> BankAccount:
        """Закрывает счёт владельца."""
        account = self.find_account(owner)
        if not account:
            raise AccountNotFoundError(f"Счёт для {owner} не найден!")
        
        account.close()
        return account