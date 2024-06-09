from django.contrib import admin
from .models import LogEntry

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'object_repr', 'action_flag', 'change_message')
    search_fields = ('object_repr', 'action_flag')
    list_filter = ('action_flag', 'action_time')

admin.site.register(LogEntry, LogEntryAdmin)
