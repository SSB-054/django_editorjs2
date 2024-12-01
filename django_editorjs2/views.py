from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse
from django_editorjs2.models import EditorJsUploadFiles
from django.conf import settings
from django.utils.module_loading import import_string


callback_before_file_save = lambda x: x
callback_before_return_response = lambda x: x


if hasattr(settings, "DJANGO_EDITORJS2_CONFIG"):
    # callback modifies the file before saving it
    if "callback_before_file_save" in settings.DJANGO_EDITORJS2_CONFIG:
        callback_before_file_save = import_string(
            settings.DJANGO_EDITORJS2_CONFIG["callback_before_file_save"]
        )
    # callback fixes the response before returning it
    if "callback_before_return_response" in settings.DJANGO_EDITORJS2_CONFIG:
        callback_before_return_response = import_string(
            settings.DJANGO_EDITORJS2_CONFIG["callback_before_return_response"]
        )
        


class EditorJsAttachments(LoginRequiredMixin, View):

    def post(self, request):
        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        f = EditorJsUploadFiles()
        f.name = uploaded_file.name
        f.file = uploaded_file
        f.user = request.user
        callback_before_file_save(f)
        f.save()
        extension = f.name.split(".").pop()
        return JsonResponse(
            callback_before_return_response(
                {
                    "success": 1,
                    "title": f.name,
                    "file": {
                        "url": f.file.url,
                        "size": f.storage_used,
                        "name": f.name,
                        "extension": extension[:5],
                    },
                }
            )
        )
