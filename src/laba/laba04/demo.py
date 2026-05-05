"""
Демонстрация ЛР-4
"""

import sys
import os

# ========== НАСТРОЙКА ПУТЕЙ ==========
sys.path.insert(0, r"C:\Users\HONOR\laba_prog\laba_sem2\src\laba\laba04")
sys.path.insert(0, r"C:\Users\HONOR\laba_prog\laba_sem2\src\laba\labа03")
sys.path.insert(0, r"C:\Users\HONOR\laba_prog\laba_sem2")

# Импорт классов и интерфейсов
from models import BankAccount, SavingsAccount, CreditAccount, PremiumAccount, AccountCollection
from interfaces import Printable, Comparable


def header(text):
    """Вывод красивого заголовка"""
    print("\n" + "=" * 60)
    print(f" {text}")
    print("=" * 60)


# ========== СЦЕНАРИЙ 1: ПРОВЕРКА ИНТЕРФЕЙСОВ ==========
def scenario1():
    header("СЦЕНАРИЙ 1: ПРОВЕРКА ИНТЕРФЕЙСОВ")
    
    # Создаём объекты разных классов
    acc1 = BankAccount("Иван Петров", 50000, 0.04)
    acc2 = SavingsAccount("Мария Смирнова", 75000, 0.05, 0.015, 3)
    acc3 = CreditAccount("Пётр Сидоров", -5000, 0.02, 100000, 0.15)
    acc4 = PremiumAccount("Елена Иванова", 300000)
    
    # 1. Проверяем, что все классы реализуют интерфейсы
    print("1. Проверка isinstance:")
    accounts = [acc1, acc2, acc3, acc4]
    for acc in accounts:
        interfaces = []
        if isinstance(acc, Printable):
            interfaces.append("Printable")
        if isinstance(acc, Comparable):
            interfaces.append("Comparable")
        print(f"   {acc.owner}: {', '.join(interfaces)}")
    
    # 2. Вызываем to_string() у всех - у каждого свой вывод
    print("\n2. Вызов to_string():")
    for acc in accounts:
        print(f"   {acc.to_string()}")
    
    # 3. Сравниваем объекты через compare_to()
    print("\n3. Сравнение через compare_to():")
    print(f"   Иван vs Мария: {acc1.compare_to(acc2)} (50000 < 75000)")
    print(f"   Мария vs Пётр: {acc2.compare_to(acc3)} (75000 > -5000)")


# ========== СЦЕНАРИЙ 2: ИНТЕРФЕЙС КАК ТИП ==========
def scenario2():
    header("СЦЕНАРИЙ 2: ИНТЕРФЕЙС КАК ТИП")
    
    # Создаём коллекцию и добавляем счета
    coll = AccountCollection()
    coll.add(BankAccount("Анна Базовая", 45000, 0.04))
    coll.add(SavingsAccount("Борис Сберегатель", 120000, 0.05, 0.02, 5))
    coll.add(CreditAccount("Виктор Кредитов", 15000, 0.02, 80000, 0.16))
    coll.add(PremiumAccount("Галина Премиум", 250000))
    
    # Универсальная функция - работает с любыми Printable
    def print_all(items: list):
        for item in items:
            print(f"   {item.to_string()}")
    
    # Универсальная функция - работает с любыми Comparable
    def find_max(items: list):
        if not items:
            return None
        max_item = items[0]
        for item in items[1:]:
            if item.compare_to(max_item) > 0:
                max_item = item
        return max_item
    
    # 1. Вывод всех через интерфейс Printable
    print("1. Вывод через Printable:")
    print_all(coll.get_printable())
    
    # 2. Поиск максимума через интерфейс Comparable
    print("\n2. Поиск максимума через Comparable:")
    best = find_max(coll.get_comparable())
    print(f"   Лучший: {best.to_string()}")


# ========== СЦЕНАРИЙ 3: ПОЛИМОРФИЗМ ==========
def scenario3():
    header("СЦЕНАРИЙ 3: ПОЛИМОРФИЗМ")
    
    # Создаём коллекцию с разными счетами
    coll = AccountCollection()
    coll.add(BankAccount("Иван Тестов", 50000, 0.04))
    coll.add(SavingsAccount("Петр Тестов", 100000, 0.05, 0.02, 5))
    coll.add(PremiumAccount("Ольга Тестова", 500000))
    coll.add(CreditAccount("Анна Тестова", -10000, 0.02, 50000, 0.18))
    
    # 1. Исходный порядок
    print("1. Исходная коллекция:")
    coll.print_all()
    
    # 2. Сортировка по возрастанию (без isinstance!)
    print("\n2. Сортировка через Comparable (по возрастанию):")
    coll.sort_using_comparable(reverse=False)
    coll.print_all()
    
    # 3. Сортировка по убыванию
    print("\n3. Сортировка через Comparable (по убыванию):")
    coll.sort_using_comparable(reverse=True)
    coll.print_all()
    
    # 4. Демонстрация полиморфизма - один метод, разный результат
    print("\n4. Полиморфизм - один метод, разное поведение:")
    for acc in coll:
        print(f"   {acc.to_string()}")


# ========== СЦЕНАРИЙ 4: ИНТЕГРАЦИЯ С ЛР-2 ==========
def scenario4():
    header("СЦЕНАРИЙ 4: ИНТЕГРАЦИЯ С ЛР-2")
    
    # Создаём коллекцию
    coll = AccountCollection()
    coll.add(BankAccount("Олег Петров", 60000, 0.04))
    coll.add(SavingsAccount("Светлана Иванова", 150000, 0.055, 0.015, 4))
    coll.add(CreditAccount("Игорь Смирнов", 25000, 0.02, 120000, 0.17))
    coll.add(PremiumAccount("Наталья Королева", 400000))
    coll.add(SavingsAccount("Павел Сидоров", 45000, 0.04, 0.01, 3))
    
    # 1. Фильтрация по интерфейсам (новые методы)
    print("1. Фильтрация по интерфейсам:")
    printables = coll.get_printable()
    comparables = coll.get_comparable()
    print(f"   Printable объектов: {len(printables)}")
    print(f"   Comparable объектов: {len(comparables)}")
    
    # 2. Вывод через интерфейс
    print("\n2. Вывод всех Printable объектов:")
    coll.print_all()
    
    # 3. Использование старых методов из ЛР-2
    print("\n3. Методы из ЛР-2:")
    print(f"   Всего счетов: {len(coll)}")
    print(f"   Накопительных: {len(coll.get_by_type(SavingsAccount))}")
    print(f"   Кредитных: {len(coll.get_by_type(CreditAccount))}")
    print(f"   Премиум: {len(coll.get_by_type(PremiumAccount))}")
    
    # 4. Подсчёт комиссий (метод из ЛР-2)
    print("\n4. Общая сумма комиссий (метод из ЛР-2):")
    print(f"   Сумма: {coll.total_fees():.2f}₽")
    
    # 5. Обработка всех счетов (метод из ЛР-2)
    print("\n5. Обработка всех счетов (process_monthly из ЛР-2):")
    results = coll.process_all()
    for r in results:
        if "error" not in r:
            print(f"   {r['account']}: +{r.get('interest', 0):.2f}₽")


# ========== СЦЕНАРИЙ 5: АРХИТЕКТУРНОЕ ПОВЕДЕНИЕ ==========
def scenario5():
    header("СЦЕНАРИЙ 5: АРХИТЕКТУРНОЕ ПОВЕДЕНИЕ")
    
    # Создаём коллекцию
    coll = AccountCollection()
    coll.add(BankAccount("Алексей Попов", 10000, 0.03))
    coll.add(SavingsAccount("Марина Волкова", 80000, 0.045, 0.01, 3))
    coll.add(PremiumAccount("Виктор Морозов", 600000))
    coll.add(CreditAccount("Елена Долгова", -20000, 0.02, 100000, 0.16))
    coll.add(SavingsAccount("Петр Выгодный", 200000, 0.06, 0.02, 5))
    
    # 1. Исходные балансы
    print("1. Исходная коллекция:")
    for acc in coll:
        print(f"   {acc.owner}: {acc._balance:.2f}₽")
    
    # 2. Поиск лучшего через интерфейс Comparable
    print("\n2. Поиск лучшего счёта (архитектурное поведение):")
    best = coll.find_best()
    print(f"   Лучший: {best.owner} ({best._balance:.2f}₽)")
    
    # 3. Сортировка через интерфейс Comparable
    print("\n3. Сортировка (архитектурное поведение):")
    coll.sort_using_comparable(reverse=True)
    print("   После сортировки по убыванию:")
    for acc in coll:
        print(f"   {acc.owner}: {acc._balance:.2f}₽")
    
    # 4. Полиморфный вывод всех объектов
    print("\n4. Полиморфный вывод всех объектов:")
    for acc in coll.get_printable():
        print(f"   {acc.to_string()}")


def main():
    print("=" * 60)
    print(" ЛР-4: ИНТЕРФЕЙСЫ И АБСТРАКТНЫЕ КЛАССЫ")
    print("=" * 60)
    
    scenario1()
    input("\n>>> Enter...")  
    
    scenario2()
    input("\n>>> Enter...")
    
    scenario3()
    input("\n>>> Enter...")
    
    scenario4()
    input("\n>>> Enter...")
    
    scenario5()
    
    print("\n" + "=" * 60)
    print(" ВСЕ СЦЕНАРИИ ВЫПОЛНЕНЫ!")
    print("=" * 60)


# Точка входа
if __name__ == "__main__":
    main()
