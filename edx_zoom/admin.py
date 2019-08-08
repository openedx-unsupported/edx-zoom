"""
Django Admin for edx-zoom
"""
from __future__ import absolute_import, unicode_literals

from django.contrib import admin

from .models import LaunchLog, LTICredential


admin.site.register(LTICredential)


@admin.register(LaunchLog)
class LaunchLogAdmin(admin.ModelAdmin):
    readonly_fields = ('first_access', 'last_access', 'user')
    list_display = ('id',  'user', 'course_id', 'location', 'last_access')
