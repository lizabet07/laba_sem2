"""
CLI интерфейс для консольного приложения
"""

from typing import Optional, Callable, Any
from .app import BankApp
from .exceptions import AccountNotFoundError, DuplicateAccountError, InvalidAccountDataError


def print_header(text: str) -> None:
    """Печатает заголовок."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_table(accounts: list, title: str = "Счета") -> None:
    """
    Выводит список счетов в виде форматированной таблицы.
    
    Args:
        accounts: Список объектов BankAccount
        title: Заголовок таблицы
    """
    if not accounts:
        print(f"\n{title}: нет счетов")
        return
    
    print(f"\n{title}:")
    print("-" * 80)
    print(f"{'Владелец':<20} {'Баланс':>12} {'Ставка':>8} {'Статус':<12} {'Тип':<15}")
    print("-" * 80)
    
    for acc in accounts:
        acc_type = acc.get_type() if hasattr(acc, 'get_type') else "Обычный"
        print(f"{acc.owner:<20} {acc.balance:>12.2f}₽ {acc.rate*100:>7.1f}% {acc.status:<12} {acc_type:<15}")
    
    print("-" * 80)
    print(f"Всего: {len(accounts)} счетов")


def print_account(account, title: str = "Информация о счёте") -> None:
    """Выводит информацию об одном счёте."""
    print(f"\n{title}:")
    print("-" * 50)
    print(f"  Владелец: {account.owner}")
    print(f"  Баланс: {account.balance:.2f}₽")
    print(f"  Ставка: {account.rate*100:.1f}%")
    print(f"  Статус: {account.status}")
    if hasattr(account, 'get_type'):
        print(f"  Тип: {account.get_type()}")
    if hasattr(account, 'account_number'):
        print(f"  Номер: {account.account_number}")
    print("-" * 50)


def get_input(prompt: str, validator: Optional[Callable] = None, error_msg: str = "Ошибка ввода") -> Any:
    """
    Получает ввод от пользователя с валидацией.
    
    Args:
        prompt: Текст приглашения
        validator: Функция для проверки ввода (опционально)
        error_msg: Сообщение об ошибке
        
    Returns:
        Введённое значение (преобразованное)
    """
    while True:
        try:
            value = input(prompt)
            if validator:
                value = validator(value)
            return value
        except ValueError as e:
            print(f"{error_msg}: {e}")


def get_float(prompt: str, min_val: float = None, max_val: float = None) -> float:
    """Получает вещественное число с проверкой диапазона."""
    def validate(value: str) -> float:
        num = float(value)
        if min_val is not None and num < min_val:
            raise ValueError(f"не может быть меньше {min_val}")
        if max_val is not None and num > max_val:
            raise ValueError(f"не может быть больше {max_val}")
        return num
    
    return get_input(prompt, validate, "Ошибка: введите число")


def get_choice(prompt: str, options: list) -> str:
    """Получает выбор из списка опций."""
    while True:
        choice = input(prompt).strip()
        if choice in options:
            return choice
        print(f"Ошибка: выберите из {options}")


def confirm_action(message: str) -> bool:
    """Запрашивает подтверждение действия."""
    response = input(f"{message} (y/n): ").strip().lower()
    return response == 'y' or response == 'да'


class BankCLI:
    """Класс CLI для работы с банковским приложением."""
    
    def __init__(self) -> None:
        """Инициализирует CLI и приложение."""
        self._app: BankApp = BankApp()
    
    def _show_main_menu(self) -> None:
        """Показывает главное меню."""
        print_header("БАНКОВСКАЯ СИСТЕМА")
        print("\n  1. Добавить счёт")
        print("  2. Показать все счета")
        print("  3. Найти счёт")
        print("  4. Удалить счёт")
        print("  5. Операции со счётом")
        print("  6. Сортировка")
        print("  7. Фильтрация")
        print("  8. Статистика")
        print("  0. Выход")
        print("-" * 30)
    
    def _add_account_flow(self) -> None:
        """Сценарий добавления счёта."""
        print_header("ДОБАВЛЕНИЕ СЧЁТА")
        
        print("\nТипы счетов:")
        print("  1. Обычный")
        print("  2. Накопительный")
        print("  3. Кредитный")
        print("  4. Премиум")
        
        account_type = get_choice("Выберите тип счёта (1-4): ", ["1", "2", "3", "4"])
        
        owner = get_input("Введите имя владельца: ")
        balance = get_float("Введите начальный баланс: ", min_val=0)
        rate = get_float("Введите процентную ставку (%): ", min_val=0, max_val=100) / 100
        
        params = {"owner": owner, "balance": balance, "rate": rate}
        
        if account_type == "2":  # Накопительный
            bonus_rate = get_float("Введите бонусную ставку (%): ", min_val=0) / 100
            min_term = int(get_float("Введите минимальный срок (месяцев): ", min_val=1))
            params["bonus_rate"] = bonus_rate
            params["min_term"] = min_term
        elif account_type == "3":  # Кредитный
            credit_limit = get_float("Введите кредитный лимит: ", min_val=0)
            interest_rate = get_float("Введите процентную ставку по кредиту (%): ", min_val=0) / 100
            params["credit_limit"] = credit_limit
            params["interest_rate"] = interest_rate
        elif account_type == "4":  # Премиум
            cashback_rate = get_float("Введите ставку кэшбэка (%): ", min_val=0) / 100
            service_level = int(get_float("Введите уровень обслуживания (1-10): ", min_val=1, max_val=10))
            params["cashback_rate"] = cashback_rate
            params["service_level"] = service_level
        
        try:
            account = self._app.add_account(account_type, **params)
            print_account(account, "Счёт успешно добавлен!")
        except (DuplicateAccountError, InvalidAccountDataError) as e:
            print(f"\nОшибка: {e}")
    
    def _show_all_accounts_flow(self) -> None:
        """Сценарий показа всех счетов."""
        accounts = self._app.get_all_accounts()
        print_table(accounts, "ВСЕ СЧЕТА")
    
    def _find_account_flow(self) -> None:
        """Сценарий поиска счёта."""
        print_header("ПОИСК СЧЁТА")
        
        print("\nПоиск по:")
        print("  1. Имени владельца")
        print("  2. Диапазону баланса")
        
        choice = get_choice("Выберите вариант (1-2): ", ["1", "2"])
        
        if choice == "1":
            owner = get_input("Введите имя владельца: ")
            account = self._app.find_account(owner)
            if account:
                print_account(account, "Счёт найден:")
            else:
                print(f"\nСчёт для {owner} не найден!")
        else:
            min_balance = get_float("Введите минимальный баланс: ", min_val=0)
            max_balance = get_float("Введите максимальный баланс: ", min_val=min_balance)
            accounts = self._app.find_accounts_by_balance(min_balance, max_balance)
            print_table(accounts, f"Счета с балансом от {min_balance} до {max_balance}")
    
    def _remove_account_flow(self) -> None:
        """Сценарий удаления счёта с подтверждением."""
        print_header("УДАЛЕНИЕ СЧЁТА")
        
        owner = get_input("Введите имя владельца счёта для удаления: ")
        account = self._app.find_account(owner)
        
        if not account:
            print(f"\nСчёт для {owner} не найден!")
            return
        
        print_account(account, "Найден счёт:")
        
        if confirm_action(f"Удалить счёт {owner}?"):
            try:
                removed = self._app.remove_account(owner)
                print(f"\nСчёт {removed.owner} успешно удалён!")
            except AccountNotFoundError as e:
                print(f"\nОшибка: {e}")
        else:
            print("\nУдаление отменено.")
    
    def _operations_flow(self) -> None:
        """Сценарий операций со счётом."""
        print_header("ОПЕРАЦИИ СО СЧЁТОМ")
        
        owner = get_input("Введите имя владельца: ")
        account = self._app.find_account(owner)
        
        if not account:
            print(f"\nСчёт для {owner} не найден!")
            return
        
        print_account(account, "Выбран счёт:")
        
        print("\nДоступные операции:")
        print("  1. Пополнить")
        print("  2. Снять")
        print("  3. Заблокировать")
        print("  4. Закрыть")
        
        choice = get_choice("Выберите операцию (1-4): ", ["1", "2", "3", "4"])
        
        try:
            if choice == "1":
                amount = get_float("Введите сумму пополнения: ", min_val=0.01)
                updated = self._app.deposit(owner, amount)
                print_account(updated, "Счёт после пополнения:")
            elif choice == "2":
                amount = get_float("Введите сумму снятия: ", min_val=0.01)
                updated = self._app.withdraw(owner, amount)
                print_account(updated, "Счёт после снятия:")
            elif choice == "3":
                if confirm_action(f"Заблокировать счёт {owner}?"):
                    updated = self._app.block_account(owner)
                    print_account(updated, "Счёт заблокирован:")
            elif choice == "4":
                if confirm_action(f"Закрыть счёт {owner}?"):
                    updated = self._app.close_account(owner)
                    print_account(updated, "Счёт закрыт:")
        except (AccountNotFoundError, ValueError) as e:
            print(f"\nОшибка: {e}")
    
    def _sort_flow(self) -> None:
        """Сценарий сортировки с выбором стратегии."""
        print_header("СОРТИРОВКА СЧЕТОВ")
        
        print("\nСортировать по:")
        print("  1. Балансу (возрастание)")
        print("  2. Балансу (убывание)")
        print("  3. Имени владельца (А-Я)")
        print("  4. Имени владельца (Я-А)")
        print("  5. Статусу")
        
        choice = get_choice("Выберите вариант (1-5): ", ["1", "2", "3", "4", "5"])
        
        sort_configs = {
            "1": (lambda a: a.balance, False),
            "2": (lambda a: a.balance, True),
            "3": (lambda a: a.owner, False),
            "4": (lambda a: a.owner, True),
            "5": (lambda a: a.status, False),
        }
        
        key_func, reverse = sort_configs[choice]
        sorted_accounts = self._app.sort_collection(key_func, reverse)
        
        order = "по возрастанию" if not reverse else "по убыванию"
        print_table(sorted_accounts, f"Счета, отсортированные {order}")
    
    def _filter_flow(self) -> None:
        """Сценарий фильтрации счетов."""
        print_header("ФИЛЬТРАЦИЯ СЧЕТОВ")
        
        print("\nФильтровать по:")
        print("  1. Статусу")
        print("  2. Типу счёта")
        print("  3. Диапазону баланса")
        
        choice = get_choice("Выберите вариант (1-3): ", ["1", "2", "3"])
        
        if choice == "1":
            print("\nСтатусы: активен, заблокирован, закрыт")
            status = get_input("Введите статус: ").lower()
            filtered = self._app.filter_by_status(status)
            print_table(filtered, f"Счета со статусом '{status}'")
        elif choice == "2":
            types = {
                "1": ("Обычный", lambda a: a.get_type() == "Обычный"),
                "2": ("Накопительный", lambda a: a.get_type() == "Накопительный"),
                "3": ("Кредитный", lambda a: a.get_type() == "Кредитный"),
                "4": ("Премиум", lambda a: a.get_type() == "Премиум"),
            }
            print("\nТипы счетов:")
            for key, (name, _) in types.items():
                print(f"  {key}. {name}")
            type_choice = get_choice("Выберите тип (1-4): ", ["1", "2", "3", "4"])
            type_name, predicate = types[type_choice]
            filtered = [a for a in self._app.get_all_accounts() if predicate(a)]
            print_table(filtered, f"Счета типа '{type_name}'")
        else:
            min_balance = get_float("Введите минимальный баланс: ", min_val=0)
            max_balance = get_float("Введите максимальный баланс: ", min_val=min_balance)
            filtered = self._app.find_accounts_by_balance(min_balance, max_balance)
            print_table(filtered, f"Счета с балансом от {min_balance} до {max_balance}")
    
    def _stats_flow(self) -> None:
        """Сценарий статистики."""
        print_header("СТАТИСТИКА")
        
        accounts = self._app.get_all_accounts()
        
        if not accounts:
            print("\nНет счетов для отображения статистики.")
            return
        
        total_balance = sum(a.balance for a in accounts)
        active_count = len(self._app.filter_by_status("активен"))
        blocked_count = len(self._app.filter_by_status("заблокирован"))
        closed_count = len(self._app.filter_by_status("закрыт"))
        
        # Статистика по типам
        type_stats = {}
        for a in accounts:
            t = a.get_type() if hasattr(a, 'get_type') else "Обычный"
            type_stats[t] = type_stats.get(t, 0) + 1
        
        print("\n" + "-" * 40)
        print(f"  Всего счетов: {len(accounts)}")
        print(f"  Общий баланс: {total_balance:.2f}₽")
        print(f"  Средний баланс: {total_balance/len(accounts):.2f}₽")
        print(f"  Активных: {active_count}")
        print(f"  Заблокированных: {blocked_count}")
        print(f"  Закрытых: {closed_count}")
        print("-" * 40)
        
        print("\nСтатистика по типам счетов:")
        for t, count in type_stats.items():
            print(f"  {t}: {count}")
    
    def run(self) -> None:
        """Запускает основной цикл CLI."""
        while True:
            self._show_main_menu()
            
            choice = get_choice("Выберите действие (0-8): ", ["0", "1", "2", "3", "4", "5", "6", "7", "8"])
            
            menu_actions = {
                "1": self._add_account_flow,
                "2": self._show_all_accounts_flow,
                "3": self._find_account_flow,
                "4": self._remove_account_flow,
                "5": self._operations_flow,
                "6": self._sort_flow,
                "7": self._filter_flow,
                "8": self._stats_flow,
            }
            
            if choice == "0":
                print("\nДо свидания!")
                break
            
            if choice in menu_actions:
                menu_actions[choice]()
    
    @property
    def app(self) -> BankApp:
        """Возвращает приложение (для доступа из main)."""
        return self._app