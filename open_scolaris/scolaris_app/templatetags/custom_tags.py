from datetime import datetime
import locale
from scolaris_app.models import CanteenMenu
from django import template

register = template.Library()

@register.simple_tag
def get_now():
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    now = datetime.now()
    date_formatee = now.strftime("%H:%M - %A %e %B %Y")
    locale.setlocale(locale.LC_TIME, '')
    return date_formatee

@register.simple_tag
def menu_today():
    today = datetime.now()
    try:
        canteen_menu = CanteenMenu.objects.get(date=today)
    except CanteenMenu.DoesNotExist:
        canteen_menu = None
    return canteen_menu
