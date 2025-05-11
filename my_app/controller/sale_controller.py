from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET
from ..services import sale_service

@require_GET
def import_sales(request):
    sale_service_instance = sale_service.SaleService()
    response = sale_service_instance.import_sales_from_file()
    if 'error' in response:
        return JsonResponse(response, status = 500)
    return JsonResponse(response, status=201)