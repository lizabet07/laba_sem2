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

def demo_basic_operations():
    """Демонстрация базовых операций с коллекцией"""
    print_header("1. БАЗОВЫЕ ОПЕРАЦИИ С КОЛЛЕКЦИЕЙ")

    # Создаём коллекцию
    collection = BankAccountCollection()

    # Создаём несколько счетов
    acc1 = BankAccount("Иван Петров", 50000, 0.04)
    acc2 = BankAccount("Анна Сидорова", 150000, 0.05)
    acc3 = BankAccount("Пётр Иванов", 25000, 0.03)

    # Добавляем счета в коллекцию
    print("Добавляем счета в коллекцию:")
    collection.add(acc1)
    collection.add(acc2)
    collection.add(acc3)
    print(f"Добавлено 3 счёта. Всего в коллекции: {len(collection)}")

    # Выводим все элементы
    print("\nВсе счета в коллекции:")
    for account in collection:
        print(f"- {account.owner_name}: {account.balance:.2f} руб.")

    # Удаляем один счёт
    print(f"\nУдаляем счёт {acc2.owner_name}")
    collection.remove(acc2)
    print(f"Осталось счетов: {len(collection)}")

    # Повторный вывод
    print("\nПосле удаления:")
    for i, account in enumerate(collection):
        print(f"{i+1}. {account.owner_name}: {account.balance:.2f} руб.")

def demo_search_operations():
    """Демонстрация поиска в коллекции"""
    print_header("2. ПОИСК В КОЛЛЕКЦИИ")

    collection = BankAccountCollection()
    acc1 = BankAccount("Мария Соколова", 75000, 0.045)
    acc2 = BankAccount("Анна Сидорова", 150000, 0.05)
    acc3 = BankAccount("Мария Петрова", 30000, 0.035)

    for acc in [acc1, acc2, acc3]:
        collection.add(acc)

    # Поиск по имени владельца
    maria_accounts = collection.find_by_owner_name("Мария Соколова")
    print(f"Найдено счетов с именем 'Мария Соколова': {len(maria_accounts)}")
    for acc in maria_accounts:
        print(f"- {acc.owner_name}: {acc.balance:.2f} руб.")

    # Поиск по статусу
    active_accounts = collection.get_active()
    print(f"\nАктивных счетов: {len(active_accounts)}")

    # Поиск по диапазону балансов
    medium_balance = collection.find_by_balance_range(50000, 100000)
    print(f"\nСчетов с балансом 50 000–100 000 руб.: {len(medium_balance)}")
    for acc in medium_balance:
        print(f"- {acc.owner_name}: {acc.balance:.2f} руб.")

def demo_advanced_operations():
    """Демонстрация продвинутых операций"""
    print_header("3. ПРОДВИНУТЫЕ ОПЕРАЦИИ")

    collection = BankAccountCollection()
    acc1 = BankAccount("Борис Борисов", 200000, 0.06)
    acc2 = BankAccount("Анна Антонова", 50000, 0.03)
    acc3 = BankAccount("Виктор Васильев", 120000, 0.04)

    for acc in [acc1, acc2, acc3]:
        collection.add(acc)

    # Индексация
    print("Доступ по индексу:")
    print(f"Первый счёт: {collection[0].owner_name}")
    print(f"Последний счёт: {collection[-1].owner_name}")

    # Удаление по индексу
    print(f"\nУдаляем счёт по индексу 1")
    removed = collection.remove_at(1)
    print(f"Удален счёт: {removed.owner_name}")
    print(f"Осталось счетов: {len(collection)}")

    # Сортировка по балансу
    print("\nСортировка по балансу (убывание):")
    collection.sort_by_balance(reverse=True)
    for i, acc in enumerate(collection):
        print(f"{i+1}. {acc.owner_name}: {acc.balance:.2f} руб.")

    # Фильтрация
    print("\nСчета с балансом > 100 000 руб.:")
    high_balance = collection.get_high_balance()
    for acc in high_balance:
        print(f"- {acc.owner_name}: {acc.balance:.2f} руб.")

def main():
    """Главная функция"""
    print("=" * 70)
    print(" ЛАБОРАТОРНАЯ РАБОТА №2")
    print(" Коллекция банковских счетов — демонстрация всех возможностей")
    print("=" * 70)

    demo_basic_operations()
    input("\nНажмите Enter для продолжения...")

    demo_search_operations()
    input("\nНажмите Enter для продолжения...")

    demo_advanced_operations()

if __name__ == "__main__":
    main()
