import re


color_pattern = r'^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'


def is_valid_color(color_code):
    color_code = color_code.replace('#', '')
    if re.match(color_pattern, color_code):
        return True
    else:
        return False
