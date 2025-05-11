from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET
from ..services import sale_service

@require_GET
def import_sales(request):
    sale_service.import_sales_from_file()
    return HttpResponse({}, status=201)