from django.conf import settings
from django.http import HttpResponse


class MaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            getattr(settings, "MAINTENANCE_MODE", False)
            and not request.path.startswith("/admin/")
        ):
            return HttpResponse("Site is under maintenance")

        return self.get_response(request)
