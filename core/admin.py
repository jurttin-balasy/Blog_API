from django.contrib import admin

# Register your models here.
from . import models

@admin.register(models.Post)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('author', 'created_at')