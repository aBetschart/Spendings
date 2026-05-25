

import pytest

from typing import Dict
from unittest.mock import Mock

from SpendingsApp.finance.category_data import CategoryData
from SpendingsApp.request_data_preparation.category_converter import CategoryConverter
from SpendingsApp.request_data_preparation.monthly_average.monthly_average_data_preparer import MonthlyAverageDataPreparer

@pytest.fixture
def category_converter_mock() -> CategoryConverter:
    mock = Mock(spec=CategoryConverter)
    mock.convert_to_category.return_value = CategoryData(id=1, name="Test Category")
    return mock

@pytest.fixture
def data_preparer(category_converter_mock: Mock) -> MonthlyAverageDataPreparer:
    return MonthlyAverageDataPreparer(category_converter_mock)

def get_example_request_data(year: int = 2020, category: str = "Test Category") -> Dict[str, any]:
    return {"year": year, "category": category}

def test_extract_shouldRaiseException_IfYearIsMissing(data_preparer: MonthlyAverageDataPreparer) -> None:
    request_data = {"category": "Test Category"}
    with pytest.raises(ValueError) as error:
        data_preparer.extract_average_data(request_data)

        expected = "Missing required field: year"
        actual = str(error)
        assert expected == actual


@pytest.mark.parametrize("year", [
    ("invalid"),
    ("test"),
    (-1),
    (-202),
    ("-2025")
])
def test_extract_shouldRaiseExceptionIfYearInvalid(
        data_preparer: MonthlyAverageDataPreparer, year: any) -> None:
    request_data = get_example_request_data(year=year)
    with pytest.raises(ValueError) as error:
        data_preparer.extract_average_data(request_data)
    
    expected = "Invalid year format: expected an integer greater than or equal to 0."
    assert expected == str(error.value)

@pytest.mark.parametrize("year", [
    (2020),
    (0),
    (9999)
])
def test_extract_shouldReturnRightYearIfValid(
            data_preparer: MonthlyAverageDataPreparer, year: int) -> None:
    request_data = get_example_request_data(year=year)
    
    average_request_data = data_preparer.extract_average_data(request_data)
    
    expected = year
    actual = average_request_data.year
    assert expected == actual


@pytest.mark.parametrize("category_input", [
    ("Test Category"),
    ("Another Category"),
    ({"id": 1, "name": "some category"})
])
def test_extract_shouldConvertCategory(
        data_preparer: MonthlyAverageDataPreparer, 
        category_converter_mock: Mock,
        category_input: any) -> None:
    request_data = get_example_request_data(category=category_input)

    data_preparer.extract_average_data(request_data)

    assert 1 == category_converter_mock.convert_to_category.call_count
    call_args = category_converter_mock.convert_to_category.call_args.args
    assert 1 == len(call_args)
    expected = category_input
    actual = call_args[0]
    assert expected == actual


def test_extract_shouldNotConvertCategoryIfNone(
        data_preparer: MonthlyAverageDataPreparer, 
        category_converter_mock: Mock) -> None:
    request_data = get_example_request_data(category=None)

    with pytest.raises(ValueError) as error:
        data_preparer.extract_average_data(request_data)

    assert 0 == category_converter_mock.convert_to_category.call_count
    expected = "Missing required field: category"
    actual = str(error.value)
    assert expected == actual


@pytest.mark.parametrize("category_data",[
    CategoryData(id=1, name="Test Category"),
    CategoryData(id=202, name="Another Category"),
    CategoryData(id=55, name="Some Category")
])
def test_extract_shouldReturnRightCategory(
        data_preparer: MonthlyAverageDataPreparer, 
        category_converter_mock: Mock,
        category_data: CategoryData) -> None:
    category_converter_mock.convert_to_category.return_value = category_data
    request_data = get_example_request_data()

    average_request_data = data_preparer.extract_average_data(request_data)

    expected = category_data
    actual = average_request_data.category
    assert expected == actual

@pytest.mark.parametrize("error_message", [
    "Some error",
    "Invalid category",
    "Conversion failed"
])
def test_extract_shouldRaiseExceptionIfCategoryInvalid(
        data_preparer: MonthlyAverageDataPreparer, 
        category_converter_mock: Mock,
        error_message: str) -> None:
    category_converter_mock.convert_to_category.side_effect = ValueError(error_message)

    request_data = get_example_request_data()
    with pytest.raises(ValueError) as error:
        data_preparer.extract_average_data(request_data)

    expected = error_message
    actual = str(error.value)
    assert expected == actual
