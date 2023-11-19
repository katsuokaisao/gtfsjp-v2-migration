import re


japanese_postal_code_pattern = r'^\d{7}$'


def is_valid_japanese_postal_code(postal_code):
    return bool(re.match(japanese_postal_code_pattern, postal_code))