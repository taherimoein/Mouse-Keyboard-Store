from django import template
from datetime import datetime, date
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

# -------------------------------------------------------------------------------------------------------------------------------------

def currency(value):
    return '{:,}'.format(int(value))
register.filter('currency', currency)