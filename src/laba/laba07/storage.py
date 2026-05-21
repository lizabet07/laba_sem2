"""
Сохранение и загрузка коллекции в JSON-файл
"""

import json
import os
from typing import List, Dict, Any
from datetime import datetime

from .exceptions import StorageError
from .models import BankAccount, SavingsAccount, CreditAccount, PremiumAccount


def account_to_dict(account: BankAccount) -> Dict[str, Any]:
    """
    Преобразует объект счёта в словарь для JSON.
    
    Args:
        account: Объект банковского счёта
        
    Returns:
        Словарь с данными счёта
    """
    data = {
        "type": account.get_type(),
        "owner": account.owner,
        "balance": account.balance,
        "rate": account.rate,
        "status": account.status,
        "number": account.account_number if hasattr(account, 'account_number') else None
    }
    
    # Добавляем специфичные поля для разных типов счетов
    if isinstance(account, SavingsAccount):
        data["bonus_rate"] = account._bonus_rate
        data["min_term"] = account._min_term
    elif isinstance(account, CreditAccount):
        data["credit_limit"] = account._credit_limit
        data["interest_rate"] = account._interest_rate
    elif isinstance(account, PremiumAccount):
        data["cashback_rate"] = account._cashback_rate
        data["service_level"] = account._service_level
    
    return data


def dict_to_account(data: Dict[str, Any]) -> BankAccount:
    """
    Восстанавливает объект счёта из словаря.
    
    Args:
        data: Словарь с данными счёта
        
    Returns:
        Восстановленный объект банковского счёта
    """
    account_type = data.get("type", "Обычный")
    owner = data["owner"]
    balance = data["balance"]
    rate = data["rate"]
    
    if account_type == "Накопительный":
        return SavingsAccount(
            owner, balance, rate,
            data.get("bonus_rate", 0.02),
            data.get("min_term", 3)
        )
    elif account_type == "Кредитный":
        return CreditAccount(
            owner, balance, rate,
            data.get("credit_limit", 50000),
            data.get("interest_rate", 0.15)
        )
    elif account_type == "Премиум":
        return PremiumAccount(
            owner, balance, rate,
            data.get("cashback_rate", 0.02),
            data.get("service_level", 1)
        )
    else:
        account = BankAccount(owner, balance, rate)
        if data.get("status") == "заблокирован":
            account.block()
        elif data.get("status") == "закрыт":
            account.close()
        return account


def save_collection(collection, filepath: str) -> None:
    """
    Сохраняет коллекцию в JSON-файл.
    
    Args:
        collection: Коллекция счетов (должна иметь метод get_all)
        filepath: Путь к файлу для сохранения
        
    Raises:
        StorageError: При ошибке записи в файл
    """
    try:
        data = [account_to_dict(acc) for acc in collection.get_all()]
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        raise StorageError(f"Ошибка сохранения: {e}")


def load_collection(collection, filepath: str) -> int:
    """
    Загружает данные из JSON-файла в коллекцию.
    
    Args:
        collection: Коллекция для загрузки (должна иметь метод add)
        filepath: Путь к файлу для загрузки
        
    Returns:
        Количество загруженных счетов
        
    Raises:
        StorageError: При ошибке чтения файла
    """
    if not os.path.exists(filepath):
        return 0
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        count = 0
        for item in data:
            try:
                account = dict_to_account(item)
                collection.add(account)
                count += 1
            except Exception:
                continue
        
        return count
    except Exception as e:
        raise StorageError(f"Ошибка загрузки: {e}")