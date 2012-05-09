from django import template
from operator import itemgetter

register = template.Library()

@register.filter
def multiply(value, arg):
    return int(value) * int(arg)

@register.filter
def truncatewords_by_chars(value, arg):
    """Truncate the text when it exceeds a certain number of characters.
    Delete the last word only if partial.
    Adds '...' at the end of the text.
    
    Example:
    
        {{ text|truncatewords_by_chars:25 }}
    """
    try:
        length = int(arg)
    except ValueError:
        return value
    
    if len(value) > length:
        if value[length:length + 1].isspace():
            return value[:length].rstrip() + '...'
        else:
            return value[:length].rsplit(' ', 1)[0].rstrip() + '...'
    else:
        return value

@register.filter
def toDays(value,prd):
    output = ""
    if value:
        for num, period in zip(value, prd):
            lists = [x.strip() for x in num.split(',')]
            output += period +": "
            for day in lists:
                try:
                    if int(day) == 1:
                        output += "M, "
                except ValueError:
                    return Value
                try:
                    if int(day) == 2:
                        output += "T, "
                except ValueError:
                    return Value
                try:
                    if int(day) == 3:
                        output += "W, "
                except ValueError:
                    return Value
                try:
                    if int(day) == 4:
                        output += "R, "
                except ValueError:
                    return Value
                try:
                    if int(day) == 5:
                        output += "F1, "
                except ValueError:
                    return Value
                try:
                    if int(day) == 6:
                        output += "F2, "
                except ValueError:
                    return Value
                try:
                    if int(day) == 7:
                        output += "F3, "
                except ValueError:
                    return Value
                try:
                    if int(day) == 8:
                        output += "F4, "
                except ValueError:
                    return Value

            output = output[:-2] + "<br /><br />"
        return output[:-12]
    else:
        return value