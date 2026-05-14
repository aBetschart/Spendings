
from typing import List
from datetime import date

import pytest

from SpendingsApp.filtering.spending_filtering.spending_filter_extractor import SpendingFilterExtractor
from SpendingsApp.filtering.spending_filtering.spending_filter_request_data import SpendingFilterRequestData



@pytest.fixture
def extractor() -> SpendingFilterExtractor:
    return SpendingFilterExtractor()

@pytest.fixture
def example_request_data() -> SpendingFilterRequestData:
    return get_example_request_data()

def get_example_request_data(
            start_date: str = "2025-01-01",
            end_date: str = "2025-12-31",
            category_ids: List[str] = [1, 2, 3],
            min_amount: float = 10.0,
            max_amount: float = 100.0,
            description: str = "Test description"
        ) -> SpendingFilterRequestData:
    return SpendingFilterRequestData(
        start_date=start_date,
        end_date=end_date,
        category_ids=category_ids,
        min_amount=min_amount,
        max_amount=max_amount,
        description=description
    )


def test_extract_shouldRaiseException_IfStartDateNotAvailable(extractor: SpendingFilterExtractor) -> None:
    request_data = get_example_request_data(start_date=None)
    with pytest.raises(ValueError):
        extractor.extract_filter_data(request_data)

def test_extract_shouldRaiseException_IfEndDateNotAvailable(extractor: SpendingFilterExtractor) -> None:
    request_data = get_example_request_data(end_date=None)
    with pytest.raises(ValueError):
        extractor.extract_filter_data(request_data)

@pytest.mark.parametrize("start_date_in", [
    "1-1-2025",
    "2025/01/01",
    "2025.01.01",
    "2025--01--01",
    "25-01-01",
])
def test_extract_shouldRaiseException_IfStartDateIsNotIsoFormat(extractor: SpendingFilterExtractor, start_date_in: str) -> None:
    request_data = get_example_request_data(start_date=start_date_in)

    with pytest.raises(ValueError):
        extractor.extract_filter_data(request_data)

@pytest.mark.parametrize("start_date_in, end_date_in, expected_start_date, expected_end_date", [
    ("2025-01-01", "2025-12-31", date(2025, 1, 1), date(2025, 12, 31)),
    ("2024-06-01", "2024-06-30", date(2024, 6, 1), date(2024, 6, 30)),
    ("1999-01-12", "2042-12-31", date(1999, 1, 12), date(2042, 12, 31))
])
def test_extract_shouldExtractRightDatesIfValid(extractor: SpendingFilterExtractor, start_date_in: str, end_date_in: str, expected_start_date: date, expected_end_date: date) -> None:
    request_data = get_example_request_data(start_date=start_date_in, end_date=end_date_in)
    
    filter_data = extractor.extract_filter_data(request_data)
    
    actual_date_range = filter_data.date_range
    actual_start = actual_date_range.start
    actual_end = actual_date_range.end
    assert expected_start_date == actual_start
    assert expected_end_date == actual_end


