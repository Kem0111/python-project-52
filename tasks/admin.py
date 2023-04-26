from django.contrib import admin

# Register your models here.
from .models import Tasks


class TasksAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'author')
    list_display_links = ('name',)
    search_fields = ('name',)


admin.site.register(Tasks, TasksAdmin)
