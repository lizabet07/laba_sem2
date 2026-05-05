"""
Демонстрация ЛР-5: Функции как аргументы. Стратегии и делегаты
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from laba03.base import BankAccount
from laba03.model import SavingsAccount, CreditAccount, PremiumAccount
from laba05.collection import BankAccountCollection
import laba05.strategies as st


def print_section(title):
    """Печать заголовка секции"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def create_collection():
    """Создание тестовой коллекции из 8 счетов"""
    col = BankAccountCollection()
    
    # Создаём счета
    acc1 = BankAccount("Иванов Иван", 50000, 0.05)
    acc2 = SavingsAccount("Петрова Мария", 120000, 0.06, 0.02, 5)
    acc3 = CreditAccount("Сидоров Алексей", 30000, 0.04, 100000, 0.18)
    acc4 = PremiumAccount("Кузнецова Елена", 250000, 0.07, 0.025, 10)
    acc5 = BankAccount("Смирнов Дмитрий", 8000, 0.03)
    acc5.block()
    acc6 = SavingsAccount("Васильева Анна", 0, 0.055, 0.015, 3)
    acc6.close()
    acc7 = CreditAccount("Козлов Артем", 0, 0.045, 150000, 0.20)
    acc7.withdraw(5000)
    acc8 = PremiumAccount("Новикова Ольга", 600000, 0.08, 0.03, 15)
    
    for acc in [acc1, acc2, acc3, acc4, acc5, acc6, acc7, acc8]:
        try:
            col.add(acc)
        except ValueError as e:
            print(f"Ошибка: {e}")
    
    return col


# ========== СЦЕНАРИЙ 1: СОРТИРОВКА С ПАРАМЕТРОМ key= ==========

def scenario_sorting(col):
    print_section("СЦЕНАРИЙ 1: СОРТИРОВКА С ПАРАМЕТРОМ key=")
    
    # 1. collection.sort(key=by_balance) - именованная функция
    items1 = col.get_all()
    items1.sort(key=st.by_balance)
    print("1. collection.sort(key=by_balance) - по балансу (возрастание):")
    for acc in items1:
        print(f"   {acc.owner}: {acc.balance:.0f}₽")
    
    # 2. sorted(collection, key=lambda x: x.name) - lambda
    sorted_by_name = sorted(col.get_all(), key=lambda acc: acc.owner)
    print("\n2. sorted(collection, key=lambda acc: acc.owner) - по имени:")
    for acc in sorted_by_name:
        print(f"   {acc.owner}: {acc.balance:.0f}₽")
    
    # 3. collection.sort(key=...) - сортировка по нескольким критериям
    items3 = col.get_all()
    items3.sort(key=st.by_multiple_criteria)
    print("\n3. collection.sort(key=by_multiple_criteria) - по статусу + балансу:")
    for acc in items3:
        print(f"   [{acc.status}] {acc.owner}: {acc.balance:.0f}₽")
    
    # 4. sorted() с reverse=True
    sorted_desc = sorted(col.get_all(), key=st.by_balance, reverse=True)
    print("\n4. sorted(key=by_balance, reverse=True) - по убыванию баланса:")
    for acc in sorted_desc:
        print(f"   {acc.owner}: {acc.balance:.0f}₽")


# ========== СЦЕНАРИЙ 2: ФИЛЬТРАЦИЯ ==========

def scenario_filtering(col):
    print_section("СЦЕНАРИЙ 2: ФИЛЬТРАЦИЯ (filter)")
    
    # Фильтр 1: через filter() с именованной функцией
    active = list(filter(st.is_active, col.get_all()))
    print("1. filter(is_active, collection) - активные счета:")
    for acc in active:
        print(f"   {acc.owner}: {acc.balance:.0f}₽ - {acc.get_type()}")
    
    # Фильтр 2: через filter() с lambda
    credit = list(filter(lambda acc: acc.get_type() == "Кредитный", col.get_all()))
    print("\n2. filter(lambda acc: acc.get_type() == 'Кредитный') - кредитные счета:")
    for acc in credit:
        print(f"   {acc.owner}: {acc.balance:.0f}₽")
    
    # Фильтр 3: через filter() и isinstance
    savings = list(filter(lambda acc: isinstance(acc, SavingsAccount), col.get_all()))
    print("\n3. filter(isinstance, SavingsAccount) - накопительные счета:")
    for acc in savings:
        print(f"   {acc.owner}: {acc.balance:.0f}₽")
    
    # Фильтр 4: через фабрику функций
    high_balance_filter = st.make_balance_filter(100000)
    high_balance = list(filter(high_balance_filter, col.get_all()))
    print(f"\n4. filter(фабрика make_balance_filter(100000)) - счета с балансом > 100000₽:")
    for acc in high_balance:
        print(f"   {acc.owner}: {acc.balance:.0f}₽")


# ========== СЦЕНАРИЙ 3: map() ==========

def scenario_map(col):
    print_section("СЦЕНАРИЙ 3: ПРЕОБРАЗОВАНИЕ ЧЕРЕЗ map()")
    
    # map с именованной функцией (преобразование в строки)
    short_strings = list(map(st.to_short_string, col.get_all()))
    print("1. map(to_short_string, collection) - краткие строки:")
    for s in short_strings[:5]:
        print(f"   {s}")
    
    # map с lambda (извлечение поля)
    names = list(map(lambda acc: acc.owner, col.get_all()))
    print("\n2. map(lambda acc: acc.owner, collection) - имена владельцев:")
    print(f"   {', '.join(names[:5])}")
    
    # map с фабрикой функций (применение скидки)
    discount_20 = st.make_discount_applier(20)
    discounted = list(map(discount_20, col.get_all()))
    print("\n3. map(фабрика_скидки, collection) - скидка 20%:")
    for d in discounted[:5]:
        print(f"   {d['account']}: {d['original']:.0f}₽ → {d['discounted']:.0f}₽")
    
    # map с lambda (преобразование в словари)
    dicts = list(map(lambda acc: {"owner": acc.owner, "balance": acc.balance}, col.get_all()))
    print("\n4. map(lambda acc: dict, collection) - преобразование в словари (первые 3):")
    for d in dicts[:3]:
        print(f"   {d}")


# ========== СЦЕНАРИЙ 4: ЦЕПОЧКА С ПОШАГОВЫМ ВЫВОДОМ ==========

def scenario_chain_with_output(col):
    print_section("СЦЕНАРИЙ 4: ЦЕПОЧКА filter → sort → apply (с выводом на каждом шаге)")
    
    print("ШАГ 1: Исходная коллекция (все счета):")
    for acc in col.get_all():
        print(f"   {acc.owner}: {acc.balance:.0f}₽ [{acc.status}]")
    
    # Шаг 2: фильтрация
    print("\n" + "-"*40)
    print("ШАГ 2: Применяем filter_by(is_active) - оставляем только активные счета")
    filtered = col.filter_by(st.is_active)
    print("Результат фильтрации:")
    for acc in filtered.get_all():
        print(f"   {acc.owner}: {acc.balance:.0f}₽ [{acc.status}]")
    
    # Шаг 3: сортировка
    print("\n" + "-"*40)
    print("ШАГ 3: Применяем sort_by(by_balance_desc) - сортируем по убыванию баланса")
    sorted_col = filtered.sort_by(st.by_balance_desc)
    print("Результат сортировки:")
    for acc in sorted_col.get_all():
        print(f"   {acc.owner}: {acc.balance:.0f}₽")
    
    # Шаг 4: преобразование
    print("\n" + "-"*40)
    print("ШАГ 4: Применяем apply(to_short_string) - преобразуем в краткие строки")
    result = sorted_col.apply(st.to_short_string)
    print("Результат преобразования:")
    for r in result:
        print(f"   {r}")
    
    # Финальный результат
    print("\n" + "="*40)
    print("ИТОГОВЫЙ РЕЗУЛЬТАТ ЦЕПОЧКИ:")
    for r in result:
        print(f"   {r}")


# ========== СЦЕНАРИЙ 5: ПАТТЕРН СТРАТЕГИЯ (callable-объекты) ==========

def scenario_strategies(col):
    print_section("СЦЕНАРИЙ 5: ПАТТЕРН СТРАТЕГИЯ (callable-объекты)")
    
    active = list(filter(st.is_active, col.get_all()))
    
    print("Активные счета:")
    for acc in active:
        print(f"   {acc.owner}: баланс {acc.balance:.0f}₽, ставка {acc.rate*100:.1f}%")
    
    print("\n" + "-"*40)
    print("СЦЕНАРИЙ 5.1: SimpleInterestStrategy (простая стратегия)")
    simple = st.SimpleInterestStrategy()
    for acc in active:
        print(f"   {acc.owner}: проценты = {simple(acc):.2f}₽")
    
    print("\n" + "-"*40)
    print("СЦЕНАРИЙ 5.2: AggressiveInterestStrategy (агрессивная стратегия - замена стратегии)")
    aggressive = st.AggressiveInterestStrategy(threshold=50000, bonus=0.01)
    for acc in active:
        interest = aggressive(acc)
        bonus = " + бонус" if acc.balance > 50000 else ""
        print(f"   {acc.owner}: проценты = {interest:.2f}₽{bonus}")
    
    print("\n" + "-"*40)
    print("СЦЕНАРИЙ 5.3: Замена стратегии на лету (один и тот же счёт, разные стратегии)")
    test_acc = active[0] if active else col.get_all()[0]
    print(f"Счёт: {test_acc.owner}, баланс: {test_acc.balance:.0f}₽, ставка: {test_acc.rate*100:.1f}%")
    
    strategies = [
        ("SimpleInterestStrategy", simple),
        ("AggressiveInterestStrategy", aggressive),
        ("ConservativeInterestStrategy (новый тест)", st.ConservativeInterestStrategy())
    ]
    
    for name, strategy in strategies:
        print(f"   {name}: {strategy(test_acc):.2f}₽")


# ========== СЦЕНАРИЙ 6: LAMBDA vs ИМЕНОВАННАЯ ФУНКЦИЯ ==========

def scenario_lambda_vs_named(col):
    print_section("СЦЕНАРИЙ 6: LAMBDA vs ИМЕНОВАННАЯ ФУНКЦИЯ")
    
    # Именованная функция
    def get_owner(acc):
        return acc.owner
    
    names_named = list(map(get_owner, col.get_all()))
    
    # Lambda выражение
    names_lambda = list(map(lambda acc: acc.owner, col.get_all()))
    
    print("Именованная функция (map):")
    print(f"   {', '.join(names_named[:5])}")
    print("\nLambda выражение (map):")
    print(f"   {', '.join(names_lambda[:5])}")
    
    # Дополнительная демонстрация для сортировки
    print("\n" + "-"*40)
    print("Сортировка через lambda:")
    sorted_lambda = sorted(col.get_all(), key=lambda acc: acc.balance)
    print(f"   Минимальный баланс: {sorted_lambda[0].owner} ({sorted_lambda[0].balance:.0f}₽)")
    
    print("\nСортировка через именованную функцию:")
    sorted_named = sorted(col.get_all(), key=st.by_balance)
    print(f"   Минимальный баланс: {sorted_named[0].owner} ({sorted_named[0].balance:.0f}₽)")
    



# ========== ГЛАВНАЯ ФУНКЦИЯ ==========

def main():
    print("\n" + "="*60)
    print("   ЛАБОРАТОРНАЯ РАБОТА №5")
    print("   Функции как аргументы. Стратегии и делегаты")
    print("="*60)
    
    col = create_collection()
    print(f"\nСоздана коллекция из {len(col)} счетов")
    
    # Запуск всех сценариев
    scenario_sorting(col)           # Сценарий 1: сортировка с key=
    scenario_filtering(col)         # Сценарий 2: фильтрация с filter()
    scenario_map(col)               # Сценарий 3: map()
    scenario_chain_with_output(col) # Сценарий 4: цепочка с пошаговым выводом
    scenario_strategies(col)        # Сценарий 5: callable-стратегии
    scenario_lambda_vs_named(col)   # Сценарий 6: lambda vs именованная
    

if __name__ == "__main__":
    main()