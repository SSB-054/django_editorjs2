# django_editorjs2
A Django app that seamlessly integrates EditorJS, a powerful block-styled editor with a clean, intuitive interface.


# Django EditorJS2

A Django app that seamlessly integrates [EditorJS](https://editorjs.io/), a powerful block-styled editor with a clean, intuitive interface.

## Features

- Easy integration with Django projects
- Full support for EditorJS block-style editing
- Customizable configuration
- File upload and preprocessing capabilities
- Extensible with custom preprocessors and callbacks

## Requirements

- Python 3.8+
- Django 3.2+

## Installation

### 1. Install the Package

```bash
pip install django-editorjs2
```

### 2. Configure Django Settings

Add `django_editorjs2` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'django_editorjs2',
    ...
]
```

### 3. Configure URL Routing

In your project's `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    ...
    path('editorjs/', include('django_editorjs2.urls')),
    ...
]
```

### 4. Configure Media and Static Files

Ensure your `MEDIA_URL` and `STATIC_URL` are properly configured in `settings.py`.

### 5. Run Migrations

```bash
python manage.py migrate
python manage.py collectstatic
```


### 6. Add static tag
```html
<head>
....
{{form.media}}
....
</head>
```

## Configuration

### Advanced Configuration Options

In your `settings.py`, you can customize the EditorJS2 behavior:

```python
DJANGO_EDITORJS2_CONFIG = {
    # Preprocessors for preview generation
    "image_link_preprocessor": "django_editorjs2.blogapp.utils.image_link_preprocessor",
    "download_link_preprocessor": "django_editorjs2.blogapp.utils.download_link_preprocessor",
    
    # Custom styling and attributes for different block types
    "extra_attributes": {
        "list": {"style": "list-style: none"},
        "checklist": {"style": "list-style: none"},
        "paragraph": {},
        "header": {},
        "quote": {},
        "code": {},
        "image": {},
        "embed": {},
        "table": {},
        "delimiter": {},
        "attaches": {},
    },
    
    # before saving the file, djanog model object EditorJsUploadFiles is passed to this function
    "callback_before_file_save": "django_editorjs2.blogapp.utils.callback_before_file_save",
    # before returning the response, the response object is passed to this function
    "callback_before_return_response": "django_editorjs2.blogapp.utils.callback_before_return_response",
    
    # widget
    "editorjs_field_preview_callback": "django_editorjs2.blogapp.utils.editorjs_field_preview_callback",
    "editorjs_field_save_callback": "django_editorjs2.blogapp.utils.editorjs_field_save_callback",

    "max_attachment_size_bytes": 5 * 1024 * 1024,  # 5 MiB
    "attachment_file_extensions": ["zip","doc","docx",]

}
```

## Usage Example

```python
from django_editorjs2.fields import EditorJsField
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = EditorJsField()
    
# you can get preview like this
article = Article.objects.first()
# this will render html
article.content_preview()
```

## Custom Preprocessors and Callbacks

You can create custom preprocessors and callbacks to:
- Modify image links
- Handle file downloads
- Add custom processing before file save
- Modify response handling

## Troubleshooting

- Ensure all static files are collected
- Check that `MEDIA_URL` and `STATIC_URL` are correctly configured
- Verify path to preprocessors and callbacks

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/surajsinghbisht054/django_editorjs2/issues) on GitHub.
