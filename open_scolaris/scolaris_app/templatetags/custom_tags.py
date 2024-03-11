from django.utils import timezone
from scolaris_app.models import CanteenMenu
from django import template
import locale

register = template.Library()


@register.simple_tag
def menu_today():
    today = timezone.now()
    try:
        canteen_menu = CanteenMenu.objects.get(date=today)
    except CanteenMenu.DoesNotExist:
        canteen_menu = None
    return canteen_menu
