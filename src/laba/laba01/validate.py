"""
Модуль с функциями валидации для лабораторной работы №1
"""

def validate_name(name):
    """
    Проверка имени владельца счета
    
    Параметры:
        name: имя для проверки
        
    Возвращает:
        (bool, str): (True, "OK") если имя корректно, иначе (False, описание ошибки)
    """
    if not isinstance(name, str):
        return False, "Имя должно быть строкой"
    
    name = name.strip()
    if not name:
        return False, "Имя не может быть пустым"
    
    if len(name) < 5:
        return False, "Имя должно содержать минимум 5 символов"
    
    if len(name) > 50:
        return False, "Имя слишком длинное (макс. 50 символов)"
    
    # Проверяем, что имя состоит из букв и пробелов
    for c in name:
        if not (c.isalpha() or c.isspace()):
            return False, "Имя может содержать только буквы и пробелы"
    
    return True, "OK"


def validate_balance(balance):
    """
    Проверка баланса счета
    
    Параметры:
        balance: баланс для проверки
        
    Возвращает:
        (bool, str): (True, "OK") если баланс корректен, иначе (False, описание ошибки)
    """
    if not isinstance(balance, (int, float)):
        return False, "Баланс должен быть числом"
    
    if balance < 0:
        return False, "Баланс не может быть отрицательным"
    
    if balance > 10000000:
        return False, "Баланс не может превышать 10 миллионов"
    
    return True, "OK"


def validate_interest_rate(rate):
    """
    Проверка процентной ставки
    
    Параметры:
        rate: ставка для проверки
        
    Возвращает:
        (bool, str): (True, "OK") если ставка корректна, иначе (False, описание ошибки)
    """
    if not isinstance(rate, (int, float)):
        return False, "Процентная ставка должна быть числом"
    
    if rate < 0:
        return False, "Процентная ставка не может быть отрицательной"
    
    if rate > 1:
        return False, "Процентная ставка не может быть больше 1 (100%)"
    
    return True, "OK"


def validate_amount(amount, operation="операция"):
    """
    Проверка суммы операции
    
    Параметры:
        amount: сумма для проверки
        operation: название операции (для сообщения об ошибке)
        
    Возвращает:
        (bool, str): (True, "OK") если сумма корректна, иначе (False, описание ошибки)
    """
    if not isinstance(amount, (int, float)):
        return False, f"Сумма {operation} должна быть числом"
    
    if amount <= 0:
        return False, f"Сумма {operation} должна быть положительной"
    
    if amount > 10000000:
        return False, f"Сумма {operation} не может превышать 10 миллионов"
    
    return True, "OK"


def validate_transfer_target(target):
    """
    Проверка получателя перевода
    
    Параметры:
        target: объект-получатель
        
    Возвращает:
        (bool, str): (True, "OK") если получатель корректен, иначе (False, описание ошибки)
    """
    # Импортируем здесь, чтобы избежать циклических импортов
    from model import BankAccount
    
    if not isinstance(target, BankAccount):
        return False, "Получатель должен быть банковским счетом"
    
    return True, "OK"


def validate_status_for_operation(status, operation):
    """
    Проверка статуса счета для выполнения операции
    
    Параметры:
        status: текущий статус
        operation: название операции
        
    Возвращает:
        (bool, str): (True, "OK") если операция разрешена, иначе (False, описание ошибки)
    """
    if status == "закрыт":
        return False, f"Нельзя {operation}: счет закрыт"
    
    if status == "заблокирован":
        return False, f"Нельзя {operation}: счет заблокирован"
    
    return True, "OK"


def validate_withdrawal(balance, amount):
    """
    Проверка возможности снятия средств
    
    Параметры:
        balance: текущий баланс
        amount: запрашиваемая сумма
        
    Возвращает:
        (bool, str): (True, "OK") если снятие возможно, иначе (False, описание ошибки)
    """
    if amount > balance:
        return False, f"Недостаточно средств. Доступно: {balance:.2f}"
    
    return True, "OK"


def validate_close(balance):
    """
    Проверка возможности закрытия счета
    
    Параметры:
        balance: текущий баланс
        
    Возвращает:
        (bool, str): (True, "OK") если закрытие возможно, иначе (False, описание ошибки)
    """
    if balance != 0:
        return False, f"Нельзя закрыть счет с деньгами. Баланс: {balance:.2f}"
    
    return True, "OK"