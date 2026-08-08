

from dataclasses import dataclass
from typing import List, Optional

from SpendingsApp.finance.user_data import UserData
from SpendingsApp.utils.date_range import DateRange

@dataclass(frozen=True)
class AmountRange:
    min: float
    max: float

    def __post_init__(self) -> None:
        if self.min < 0 or self.max < 0:
            raise ValueError("Amount cannot be negative")
        if self.min > self.max:
            raise ValueError("min amount cannot be greater than max amount")

@dataclass(frozen=True)
class SpendingFilterData:
    user: UserData
    date_range: DateRange
    category_ids: List[int]
    amount_range: AmountRange
    description: str
    