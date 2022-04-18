from django import template
from news.resources.constants import CENS_CORE

register = template.Library()


@register.filter(name='censor')
def censor(value):
    for word in CENS_CORE:
        while word in value:
            value = value.replace(word, '***')

    return value


@register.filter(name='update_page')
def update_page(full_path:str, page:int):
    try:
        params_list = full_path.split('?')[1].split('&')
        params = dict([tuple(str(param).split('=')) for param  in params_list])
        params.update({'page': page})
        link = ''
        for key, value in params.items():
            link += (f"{key}={value}&")
        return link[:-1]
    except:
        return f"page={page}"
