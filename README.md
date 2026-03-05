# Лабораторная работа №1: Банковская система 4 вариант
## Цель работы

- Освоить объявление пользовательских классов
- Разобраться с инкапсуляцией (закрытые поля)
- Реализовать свойства (`@property`)
- Переопределить магические методы (`__str__`, `__repr__`, `__eq__`)
- Понять разницу между атрибутами класса и экземпляра

## Реализованные классы
**AccountStatus**
```python
class AccountStatus(Enum):
    ACTIVE = "активен"
    BLOCKED = "заблокирован"
    CLOSED = "закрыт"
    FROZEN = "заморожен"
```
Хранит возможные статусы банковского счета. Использование Enum предотвращает ошибки с опечатками в строках.

**BankAccount**
```python
class BankAccount:
    # Атрибуты класса
    BANK_NAME = "Python Bank"
    MIN_BALANCE = 0.0
    MAX_BALANCE = 10_000_000.0
```
Главный класс, моделирующий банковский счет. Содержит всю логику работы со счетом.

*Атрибуты:*

~_account_number — уникальный номер счета

~_owner_name — ФИО владельца

~_balance — текущий баланс

~_status — статус (из AccountStatus)

~ _interest_rate — процентная ставка

~ _opening_date — дата открытия

*Методы:*

~ deposit(amount) — внесение денег

~ withdraw(amount) — снятие денег

~ transfer_to(target, amount) — перевод на другой счет

~ calculate_interest() — расчет процентов

~ apply_interest() — начисление процентов

~ activate()/block()/freeze()/close() — управление статусом

**Transaction**
```python
class Transaction:
    def __init__(self, from_account, to_account, amount):
```
Представляет банковскую транзакцию (перевод). Хранит информацию о переводе между счетами.

*Атрибуты:*

~ from_account — счет отправителя

~ to_account — счет получателя

~ amount — сумма перевода

~ timestamp — дата и время

~ status — статус (pending/completed/failed)

*Методы:*

~ execute() — выполнить транзакцию
**Client**
```python
class Client:
    def __init__(self, full_name, passport, phone, email):
```
Моделирует клиента банка. Связывает все счета, кредиты и вклады одного человека.

*Атрибуты:*

~ _client_id — уникальный ID клиента

~ _full_name — полное имя

~ _passport — паспортные данные

~ _phone — телефон

~ _email — email

~ _accounts — список счетов

~ _credits — список кредитов

~ _deposits — список вкладов

*Методы:*

~ add_account(acc) — добавить счет

~ add_credit(cr) — добавить кредит

~ add_deposit(dp) — добавить вклад

~ total_balance — общий баланс по всем счетам
**Credit**
```python
class Credit:
    def __init__(self, client, amount, rate, term):
```
Моделирует банковский кредит с расчетом ежемесячных платежей.

*Атрибуты:*

~ _credit_id — ID кредита

~ _amount — сумма кредита

~ _interest_rate — процентная ставка

~ _term_months — срок в месяцах

~ _remaining — остаток долга

~ _status — статус кредита

*Методы:*

~ monthly_payment() — расчет ежемесячного платежа

~ total_payment() — общая сумма к выплате

~ overpayment() — переплата по кредиту

~ make_payment(amount) — внести платеж

**Deposit**
```python
class Deposit:
    def __init__(self, client, amount, rate, term, capitalization):
```
Моделирует банковский вклад с возможностью капитализации процентов.

*Атрибуты:*

~ _deposit_id — ID вклада
 
~ _amount — сумма вклада

~ _interest_rate — процентная ставка

~ _term_months — срок в месяцах

~ _capitalization — флаг капитализации

~ _current — текущая сумма (с процентами)

*Методы:*

~ calculate_income() — расчет дохода

~ total_at_maturity() — сумма в конце срока

~ apply_monthly_interest() — ежемесячное начисление процентов

~ prolong(months) — продление вклада



**Дополнительные Enum классы**
```python
class TransactionType(Enum):
    DEPOSIT = "пополнение"
    WITHDRAWAL = "снятие"
    TRANSFER = "перевод"
    INTEREST = "начисление %"

class TransactionStatus(Enum):
    PENDING = "ожидает"
    COMPLETED = "выполнена"
    FAILED = "ошибка"
    CANCELLED = "отменена"

class CreditStatus(Enum):
    ACTIVE = "активен"
    APPROVED = "одобрен"
    PAID = "погашен"
    OVERDUE = "просрочен"
    REJECTED = "отказано"

class DepositStatus(Enum):
    ACTIVE = "активен"
    CLOSED = "закрыт"
    PROLONGED = "продлен"
```
 ## Демонстрация работы
В файле demo.py реализовано 9 сценариев, показывающих все возможности:

**Сценарий 1: Создание счетов**
```python
def demonstrate_creation():
    print_header("1. СОЗДАНИЕ БАНКОВСКИХ СЧЕТОВ")
    
    # Создание счета с параметрами по умолчанию
    print_subheader("Создание счета с параметрами по умолчанию")
    acc1 = BankAccount("Иван Петров")
    print(acc1)
    print(f"Дата открытия: {acc1.opening_date.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Создание счета с начальным балансом и ставкой
    print_subheader("Создание счета с начальным балансом 10000 и ставкой 5%")
    acc2 = BankAccount("Анна Сидорова", 10000.0, 0.05)
    print(acc2)
    
    # Создание счета с большим балансом
    print_subheader("Создание счета с балансом 500000")
    acc3 = BankAccount("Петр Иванов", 500000.0, 0.03)
    print(acc3)
    
    return acc1, acc2, acc3
```
Создание счета с параметрами по умолчанию

Создание счета с начальным балансом 10000 и ставкой 5%

Создание счета с балансом 500000

**Сценарий 2: Валидация (обработка ошибок)**
```python
def demonstrate_validation_errors():
    """Демонстрация обработки ошибок валидации"""
    print_header("2. ДЕМОНСТРАЦИЯ ВАЛИДАЦИИ (ОБРАБОТКА ОШИБОК)")
    
    # Ошибка в имени
    print_subheader("Попытка создать счет с некорректным именем")
    test_cases = [
        ("", "пустое имя"),
        ("   ", "имя из пробелов"),
        ("A", "слишком короткое имя"),
        ("Иван123", "имя с цифрами"),
        ("Иван!@#", "имя со спецсимволами"),
        ("Иван Петров Сидорович Алекс" * 5, "слишком длинное имя")
    ]
    
    for name, description in test_cases:
        try:
            print(f"\nТест: {description}")
            acc = BankAccount(name)
            print(f"Успешно создан: {acc.owner_name}")
        except (ValueError, TypeError) as e:
            print(f"Ошибка: {e}")
    
    # Ошибка в балансе
    print_subheader("Попытка создать счет с некорректным балансом")
    try:
        print("\nПопытка создать счет с отрицательным балансом -1000")
        acc = BankAccount("Тест Тестов", -1000.0)
    except ValueError as e:
        print(f"Ошибка: {e}")
    
    try:
        print("\nПопытка создать счет с балансом 20_000_000 (превышение MAX_BALANCE)")
        acc = BankAccount("Тест Тестов", 20_000_000.0)
    except ValueError as e:
        print(f"Ошибка: {e}")
    
    # Ошибка в процентной ставке
    print_subheader("Попытка создать счет с некорректной процентной ставкой")
    try:
        print("\nПопытка создать счет со ставкой 1.5 (> 1)")
        acc = BankAccount("Тест Тестов", 1000.0, 1.5)
    except ValueError as e:
        print(f"Ошибка: {e}")
    
    try:
        print("\nПопытка создать счет с отрицательной ставкой -0.1")
        acc = BankAccount("Тест Тестов", 1000.0, -0.1)
    except ValueError as e:
        print(f"Ошибка: {e}")
```
Некорректные имена (пустые, короткие, с цифрами)

Отрицательный баланс

Превышение максимального баланса

Некорректная процентная ставка

**Сценарий 3: Свойства (геттеры/сеттеры)**
```python
def demonstrate_properties_and_setters():
    """Демонстрация свойств и сеттеров"""
    print_header("3. ДЕМОНСТРАЦИЯ СВОЙСТВ (GETTERS/SETTERS)")
    
    acc = BankAccount("Михаил Демин", 50000.0, 0.04)
    print("Исходный счет:")
    print(acc)
    
    # Демонстрация геттеров
    print_subheader("Чтение свойств (геттеры)")
    print(f"Номер счета (read-only): {acc.account_number}")
    print(f"Владелец: {acc.owner_name}")
    print(f"Баланс (read-only): {acc.balance}")
    print(f"Ставка: {acc.interest_rate}")
    print(f"Статус: {acc.status.value}")
    print(f"Дней с открытия: {acc.days_since_opened}")
    
    # Демонстрация сеттеров
    print_subheader("Изменение свойств через сеттеры")
    
    # Изменение имени
    try:
        print("\nИзменяем имя владельца на 'Демин Михаил Сергеевич'")
        acc.owner_name = "Демин Михаил Сергеевич"
        print(f"Новое имя: {acc.owner_name}")
    except ValueError as e:
        print(f"Ошибка: {e}")
    
    # Изменение процентной ставки
    try:
        print("\nИзменяем процентную ставку на 6.5%")
        acc.interest_rate = 0.065
        print(f"Новая ставка: {acc.interest_rate * 100}%")
    except ValueError as e:
        print(f"Ошибка: {e}")
    
    # Попытка изменить баланс через прямое обращение
    print_subheader("Попытка прямого изменения баланса")
    try:
        print("Пытаемся: acc.balance = 100000")
        acc.balance = 100000  # Это вызовет ошибку
    except AttributeError as e:
        print(f"Ошибка: {e} - баланс доступен только для чтения")
    
    print("\nИтоговое состояние счета:")
    print(acc)

```
Чтение всех свойств

Изменение имени владельца

Изменение процентной ставки

Попытка изменения баланса (ошибка)

**Сценарий 4: Банковские операции**
```python
def demonstrate_operations():
    """Демонстрация банковских операций"""
    print_header("4. ДЕМОНСТРАЦИЯ БАНКОВСКИХ ОПЕРАЦИЙ")
    
    acc = BankAccount("Олег Операторов", 100000.0, 0.05)
    print("Начальное состояние:")
    print(acc)
    
    # Внесение средств
    print_subheader("Внесение средств (deposit)")
    try:
        print("Вносим 25000 рублей")
        new_balance = acc.deposit(25000.0)
        print(f"Новый баланс: {new_balance:,.2f}")
    except (ValueError, PermissionError) as e:
        print(f"Ошибка: {e}")
    
    # Снятие средств
    print_subheader("Снятие средств (withdraw)")
    try:
        print("Снимаем 15000 рублей")
        new_balance = acc.withdraw(15000.0)
        print(f"Новый баланс: {new_balance:,.2f}")
    except (ValueError, PermissionError) as e:
        print(f"Ошибка: {e}")
    
    # Попытка снять больше чем есть
    print_subheader("Попытка снять больше баланса")
    try:
        print("Пытаемся снять 200000 рублей")
        acc.withdraw(200000.0)
    except ValueError as e:
        print(f"Ошибка: {e}")
    
    # Расчет и начисление процентов
    print_subheader("Расчет и начисление процентов")
    interest = acc.calculate_interest()
    print(f"Сумма процентов к начислению: {interest:.2f}")
    
    print("Начисляем проценты")
    new_balance = acc.apply_interest()
    print(f"Баланс после начисления процентов: {new_balance:,.2f}")
    
    # Некорректные операции
    print_subheader("Некорректные операции")
    try:
        print("Пытаемся внести отрицательную сумму -5000")
        acc.deposit(-5000.0)
    except ValueError as e:
        print(f"Ошибка: {e}")
    
    try:
        print("Пытаемся внести 0 рублей")
        acc.deposit(0.0)
    except ValueError as e:
        print(f"Ошибка: {e}")
```
Внесение средств

Снятие средств

Попытка снять больше баланса (ошибка)

Расчет и начисление процентов

Некорректные операции (отрицательная сумма, ноль)

**Сценарий 5: Изменение статусов**
```python
def demonstrate_status_changes():
    """Демонстрация изменения статусов счета"""
    print_header("5. ДЕМОНСТРАЦИЯ ИЗМЕНЕНИЯ СТАТУСОВ")
    
    acc = BankAccount("Станислав Статусов", 50000.0, 0.04)
    print("Исходный статус:")
    print(f"Статус: {acc.status.value}")
    
    # Блокировка счета
    print_subheader("Блокировка счета (block)")
    acc.block()
    print(f"Статус после блокировки: {acc.status.value}")
    
    # Попытка операции с заблокированным счетом
    print_subheader("Попытка операции с заблокированным счетом")
    try:
        print("Пытаемся снять 10000 рублей")
        acc.withdraw(10000.0)
    except PermissionError as e:
        print(f"Ошибка: {e}")
    
    # Активация счета
    print_subheader("Активация счета (activate)")
    acc.activate()
    print(f"Статус после активации: {acc.status.value}")
    
    # Проверка, что операции снова доступны
    print("Снимаем 10000 рублей после активации")
    new_balance = acc.withdraw(10000.0)
    print(f"Операция выполнена. Новый баланс: {new_balance:,.2f}")
    
    # Заморозка счета
    print_subheader("Заморозка счета (freeze)")
    acc.freeze()
    print(f"Статус после заморозки: {acc.status.value}")
    
    # Попытка операции с замороженным счетом
    try:
        print("Пытаемся внести 20000 рублей")
        acc.deposit(20000.0)
    except PermissionError as e:
        print(f"Ошибка: {e}")
    
    # Активация и подготовка к закрытию
    print_subheader("Подготовка к закрытию счета")
    acc.activate()
    print(f"Счет активирован. Баланс: {acc.balance}")
    
    # Снятие всех средств
    print(f"Снимаем {acc.balance} рублей")
    acc.withdraw(acc.balance)
    print(f"Баланс после снятия: {acc.balance}")
    
    # Закрытие счета
    print_subheader("Закрытие счета (close)")
    acc.close()
    print(f"Статус после закрытия: {acc.status.value}")
    
    # Попытка операции с закрытым счетом
    try:
        print("Пытаемся выполнить операцию с закрытым счетом")
        acc.deposit(1000.0)
    except PermissionError as e:
        print(f"Ошибка: {e}")
```
Блокировка счета

Операция с заблокированным счетом (ошибка)

Активация счета

Заморозка счета

Операция с замороженным счетом (ошибка)

Снятие всех средств и закрытие счета

Операция с закрытым счетом (ошибка)

**Сценарий 6: Переводы между счетами**
```python
def demonstrate_transfer():
    """Демонстрация перевода между счетами"""
    print_header("6. ДЕМОНСТРАЦИЯ ПЕРЕВОДА МЕЖДУ СЧЕТАМИ")
    
    # Создаем счета
    acc_from = BankAccount("Отправитель Иванов", 50000.0, 0.03)
    acc_to = BankAccount("Получатель Петров", 10000.0, 0.04)
    
    print("Счета до перевода:")
    print(f"Отправитель:\n{acc_from}")
    print(f"\nПолучатель:\n{acc_to}")
    
    # Выполняем перевод
    print_subheader("Выполнение перевода 15000 рублей")
    try:
        acc_from.transfer_to(acc_to, 15000.0)
        print("Перевод выполнен успешно")
    except (ValueError, PermissionError) as e:
        print(f"Ошибка: {e}")
    
    print("\nСчета после перевода:")
    print(f"Отправитель:\n{acc_from}")
    print(f"\nПолучатель:\n{acc_to}")
    
    # Попытка перевода с недостаточным балансом
    print_subheader("Попытка перевода с недостаточным балансом")
    try:
        print("Пытаемся перевести 100000 рублей")
        acc_from.transfer_to(acc_to, 100000.0)
    except ValueError as e:
        print(f"Ошибка: {e}")
    
    # Перевод с использованием класса Transaction
    print_subheader("Перевод с использованием класса Transaction")
    trans = Transaction(acc_from, acc_to, 5000.0)
    print("Создана транзакция:")
    print(trans)
    
    print("\nВыполняем транзакцию...")
    if trans.execute():
        print("Транзакция выполнена успешно")
        print(trans)
        print(f"\nБаланс отправителя: {acc_from.balance:.2f}")
        print(f"Баланс получателя: {acc_to.balance:.2f}")
    else:
        print("Ошибка выполнения транзакции")
```
Перевод 15000 рублей

Перевод с недостаточным балансом (ошибка)

Использование класса Transaction

**Сценарий 7: Магические методы**
```python
def demonstrate_magic_methods():
    """Демонстрация магических методов"""
    print_header("7. ДЕМОНСТРАЦИЯ МАГИЧЕСКИХ МЕТОДОВ")
    
    # Создаем счета
    acc1 = BankAccount("Мария Соколова", 75000.0, 0.045)
    acc2 = BankAccount("Мария Соколова", 75000.0, 0.045)  # Разные номера
    acc3 = BankAccount("Иван Крылов", 75000.0, 0.045)
    
    # __str__
    print_subheader("Метод __str__ (для пользователей)")
    print(str(acc1))
    
    # __repr__
    print_subheader("Метод __repr__ (для разработчиков)")
    print(repr(acc1))
    
    # __eq__
    print_subheader("Метод __eq__ (сравнение)")
    print(f"acc1 == acc2: {acc1 == acc2} (разные номера счетов)")
    print(f"acc1 == acc3: {acc1 == acc3}")
    
    # __lt__
    print_subheader("Метод __lt__ (сравнение по балансу)")
    acc4 = BankAccount("Богатый", 1000000.0)
    acc5 = BankAccount("Бедный", 1000.0)
    print(f"Богатый баланс: {acc4.balance}")
    print(f"Бедный баланс: {acc5.balance}")
    print(f"Богатый < Бедный: {acc4 < acc5}")
    print(f"Бедный < Богатый: {acc5 < acc4}")
    
    # Сортировка с использованием __lt__
    accounts = [acc5, acc3, acc1, acc4, acc2]
    print("\nСортировка счетов по балансу:")
    sorted_accounts = sorted(accounts)
    for i, acc in enumerate(sorted_accounts, 1):
        print(f"{i}. {acc.owner_name}: {acc.balance:,.2f}")
```
__str__ (пользовательский вывод)

__repr__ (отладочный вывод)

__eq__ (сравнение счетов)

__lt__ (сравнение по балансу)

Сортировка счетов

**Сценарий 8: Атрибуты класса**
```python
def demonstrate_class_attributes():
    """Демонстрация атрибутов класса"""
    print_header("8. ДЕМОНСТРАЦИЯ АТРИБУТОВ КЛАССА")
    
    print(f"Название банка (через класс): {BankAccount.BANK_NAME}")
    print(f"Минимальный баланс: {BankAccount.MIN_BALANCE}")
    print(f"Максимальный баланс: {BankAccount.MAX_BALANCE}")
    
    # Создаем несколько счетов
    print_subheader("Создание счетов и отслеживание счетчика")
    
    print("Создаем счет 1")
    acc1 = BankAccount("Клиент 1")
    print(f"Текущий счетчик: {BankAccount._next_account_number}")
    
    print("Создаем счет 2")
    acc2 = BankAccount("Клиент 2")
    print(f"Текущий счетчик: {BankAccount._next_account_number}")
    
    print("Создаем счет 3")
    acc3 = BankAccount("Клиент 3")
    print(f"Текущий счетчик: {BankAccount._next_account_number}")
    
    # Доступ через экземпляры
    print_subheader("Доступ к атрибутам класса через экземпляры")
    print(f"acc1.BANK_NAME: {acc1.BANK_NAME}")
    print(f"acc2.MIN_BALANCE: {acc2.MIN_BALANCE}")
    print(f"acc3.MAX_BALANCE: {acc3.MAX_BALANCE}")
    
    # Изменение атрибута класса
    print_subheader("Изменение атрибута класса")
    print(f"Старое название банка: {BankAccount.BANK_NAME}")
    BankAccount.BANK_NAME = "Python Bank Premium"
    print(f"Новое название банка (через класс): {BankAccount.BANK_NAME}")
    print(f"Новое название банка (через acc1): {acc1.BANK_NAME}")
    print(f"Новое название банка (через acc2): {acc2.BANK_NAME}")
```
Доступ через класс

Доступ через экземпляр

Изменение атрибута класса

**Сценарий 9: Сложный сценарий**
```python
def demonstrate_complex_scenario():
    """Демонстрация сложного сценария работы с несколькими счетами"""
    print_header("9. СЛОЖНЫЙ СЦЕНАРИЙ: РАБОТА С НЕСКОЛЬКИМИ СЧЕТАМИ")
    
    # Создаем семейный портфель счетов
    print("Создаем семейный портфель счетов:")
    
    father = BankAccount("Игорь Петров", 500000.0, 0.04)
    mother = BankAccount("Елена Петрова", 300000.0, 0.045)
    son = BankAccount("Алексей Петров", 50000.0, 0.05)
    family_savings = BankAccount("Семейный фонд", 1000000.0, 0.06)
    
    print("Счета созданы")
    
    # Выводим информацию о счетах
    print_subheader("Информация о всех счетах")
    for i, acc in enumerate([father, mother, son, family_savings], 1):
        print(f"\n{i}. {acc.owner_name}")
        print(f"   Баланс: {acc.balance:,.2f}")
        print(f"   Ставка: {acc.interest_rate*100:.1f}%")
    
    # Выполняем несколько операций
    print_subheader("Серия операций")
    
    # Отец переводит сыну на учебу
    print("\n1. Отец переводит сыну 30000 на учебу")
    father.transfer_to(son, 30000.0)
    print(f"   Баланс отца: {father.balance:,.2f}")
    print(f"   Баланс сына: {son.balance:,.2f}")
    
    # Мать пополняет семейный фонд
    print("\n2. Мать пополняет семейный фонд на 50000")
    mother.transfer_to(family_savings, 50000.0)
    print(f"   Баланс матери: {mother.balance:,.2f}")
    print(f"   Баланс фонда: {family_savings.balance:,.2f}")
    
    # Сын платит за обучение (снятие)
    print("\n3. Сын оплачивает обучение 40000")
    son.withdraw(40000.0)
    print(f" Баланс сына: {son.balance:,.2f}")
    
    # Начисляем проценты по всем счетам
    print_subheader("Начисление процентов по всем счетам")
    accounts = [father, mother, son, family_savings]
    total_interest = 0
    
    for acc in accounts:
        interest = acc.calculate_interest()
        if interest > 0:
            acc.apply_interest()
            total_interest += interest
            print(f"{acc.owner_name}: начислено {interest:.2f}, баланс {acc.balance:,.2f}")
    
    print(f"\ Всего начислено процентов: {total_interest:,.2f}")
```
Семейный портфель счетов

Переводы между членами семьи

Начисление процентов

Подсчет общего состояния

![Картинка 1](./images/lab01/image01.png) ![Картинка 1](./images/lab01/image02.png)
![Картинка 1](./images/lab01/image03.png) ![Картинка 1](./images/lab01/image04.png)
![Картинка 1](./images/lab01/image05.png) ![Картинка 1](./images/lab01/image06.png)
![Картинка 1](./images/lab01/image07.png) ![Картинка 1](./images/lab01/image08.png)
![Картинка 1](./images/lab01/image09.png) ![Картинка 1](./images/lab01/image10.png)