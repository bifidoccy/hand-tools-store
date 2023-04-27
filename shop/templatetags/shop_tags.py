from django import template

from shop.models import Category, Manufacturer

register = template.Library()

@register.simple_tag()
def get_categories():
    return Category.objects.all()

@register.simple_tag()
def get_manufacturers():
    return Manufacturer.objects.all()