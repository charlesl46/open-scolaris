from django.contrib import admin
from accounts.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ("__str__","role")

admin.site.register(User,UserAdmin)
