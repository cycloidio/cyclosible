from django.contrib import admin
from .models import AppVersion


class AppVersionAdmin(admin.ModelAdmin):
    list_display = ('playbook', 'application', 'version', 'env', 'deployed')

admin.site.register(AppVersion, AppVersionAdmin)
