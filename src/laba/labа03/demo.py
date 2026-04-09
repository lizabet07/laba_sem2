"""
Демонстрация ЛР - 3: наследование, полиморфизм, интерфейсы
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from base import BankAccount, AccountCollection
from model import SavingsAccount, CreditAccount, PremiumAccount


def header(text):
    print("\n" + "=" * 60)
    print(f" {text}")
    print("=" * 60)


def scenario1():
    header("СЦЕНАРИЙ 1: НАСЛЕДОВАНИЕ")
    
    print("1. Базовый счёт:")
    base = BankAccount("Иван Петров", 50000, 0.04)
    print(f"   {base}")

    print("\n2. Накопительный счёт:")
    sav = SavingsAccount("Мария Смирнова", 75000, 0.05, 0.015, 3)
    print(f"   {sav}")

    print("\n3. Кредитный счёт:")
    cred = CreditAccount("Пётр Сидоров", 20000, 0.02, 100000, 0.15)
    print(f"   {cred}")

    print("\n4. Премиум счёт:")
    prem = PremiumAccount("Елена VIP", 150000)
    print(f"   {prem}")


def scenario2():
    header("СЦЕНАРИЙ 2: ПОЛИМОРФИЗМ")
    
    coll = AccountCollection()
    
    coll.add(BankAccount("Анна Базовая", 45000, 0.04))
    coll.add(SavingsAccount("Борис Сберегатель", 120000, 0.05, 0.02, 5))
    coll.add(CreditAccount("Виктор Кредитов", 15000, 0.02, 80000, 0.16))
    coll.add(SavingsAccount("Галина Накопитель", 35000, 0.045, 0.01, 3))
    
    dmitry = CreditAccount("Дмитрий Заемщик", 5000, 0.01, 50000, 0.18)
    coll.add(dmitry)
    dmitry.withdraw(10000)
    
    coll.add(PremiumAccount("Елена Премиум", 200000))

    print("Коллекция:")
    for a in coll:
        print(f"  {a}")

    print("\n1. Типы через isinstance():")
    for a in coll:
        if isinstance(a, PremiumAccount):
            t = "Премиум"
        elif isinstance(a, SavingsAccount):
            t = "Накопительный"
        elif isinstance(a, CreditAccount):
            t = "Кредитный"
        else:
            t = "Базовый"
        print(f"   {a.owner}: {t}")

    print("\n2. Полиморфные проценты:")
    for a in coll:
        print(f"   {a.owner}: {a.calculate_interest():.2f} руб.")


def scenario3():
    header("СЦЕНАРИЙ 3: ОБЩИЙ ИНТЕРФЕЙС")
    
    coll = AccountCollection()
    coll.add(SavingsAccount("Сергей Сберегов", 80000, 0.05, 0.015, 5))
    coll.add(CreditAccount("Кирилл Кредитов", 30000, 0.02, 100000, 0.14))
    coll.add(PremiumAccount("Виктор Важный", 250000))
    coll.add(BankAccount("Борис Базовый", 40000, 0.04))

    print("1. process_monthly() для всех:")
    for r in coll.process_all():
        if "error" in r:
            print(f"   ✗ {r['error']}")
        else:
            print(f"   ✓ {r['account']}: +{r.get('interest', 0):.2f} руб.")

    print("\n2. Фильтрация по типу:")
    print(f"   Накопительных: {len(coll.get_by_type(SavingsAccount))}")
    print(f"   Кредитных: {len(coll.get_by_type(CreditAccount))}")
    print(f"   Премиум: {len(coll.get_by_type(PremiumAccount))}")


def main():
    print("=" * 60)
    print(" ЛР-3: НАСЛЕДОВАНИЕ И ПОЛИМОРФИЗМ")
    print("=" * 60)
    
    scenario1()
    input("\n>>> Enter...")
    scenario2()
    input("\n>>> Enter...")
    scenario3()
    print("\nГОТОВО!")


if __name__ == "__main__":
    main()