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
def toDays(value):
    output = ""
    if value:
        for num in value:
            lists = [x.strip() for x in num.split(',')]
            for day in lists:
                if int(day) == 1:
                    output += "M,"
                if int(day) == 2:
                    output += "T,"
                if int(day) == 3:
                    output += "W,"
                if int(day) == 4:
                    output += "R,"
                if int(day) == 5:
                    output += "F1,"
                if int(day) == 6:
                    output += "F2,"
                if int(day) == 7:
                    output += "F3,"
                if int(day) == 8:
                    output += "F4,"
        return output[:-1]
    else:
        return value