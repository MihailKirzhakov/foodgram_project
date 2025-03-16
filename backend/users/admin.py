from django.contrib import admin

from .models import Subscribe, UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
    ordering = ('username',)
    exclude = ('last_login',)


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Subscribe)
