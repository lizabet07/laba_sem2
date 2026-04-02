"""
Демонстрационный файл для лабораторной работы №2
"""

from model import BankAccount
from collection import BankAccountCollection


def print_header(title):
    """Вывод заголовка раздела"""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def scenario_1_basic_operations():
    """Сценарий 1: Базовые операции с коллекцией"""
    print_header("СЦЕНАРИЙ 1: БАЗОВЫЕ ОПЕРАЦИИ (ADD, REMOVE, ITERATION)")

    collection = BankAccountCollection()

    # Создаём счета
    acc1 = BankAccount("Иван Петров", 50000, 0.04)
    acc2 = BankAccount("Анна Сидорова", 150000, 0.05)
    acc3 = BankAccount("Пётр Иванов", 25000, 0.03)

    # 1. Добавление
    print("1. Добавление счетов в коллекцию:")
    collection.add(acc1)
    collection.add(acc2)
    collection.add(acc3)
    print(f"   Всего счетов: {len(collection)}")

    # 2. Итерация (for)
    print("\n2. Перебор всех счетов (for acc in collection):")
    for acc in collection:
        print(f"   - {acc.owner_name}: {acc.balance:.2f} руб. [{acc.status}]")

    # 3. Защита от дубликатов
    print("\n3. Проверка защиты от дубликатов:")
    try:
        duplicate = BankAccount("Иван Петров", 50000, 0.04)
        collection.add(duplicate)
    except ValueError as e:
        print(f"   ✓ Ошибка (корректно): {e}")

    # 4. Удаление
    print(f"\n4. Удаление счёта {acc2.owner_name}:")
    collection.remove(acc2)
    print(f"   Осталось счетов: {len(collection)}")

    # 5. Повторный вывод после удаления
    print("\n5. Все счета после удаления:")
    for acc in collection:
        print(f"   - {acc.owner_name}: {acc.balance:.2f} руб.")

    return collection


def scenario_2_search_and_filter():
    """Сценарий 2: Поиск и фильтрация"""
    print_header("СЦЕНАРИЙ 2: ПОИСК (FIND_BY_*) И ФИЛЬТРАЦИЯ (GET_*)")

    collection = BankAccountCollection()

    # Подготовка данных
    acc1 = BankAccount("Мария Соколова", 75000, 0.045)
    acc2 = BankAccount("Анна Сидорова", 150000, 0.05)
    acc3 = BankAccount("Мария Петрова", 30000, 0.035)
    acc4 = BankAccount("Елена Морозова", 200000, 0.06)

    for acc in [acc1, acc2, acc3, acc4]:
        collection.add(acc)

    # Блокируем некоторые счета для демонстрации
    acc2.block()
    acc4.block()

    print("Исходная коллекция:")
    for acc in collection:
        print(f"   - {acc.owner_name}: {acc.balance:.2f} руб. [{acc.status}]")

    # 1. Поиск по имени (find_by_owner_name)
    print("\n1. Поиск по имени 'Мария Соколова' (find_by_owner_name):")
    maria_accounts = collection.find_by_owner_name("Мария Соколова")
    print(f"   Найдено: {len(maria_accounts)}")
    for acc in maria_accounts:
        print(f"   - {acc.owner_name}: {acc.balance:.2f} руб.")

    # 2. Поиск по диапазону балансов (find_by_balance_range)
    print("\n2. Поиск по диапазону балансов 50000-100000 руб.:")
    medium = collection.find_by_balance_range(50000, 100000)
    print(f"   Найдено: {len(medium)}")
    for acc in medium:
        print(f"   - {acc.owner_name}: {acc.balance:.2f} руб.")

    # 3. Фильтрация активных счетов (get_active)
    print("\n3. Фильтрация: только активные счета (get_active):")
    active = collection.get_active()
    print(f"   Активных счетов: {len(active)}")
    for acc in active:
        print(f"   - {acc.owner_name} [{acc.status}]")

    # 4. Фильтрация заблокированных счетов (get_blocked)
    print("\n4. Фильтрация: только заблокированные счета (get_blocked):")
    blocked = collection.get_blocked()
    print(f"   Заблокированных счетов: {len(blocked)}")
    for acc in blocked:
        print(f"   - {acc.owner_name} [{acc.status}]")

    # 5. Фильтрация по высокому балансу (get_high_balance)
    print("\n5. Фильтрация: счета с балансом > 100000 руб. (get_high_balance):")
    high = collection.get_high_balance(100000)
    print(f"   Найдено: {len(high)}")
    for acc in high:
        print(f"   - {acc.owner_name}: {acc.balance:.2f} руб.")

    return collection


def scenario_3_sorting_and_indexing():
    """Сценарий 3: Индексация и сортировка"""
    print_header("СЦЕНАРИЙ 3: ИНДЕКСАЦИЯ (__GETITEM__) И СОРТИРОВКА (SORT)")

    collection = BankAccountCollection()
    acc1 = BankAccount("Борис Борисов", 200000, 0.06)
    acc2 = BankAccount("Анна Антонова", 50000, 0.03)
    acc3 = BankAccount("Виктор Васильев", 120000, 0.04)
    acc4 = BankAccount("Галина Громова", 80000, 0.035)

    for acc in [acc1, acc2, acc3, acc4]:
        collection.add(acc)

    print("Исходная коллекция:")
    for i, acc in enumerate(collection):
        print(f"   [{i}] {acc.owner_name}: {acc.balance:.2f} руб.")

    # 1. Доступ по индексу (__getitem__)
    print("\n1. Доступ по индексу (__getitem__):")
    print(f"   collection[0]: {collection[0].owner_name}")
    print(f"   collection[1]: {collection[1].owner_name}")
    print(f"   collection[-1]: {collection[-1].owner_name}")

    # 2. Срез (slice)
    print("\n2. Срез collection[1:3]:")
    for acc in collection[1:3]:
        print(f"   - {acc.owner_name}")

    # 3. Удаление по индексу (remove_at)
    print(f"\n3. Удаление по индексу remove_at(2):")
    removed = collection.remove_at(2)
    print(f"   Удалён: {removed.owner_name}")
    print(f"   Осталось счетов: {len(collection)}")

    # 4. Универсальная сортировка sort(key, reverse)
    print("\n4. Универсальная сортировка sort(key=lambda acc: acc.balance, reverse=True):")
    collection.sort(key=lambda acc: acc.balance, reverse=True)
    for i, acc in enumerate(collection):
        print(f"   {i+1}. {acc.owner_name}: {acc.balance:.2f} руб.")

    # 5. Сортировка по имени (удобный метод)
    print("\n5. Сортировка по имени sort_by_owner_name():")
    collection.sort_by_owner_name()
    for i, acc in enumerate(collection):
        print(f"   {i+1}. {acc.owner_name}: {acc.balance:.2f} руб.")

    return collection


def scenario_4_chaining_operations():
    """Сценарий 4: Цепочки операций (методы возвращают коллекции)"""
    print_header("СЦЕНАРИЙ 4: ЦЕПОЧКИ ОПЕРАЦИЙ (CHAINING)")

    collection = BankAccountCollection()

    # Создаём счета с разными балансами и статусами
    accounts_data = [
        ("Активный Богатый", 500000),
        ("Активный Бедный", 10000),
        ("Заблокированный Богатый", 300000),
        ("Активный Средний", 75000),
        ("Активный Очень Богатый", 1000000),
    ]
    
    for name, balance in accounts_data:
        acc = BankAccount(name, balance, 0.05)
        if "Заблокированный" in name:
            acc.block()
        collection.add(acc)

    print("Исходная коллекция:")
    print(collection)

    # 1. Цепочка: активные И с высоким балансом
    print("\n1. Цепочка: get_active().get_high_balance(100000)")
    result = collection.get_active().get_high_balance(100000)
    print(f"   Активных счетов с балансом > 100000 руб.: {len(result)}")
    for acc in result:
        print(f"   - {acc.owner_name}: {acc.balance:.2f} руб.")

    # 2. Цепочка: найти по имени, затем отсортировать
    print("\n2. Цепочка: find_by_owner_name('Активный').sort(key=...)")
    found = collection.find_by_owner_name("Активный Богатый")
    found.sort(key=lambda acc: acc.balance, reverse=True)
    print(f"   Найдено и отсортировано: {len(found)}")
    for acc in found:
        print(f"   - {acc.owner_name}: {acc.balance:.2f} руб.")

    # 3. Цепочка: фильтрация + срез
    print("\n3. Цепочка: get_high_balance(200000)[0:2]")
    top_accounts = collection.get_high_balance(200000)[0:2]
    print(f"   Топ-2 счета с балансом > 200000 руб.:")
    for acc in top_accounts:
        print(f"   - {acc.owner_name}: {acc.balance:.2f} руб.")

    # 4. Цепочка: несколько фильтров подряд
    print("\n4. Цепочка: get_active().get_high_balance(50000).sort_by_owner_name()")
    filtered = collection.get_active().get_high_balance(50000)
    filtered.sort_by_owner_name()
    print(f"   Активных счетов с балансом > 50000 руб.: {len(filtered)}")
    for acc in filtered:
        print(f"   - {acc.owner_name}: {acc.balance:.2f} руб.")


def main():
    """Главная функция - демонстрация всех возможностей"""
    print("=" * 70)
    print(" ЛАБОРАТОРНАЯ РАБОТА №2 - ОЦЕНКА 5")
    print(" КОЛЛЕКЦИЯ БАНКОВСКИХ СЧЕТОВ - 4 СЦЕНАРИЯ")
    print("=" * 70)

    # Сценарий 1: Базовые операции
    scenario_1_basic_operations()
    input("\n▶ Нажмите Enter для сценария 2...")

    # Сценарий 2: Поиск и фильтрация
    scenario_2_search_and_filter()
    input("\n▶ Нажмите Enter для сценария 3...")

    # Сценарий 3: Индексация и сортировка
    scenario_3_sorting_and_indexing()
    input("\n▶ Нажмите Enter для сценария 4...")

    # Сценарий 4: Цепочки операций
    scenario_4_chaining_operations()



if __name__ == "__main__":
    main()