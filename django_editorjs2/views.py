from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse
from .models import EditorJsUploadFiles

class EditorJsAttachments(LoginRequiredMixin, View):
    def post(self, request):
        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        f = EditorJsUploadFiles()
        f.name = uploaded_file.name
        f.file = uploaded_file
        f.user = request.user
        f.save()
        extension = f.name.split(".").pop()
        return JsonResponse(
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