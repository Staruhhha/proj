from django import template

from django.template.defaultfilters import stringfilter

register = template.Library()


@register.simple_tag
def header_active_link_class():
    return "nav_link px-2 link-secondary"


@register.simple_tag()
def header_passive_link_class():
    return "nav-link px-2"


@register.simple_tag(name='head_link')
def header_link(curr_page, state):
    if curr_page == state:
        return header_active_link_class()
    return header_passive_link_class()


@register.filter()
def money_yag(value, currency_unit: str="RUB"):
    value = str(value)
    if currency_unit == "RUB":
        return value + " ₽"
    elif currency_unit == "USD":
        return value + " $"
    elif currency_unit == "EUR":
        return value + " €"
    else:
        return value

@register.simple_tag()
def show_tags(item):
    tags = item.tag.all()
    return {"tags": tags}


@register.inclusion_tag("_inc/_tags.html")
def show_tags_inclusion(item):
    tags = item.tag.all()
    return {"tags": tags}

