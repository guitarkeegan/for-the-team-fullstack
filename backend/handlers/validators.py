import re
from datetime import datetime
from flask import jsonify

def validate_date_range(start_date, end_date):
    """
    Validate the format and logic of a date range.

    Args:
        start_date (str): The start date in 'YYYY-MM-DD' format.
        end_date (str): The end date in 'YYYY-MM-DD' format.

    Returns:
        tuple: (bool, dict or None)
            - bool: True if validation passes, False otherwise.
            - dict: Error message if validation fails, None if it passes.
    """
    # Validate date format
    date_pattern = r'^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])$'
    if not re.match(date_pattern, start_date) or not re.match(date_pattern, end_date):
        return False, {"error": "Invalid date format. Please use 'YYYY-MM-DD'."}

    # Convert strings to datetime objects for comparison
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return False, {"error": "Invalid date. Please check the day and month values."}

    # Check if end date is not before start date
    if end < start:
        return False, {"error": "End date cannot be before start date."}

    return True, None

def validate_month_format(month):
    """
    Validate the format of a month string.

    Args:
        month (str): The month string in 'YYYY-MM' format.

    Returns:
        tuple: (bool, dict or None)
            - bool: True if validation passes, False otherwise.
            - dict: Error message if validation fails, None if it passes.
    """
    if not re.match(r'^\d{4}-(?:0[1-9]|1[0-2])$', month):
        return False, {"error": "Invalid month format. Please use 'YYYY-MM'."}
    return True, None