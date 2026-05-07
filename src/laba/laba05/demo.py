"""
Демонстрация ЛР-5: Функции как аргументы. Стратегии и делегаты
"""

import sys
import os

# Добавляем путь для импорта модулей из соседних папок
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Импортируем классы счетов из ЛР-3
from laba03.base import BankAccount
from laba03.model import SavingsAccount, CreditAccount, PremiumAccount
# Импортируем коллекцию из ЛР-5
from laba05.collection import BankAccountCollection
# Импортируем все стратегии и функции под именем st
import laba05.strategies as st


def print_section(title):
    """Печать заголовка секции"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def create_collection():
    """Создание тестовой коллекции из 8 счетов"""
    col = BankAccountCollection()
    
    # Создаём разные типы счетов (из ЛР-3)
    acc1 = BankAccount("Иванов Иван", 50000, 0.05)           # Обычный
    acc2 = SavingsAccount("Петрова Мария", 120000, 0.06, 0.02, 5)  # Накопительный
    acc3 = CreditAccount("Сидоров Алексей", 30000, 0.04, 100000, 0.18)  # Кредитный
    acc4 = PremiumAccount("Кузнецова Елена", 250000, 0.07, 0.025, 10)   # Премиум
    acc5 = BankAccount("Смирнов Дмитрий", 8000, 0.03)
    acc5.block()  # Блокируем счёт
    acc6 = SavingsAccount("Васильева Анна", 0, 0.055, 0.015, 3)
    acc6.close()  # Закрываем счёт
    acc7 = CreditAccount("Козлов Артем", 0, 0.045, 150000, 0.20)
    acc7.withdraw(5000)  # Уходим в минус
    acc8 = PremiumAccount("Новикова Ольга", 600000, 0.08, 0.03, 15)
    
    # Добавляем все счета в коллекцию
    for acc in [acc1, acc2, acc3, acc4, acc5, acc6, acc7, acc8]:
        try:
            col.add(acc)
        except ValueError as e:
            print(f"Ошибка: {e}")
    
    return col


# ========== СЦЕНАРИЙ 1: СОРТИРОВКА (sorted с параметром key) ==========

def scenario_sorting(col):
    """Демонстрация сортировки с разными ключами"""
    print_section("СЦЕНАРИЙ 1: СОРТИРОВКА С ПАРАМЕТРОМ key=")
    
    # 1. Именованная функция как ключ
    items1 = col.get_all()
    items1.sort(key=st.by_balance)  # st.by_balance - функция без вызова
    print("1. По балансу (возрастание):")
    for acc in items1:
        print(f"   {acc.owner}: {acc.balance:.0f}₽")
    
    # 2. Lambda как ключ
    sorted_by_name = sorted(col.get_all(), key=lambda acc: acc.owner)
    print("\n2. По имени (lambda):")
    for acc in sorted_by_name:
        print(f"   {acc.owner}: {acc.balance:.0f}₽")
    
    # 3. Сложный ключ (кортеж) - сначала статус, потом баланс
    items3 = col.get_all()
    items3.sort(key=st.by_multiple_criteria)
    print("\n3. По статусу + балансу (несколько критериев):")
    for acc in items3:
        print(f"   [{acc.status}] {acc.owner}: {acc.balance:.0f}₽")
    
    # 4. Обратная сортировка
    sorted_desc = sorted(col.get_all(), key=st.by_balance, reverse=True)
    print("\n4. По убыванию баланса (reverse=True):")
    for acc in sorted_desc:
        print(f"   {acc.owner}: {acc.balance:.0f}₽")


# ========== СЦЕНАРИЙ 2: ФИЛЬТРАЦИЯ (filter) ==========

def scenario_filtering(col):
    """Демонстрация фильтрации с разными предикатами"""
    print_section("СЦЕНАРИЙ 2: ФИЛЬТРАЦИЯ (filter)")
    
    # 1. Именованная функция-предикат
    active = list(filter(st.is_active, col.get_all()))
    print("1. Только активные счета (is_active):")
    for acc in active:
        print(f"   {acc.owner}: {acc.balance:.0f}₽")
    
    # 2. Lambda как предикат
    credit = list(filter(lambda acc: acc.get_type() == "Кредитный", col.get_all()))
    print("\n2. Только кредитные счета (lambda):")
    for acc in credit:
        print(f"   {acc.owner}: {acc.balance:.0f}₽")
    
    # 3. Фильтр по типу через isinstance
    savings = list(filter(lambda acc: isinstance(acc, SavingsAccount), col.get_all()))
    print("\n3. Только накопительные счета (isinstance):")
    for acc in savings:
        print(f"   {acc.owner}: {acc.balance:.0f}₽")
    
    # 4. Фильтр, созданный фабрикой (замыкание)
    high_balance_filter = st.make_balance_filter(100000)  # Создаём фильтр
    high_balance = list(filter(high_balance_filter, col.get_all()))
    print(f"\n4. С балансом > 100000₽ (фабрика):")
    for acc in high_balance:
        print(f"   {acc.owner}: {acc.balance:.0f}₽")


# ========== СЦЕНАРИЙ 3: ПРЕОБРАЗОВАНИЕ (map) ==========

def scenario_map(col):
    """Демонстрация преобразования коллекции через map"""
    print_section("СЦЕНАРИЙ 3: ПРЕОБРАЗОВАНИЕ ЧЕРЕЗ map()")
    
    # 1. Именованная функция для преобразования
    short_strings = list(map(st.to_short_string, col.get_all()))
    print("1. В краткие строки (to_short_string):")
    for s in short_strings[:5]:
        print(f"   {s}")
    
    # 2. Lambda для извлечения поля
    names = list(map(lambda acc: acc.owner, col.get_all()))
    print("\n2. Извлечение имён (lambda):")
    print(f"   {', '.join(names[:5])}")
    
    # 3. Фабрика для создания функции со скидкой
    discount_20 = st.make_discount_applier(20)  # Создаём функцию скидки
    discounted = list(map(discount_20, col.get_all()))
    print("\n3. Применение скидки 20% (фабрика):")
    for d in discounted[:5]:
        print(f"   {d['account']}: {d['original']:.0f}₽ → {d['discounted']:.0f}₽")
    
    # 4. Lambda для преобразования в словарь
    dicts = list(map(lambda acc: {"owner": acc.owner, "balance": acc.balance}, col.get_all()))
    print("\n4. В словари (lambda):")
    for d in dicts[:3]:
        print(f"   {d}")


# ========== СЦЕНАРИЙ 4: ЦЕПОЧКА ОПЕРАЦИЙ (filter → sort → apply) ==========

def scenario_chain_with_output(col):
    """Демонстрация цепочки операций с пошаговым выводом"""
    print_section("СЦЕНАРИЙ 4: ЦЕПОЧКА filter → sort → apply")
    
    print("ШАГ 1: Исходная коллекция:")
    for acc in col.get_all():
        print(f"   {acc.owner}: {acc.balance:.0f}₽ [{acc.status}]")
    
    # Шаг 2: Фильтрация - оставляем только активные
    print("\n---")
    print("ШАГ 2: filter_by(is_active):")
    filtered = col.filter_by(st.is_active)
    for acc in filtered.get_all():
        print(f"   {acc.owner}: {acc.balance:.0f}₽")
    
    # Шаг 3: Сортировка по убыванию баланса
    print("\n---")
    print("ШАГ 3: sort_by(by_balance_desc):")
    sorted_col = filtered.sort_by(st.by_balance_desc)
    for acc in sorted_col.get_all():
        print(f"   {acc.owner}: {acc.balance:.0f}₽")
    
    # Шаг 4: Преобразование в строки
    print("\n---")
    print("ШАГ 4: apply(to_short_string):")
    result = sorted_col.apply(st.to_short_string)
    for r in result:
        print(f"   {r}")
    
    # ИТОГ: цепочка без промежуточных переменных
    print("\n" + "="*40)
    print("ТА ЖЕ ЦЕПОЧКА В ОДНУ СТРОКУ:")
    print("col.filter_by(is_active).sort_by(by_balance_desc).apply(to_short_string)")


# ========== СЦЕНАРИЙ 5: ПАТТЕРН СТРАТЕГИЯ (callable-объекты) ==========

def scenario_strategies(col):
    """Демонстрация callable-объектов как стратегий"""
    print_section("СЦЕНАРИЙ 5: ПАТТЕРН СТРАТЕГИЯ (callable-объекты)")
    
    # Берём только активные счета для начисления процентов
    active = list(filter(st.is_active, col.get_all()))
    print("Активные счета:")
    for acc in active:
        print(f"   {acc.owner}: {acc.balance:.0f}₽, ставка {acc.rate*100:.1f}%")
    
    # Стратегия 1: Простая
    print("\n---")
    print("СТРАТЕГИЯ 1: SimpleInterestStrategy")
    simple = st.SimpleInterestStrategy()  # Callable-объект
    for acc in active:
        print(f"   {acc.owner}: проценты = {simple(acc):.2f}₽")  # Вызов как функции
    
    # Стратегия 2: Агрессивная (с бонусом)
    print("\n---")
    print("СТРАТЕГИЯ 2: AggressiveInterestStrategy (бонус за большой баланс)")
    aggressive = st.AggressiveInterestStrategy(threshold=50000, bonus=0.01)
    for acc in active:
        interest = aggressive(acc)
        bonus = " + бонус" if acc.balance > 50000 else ""
        print(f"   {acc.owner}: проценты = {interest:.2f}₽{bonus}")
    
    # Стратегия 3: Меняем стратегию на лету для одного счёта
    print("\n---")
    print("СТРАТЕГИЯ 3: Замена стратегии на лету")
    test_acc = active[0]
    print(f"Счёт: {test_acc.owner}, баланс: {test_acc.balance:.0f}₽")
    
    # Один и тот же счёт, разные стратегии
    print(f"   Простая стратегия: {simple(test_acc):.2f}₽")
    print(f"   Агрессивная стратегия: {aggressive(test_acc):.2f}₽")
    print(f"   Консервативная стратегия: {st.ConservativeInterestStrategy()(test_acc):.2f}₽")


# ========== СЦЕНАРИЙ 6: LAMBDA vs ИМЕНОВАННАЯ ФУНКЦИЯ ==========

def scenario_lambda_vs_named(col):
    """Сравнение lambda и именованной функции"""
    print_section("СЦЕНАРИЙ 6: LAMBDA vs ИМЕНОВАННАЯ ФУНКЦИЯ")
    
    # Оба способа делают одно и то же
    def get_owner(acc):      # Именованная
        return acc.owner
    
    names_named = list(map(get_owner, col.get_all()))
    names_lambda = list(map(lambda acc: acc.owner, col.get_all()))  # Lambda
    
    print("Именованная функция:")
    print(f"   {', '.join(names_named[:5])}")
    print("\nLambda выражение:")
    print(f"   {', '.join(names_lambda[:5])}")
    
    # Сортировка тоже работает одинаково
    print("\n---")
    print("Сортировка через lambda:")
    sorted_lambda = sorted(col.get_all(), key=lambda acc: acc.balance)
    print(f"   Минимум: {sorted_lambda[0].owner} ({sorted_lambda[0].balance:.0f}₽)")
    
    print("\nСортировка через именованную функцию:")
    sorted_named = sorted(col.get_all(), key=st.by_balance)
    print(f"   Минимум: {sorted_named[0].owner} ({sorted_named[0].balance:.0f}₽)")
    
    print("\nВЫВОД: lambda короче, именованная функция понятнее и переиспользуется")


# ========== ГЛАВНАЯ ФУНКЦИЯ ==========

def main():
    print("\n" + "="*60)
    print("   ЛАБОРАТОРНАЯ РАБОТА №5")
    print("   Функции как аргументы. Стратегии и делегаты")
    print("="*60)
    
    col = create_collection()
    print(f"\nСоздана коллекция из {len(col)} счетов")
    
    # Запускаем все 6 сценариев
    scenario_sorting(col)           # Сортировка
    scenario_filtering(col)         # Фильтрация
    scenario_map(col)               # Преобразование
    scenario_chain_with_output(col) # Цепочка операций
    scenario_strategies(col)        # Паттерн Стратегия
    scenario_lambda_vs_named(col)   # Сравнение lambda и функций


if __name__ == "__main__":
    main()
