from django.db import models
from django.forms import JSONField as JSONFormField
from django import forms
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from django_editorjs2.block_processor import converter

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

class EditorJSFormField(JSONFormField):
    def __init__(self, *args, **kwargs):
        kwargs["widget"] = EditorJsWidget
        super().__init__(*args, **kwargs)


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
