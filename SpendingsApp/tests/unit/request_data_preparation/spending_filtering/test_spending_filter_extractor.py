
import sys
import pytest
from unittest.mock import Mock
from typing import List
from datetime import date

from SpendingsApp.finance.user_data import UserData
from SpendingsApp.request_data_preparation.spending_filtering.spending_filter_data import AmountRange
from SpendingsApp.request_data_preparation.spending_filtering.spending_filter_extractor import SpendingFilterExtractor
from SpendingsApp.request_data_preparation.spending_filtering.spending_filter_request_data import SpendingFilterRequestData
from SpendingsApp.request_data_preparation.user_converter import UserConverter


@pytest.fixture
def user_converter_mock() -> Mock:
    mock = Mock(spec=UserConverter)
    mock.convert_to_user.return_value = UserData(id=12, name="name")
    return mock
    

@pytest.fixture
def extractor(user_converter_mock: Mock) -> SpendingFilterExtractor:
    return SpendingFilterExtractor(user_converter_mock)

@pytest.fixture
def example_request_data() -> SpendingFilterRequestData:
    return get_example_request_data()

def get_example_request_data(
            start_date: str = "2025-01-01",
            end_date: str = "2025-12-31",
            category_ids: List[str] = [1, 2, 3],
            min_amount: float = 10.0,
            max_amount: float = 100.0,
            description: str = "Test description",
            user: any = 100,
        ) -> SpendingFilterRequestData:
    return SpendingFilterRequestData(
        start_date=start_date,
        end_date=end_date,
        category_ids=category_ids,
        min_amount=min_amount,
        max_amount=max_amount,
        description=description,
        user=user
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
def test_extract_shouldRaiseException_IfStartDateIsNotIsoFormat(
        extractor: SpendingFilterExtractor, 
        start_date_in: str) -> None:
    request_data = get_example_request_data(start_date=start_date_in)

    with pytest.raises(ValueError):
        extractor.extract_filter_data(request_data)

@pytest.mark.parametrize("start_date_in, end_date_in, expected_start_date, expected_end_date", [
    ("2025-01-01", "2025-12-31", date(2025, 1, 1), date(2025, 12, 31)),
    ("2024-06-01", "2024-06-30", date(2024, 6, 1), date(2024, 6, 30)),
    ("1999-01-12", "2042-12-31", date(1999, 1, 12), date(2042, 12, 31))
])
def test_extract_shouldExtractRightDates_IfValid(extractor: SpendingFilterExtractor, start_date_in: str, end_date_in: str, expected_start_date: date, expected_end_date: date) -> None:
    request_data = get_example_request_data(start_date=start_date_in, end_date=end_date_in)
    
    filter_data = extractor.extract_filter_data(request_data)
    
    actual_date_range = filter_data.date_range
    actual_start = actual_date_range.start
    actual_end = actual_date_range.end
    assert expected_start_date == actual_start
    assert expected_end_date == actual_end

@pytest.mark.parametrize("category_ids, expected_ids", [
    (["1", "2", "3", 4], [1, 2, 3, 4]),
    ([10, 20], [10, 20]),
    (["100"], [100])
])
def test_extract_shouldExtractRightCategoryIds_IfValid(extractor: SpendingFilterExtractor, category_ids: List[any], expected_ids: List[int]) -> None:
    request_data = get_example_request_data(category_ids=category_ids)

    filter_data = extractor.extract_filter_data(request_data)

    actual_ids = filter_data.category_ids
    assert expected_ids == actual_ids


def test_extract_shouldReturnEmptyCategoryIds_IfNotAvailable(extractor: SpendingFilterExtractor) -> None:
    request_data = get_example_request_data(category_ids=None)

    filter_data = extractor.extract_filter_data(request_data)

    actual_ids = filter_data.category_ids
    assert [] == actual_ids

@pytest.mark.parametrize("category_ids", [
    ([1, 2, "abc"]),
    (["x"]),
    (["20.5", 12])
])
def test_extract_shouldRaiseException_IfCategoryIdNotParsable(extractor: SpendingFilterExtractor, category_ids: List[any]) -> None:
    request_data = get_example_request_data(category_ids=category_ids)

    with pytest.raises(ValueError):
        extractor.extract_filter_data(request_data)


@pytest.mark.parametrize("min_amount, max_amount, expected_range", [
    (10, 100, AmountRange(min=10.0, max=100.0)),
    (0, 55.5, AmountRange(min=0.0, max=55.5)),
    (7.25, 7.3, AmountRange(min=7.25, max=7.3)),
    (None, 33, AmountRange(min=0, max=33)),
    (0.5, None, AmountRange(min=0.5, max=sys.float_info.max)),
    (None, None, None)
])
def test_extract_shouldExtractRightAmountRangeIfAvailable(
        extractor: SpendingFilterExtractor, 
        min_amount: float, 
        max_amount: float,
        expected_range: AmountRange) -> None:
    request_data = get_example_request_data(min_amount=min_amount, max_amount=max_amount)

    filter_data = extractor.extract_filter_data(request_data)

    actual_range = filter_data.amount_range
    assert expected_range == actual_range

@pytest.mark.parametrize("min_amount, max_amount", [
    ("abc", 100),
    (12.5, "xyz"),
    ("zero", "hundred"),
])
def test_extract_shouldRaiseException_IfAmountIsInvalid(
        extractor: SpendingFilterExtractor, 
        min_amount: float, 
        max_amount: float) -> None:
    request_data = get_example_request_data(min_amount=min_amount, max_amount=max_amount)

    with pytest.raises(ValueError) as error:
        extractor.extract_filter_data(request_data)

    actual_message = str(error.value)
    assert actual_message.startswith("Could not convert amount:")

def test_extract_shouldNotSetAmountsIfNotAvailable(extractor: SpendingFilterExtractor) -> None:
    request_data = get_example_request_data(min_amount=None, max_amount=None)

    filter_data = extractor.extract_filter_data(request_data)

    actual_range = filter_data.amount_range
    assert actual_range is None
        
@pytest.mark.parametrize("description", [
    "Test description",
    "Another description",
    "",
    None
])
def test_extract_shouldSetDescription(extractor: SpendingFilterExtractor, description: str) -> None:
    request_data = get_example_request_data(description=description)

    filter_data = extractor.extract_filter_data(request_data)

    expected = description
    actual = filter_data.description
    assert expected == actual

def test_extract_shouldRaiseExceptionIfUserIsNotAvailable(extractor: SpendingFilterExtractor) -> None:
    request_data = get_example_request_data(user=None)

    with pytest.raises(ValueError) as error:
        extractor.extract_filter_data(request_data)

    expected = "Missing required field: user."
    actual = str(error.value)
    assert expected == actual

@pytest.mark.parametrize("error_message", [
    "test123",
    "ERROR!!!",
    "Can not convert :(",
])
def test_extract_shouldRaiseExceptionIfUserNotConvertable(
        extractor: SpendingFilterExtractor, 
        user_converter_mock: Mock,
        error_message: str) -> None:
    request_data = get_example_request_data()
    user_converter_mock.convert_to_user.side_effect = Exception(error_message)

    with pytest.raises(Exception) as error:
        extractor.extract_filter_data(request_data)
        
    expected = error_message
    actual = str(error.value)
    assert expected == actual
    
@pytest.mark.parametrize("user", [
    UserData(id=20, name="gna gna"),
    20,
    "some username",
])
def test_extract_shouldUseRightUserToConvert(
        extractor: SpendingFilterExtractor, user_converter_mock: Mock, user: any) -> None:
    request_data = get_example_request_data(user=user)

    extractor.extract_filter_data(request_data)

    assert 1 == user_converter_mock.convert_to_user.call_count

    call_args = user_converter_mock.convert_to_user.call_args.args
    assert 1 == len(call_args)

    expected = user
    actual = call_args[0]
    assert expected == actual

@pytest.mark.parametrize("user_data", [
    UserData(id=20, name="gna gna"),
    UserData(id=1, name="Hello world"),
    UserData(id=5987, name="some funny name"),
])
def test_extract_shouldReturnRightUserData(
        extractor: SpendingFilterExtractor, 
        user_converter_mock: Mock, 
        user_data: UserData) -> None:
    request_data = get_example_request_data()
    user_converter_mock.convert_to_user.return_value = user_data

    filter_data = extractor.extract_filter_data(request_data)

    expected = user_data
    actual = filter_data.user
    assert expected == actual

