from .views import EditorJsAttachments
from django.urls import path

app_name = 'django_editorjs2'

urlpatterns = [
    path('attachments/', EditorJsAttachments.as_view(), name='attachments'),
]