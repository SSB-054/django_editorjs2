from django.db import models
from django_editorjs2.fields import EditorJSField
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = EditorJSField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('django_editorjs2_blogapp:post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title