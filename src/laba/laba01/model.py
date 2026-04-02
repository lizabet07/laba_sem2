"""
Модуль с классом BankAccount для лабораторной работы №1
"""

from datetime import datetime
import validate

class BankAccount:
    """Класс банковского счета"""
    
    # Атрибут класса
    bank_name = "Python Bank"
    _next_account_number = 1000
    
    def __init__(self, owner_name, initial_balance=0.0, interest_rate=0.01):
        """
        Конструктор с проверкой данных через функции validate
        """
        # Валидация через отдельный модуль
        is_valid, error = validate.validate_name(owner_name)
        if not is_valid:
            raise ValueError(f"Ошибка в имени: {error}")
        
        is_valid, error = validate.validate_balance(initial_balance)
        if not is_valid:
            raise ValueError(f"Ошибка в балансе: {error}")
        
        is_valid, error = validate.validate_interest_rate(interest_rate)
        if not is_valid:
            raise ValueError(f"Ошибка в ставке: {error}")
        
        # Закрытые атрибуты
        self._owner_name = owner_name.strip()
        self._balance = float(initial_balance)
        self._interest_rate = float(interest_rate)
        self._account_number = f"ACC{BankAccount._next_account_number}"
        BankAccount._next_account_number += 1
        self._status = "активен"  # активен, заблокирован, закрыт
        self._opening_date = datetime.now()
    
    # Свойства (@property) - для чтения и записи
    @property
    def account_number(self):
        """Номер счета (только чтение)"""
        return self._account_number
    
    @property
    def owner_name(self):
        """Имя владельца"""
        return self._owner_name
    
    @owner_name.setter
    def owner_name(self, value):
        """Сеттер с валидацией"""
        is_valid, error = validate.validate_name(value)
        if not is_valid:
            raise ValueError(f"Ошибка в имени: {error}")
        self._owner_name = value.strip()
    
    @property
    def balance(self):
        """Баланс (только чтение)"""
        return self._balance
    
    @property
    def interest_rate(self):
        """Процентная ставка"""
        return self._interest_rate
    
    @interest_rate.setter
    def interest_rate(self, value):
        """Сеттер для ставки"""
        is_valid, error = validate.validate_interest_rate(value)
        if not is_valid:
            raise ValueError(f"Ошибка в ставке: {error}")
        self._interest_rate = value
    
    @property
    def status(self):
        """Статус счета"""
        return self._status
    
    @property
    def days_open(self):
        """Сколько дней счет открыт"""
        return (datetime.now() - self._opening_date).days
    
    # Бизнес-методы
    def deposit(self, amount):
        """Пополнение счета"""
        # Проверка статуса
        is_valid, error = validate.validate_status_for_operation(self._status, "пополнить счет")
        if not is_valid:
            raise PermissionError(error)
        
        # Проверка суммы
        is_valid, error = validate.validate_amount(amount, "пополнения")
        if not is_valid:
            raise ValueError(error)
        
        # Проверка нового баланса
        new_balance = self._balance + amount
        is_valid, error = validate.validate_balance(new_balance)
        if not is_valid:
            raise ValueError(error)
        
        self._balance = new_balance
        return self._balance
    
    def withdraw(self, amount):
        """Снятие со счета"""
        # Проверка статуса
        is_valid, error = validate.validate_status_for_operation(self._status, "снять деньги")
        if not is_valid:
            raise PermissionError(error)
        
        # Проверка суммы
        is_valid, error = validate.validate_amount(amount, "снятия")
        if not is_valid:
            raise ValueError(error)
        
        # Проверка наличия средств
        is_valid, error = validate.validate_withdrawal(self._balance, amount)
        if not is_valid:
            raise ValueError(error)
        
        self._balance -= amount
        return self._balance
    
    def calculate_interest(self):
        """Расчет процентов (бизнес-метод 1)"""
        if self._status == "закрыт":
            return 0.0
        return self._balance * self._interest_rate
    
    def apply_interest(self):
        """Начисление процентов (бизнес-метод 2)"""
        if self._status == "закрыт":
            raise PermissionError("Нельзя начислить проценты на закрытый счет")
        
        interest = self.calculate_interest()
        if interest > 0:
            self._balance += interest
        return interest
    
    # Методы изменения состояния
    def block(self):
        """Заблокировать счет"""
        if self._status == "закрыт":
            raise PermissionError("Нельзя заблокировать закрытый счет")
        self._status = "заблокирован"
    
    def activate(self):
        """Активировать счет"""
        if self._status == "закрыт":
            raise PermissionError("Нельзя активировать закрытый счет")
        self._status = "активен"
    
    def close(self):
        """Закрыть счет"""
        is_valid, error = validate.validate_close(self._balance)
        if not is_valid:
            raise ValueError(error)
        self._status = "закрыт"
    
    def transfer_to(self, other_account, amount):
        """Перевод на другой счет"""
        # Проверка получателя
        is_valid, error = validate.validate_transfer_target(other_account)
        if not is_valid:
            raise TypeError(error)
        
        # Снимаем с этого счета
        self.withdraw(amount)
        
        try:
            # Кладем на другой счет
            other_account.deposit(amount)
        except Exception as e:
            # Если ошибка, возвращаем деньги
            self._balance += amount
            raise e
    
    # Магические методы
    def __str__(self):
        """Для пользователей (красивое отображение)"""
        return (f"┌─────────────────────────┐\n"
                f"│ СЧЕТ {self._account_number}         │\n"
                f"├─────────────────────────┤\n"
                f"│ Владелец: {self._owner_name:<14} │\n"
                f"│ Баланс: {self._balance:>14.2f} руб. │\n"
                f"│ Ставка: {self._interest_rate*100:>13.1f}%      │\n"
                f"│ Статус: {self._status:<14} │\n"
                f"│ Дней: {self.days_open:>16} │\n"
                f"└─────────────────────────┘")
    
    def __repr__(self):
        """Для разработчиков"""
        return f"BankAccount('{self._owner_name}', {self._balance:.2f}, {self._interest_rate:.2f})"
    
    def __eq__(self, other):
        """Сравнение счетов по номеру"""
        if not isinstance(other, BankAccount):
            return False
        return self._account_number == other._account_number
    
    def __lt__(self, other):
        """Сравнение по балансу (для сортировки)"""
        if not isinstance(other, BankAccount):
            return False
        return self._balance < other._balance