import re
import logging



""" params: name - a string in camelCase """
def camel_to_snake(name):
    """Convert camelCase to snake_case"""
    s1 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return s1.lower()

""" params: data - a dictionary with keys in camelCase """
def convert_json_keys_to_snake_case(data):
    """Convert all keys in a dictionary to snake_case"""
    return {camel_to_snake(k): v for k, v in data.items()}

def check_contract_type(contract_type):
    if contract_type == 'Two-Way':
        return 'TWO_WAY'
    return contract_type