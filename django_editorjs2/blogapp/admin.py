from django.contrib import admin
from .models import Post
from django.forms import JSONField

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    formfield_overrides = {
        "content": {"widget": JSONField()}
    }