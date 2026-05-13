"""
Лабораторная работа №6 - Generics и typing (оценка 5)
"""

from typing import TypeVar, Generic, Callable, Optional, List, Protocol

# ========== ПРОТОКОЛЫ ==========
class Displayable(Protocol):
    def display(self) -> str: ...

class Scorable(Protocol):
    def score(self) -> float: ...

# ========== TYPEVAR ==========
D = TypeVar('D', bound=Displayable)
S = TypeVar('S', bound=Scorable)
T = TypeVar('T')
R = TypeVar('R')

# ========== GENERIC-КОЛЛЕКЦИЯ ==========
class TypedCollection(Generic[T]):
    def __init__(self) -> None:
        self._items: List[T] = []
    
    def add(self, item: T) -> 'TypedCollection[T]':
        self._items.append(item)
        return self
    
    def remove(self, item: T) -> 'TypedCollection[T]':
        self._items.remove(item)
        return self
    
    def get_all(self) -> List[T]:
        return self._items.copy()
    
    def sort_by(self, key_func: Callable[[T], any], reverse: bool = False) -> 'TypedCollection[T]':
        self._items.sort(key=key_func, reverse=reverse)
        return self
    
    def filter_by(self, predicate: Callable[[T], bool]) -> 'TypedCollection[T]':
        filtered = [item for item in self._items if predicate(item)]
        result = TypedCollection[T]()
        result._items = filtered
        return result
    
    # Методы для оценки 4
    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        for item in self._items:
            if predicate(item):
                return item
        return None
    
    def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        return [item for item in self._items if predicate(item)]
    
    def map(self, transform: Callable[[T], R]) -> List[R]:
        return [transform(item) for item in self._items]
    
    def __len__(self) -> int:
        return len(self._items)
    
    def __getitem__(self, index: int) -> T:
        return self._items[index]
    
    def __iter__(self):
        return iter(self._items)


# ========== КЛАССЫ ИЗ ЛР-1 И ЛР-3 (с аннотациями) ==========
class BankAccount:
    def __init__(self, owner: str, balance: float, rate: float = 0.05) -> None:
        self._owner: str = owner
        self._balance: float = balance
        self._rate: float = rate
        self._status: str = "активен"
        self._number: str = f"ACC-{id(self)}"
    
    @property
    def owner(self) -> str: return self._owner
    @property
    def balance(self) -> float: return self._balance
    @property
    def status(self) -> str: return self._status
    
    def get_owner(self) -> str: return self._owner
    def get_balance(self) -> float: return self._balance
    def get_type(self) -> str: return "Обычный"
    
    def block(self) -> None: self._status = "заблокирован"
    def close(self) -> None: self._status = "закрыт"
    
    def display(self) -> str:  # Для протокола Displayable
        return f"{self._number}: {self._owner} | {self._balance:.2f}₽ | {self._status}"
    
    def score(self) -> float:  # Для протокола Scorable
        return self._balance
    
    def __str__(self) -> str: return self.display()


class SavingsAccount(BankAccount):
    def __init__(self, owner: str, balance: float, rate: float, bonus_rate: float, min_term: int) -> None:
        super().__init__(owner, balance, rate)
        self._bonus_rate = bonus_rate
    
    def get_type(self) -> str: return "Накопительный"
    
    def display(self) -> str:
        return f"{super().display()} | накопительный"


class CreditAccount(BankAccount):
    def __init__(self, owner: str, balance: float, rate: float, credit_limit: float, interest: float) -> None:
        super().__init__(owner, balance, rate)
        self._credit_limit = credit_limit
    
    def withdraw(self, amount: float) -> float:
        if amount > self._balance + self._credit_limit:
            raise ValueError("Превышен кредитный лимит")
        self._balance -= amount
        return self._balance
    
    def get_type(self) -> str: return "Кредитный"
    
    def display(self) -> str:
        return f"{super().display()} | кредитный"


class PremiumAccount(BankAccount):
    def __init__(self, owner: str, balance: float, rate: float, cashback: float, level: int) -> None:
        super().__init__(owner, balance, rate)
        self._cashback_rate = cashback
    
    def get_type(self) -> str: return "Премиум"
    
    def display(self) -> str:
        return f"{super().display()} | премиум (кэшбэк {self._cashback_rate*100:.1f}%)"