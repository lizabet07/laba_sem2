class BankAccount:
    def __init__(self, owner, balance):
        if not owner or not isinstance(owner, str):
            raise ValueError("Владелец должен быть непустой строкой")
        if balance < 0:
            raise ValueError("Баланс не может быть отрицательным")
        
        self.__owner = owner
        self.__balance = float(balance)
    
    @property
    def owner(self):
        return self.__owner
    
    @property
    def balance(self):
        return self.__balance
    
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть больше 0")
        self.__balance += amount
    
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть больше 0")
        if amount > self.__balance:
            raise ValueError("Недостаточно средств")
        self.__balance -= amount
    
    def __str__(self):
        return f"Счёт: {self.__owner}, баланс {self.__balance} руб."


class SavingsAccount(BankAccount):
    def __init__(self, owner, balance, interest_rate):
        super().__init__(owner, balance)
        if not 0 <= interest_rate <= 1:
            raise ValueError("Ставка должна быть от 0 до 1")
        self.__interest_rate = interest_rate
    
    @property
    def interest_rate(self):
        return self.__interest_rate
    
    def apply_interest(self):
        self._BankAccount__balance += self._BankAccount__balance * self.__interest_rate
    
    def __str__(self):
        return f"{super().__str__()} (сбер., ставка {self.__interest_rate * 100}%)"


class CheckingAccount(BankAccount):
    def __init__(self, owner, balance, overdraft_limit):
        super().__init__(owner, balance)
        if overdraft_limit < 0:
            raise ValueError("Лимит овердрафта не может быть отрицательным")
        self.__overdraft_limit = overdraft_limit
    
    @property
    def overdraft_limit(self):
        return self.__overdraft_limit
    
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть больше 0")
        if amount > self.balance + self.__overdraft_limit:
            raise ValueError("Превышен лимит овердрафта")
        self._BankAccount__balance -= amount
    
    def __str__(self):
        return f"{super().__str__()} (расч., лимит {self.__overdraft_limit})"

print("=== SavingsAccount ===")
sav = SavingsAccount('Иванов И.И.', 10000, 0.1)
sav.apply_interest()
print(sav.balance)   # 11000.0
print(sav)           

print("\n=== CheckingAccount ===")
chk = CheckingAccount('Петров П.П.', 1000, 5000)
chk.withdraw(4000)
print(chk.balance)   # -3000.0

print("\n=== Проверка ошибки (овердрафт) ===")
try:
    chk.withdraw(5000)
except ValueError as e:
    print("ValueError:", e)