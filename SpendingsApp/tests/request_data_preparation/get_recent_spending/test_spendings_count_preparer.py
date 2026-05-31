
import pytest

from SpendingsApp.request_data_preparation.get_recent_spending.spendings_count_preparer import SpendingsCountPreparer, DEFAULT_COUNT, MAX_COUNT


@pytest.fixture
def preparer() -> SpendingsCountPreparer:
    return SpendingsCountPreparer()


def test_extract_shouldReturnDefaultIfCountMissing(preparer: SpendingsCountPreparer) -> None:
    request_data = {}
    count = preparer.extract_spendings_count(request_data)

    expected = DEFAULT_COUNT
    assert expected == count

@pytest.mark.parametrize("count", [
    ("invalid"),
    ("test"),
    (-1),
    (-27),
    (MAX_COUNT + 1),
    (MAX_COUNT + 100),
])
def test_extract_shouldReturnDefaultCountIfInvalid(
        preparer: SpendingsCountPreparer, count: any) -> None:
    request_data = {"spendings_count": count}
    count = preparer.extract_spendings_count(request_data)

    expected = DEFAULT_COUNT
    assert expected == count


@pytest.mark.parametrize("input_count", [
    (1),
    (25),
    (MAX_COUNT),
    ("10"),
    ("99")
])
def test_extract_shouldReturnCountIfValid(preparer: SpendingsCountPreparer, input_count: any) -> None:
    request_data = {"spendings_count": input_count}
    actual = preparer.extract_spendings_count(request_data)

    expected = int(input_count)
    assert expected == actual