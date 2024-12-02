from django.db import models
from django.conf import settings
from uuid import uuid4
from django.core.validators import FileExtensionValidator
from django.template.defaultfilters import filesizeformat
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
import os
import uuid


@deconstructible
class MaxFileSizeValidator:
    def __init__(self, bytes_size):
        self.bytes_size = bytes_size

    def __call__(self, file_obj):
        if file_obj.size > self.bytes_size:
            raise ValidationError(
                "File size exceede limit. Max Size {} KiB.".format(
                    str(self.bytes_size / 1024)
                )
            )


ATTACHMENT_FILE_EXTENSIONS = [
    "zip",
    "doc",
    "docx",
    "pdf",
    "txt",
    "csv",
    "xlsx",
    "xls",
    "pptx",
    "mp4",
    "avi",
    "mkv",
    "mov",
    "webm",
    "m4v",
    "mpeg",
    "m4p",
    "gif",
    "wmv",
]
MAX_ATTACHMENT_SIZE_BYTES = 5 * 1024 * 1024  # 5 MiB

if hasattr(settings, "DJANGO_EDITORJS2_CONFIG"):
    if "attachment_file_extensions" in settings.DJANGO_EDITORJS2_CONFIG:
        ATTACHMENT_FILE_EXTENSIONS = settings.DJANGO_EDITORJS2_CONFIG[
            "attachment_file_extensions"
        ]
        
    if "max_attachment_size_bytes" in settings.DJANGO_EDITORJS2_CONFIG:
        MAX_ATTACHMENT_SIZE_BYTES = settings.DJANGO_EDITORJS2_CONFIG[
            "max_attachment_size_bytes"
        ]

def custom_upload_to(instance, filename):
    random_str = uuid.uuid4().hex
    new_filename = f"{random_str}_{filename[-10:]}".replace(" ", "_")
    return os.path.join("django-editorjs2", "files", new_filename)


class EditorJsUploadFiles(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=100, help_text="Enter file name.")
    file = models.FileField(
        "File",
        upload_to=custom_upload_to,
        validators=[
            MaxFileSizeValidator(MAX_ATTACHMENT_SIZE_BYTES),
            FileExtensionValidator(allowed_extensions=ATTACHMENT_FILE_EXTENSIONS),
        ],
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="editorjs_uploaded_files",
    )

    storage_used = models.BigIntegerField(
        "Storage Used (in kb)", null=True, editable=False, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if (not self.storage_used) and self.file:
            try:
                self.storage_used = self.file.size
            except Exception as e:
                if "404" in str(e):
                    self.storage_used = 0
                pass
        return super().save(*args, **kwargs)

    def display_storage_used(self):
        return filesizeformat(self.storage_used) if self.storage_used else 0

    def __str__(self):
        return f"EditorJsFile[{self.id}]"

    class Meta:
        verbose_name = "EditorJs File"
        verbose_name_plural = "EditorJs Files"
        ordering = ["-created_at"]
