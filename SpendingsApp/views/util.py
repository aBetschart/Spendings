

from SpendingsApp.models import Category


def get_category_from_id(id: int) -> Category:
    try:
        return Category.objects.get(pk=id)
    except Category.DoesNotExist:
        raise ValueError(f"Category with id {id} does not exist.")
    
def is_category_used(category: Category) -> bool:
    return category.spending_set.exists()

def is_category_name_used(name: str) -> bool:
    return Category.objects.filter(name=name).exists()