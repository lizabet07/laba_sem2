"""
Модуль для работы с банковским счетом
Класс BankAccount - демонстрация инкапсуляции, свойств и магических методов
"""

from datetime import datetime
from enum import Enum


class AccountStatus(Enum):
    """Статусы банковского счета"""
    ACTIVE = "активен"
    BLOCKED = "заблокирован"
    CLOSED = "закрыт"
    FROZEN = "заморожен"


class BankAccount:
    """
    Класс, представляющий банковский счет
    
    Атрибуты класса:
        _next_account_number (int): Счетчик для генерации номеров счетов
        MIN_BALANCE (float): Минимальный допустимый баланс
        MAX_BALANCE (float): Максимальный допустимый баланс
        BANK_NAME (str): Название банка
    
    Атрибуты экземпляра:
        _account_number (str): Номер счета (закрытый)
        _owner_name (str): ФИО владельца (закрытый)
        _balance (float): Баланс счета (закрытый)
        _status (AccountStatus): Статус счета (закрытый)
        _interest_rate (float): Процентная ставка (закрытый)
        _opening_date (datetime): Дата открытия счета (закрытый)
    """
    
    # Атрибуты класса
    _next_account_number = 1000
    MIN_BALANCE = 0.0
    MAX_BALANCE = 10000000.0  # 10 миллионов
    BANK_NAME = "Python Bank"
    
    def __init__(self, owner_name: str, initial_balance: float = 0.0, interest_rate: float = 0.01):
        """
        Конструктор класса BankAccount
        
        Args:
            owner_name: ФИО владельца счета
            initial_balance: Начальный баланс (по умолчанию 0.0)
            interest_rate: Процентная ставка (по умолчанию 1%)
            
        Raises:
            ValueError: При некорректных входных данных
        """
        self._validate_owner_name(owner_name)
        self._validate_balance(initial_balance)
        self._validate_interest_rate(interest_rate)
        
        self._account_number = self._generate_account_number()
        self._owner_name = owner_name.strip()
        self._balance = initial_balance
        self._interest_rate = interest_rate
        self._status = AccountStatus.ACTIVE
        self._opening_date = datetime.now()
    
    def _generate_account_number(self) -> str:
        """Генерация уникального номера счета"""
        BankAccount._next_account_number += 1
        return f"ACC{self._next_account_number:06d}"
    
    # Методы валидации
    def _validate_owner_name(self, name: str) -> None:
        """
        Валидация имени владельца
        
        Args:
            name: ФИО для проверки
            
        Raises:
            ValueError: Если имя некорректно
        """
        if not isinstance(name, str):
            raise ValueError("Имя владельца должно быть строкой")
        
        name = name.strip()
        if not name:
            raise ValueError("Имя владельца не может быть пустым")
        
        if len(name) < 5:
            raise ValueError("Имя владельца должно содержать минимум 5 символов")
        
        if len(name) > 100:
            raise ValueError("Имя владельца не может превышать 100 символов")
        
        # Проверка, что имя содержит только буквы, пробелы и дефисы
        if not all(c.isalpha() or c.isspace() or c == '-' for c in name):
            raise ValueError("Имя владельца может содержать только буквы, пробелы и дефисы")
    
    def _validate_balance(self, balance: float) -> None:
        """
        Валидация баланса
        
        Args:
            balance: Баланс для проверки
            
        Raises:
            ValueError: Если баланс некорректен
        """
        if not isinstance(balance, (int, float)):
            raise ValueError("Баланс должен быть числом")
        
        if balance < self.MIN_BALANCE:
            raise ValueError(f"Баланс не может быть меньше {self.MIN_BALANCE}")
        
        if balance > self.MAX_BALANCE:
            raise ValueError(f"Баланс не может превышать {self.MAX_BALANCE}")
    
    def _validate_interest_rate(self, rate: float) -> None:
        """
        Валидация процентной ставки
        
        Args:
            rate: Процентная ставка для проверки
            
        Raises:
            ValueError: Если ставка некорректна
        """
        if not isinstance(rate, (int, float)):
            raise ValueError("Процентная ставка должна быть числом")
        
        if rate < 0 or rate > 1:
            raise ValueError("Процентная ставка должна быть в диапазоне [0, 1]")
    
    def _validate_amount(self, amount: float, operation: str = "операция") -> None:
        """
        Валидация суммы операции
        
        Args:
            amount: Сумма для проверки
            operation: Название операции
            
        Raises:
            ValueError: Если сумма некорректна
        """
        if not isinstance(amount, (int, float)):
            raise ValueError(f"Сумма {operation} должна быть числом")
        
        if amount <= 0:
            raise ValueError(f"Сумма {operation} должна быть положительной")
        
        if amount > self.MAX_BALANCE:
            raise ValueError(f"Сумма {operation} не может превышать {self.MAX_BALANCE}")
    
    def _check_status_for_operation(self, operation: str) -> None:
        """
        Проверка статуса счета для выполнения операции
        
        Args:
            operation: Название операции
            
        Raises:
            PermissionError: Если операция запрещена в текущем статусе
        """
        if self._status == AccountStatus.CLOSED:
            raise PermissionError(f"Невозможно выполнить {operation}: счет закрыт")
        
        if self._status == AccountStatus.BLOCKED:
            raise PermissionError(f"Невозможно выполнить {operation}: счет заблокирован")
        
        if self._status == AccountStatus.FROZEN:
            raise PermissionError(f"Невозможно выполнить {operation}: счет заморожен")
    
    # Свойства (геттеры)
    @property
    def account_number(self) -> str:
        """Номер счета (только для чтения)"""
        return self._account_number
    
    @property
    def owner_name(self) -> str:
        """ФИО владельца"""
        return self._owner_name
    
    @owner_name.setter
    def owner_name(self, value: str) -> None:
        """
        Сеттер для имени владельца с валидацией
        
        Args:
            value: Новое имя владельца
        """
        self._validate_owner_name(value)
        self._owner_name = value.strip()
    
    @property
    def balance(self) -> float:
        """Баланс счета (только для чтения)"""
        return self._balance
    
    @property
    def status(self) -> AccountStatus:
        """Статус счета"""
        return self._status
    
    @property
    def interest_rate(self) -> float:
        """Процентная ставка"""
        return self._interest_rate
    
    @interest_rate.setter
    def interest_rate(self, value: float) -> None:
        """
        Сеттер для процентной ставки с валидацией
        
        Args:
            value: Новая процентная ставка
        """
        self._validate_interest_rate(value)
        self._interest_rate = value
    
    @property
    def opening_date(self) -> datetime:
        """Дата открытия счета (только для чтения)"""
        return self._opening_date
    
    @property
    def days_since_opened(self) -> int:
        """Количество дней с момента открытия счета"""
        return (datetime.now() - self._opening_date).days
    
    # Бизнес-методы
    def deposit(self, amount: float) -> float:
        """
        Внесение средств на счет
        
        Args:
            amount: Сумма для внесения
            
        Returns:
            float: Новый баланс
            
        Raises:
            ValueError: При некорректной сумме
            PermissionError: При запрещенной операции
        """
        self._check_status_for_operation("внесение средств")
        self._validate_amount(amount, "внесения")
        
        new_balance = self._balance + amount
        self._validate_balance(new_balance)
        
        self._balance = new_balance
        return self._balance
    
    def withdraw(self, amount: float) -> float:
        """
        Снятие средств со счета
        
        Args:
            amount: Сумма для снятия
            
        Returns:
            float: Новый баланс
            
        Raises:
            ValueError: При некорректной сумме или недостатке средств
            PermissionError: При запрещенной операции
        """
        self._check_status_for_operation("снятие средств")
        self._validate_amount(amount, "снятия")
        
        if amount > self._balance:
            raise ValueError(f"Недостаточно средств. Доступно: {self._balance:.2f}")
        
        new_balance = self._balance - amount
        self._validate_balance(new_balance)
        
        self._balance = new_balance
        return self._balance
    
    def calculate_interest(self) -> float:
        """
        Расчет процентов по счету
        
        Returns:
            float: Сумма процентов
        """
        if self._status == AccountStatus.CLOSED:
            return 0.0
        
        return self._balance * self._interest_rate
    
    def apply_interest(self) -> float:
        """
        Начисление процентов на счет
        
        Returns:
            float: Новый баланс
            
        Raises:
            PermissionError: При попытке начислить проценты на закрытый счет
        """
        if self._status == AccountStatus.CLOSED:
            raise PermissionError("Невозможно начислить проценты на закрытый счет")
        
        interest = self.calculate_interest()
        if interest > 0:
            self._balance += interest
        return self._balance
    
    # Методы изменения состояния
    def activate(self) -> None:
        """Активация счета"""
        if self._status == AccountStatus.CLOSED:
            raise PermissionError("Невозможно активировать закрытый счет")
        self._status = AccountStatus.ACTIVE
    
    def block(self) -> None:
        """Блокировка счета"""
        if self._status == AccountStatus.CLOSED:
            raise PermissionError("Невозможно заблокировать закрытый счет")
        self._status = AccountStatus.BLOCKED
    
    def freeze(self) -> None:
        """Заморозка счета"""
        if self._status == AccountStatus.CLOSED:
            raise PermissionError("Невозможно заморозить закрытый счет")
        self._status = AccountStatus.FROZEN
    
    def close(self) -> None:
        """Закрытие счета (можно только при нулевом балансе)"""
        if self._balance != 0:
            raise ValueError("Невозможно закрыть счет с ненулевым балансом")
        self._status = AccountStatus.CLOSED
    
    def transfer_to(self, target_account: 'BankAccount', amount: float) -> None:
        """
        Перевод средств на другой счет
        
        Args:
            target_account: Счет получателя
            amount: Сумма перевода
            
        Raises:
            ValueError: При некорректных параметрах
            PermissionError: При запрещенных операциях
        """
        if not isinstance(target_account, BankAccount):
            raise ValueError("Цель перевода должна быть банковским счетом")
        
        # Снимаем средства со счета отправителя
        self.withdraw(amount)
        
        try:
            # Вносим средства на счет получателя
            target_account.deposit(amount)
        except Exception as e:
            # В случае ошибки возвращаем средства
            self._balance += amount
            raise e
    
    # Магические методы
    def __str__(self) -> str:
        """
        Строковое представление для пользователей
        
        Returns:
            str: Информация о счете в удобном формате
        """
        return (f"Счет {self._account_number}\n"
                f"Владелец: {self._owner_name}\n"
                f"Баланс: {self._balance:,.2f} {self._get_currency_symbol()}\n"
                f"Статус: {self._status.value}\n"
                f"Ставка: {self._interest_rate * 100:.1f}%\n"
                f"Дней с открытия: {self.days_since_opened}")
    
    def __repr__(self) -> str:
        """
        Официальное строковое представление для разработчиков
        
        Returns:
            str: Представление для отладки
        """
        return (f"BankAccount(owner_name='{self._owner_name}', "
                f"balance={self._balance:.2f}, "
                f"status='{self._status.value}', "
                f"interest_rate={self._interest_rate:.3f})")
    
    def __eq__(self, other: object) -> bool:
        """
        Сравнение счетов по номеру
        
        Args:
            other: Другой объект для сравнения
            
        Returns:
            bool: True если счета равны
        """
        if not isinstance(other, BankAccount):
            return False
        return self._account_number == other._account_number
    
    def __lt__(self, other: 'BankAccount') -> bool:
        """
        Сравнение счетов по балансу (для сортировки)
        
        Args:
            other: Другой счет
            
        Returns:
            bool: True если баланс текущего счета меньше
        """
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self._balance < other._balance
    
    def _get_currency_symbol(self) -> str:
        """Возвращает символ валюты"""
        return "₽"  # Можно расширить для разных валют


# Дополнительный класс для демонстрации взаимодействия
class Transaction:
    """
    Класс для представления банковской транзакции
    """
    
    def __init__(self, from_account: BankAccount, to_account: BankAccount, amount: float):
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount
        self.timestamp = datetime.now()
        self.status = "pending"
    
    def execute(self) -> bool:
        """Выполнение транзакции"""
        try:
            self.from_account.transfer_to(self.to_account, self.amount)
            self.status = "completed"
            return True
        except Exception as e:
            self.status = f"failed: {str(e)}"
            return False
    
    def __str__(self) -> str:
        return (f"Транзакция {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Отправитель: {self.from_account.account_number}\n"
                f"Получатель: {self.to_account.account_number}\n"
                f"Сумма: {self.amount:.2f}\n"
                f"Статус: {self.status}")