#!/usr/bin/env python3
"""
Консольное приложение "Банковская система" (автономная версия)
"""

import os
import json
from typing import List, Optional, Callable, Any
from datetime import datetime

# ========== КЛАССЫ ИЗ ЛР-1 ==========

class BankAccount:
    """Банковский счёт (базовый класс)"""
    _next_account_number = 1000
    
    def __init__(self, owner: str, balance: float = 0.0, rate: float = 0.05) -> None:
        self._owner: str = owner
        self._balance: float = balance
        self._rate: float = rate
        self._status: str = "активен"
        self._account_number: int = BankAccount._next_account_number
        BankAccount._next_account_number += 1
    
    @property
    def owner(self) -> str:
        return self._owner
    
    @property
    def balance(self) -> float:
        return self._balance
    
    @property
    def rate(self) -> float:
        return self._rate
    
    @property
    def status(self) -> str:
        return self._status
    
    @property
    def account_number(self) -> int:
        return self._account_number
    
    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        self._balance += amount
        return self._balance
    
    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        if amount > self._balance:
            raise ValueError("Недостаточно средств")
        self._balance -= amount
        return self._balance
    
    def block(self) -> None:
        if self._status != "закрыт":
            self._status = "заблокирован"
    
    def close(self) -> None:
        if self._balance != 0:
            raise ValueError(f"Нельзя закрыть счёт с балансом {self._balance:.2f}")
        self._status = "закрыт"
    
    def get_type(self) -> str:
        return "Обычный"
    
    def __str__(self) -> str:
        return f"{self._owner}: {self._balance:.2f}₽ [{self._status}]"


class SavingsAccount(BankAccount):
    def __init__(self, owner: str, balance: float = 0.0, rate: float = 0.06, 
                 bonus_rate: float = 0.02, min_term: int = 3) -> None:
        super().__init__(owner, balance, rate)
        self._bonus_rate = bonus_rate
    
    def get_type(self) -> str:
        return "Накопительный"


class CreditAccount(BankAccount):
    def __init__(self, owner: str, balance: float = 0.0, rate: float = 0.04,
                 credit_limit: float = 50000, interest_rate: float = 0.18) -> None:
        super().__init__(owner, balance, rate)
        self._credit_limit = credit_limit
    
    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        if amount > self._balance + self._credit_limit:
            raise ValueError("Превышен кредитный лимит")
        self._balance -= amount
        return self._balance
    
    def get_type(self) -> str:
        return "Кредитный"


class PremiumAccount(BankAccount):
    def __init__(self, owner: str, balance: float = 0.0, rate: float = 0.07,
                 cashback_rate: float = 0.025, service_level: int = 1) -> None:
        super().__init__(owner, balance, rate)
        self._cashback_rate = cashback_rate
    
    def get_type(self) -> str:
        return "Премиум"


# ========== КОЛЛЕКЦИЯ ==========

class BankAccountCollection:
    def __init__(self, items=None):
        self._items = list(items) if items else []
    
    def add(self, item):
        if not isinstance(item, BankAccount):
            raise TypeError("Можно добавлять только объекты BankAccount")
        self._items.append(item)
        return self
    
    def remove(self, item):
        self._items.remove(item)
        return self
    
    def get_all(self):
        return self._items.copy()
    
    def __len__(self):
        return len(self._items)
    
    def __getitem__(self, index):
        return self._items[index]
    
    def __iter__(self):
        return iter(self._items)


# ========== ИСКЛЮЧЕНИЯ ==========

class AccountNotFoundError(Exception):
    pass

class DuplicateAccountError(Exception):
    pass


# ========== ПРИЛОЖЕНИЕ ==========

class BankApp:
    def __init__(self) -> None:
        self._collection: BankAccountCollection = BankAccountCollection()
    
    @property
    def collection(self) -> BankAccountCollection:
        return self._collection
    
    def add_account(self, account_type: str, **kwargs) -> BankAccount:
        for acc in self._collection.get_all():
            if acc.owner == kwargs.get("owner"):
                raise DuplicateAccountError(f"Счёт для {kwargs.get('owner')} уже существует!")
        
        if account_type == "1":
            account = BankAccount(kwargs["owner"], kwargs["balance"], kwargs.get("rate", 0.05))
        elif account_type == "2":
            account = SavingsAccount(kwargs["owner"], kwargs["balance"], kwargs.get("rate", 0.06))
        elif account_type == "3":
            account = CreditAccount(kwargs["owner"], kwargs["balance"], kwargs.get("rate", 0.04))
        elif account_type == "4":
            account = PremiumAccount(kwargs["owner"], kwargs["balance"], kwargs.get("rate", 0.07))
        else:
            raise ValueError("Неизвестный тип счёта")
        
        self._collection.add(account)
        return account
    
    def remove_account(self, owner: str) -> BankAccount:
        for acc in self._collection.get_all():
            if acc.owner.lower() == owner.lower():
                self._collection.remove(acc)
                return acc
        raise AccountNotFoundError(f"Счёт для {owner} не найден!")
    
    def find_account(self, owner: str) -> Optional[BankAccount]:
        for acc in self._collection.get_all():
            if acc.owner.lower() == owner.lower():
                return acc
        return None
    
    def get_all_accounts(self) -> List[BankAccount]:
        return self._collection.get_all()
    
    def deposit(self, owner: str, amount: float) -> BankAccount:
        account = self.find_account(owner)
        if not account:
            raise AccountNotFoundError(f"Счёт для {owner} не найден!")
        account.deposit(amount)
        return account
    
    def withdraw(self, owner: str, amount: float) -> BankAccount:
        account = self.find_account(owner)
        if not account:
            raise AccountNotFoundError(f"Счёт для {owner} не найден!")
        account.withdraw(amount)
        return account
    
    def block_account(self, owner: str) -> BankAccount:
        account = self.find_account(owner)
        if not account:
            raise AccountNotFoundError(f"Счёт для {owner} не найден!")
        account.block()
        return account
    
    def sort_by_balance(self, reverse: bool = False) -> List[BankAccount]:
        items = self._collection.get_all()
        items.sort(key=lambda a: a.balance, reverse=reverse)
        return items


# ========== СОХРАНЕНИЕ ==========

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'accounts.json')

def save_collection(collection, filepath: str) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    data = []
    for acc in collection.get_all():
        data.append({
            "type": acc.get_type(),
            "owner": acc.owner,
            "balance": acc.balance,
            "rate": acc.rate,
            "status": acc.status,
            "account_number": acc.account_number
        })
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_collection(collection, filepath: str) -> int:
    if not os.path.exists(filepath):
        return 0
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for item in data:
        acc_type = item.get("type", "Обычный")
        if acc_type == "Накопительный":
            acc = SavingsAccount(item["owner"], item["balance"], item["rate"])
        elif acc_type == "Кредитный":
            acc = CreditAccount(item["owner"], item["balance"], item["rate"])
        elif acc_type == "Премиум":
            acc = PremiumAccount(item["owner"], item["balance"], item["rate"])
        else:
            acc = BankAccount(item["owner"], item["balance"], item["rate"])
        if item.get("status") == "заблокирован":
            acc.block()
        elif item.get("status") == "закрыт":
            acc.close()
        collection.add(acc)
    return len(data)


# ========== CLI ==========

def print_table(accounts: list, title: str = "Счета") -> None:
    if not accounts:
        print(f"\n{title}: нет счетов")
        return
    print(f"\n{title}:")
    print("-" * 65)
    print(f"{'Владелец':<20} {'Баланс':>12} {'Ставка':>8} {'Статус':<12} {'Тип':<12}")
    print("-" * 65)
    for acc in accounts:
        print(f"{acc.owner:<20} {acc.balance:>12.2f}₽ {acc.rate*100:>7.1f}% {acc.status:<12} {acc.get_type():<12}")
    print("-" * 65)
    print(f"Всего: {len(accounts)} счетов")

def print_account(account) -> None:
    print(f"\n  Номер: {account.account_number}")
    print(f"  Владелец: {account.owner}")
    print(f"  Баланс: {account.balance:.2f}₽")
    print(f"  Ставка: {account.rate*100:.1f}%")
    print(f"  Статус: {account.status}")
    print(f"  Тип: {account.get_type()}")

def get_float(prompt: str, min_val: float = None) -> float:
    while True:
        try:
            val = float(input(prompt))
            if min_val is not None and val < min_val:
                print(f"Ошибка: не может быть меньше {min_val}")
                continue
            return val
        except ValueError:
            print("Ошибка: введите число")

def confirm(prompt: str) -> bool:
    return input(prompt + " (y/n): ").lower() in ('y', 'да')


# ========== ГЛАВНАЯ ==========

def main():
    print("\n" + "=" * 50)
    print("  БАНКОВСКАЯ СИСТЕМА")
    print("=" * 50)
    
    app = BankApp()
    
    try:
        loaded = load_collection(app.collection, DATA_FILE)
        print(f"✓ Загружено {loaded} счетов")
    except Exception as e:
        print(f"⚠ Ошибка загрузки: {e}")
    
    while True:
        print("\n" + "-" * 40)
        print("1. Добавить счёт")
        print("2. Показать все счета")
        print("3. Найти счёт")
        print("4. Удалить счёт")
        print("5. Пополнить счёт")
        print("6. Снять со счёта")
        print("7. Заблокировать счёт")
        print("8. Сортировка по балансу")
        print("0. Выход")
        
        choice = input("\nВыберите действие: ").strip()
        
        if choice == "0":
            save_collection(app.collection, DATA_FILE)
            print("\n✓ Данные сохранены")
            print("До свидания!")
            break
        
        elif choice == "1":
            print("\n--- ДОБАВЛЕНИЕ СЧЁТА ---")
            print("Типы: 1-Обычный, 2-Накопительный, 3-Кредитный, 4-Премиум")
            acc_type = input("Выберите тип (1-4): ").strip()
            if acc_type not in ["1","2","3","4"]:
                print("❌ Неверный тип")
                continue
            owner = input("Имя владельца: ")
            balance = get_float("Начальный баланс: ", 0)
            rate = get_float("Процентная ставка (%): ", 0) / 100
            try:
                acc = app.add_account(acc_type, owner=owner, balance=balance, rate=rate)
                print(f"\n✓ Счёт для {owner} создан!")
                print_account(acc)
            except DuplicateAccountError as e:
                print(f"\n❌ {e}")
        
        elif choice == "2":
            print_table(app.get_all_accounts(), "ВСЕ СЧЕТА")
        
        elif choice == "3":
            print("\n--- ПОИСК СЧЁТА ---")
            owner = input("Имя владельца: ")
            acc = app.find_account(owner)
            if acc:
                print_account(acc)
            else:
                print(f"\n❌ Счёт для {owner} не найден")
        
        elif choice == "4":
            print("\n--- УДАЛЕНИЕ СЧЁТА ---")
            owner = input("Имя владельца: ")
            acc = app.find_account(owner)
            if not acc:
                print(f"\n❌ Счёт не найден")
                continue
            print_account(acc)
            if confirm(f"\nУдалить счёт {owner}?"):
                app.remove_account(owner)
                print(f"\n✓ Счёт {owner} удалён")
        
        elif choice == "5":
            print("\n--- ПОПОЛНЕНИЕ СЧЁТА ---")
            owner = input("Имя владельца: ")
            amount = get_float("Сумма: ", 0.01)
            try:
                acc = app.deposit(owner, amount)
                print(f"\n✓ Счёт {owner} пополнен на {amount:.2f}₽")
                print_account(acc)
            except AccountNotFoundError as e:
                print(f"\n❌ {e}")
        
        elif choice == "6":
            print("\n--- СНЯТИЕ СО СЧЁТА ---")
            owner = input("Имя владельца: ")
            amount = get_float("Сумма: ", 0.01)
            try:
                acc = app.withdraw(owner, amount)
                print(f"\n✓ Со счёта {owner} снято {amount:.2f}₽")
                print_account(acc)
            except (AccountNotFoundError, ValueError) as e:
                print(f"\n❌ {e}")
        
        elif choice == "7":
            print("\n--- БЛОКИРОВКА СЧЁТА ---")
            owner = input("Имя владельца: ")
            try:
                acc = app.block_account(owner)
                print(f"\n✓ Счёт {owner} заблокирован")
                print_account(acc)
            except AccountNotFoundError as e:
                print(f"\n❌ {e}")
        
        elif choice == "8":
            print("\n--- СОРТИРОВКА ПО БАЛАНСУ ---")
            order = input("По возрастанию (1) или убыванию (2)? ")
            reverse = (order == "2")
            sorted_accs = app.sort_by_balance(reverse)
            print_table(sorted_accs, "ОТСОРТИРОВАННЫЕ СЧЕТА")
        
        else:
            print("\n❌ Неверный пункт!")

if __name__ == "__main__":
    main()