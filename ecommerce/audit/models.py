from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model

User = get_user_model()

class LogEntry(models.Model):
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    ]

    action_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='custom_log_entries')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='custom_log_entries')
    object_id = models.PositiveIntegerField()
    object_repr = models.CharField(max_length=200)
    action_flag = models.CharField(max_length=10, choices=ACTION_CHOICES)
    change_message = models.TextField(blank=True)

    object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Log Entry'
        verbose_name_plural = 'Log Entries'

    def __str__(self):
        return f'{self.action_time} - {self.user} - {self.action_flag} - {self.object_repr}'
