from django.db import models
from django.forms import JSONField as JSONFormField
from django import forms
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from django_editorjs2.block_processor import converter
from django.conf import settings
from django.utils.module_loading import import_string
import json

converter.image_link_preprocessor = lambda x: x
converter.download_link_preprocessor = lambda x: x
editorjs_field_preview_callback = lambda x: x
editorjs_field_save_callback = lambda x: x

converter.extra_attributes = {
    'paragraph': {},
    'header': {},
    'list': {},
    'quote': {},
    'code': {},
    'image': {},
    'embed': {},
    'checklist': {},
    'table': {},
    'delimiter': {},
    'attachment': {},
}

if hasattr(settings, 'DJANGO_EDITORJS2_CONFIG'):
    if 'image_link_preprocessor' in settings.DJANGO_EDITORJS2_CONFIG:
        converter.image_link_preprocessor = import_string(settings.DJANGO_EDITORJS2_CONFIG['image_link_preprocessor'])
        
    if 'download_link_preprocessor' in settings.DJANGO_EDITORJS2_CONFIG:
        converter.download_link_preprocessor = import_string(settings.DJANGO_EDITORJS2_CONFIG['download_link_preprocessor'])
        
    if 'extra_attributes' in settings.DJANGO_EDITORJS2_CONFIG:
        converter.extra_attributes.update(settings.DJANGO_EDITORJS2_CONFIG['extra_attributes'])

    if 'editorjs_field_preview_callback' in settings.DJANGO_EDITORJS2_CONFIG:
        editorjs_field_preview_callback = import_string(settings.DJANGO_EDITORJS2_CONFIG['editorjs_field_preview_callback'])
    
    if 'editorjs_field_save_callback' in settings.DJANGO_EDITORJS2_CONFIG:
        editorjs_field_save_callback = import_string(settings.DJANGO_EDITORJS2_CONFIG['editorjs_field_save_callback'])
        

class EditorJsWidget(forms.Widget):
    template_name = "django_editorjs2/widget/editorjs.html"

    class Media:
        js = (
            static("django_editorjs2/editorjs.min.js"),
            static("django_editorjs2/attaches.editorjs.min.js"),
            static("django_editorjs2/checklist.editorjs.min.js"),
            static("django_editorjs2/code.editorjs.min.js"),
            static("django_editorjs2/delimiter.editorjs.min.js"),
            static("django_editorjs2/embed.editorjs.min.js"),
            static("django_editorjs2/header.editorjs.min.js"),
            static("django_editorjs2/image.editorjs.min.js"),
            static("django_editorjs2/list.editorjs.min.js"),
            static("django_editorjs2/marker.editorjs.min.js"),
            static("django_editorjs2/quote.editorjs.min.js"),
            static("django_editorjs2/table.editorjs.min.js"),
        )
        
    def format_value(self, value):
        return editorjs_field_preview_callback(json.loads(value or {}))

    
class EditorJSFormField(JSONFormField):
    def __init__(self, *args, **kwargs):
        kwargs["widget"] = EditorJsWidget
        super().__init__(*args, **kwargs)
        
    def clean(self, value):
        return editorjs_field_save_callback(super().clean(value))


class EditorJSField(models.JSONField):
    """
    Custom JSONField for EditorJS data. 
    """ 
    default = dict
    
    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        
        def preview_method(self):
            value = getattr(self, name)
            if not value:
                return ''
            return mark_safe(converter.convert(value))
        preview_method_name = f'{name}_preview'
        setattr(cls, preview_method_name, preview_method)
     
    def formfield(self, **kwargs):
        kwargs["form_class"] = EditorJSFormField
        return super().formfield(**kwargs)
