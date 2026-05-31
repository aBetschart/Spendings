
DEFAULT_COUNT: int = 10
MAX_COUNT: int = 100
COUNT_KEY: str = "spendings_count"

class SpendingsCountPreparer:

    def extract_spendings_count(self, request_data: dict[str, any]) -> int:
        if COUNT_KEY not in request_data:
            return DEFAULT_COUNT

        try:
            count = int(request_data[COUNT_KEY])
        except (TypeError, ValueError):
            return DEFAULT_COUNT
        
        if count < 1 or count > MAX_COUNT:
            return DEFAULT_COUNT

        return count
    