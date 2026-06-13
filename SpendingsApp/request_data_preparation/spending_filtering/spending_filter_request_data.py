from dataclasses import dataclass
from typing import List, Optional

@dataclass(frozen=True)
class SpendingFilterRequestData:
    start_date: str
    end_date: str
    user: any

    min_amount: Optional[str]
    max_amount: Optional[str]
    description: Optional[str]
    category_ids: Optional[List[str]]
