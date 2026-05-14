"""
Демонстрация ЛР-6 - Generics и typing (оценка 5)
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from laba.laba06.container import (
    TypedCollection, BankAccount, SavingsAccount, CreditAccount, PremiumAccount, D, S
)

def print_section(title: str) -> None:
    print(f"\n{'='*60}\n  {title}\n{'='*60}")

def create_accounts():
    accs = [
        BankAccount("Иванов", 50000), SavingsAccount("Петрова", 120000, 0.06, 0.02, 5),
        CreditAccount("Сидоров", 30000, 0.04, 100000, 0.18), PremiumAccount("Кузнецова", 250000, 0.07, 0.025, 10),
        BankAccount("Смирнов", 8000), BankAccount("Новикова", 600000)
    ]
    accs[4].block()
    return accs


# ========== СЦЕНАРИЙ 1: АННОТАЦИИ ТИПОВ ==========
def scenario_1():
    print_section("СЦЕНАРИЙ 1: АННОТАЦИИ ТИПОВ")
    acc = BankAccount("Тест", 100000)
    print(f"  BankAccount(owner: str, balance: float) -> {acc}")
    print("  ✓ Все методы аннотированы типами")


# ========== СЦЕНАРИЙ 2: GENERIC-КОЛЛЕКЦИЯ ==========
def scenario_2():
    print_section("СЦЕНАРИЙ 2: GENERIC-КОЛЛЕКЦИЯ")
    
    # Коллекция строк
    strings: TypedCollection[str] = TypedCollection()
    strings.add("A").add("B").add("C")
    print(f"  TypedCollection[str]: {strings.get_all()}")
    
    # Коллекция чисел
    numbers: TypedCollection[int] = TypedCollection()
    for i in range(1, 4): numbers.add(i)
    print(f"  TypedCollection[int]: {numbers.get_all()}")
    
    # Коллекция BankAccount
    accs = create_accounts()
    bank_coll: TypedCollection[BankAccount] = TypedCollection()
    for acc in accs[:3]: bank_coll.add(acc)
    print(f"  TypedCollection[BankAccount]: {len(bank_coll)} счетов")
    print("  ✓ Типовая безопасность на уровне статического анализа")


# ========== СЦЕНАРИЙ 3: FIND, FILTER, MAP ==========
def scenario_3():
    print_section("СЦЕНАРИЙ 3: FIND, FILTER, MAP")
    
    coll = TypedCollection[BankAccount]()
    for acc in create_accounts(): coll.add(acc)
    
    # find
    found = coll.find(lambda a: a.balance > 100000)
    print(f"  find() -> {found.owner if found else None}")
    
    # filter
    active = coll.filter(lambda a: a.status == "активен")
    print(f"  filter() -> {len(active)} активных счетов")
    
    # map - изменение типа (ключевой момент для оценки 4)
    names = coll.map(lambda a: a.owner)
    balances = coll.map(lambda a: a.balance)
    print(f"  map() -> list[str]: {names[:3]}...")
    print(f"  map() -> list[float]: {balances[:3]}...")
    print("  ✓ map() меняет тип: BankAccount → str и BankAccount → float")


# ========== СЦЕНАРИЙ 4: ПРОТОКОЛ DISPLAYABLE ==========
def scenario_4():
    print_section("СЦЕНАРИЙ 4: ПРОТОКОЛ DISPLAYABLE")
    
    # Коллекция с ограничением Displayable
    coll: TypedCollection[D] = TypedCollection()
    coll.add(BankAccount("Иванов", 50000))
    coll.add(SavingsAccount("Петрова", 120000, 0.06, 0.02, 5))
    coll.add(PremiumAccount("Кузнецова", 250000, 0.07, 0.025, 10))
    
    for acc in coll.get_all():
        print(f"  {acc.display()}")
    print("  ✓ Объекты разных типов имеют display() без явного наследования")


# ========== СЦЕНАРИЙ 5: ПРОТОКОЛ SCORABLE ==========
def scenario_5():
    print_section("СЦЕНАРИЙ 5: ПРОТОКОЛ SCORABLE")
    
    # Коллекция с ограничением Scorable
    coll: TypedCollection[S] = TypedCollection()
    for acc in create_accounts()[:4]: coll.add(acc)
    
    for acc in coll.get_all():
        print(f"  {acc.owner}: score() = {acc.score():.0f}₽")
    print("  ✓ Все счета имеют метод score()")


# ========== ГЛАВНАЯ ==========
def main():
    print("\n" + "="*60)
    print("ЛАБОРАТОРНАЯ РАБОТА №6")
    print("   GENERICS, TYPING, ПРОТОКОЛЫ")
    print("="*60)
    
    scenario_1()
    scenario_2()
    scenario_3()
    scenario_4()
    scenario_5()

if __name__ == "__main__":
    main()