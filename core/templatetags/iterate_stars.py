from django import template

register = template.Library()

@register.filter(name='filled_stars')
def _range(_num, args=None):
    result = ' ' * (_num)
    return result

@register.filter(name='blank_stars')
def _get_stars_left(_num, args=None):
    result = ' ' * (5 - _num)
    return result or ''