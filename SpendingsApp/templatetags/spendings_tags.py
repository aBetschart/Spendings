import math
from django.template.library import Library

register = Library()

@register.filter(name="split_to_group_size")
def split_to_group_size(value, arg):
    try:
        group_size = int(arg)
    except:
        type = type(arg)
        raise TypeError(f"Argument needs to be an integer, but was {type}")
    
    try:
        length = len(value)
    except:
        raise TypeError("Value must have a length")
    
    if group_size > length:
        message = f"Group size {group_size} must be smaller than length {length}"
        raise ValueError(message)

    division = float(length) / group_size
    group_count = int(math.ceil(division))

    splitted_value = []
    for group_index in range(0, group_count - 1):
        first_elem = group_index * group_size
        last_elem = first_elem + group_size - 1
        group = value[first_elem:last_elem + 1]
        splitted_value.append(group)

    first_elem = (group_count - 1) * group_size
    last_elem = length - 1
    last_group = value[first_elem:last_elem + 1]
    splitted_value.append(last_group)

    
    return splitted_value


