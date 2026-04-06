from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class DateRange:
    start: date
    end: date

    def __post_init__(self) -> None:
        if self.start > self.end:
            raise ValueError("start date cannot be after end date")
        
    def __eq__(self, value):
        if not isinstance(value, DateRange):
            return False
        return self.start == value.start and self.end == value.end
    
    def __str__(self):
        return f"DateRange(start={self.start}, end={self.end})"
