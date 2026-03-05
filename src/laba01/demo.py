"""
Демонстрационный файл для лабораторной работы №1
"""

from model import BankAccount
import validate

def print_header(title):
    """Вывод заголовка раздела"""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)

def print_subheader(title):
    """Вывод подзаголовка"""
    print(f"\n--- {title} ---")

def demo_creation():
    """Демонстрация создания счетов"""
    print_header("1. СОЗДАНИЕ БАНКОВСКИХ СЧЕТОВ")
    
    print_subheader("Создание счета с параметрами по умолчанию")
    acc1 = BankAccount("Иван Петров")
    print(f"Владелец: {acc1.owner_name}")
    print(f"Номер счета: {acc1.account_number}")
    print(f"Баланс: {acc1.balance:.2f} руб.")
    print(f"Ставка: {acc1.interest_rate*100}%")
    print(f"Статус: {acc1.status}")
    
    print_subheader("Создание счета с начальным балансом 10000 и ставкой 5%")
    acc2 = BankAccount("Анна Сидорова", 10000, 0.05)
    print(f"Владелец: {acc2.owner_name}")
    print(f"Номер счета: {acc2.account_number}")
    print(f"Баланс: {acc2.balance:.2f} руб.")
    print(f"Ставка: {acc2.interest_rate*100}%")
    print(f"Статус: {acc2.status}")
    
    print_subheader("Создание счета с балансом 500000")
    acc3 = BankAccount("Петр Иванов", 500000, 0.03)
    print(f"Владелец: {acc3.owner_name}")
    print(f"Номер счета: {acc3.account_number}")
    print(f"Баланс: {acc3.balance:.2f} руб.")
    print(f"Ставка: {acc3.interest_rate*100}%")
    print(f"Статус: {acc3.status}")
    
    return acc1, acc2, acc3

def demo_validation():
    """Демонстрация обработки ошибок валидации"""
    print_header("2. ДЕМОНСТРАЦИЯ ВАЛИДАЦИИ (ОБРАБОТКА ОШИБОК)")
    
    print_subheader("Попытка создать счет с некорректным именем")
    test_names = [
        ("", "пустое имя"),
        ("   ", "имя из пробелов"),
        ("Анна", "слишком короткое имя (4 символа)"),
        ("Иван123", "имя с цифрами"),
        ("Петр!@#", "имя со спецсимволами"),
        ("Иван Петров Сидорович Алекс" * 5, "слишком длинное имя")
    ]
    
    for name, desc in test_names:
        try:
            print(f"\nТест: {desc}")
            acc = BankAccount(name, 1000)
            print(f"Успешно создан: {acc.owner_name}")
        except (ValueError, TypeError) as e:
            print(f"ОШИБКА: {e}")
    
    print_subheader("Попытка создать счет с некорректным балансом")
    try:
        print("\nПопытка создать счет с отрицательным балансом -1000")
        acc = BankAccount("Тест Тестов", -1000)
    except ValueError as e:
        print(f"ОШИБКА: {e}")
    
    try:
        print("\nПопытка создать счет с балансом 20_000_000 (превышение MAX_BALANCE)")
        acc = BankAccount("Тест Тестов", 20_000_000)
    except ValueError as e:
        print(f"ОШИБКА: {e}")
    
    print_subheader("Попытка создать счет с некорректной процентной ставкой")
    try:
        print("\nПопытка создать счет со ставкой 1.5 (> 1)")
        acc = BankAccount("Тест Тестов", 1000, 1.5)
    except ValueError as e:
        print(f"ОШИБКА: {e}")
    
    try:
        print("\nПопытка создать счет с отрицательной ставкой -0.1")
        acc = BankAccount("Тест Тестов", 1000, -0.1)
    except ValueError as e:
        print(f"ОШИБКА: {e}")

def demo_properties():
    """Демонстрация свойств и сеттеров"""
    print_header("3. ДЕМОНСТРАЦИЯ СВОЙСТВ (GETTERS/SETTERS)")
    
    acc = BankAccount("Михаил Демин", 50000, 0.04)
    print("Исходный счет:")
    print(f"  Номер счета: {acc.account_number}")
    print(f"  Владелец: {acc.owner_name}")
    print(f"  Баланс: {acc.balance:.2f}")
    print(f"  Ставка: {acc.interest_rate*100}%")
    print(f"  Статус: {acc.status}")
    print(f"  Дней с открытия: {acc.days_open}")
    
    print_subheader("Изменение свойств через сеттеры")
    try:
        print("\nИзменяем имя владельца на 'Демин Михаил Сергеевич'")
        acc.owner_name = "Демин Михаил Сергеевич"
        print(f"  Новое имя: {acc.owner_name}")
    except ValueError as e:
        print(f"ОШИБКА: {e}")
    
    try:
        print("\nИзменяем процентную ставку на 6.5%")
        acc.interest_rate = 0.065
        print(f"  Новая ставка: {acc.interest_rate*100}%")
    except ValueError as e:
        print(f"ОШИБКА: {e}")
    
    try:
        print("\nПробуем изменить баланс напрямую")
        acc.balance = 100000
    except AttributeError as e:
        print(f"ОШИБКА: {e} - баланс доступен только для чтения")

def demo_operations():
    """Демонстрация банковских операций"""
    print_header("4. ДЕМОНСТРАЦИЯ БАНКОВСКИХ ОПЕРАЦИЙ")
    
    acc = BankAccount("Олег Операторов", 100000, 0.05)
    print(f"Начальный баланс: {acc.balance:.2f}")
    
    print_subheader("Внесение средств (deposit)")
    try:
        print("Вносим 25000 рублей")
        acc.deposit(25000)
        print(f"  Новый баланс: {acc.balance:.2f}")
    except Exception as e:
        print(f"ОШИБКА: {e}")
    
    print_subheader("Снятие средств (withdraw)")
    try:
        print("Снимаем 15000 рублей")
        acc.withdraw(15000)
        print(f"  Новый баланс: {acc.balance:.2f}")
    except Exception as e:
        print(f"ОШИБКА: {e}")
    
    print_subheader("Попытка снять больше чем есть")
    try:
        print("Пытаемся снять 200000 рублей")
        acc.withdraw(200000)
    except Exception as e:
        print(f"ОШИБКА: {e}")
    
    print_subheader("Расчет и начисление процентов")
    interest = acc.calculate_interest()
    print(f"  Сумма процентов: {interest:.2f}")
    
    print("Начисляем проценты")
    acc.apply_interest()
    print(f"  Баланс после процентов: {acc.balance:.2f}")
    
    print_subheader("Некорректные операции")
    try:
        print("Пытаемся внести отрицательную сумму -5000")
        acc.deposit(-5000)
    except Exception as e:
        print(f"ОШИБКА: {e}")
    
    try:
        print("Пытаемся внести 0 рублей")
        acc.deposit(0)
    except Exception as e:
        print(f"ОШИБКА: {e}")

def demo_status_changes():
    """Демонстрация изменения статусов счета"""
    print_header("5. ДЕМОНСТРАЦИЯ ИЗМЕНЕНИЯ СТАТУСОВ")
    
    acc = BankAccount("Станислав Статусов", 50000, 0.04)
    print(f"Исходный статус: {acc.status}")
    
    print_subheader("Блокировка счета (block)")
    acc.block()
    print(f"  Статус после блокировки: {acc.status}")
    
    print_subheader("Попытка операции с заблокированным счетом")
    try:
        print("  Пытаемся снять 10000 рублей")
        acc.withdraw(10000)
    except Exception as e:
        print(f"  ОШИБКА: {e}")
    
    print_subheader("Активация счета (activate)")
    acc.activate()
    print(f"  Статус после активации: {acc.status}")
    
    print("Снимаем 10000 рублей после активации")
    acc.withdraw(10000)
    print(f"  Баланс: {acc.balance:.2f}")
    
    print_subheader("Подготовка к закрытию счета")
    print(f"  Снимаем остаток: {acc.balance:.2f}")
    acc.withdraw(acc.balance)
    
    print_subheader("Закрытие счета (close)")
    acc.close()
    print(f"  Статус после закрытия: {acc.status}")
    
    print_subheader("Попытка операции с закрытым счетом")
    try:
        print("  Пытаемся пополнить закрытый счет")
        acc.deposit(1000)
    except Exception as e:
        print(f"  ОШИБКА: {e}")

def demo_transfer():
    """Демонстрация перевода между счетами"""
    print_header("6. ДЕМОНСТРАЦИЯ ПЕРЕВОДА МЕЖДУ СЧЕТАМИ")
    
    acc_from = BankAccount("Отправитель Иванов", 50000, 0.03)
    acc_to = BankAccount("Получатель Петров", 10000, 0.04)
    
    print("Счета до перевода:")
    print(f"  Отправитель: {acc_from.balance:.2f}")
    print(f"  Получатель: {acc_to.balance:.2f}")
    
    print_subheader("Выполнение перевода 15000 рублей")
    try:
        acc_from.transfer_to(acc_to, 15000)
        print("  Перевод выполнен успешно")
    except Exception as e:
        print(f"ОШИБКА: {e}")
    
    print("\nСчета после перевода:")
    print(f"  Отправитель: {acc_from.balance:.2f}")
    print(f"  Получатель: {acc_to.balance:.2f}")
    
    print_subheader("Попытка перевода с недостаточным балансом")
    try:
        print("  Пытаемся перевести 100000 рублей")
        acc_from.transfer_to(acc_to, 100000)
    except Exception as e:
        print(f"  ОШИБКА: {e}")

def demo_magic_methods():
    """Демонстрация магических методов"""
    print_header("7. ДЕМОНСТРАЦИЯ МАГИЧЕСКИХ МЕТОДОВ")
    
    acc1 = BankAccount("Мария Соколова", 75000, 0.045)
    acc2 = BankAccount("Мария Соколова", 75000, 0.045)
    acc3 = BankAccount("Иван Крылов", 75000, 0.045)
    
    print_subheader("Метод __str__ (для пользователей)")
    print(str(acc1))
    
    print_subheader("Метод __repr__ (для разработчиков)")
    print(repr(acc1))
    
    print_subheader("Метод __eq__ (сравнение)")
    print(f"  acc1 == acc2: {acc1 == acc2} (разные номера)")
    print(f"  acc1 == acc3: {acc1 == acc3}")
    
    print_subheader("Метод __lt__ (сравнение по балансу)")
    acc4 = BankAccount("Богатый", 1000000)
    acc5 = BankAccount("Бедный", 1000)
    print(f"  Богатый (1000000) < Бедный (1000): {acc4 < acc5}")
    print(f"  Бедный (1000) < Богатый (1000000): {acc5 < acc4}")

def demo_class_attributes():
    """Демонстрация атрибутов класса"""
    print_header("8. ДЕМОНСТРАЦИЯ АТРИБУТОВ КЛАССА")
    
    print(f"Название банка (через класс): {BankAccount.bank_name}")
    
    print_subheader("Создание счетов и отслеживание счетчика")
    a1 = BankAccount("Клиент 1")
    print(f"  Номер первого счета: {a1.account_number}")
    a2 = BankAccount("Клиент 2")
    print(f"  Номер второго счета: {a2.account_number}")
    a3 = BankAccount("Клиент 3")
    print(f"  Номер третьего счета: {a3.account_number}")
    
    print_subheader("Доступ к атрибутам класса через экземпляры")
    print(f"  a1.bank_name: {a1.bank_name}")
    print(f"  a2.bank_name: {a2.bank_name}")
    
    print_subheader("Изменение атрибута класса")
    print(f"  Старое название: {BankAccount.bank_name}")
    BankAccount.bank_name = "Супер Банк"
    print(f"  Новое название (через класс): {BankAccount.bank_name}")
    print(f"  Новое название (через экземпляр a1): {a1.bank_name}")

def demo_validate_module():
    """Демонстрация работы модуля validate"""
    print_header("ДЕМОНСТРАЦИЯ МОДУЛЯ ВАЛИДАЦИИ")
    
    print_subheader("Проверка функций валидации")
    
    print("\n1. validate_name():")
    test_names = [
        ("Иван Петров", "корректное имя"),
        ("Анна", "слишком короткое"),
        ("Иван123", "с цифрами"),
        ("", "пустое"),
        ("   ", "только пробелы")
    ]
    for name, desc in test_names:
        valid, msg = validate.validate_name(name)
        print(f"  {desc:20} '{name}': {'✓' if valid else '✗'} {msg if not valid else ''}")
    
    print("\n2. validate_balance():")
    test_balances = [
        (1000, "корректный"),
        (-500, "отрицательный"),
        (15000000, "слишком большой"),
        ("1000", "не число")
    ]
    for bal, desc in test_balances:
        valid, msg = validate.validate_balance(bal)
        print(f"  {desc:15} {bal}: {'✓' if valid else '✗'} {msg if not valid else ''}")
    
    print("\n3. validate_interest_rate():")
    test_rates = [
        (0.05, "корректная"),
        (-0.1, "отрицательная"),
        (1.5, "больше 1"),
        ("0.1", "не число")
    ]
    for rate, desc in test_rates:
        valid, msg = validate.validate_interest_rate(rate)
        print(f"  {desc:12} {rate}: {'✓' if valid else '✗'} {msg if not valid else ''}")

def main():
    """Главная функция"""
    print("=" * 70)
    print(" ЛАБОРАТОРНАЯ РАБОТА №1")
    print(" Класс BankAccount - демонстрация всех возможностей")
    print("=" * 70)
    
    demo_creation()
    input("\nНажмите Enter для продолжения...")
    
    demo_validation()
    input("\nНажмите Enter для продолжения...")
    
    demo_properties()
    input("\nНажмите Enter для продолжения...")
    
    demo_operations()
    input("\nНажмите Enter для продолжения...")
    
    demo_status_changes()
    input("\nНажмите Enter для продолжения...")
    
    demo_transfer()
    input("\nНажмите Enter для продолжения...")
    
    demo_magic_methods()
    input("\nНажмите Enter для продолжения...")
    
    demo_class_attributes()
    input("\nНажмите Enter для продолжения...")
    
    demo_validate_module()
    
    print("\n" + "=" * 70)
    print(" ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("=" * 70)

if __name__ == "__main__":
    main()