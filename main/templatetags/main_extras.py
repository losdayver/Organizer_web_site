from django import template

register = template.Library()

def get_value_from_dict(dict_data, key):
    """
    usage example {{ your_dict|get_value_from_dict:your_key }}
    """
    if key:
        return dict_data.get(key)
    
def test_if_divisible_by_7(value):
    if (value %7 == 0):
        return True
    
    return False
    
register.filter('get_value_from_dict', get_value_from_dict)
register.filter('test_if_divisible_by_7', test_if_divisible_by_7)

