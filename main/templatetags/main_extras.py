from django import template
from datetime import datetime
from django.utils.dateparse import parse_datetime


register = template.Library()

def get_value_from_dict(dict_data, key):
    """
    usage example {{ your_dict|get_value_from_dict:your_key }}
    """
    if key:
        return dict_data.get(key)
    
def calculate_next_month(year_month:str):
    year, month = year_month.split(' ')

    month = int(month)
    year = int(year)

    if month >= 12:
        return f'?year={year+1}&month={1}'
    
    return f'?year={year}&month={month + 1}'

def calculate_previous_month(year_month:str):
    year, month = year_month.split(' ')

    month = int(month)
    year = int(year)

    if month <= 1:
        return f'?year={year-1}&month={12}'
    
    return f'?year={year}&month={month - 1}'

def prettyfy_datetime(value):
    python_datetime = datetime.strftime(value, '%d %m %Y  %H:%M')

    return(python_datetime)


register.filter('calculate_previous_month', calculate_previous_month)  
register.filter('calculate_next_month', calculate_next_month)    
register.filter('get_value_from_dict', get_value_from_dict)
register.filter('prettyfy_datetime', prettyfy_datetime)

