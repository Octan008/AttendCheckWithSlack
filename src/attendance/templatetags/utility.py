from django import template

import os
register = template.Library()


@register.filter(name='domain')
def domain():
    # return str(os.environ.get('SERVER_DOMAIN'))
    return "あいう"
