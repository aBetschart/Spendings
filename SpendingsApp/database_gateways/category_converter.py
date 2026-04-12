

from SpendingsApp.models import Category


class CategoryConverter:
    def convert_to_category(self, input) -> Category:
        try:
            category = self._try_convert_options(input)
        except:
            message = f"Cannot convert '{input}' to Category. Expected either a Category, an int, a str or a dict with 'id' or 'name' key."
            raise ValueError(message)
        
        return category
    
    def _try_convert_options(self, input) -> Category:
        try:
            return Category.objects.get(id=int(input))
        except:
            pass
        
        if isinstance(input, str):
            return Category.objects.get(name=input)
        
        if isinstance(input, dict):
            if 'id' in input:
                return Category.objects.get(id=input['id'])
            if 'name' in input:
                return Category.objects.get(name=input['name'])
        
        raise ValueError()