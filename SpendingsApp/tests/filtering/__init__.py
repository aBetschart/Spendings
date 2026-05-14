import pytest

from SpendingsApp.filtering.spending_filtering.spending_filter_extractor import SpendingFilterExtractor
from SpendingsApp.filtering.spending_filtering.spending_filter_request_data import SpendingFilterRequestData


@pytest.fixture
def filter_extractor() -> SpendingFilterExtractor:
    return SpendingFilterExtractor()

@pytest.fixture
def example_request_data() -> SpendingFilterRequestData:
    return SpendingFilterRequestData(
        start_date="2025-01-01",
        end_date="2025-12-31",
        min_amount="10.00",
        max_amount="100.00",
        categories=["1", "2", "3"],
        description="Test Description"
    )