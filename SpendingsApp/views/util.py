

from typing import Dict, List
from django.forms.models import model_to_dict

from SpendingsApp.models import Category, Spending

# Spending related

def calculate_total(spendings: List[Spending]) -> float:
    sum = 0
    for spending in spendings:
        sum += spending.amount
    return sum

def convert_spendings_to_dict(spendings: List[Spending]) -> List[Dict[str, any]]:
    dicts: List[Dict[str, any]] = []
    for spending in spendings:
        spending_dict = convert_spending_to_dict(spending)
        dicts.append(spending_dict)
    return dicts

def convert_spending_to_dict(spending: Spending) -> Dict[str, any]:
    spending_dict = model_to_dict(spending)
    spending_dict['category'] = model_to_dict(spending.category)
    spending_dict['entryDate'] = spending.entryDate
    return spending_dict

def does_spending_exist(id: int) -> bool:
    return Spending.objects.filter(pk=id).exists()

def get_spending_from_id(id: int) -> Spending:
    try:
        return Spending.objects.get(pk=id)
    except Spending.DoesNotExist:
        raise ValueError(f"Spending with id {id} does not exist.")


# Category related

def get_category_from_id(id: int) -> Category:
    try:
        return Category.objects.get(pk=id)
    except Category.DoesNotExist:
        raise ValueError(f"Category with id {id} does not exist.")
    
def is_category_used(category: Category) -> bool:
    return category.spending_set.exists()

def is_category_name_used(name: str) -> bool:
    return Category.objects.filter(name=name).exists()