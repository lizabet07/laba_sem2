from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from . import validate
from .validate import ValidationError

# ========== Перечисления ==========
class AccountStatus(Enum): 
    ACTIVE = "активен"
    BLOCKED = "заблокирован"
    CLOSED = "закрыт"
    FROZEN = "заморожен"

class TransactionType(Enum): 
    DEPOSIT = "пополнение"
    WITHDRAWAL = "снятие"
    TRANSFER = "перевод"
    PAYMENT = "платеж"
    INTEREST = "начисление %"

class TransactionStatus(Enum): 
    PENDING = "ожидает"
    COMPLETED = "выполнена"
    FAILED = "ошибка"
    CANCELLED = "отменена"

class CreditStatus(Enum): 
    ACTIVE = "активен"
    APPROVED = "одобрен"
    PAID = "погашен"
    OVERDUE = "просрочен"
    REJECTED = "отказано"

class DepositStatus(Enum): 
    ACTIVE = "активен"
    CLOSED = "закрыт"
    PROLONGED = "продлен"


class Client:
    """Клиент банка"""
    _next_id = 1000
    
    def __init__(self, full_name: str, passport: str, phone: str, email: str):
        self._full_name = validate.validate_full_name(full_name)
        self._passport = validate.validate_passport(passport)
        self._phone = validate.validate_phone(phone)
        self._email = validate.validate_email(email)
        self._client_id = f"CL{Client._next_id:06d}"
        Client._next_id += 1
        self._registration_date = datetime.now()
        self._accounts = []
        self._credits = []
        self._deposits = []
        self._is_active = True
    
    @property
    def client_id(self): 
        return self._client_id
    
    @property
    def full_name(self): 
        return self._full_name
    
    @full_name.setter
    def full_name(self, v): 
        self._full_name = validate.validate_full_name(v)
    
    @property
    def accounts(self): 
        return self._accounts.copy()
    
    @property
    def total_balance(self): 
        return sum(a.balance for a in self._accounts)
    
    def add_account(self, acc): 
        self._accounts.append(acc)
    
    def add_credit(self, cr): 
        self._credits.append(cr)
    
    def add_deposit(self, dp): 
        self._deposits.append(dp)
    
    def __str__(self):
        return f"Клиент: {self._full_name}\nID: {self._client_id}\nБаланс: {self.total_balance:,.2f} ₽"
    
    def __repr__(self): 
        return f"Client('{self._full_name}')"
    
    def __eq__(self, other): 
        return isinstance(other, Client) and self._client_id == other._client_id


class BankAccount:
    """Банковский счет"""
    _next_num = 1000
    MIN_BALANCE = 0.0
    MAX_BALANCE = 1_000_000_000.0
    BANK_NAME = "Python Bank"
    
    def __init__(self, client: Client, balance: float = 0.0, rate: float = 0.01, currency: str = "RUB"):
        validate.validate_not_null(client, "client")
        self._client = client
        self._account_number = f"ACC{BankAccount._next_num:06d}"
        BankAccount._next_num += 1
        self._balance = validate.validate_balance(balance, self.MIN_BALANCE, self.MAX_BALANCE)
        self._interest_rate = validate.validate_interest_rate(rate)
        self._currency = currency
        self._status = AccountStatus.ACTIVE
        self._opening_date = datetime.now()
        self._transactions = []
        client.add_account(self)
    
    @property
    def account_number(self): 
        return self._account_number
    
    @property
    def balance(self): 
        return self._balance
    
    @property
    def interest_rate(self): 
        return self._interest_rate
    
    @interest_rate.setter
    def interest_rate(self, v): 
        self._interest_rate = validate.validate_interest_rate(v)
    
    @property
    def status(self): 
        return self._status
    
    def _check_status(self, op: str):
        if self._status == AccountStatus.CLOSED:
            raise PermissionError(f"Невозможно {op}: счет закрыт")
        if self._status == AccountStatus.BLOCKED:
            raise PermissionError(f"Невозможно {op}: счет заблокирован")
        if self._status == AccountStatus.FROZEN:
            raise PermissionError(f"Невозможно {op}: счет заморожен")
    
    def deposit(self, amount: float, desc: str = "Пополнение"):
        self._check_status("внесение")
        amount = validate.validate_amount(amount)
        self._balance = validate.validate_balance(self._balance + amount, self.MIN_BALANCE, self.MAX_BALANCE)
        return self._add_transaction(None, self, amount, TransactionType.DEPOSIT, desc)
    
    def withdraw(self, amount: float, desc: str = "Снятие"):
        self._check_status("снятие")
        amount = validate.validate_amount(amount)
        if amount > self._balance:
            raise ValidationError(f"Недостаточно средств. Доступно: {self._balance:.2f}")
        self._balance = validate.validate_balance(self._balance - amount, self.MIN_BALANCE, self.MAX_BALANCE)
        return self._add_transaction(self, None, amount, TransactionType.WITHDRAWAL, desc)
    
    def transfer_to(self, target, amount: float, desc: str = "Перевод"):
        self._check_status("перевод")
        target._check_status("получение")
        amount = validate.validate_amount(amount)
        if amount > self._balance:
            raise ValidationError(f"Недостаточно средств. Доступно: {self._balance:.2f}")
        
        self._balance -= amount
        target._balance += amount
        t = Transaction(self, target, amount, TransactionType.TRANSFER, desc)
        t._status = TransactionStatus.COMPLETED
        self._transactions.append(t)
        target._transactions.append(t)
        return t
    
    def _add_transaction(self, frm, to, amt, typ, desc):
        t = Transaction(frm, to, amt, typ, desc)
        t._status = TransactionStatus.COMPLETED
        self._transactions.append(t)
        return t
    
    def calculate_interest(self): 
        if self._status == AccountStatus.CLOSED:
            return 0.0
        return self._balance * self._interest_rate / 12
    
    def apply_interest(self):
        interest = self.calculate_interest()
        if interest <= 0: 
            return None
        self._balance += interest
        return self._add_transaction(None, self, interest, TransactionType.INTEREST, "Начисление %")
    
    def block(self): 
        self._status = AccountStatus.BLOCKED
    
    def activate(self): 
        self._status = AccountStatus.ACTIVE
    
    def freeze(self): 
        self._status = AccountStatus.FROZEN
    
    def close(self):
        if self._balance != 0: 
            raise ValidationError("Нельзя закрыть счет с ненулевым балансом")
        self._status = AccountStatus.CLOSED
    
    def __str__(self): 
        return f"Счет: {self._account_number}\nБаланс: {self._balance:,.2f} {self._currency}\nСтатус: {self._status.value}"
    
    def __repr__(self): 
        return f"BankAccount({self._account_number}, {self._balance})"
    
    def __eq__(self, other): 
        return isinstance(other, BankAccount) and self._account_number == other._account_number


class Transaction:
    """Банковская транзакция"""
    _next_id = 1000
    
    def __init__(self, frm, to, amt: float, typ: TransactionType, desc: str = ""):
        self._transaction_id = f"TR{Transaction._next_id:06d}"
        Transaction._next_id += 1
        self._from_account = frm
        self._to_account = to
        self._amount = validate.validate_amount(amt)
        self._transaction_type = typ
        self._description = desc
        self._status = TransactionStatus.PENDING
        self._timestamp = datetime.now()
        self._error = None
    
    @property
    def transaction_id(self): 
        return self._transaction_id
    
    @property
    def amount(self): 
        return self._amount
    
    @property
    def status(self): 
        return self._status
    
    def execute(self):
        try:
            self._status = TransactionStatus.COMPLETED
            return True
        except Exception as e:
            self._status = TransactionStatus.FAILED
            self._error = str(e)
            return False
    
    def cancel(self):
        if self._status == TransactionStatus.COMPLETED:
            raise PermissionError("Нельзя отменить выполненную транзакцию")
        self._status = TransactionStatus.CANCELLED
    
    def __str__(self):
        if self._from_account and self._to_account:
            dir = f"{self._from_account.account_number} → {self._to_account.account_number}"
        elif self._from_account:
            dir = f"Снятие с {self._from_account.account_number}"
        else:
            dir = f"Пополнение {self._to_account.account_number}"
        
        return f"Транзакция {self._transaction_id}\n{dir}\nСумма: {self._amount:,.2f}\nСтатус: {self._status.value}"
    
    def __repr__(self): 
        return f"Transaction({self._transaction_id}, {self._amount})"
    
    def __eq__(self, other): 
        return isinstance(other, Transaction) and self._transaction_id == other._transaction_id


class Credit:
    """Кредит"""
    _next_id = 1000
    MIN_AMOUNT = 1000.0
    MAX_AMOUNT = 5_000_000.0
    MIN_TERM = 1
    MAX_TERM = 60
    
    def __init__(self, client: Client, amount: float, rate: float, term: int, purpose: str = ""):
        validate.validate_not_null(client, "client")
        self._client = client
        self._credit_id = f"CR{Credit._next_id:06d}"
        Credit._next_id += 1
        self._amount = validate.validate_credit_amount(amount, self.MIN_AMOUNT, self.MAX_AMOUNT)
        self._interest_rate = validate.validate_interest_rate(rate)
        self._term_months = validate.validate_credit_term(term, self.MIN_TERM, self.MAX_TERM)
        self._purpose = purpose
        self._status = CreditStatus.APPROVED
        self._issue_date = datetime.now()
        self._remaining = amount
        self._paid = 0.0
        client.add_credit(self)
    
    @property
    def remaining(self): 
        return self._remaining
    
    def monthly_payment(self):
        if self._term_months == 0: 
            return self._amount
        mr = self._interest_rate / 12
        if mr == 0: 
            return self._amount / self._term_months
        return round((self._amount * mr * (1 + mr) ** self._term_months) / ((1 + mr) ** self._term_months - 1), 2)
    
    def total_payment(self): 
        return round(self.monthly_payment() * self._term_months, 2)
    
    def overpayment(self): 
        return round(self.total_payment() - self._amount, 2)
    
    def make_payment(self, amount: float):
        if self._status == CreditStatus.PAID:
            raise ValidationError("Кредит уже полностью погашен")
        if self._status == CreditStatus.REJECTED:
            raise ValidationError("Кредит отклонен")
        
        amount = validate.validate_amount(amount)
        if amount > self._remaining:
            amount = self._remaining
        
        self._remaining -= amount
        self._paid += amount
        
        if self._remaining <= 0:
            self._status = CreditStatus.PAID
        
        return self._remaining
    
    def approve(self): 
        self._status = CreditStatus.APPROVED
    
    def reject(self): 
        self._status = CreditStatus.REJECTED
    
    def __str__(self): 
        return f"Кредит: {self._credit_id}\nСумма: {self._amount:,.2f}\nОстаток: {self._remaining:,.2f}\nПлатеж: {self.monthly_payment():,.2f}"
    
    def __repr__(self): 
        return f"Credit({self._credit_id}, {self._amount})"
    
    def __eq__(self, other): 
        return isinstance(other, Credit) and self._credit_id == other._credit_id


class Deposit:
    """Вклад"""
    _next_id = 1000
    MIN_AMOUNT = 1000.0
    MAX_AMOUNT = 10_000_000.0
    MIN_TERM = 1
    MAX_TERM = 60
    
    def __init__(self, client: Client, amount: float, rate: float, term: int, capitalization: bool = False):
        validate.validate_not_null(client, "client")
        self._client = client
        self._deposit_id = f"DP{Deposit._next_id:06d}"
        Deposit._next_id += 1
        self._amount = validate.validate_deposit_amount(amount, self.MIN_AMOUNT, self.MAX_AMOUNT)
        self._interest_rate = validate.validate_interest_rate(rate)
        self._term_months = validate.validate_deposit_term(term, self.MIN_TERM, self.MAX_TERM)
        self._capitalization = validate.validate_capitalization(capitalization)
        self._status = DepositStatus.ACTIVE
        self._opening_date = datetime.now()
        self._current = amount
        self._closing_date = None
        client.add_deposit(self)
    
    @property
    def current(self): 
        return self._current
    
    def calculate_income(self):
        if self._capitalization:
            return round(self._amount * (1 + self._interest_rate / 12) ** self._term_months - self._amount, 2)
        return round(self._amount * self._interest_rate * self._term_months / 12, 2)
    
    def total_at_maturity(self): 
        return round(self._amount + self.calculate_income(), 2)
    
    def apply_monthly_interest(self):
        if not self._capitalization or self._status != DepositStatus.ACTIVE:
            return 0.0
        interest = self._current * self._interest_rate / 12
        self._current += interest
        return round(interest, 2)
    
    def close(self):
        if self._status == DepositStatus.CLOSED:
            raise ValidationError("Вклад уже закрыт")
        self._status = DepositStatus.CLOSED
        self._closing_date = datetime.now()
        
        months_passed = (datetime.now() - self._opening_date).days // 30
        if months_passed < self._term_months:
            return self._amount
        return self._current
    
    def prolong(self, months: int):
        if self._status == DepositStatus.CLOSED:
            raise ValidationError("Нельзя продлить закрытый вклад")
        self._term_months += months
        self._status = DepositStatus.PROLONGED
    
    def __str__(self):
        return f"Вклад: {self._deposit_id}\nСумма: {self._amount:,.2f}\nДоход: {self.calculate_income():,.2f}\nИтого: {self.total_at_maturity():,.2f}"
    
    def __repr__(self): 
        return f"Deposit({self._deposit_id}, {self._amount})"
    
    def __eq__(self, other): 
        return isinstance(other, Deposit) and self._deposit_id == other._deposit_id