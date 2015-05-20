from django.contrib import admin

from timed_auth_token.models import TimedAuthToken


@admin.register(TimedAuthToken)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created', 'last_used', 'expires',)
    fields = ('user',)
    ordering = ('-last_used',)
