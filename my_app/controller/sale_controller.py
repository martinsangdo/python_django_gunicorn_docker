from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET
from ..services import sale_service
from .. import settings
from django.utils.dateparse import parse_date
from datetime import datetime  # Import datetime *class*

@require_GET
def import_sales(request):
    sale_service_instance = sale_service.SaleService()
    response = sale_service_instance.import_sales_from_file()
    if 'error' in response:
        return JsonResponse(response, status = 400)
    return JsonResponse(response, status=201)

def is_valid_date_format(date_string, format):
        try:
            datetime.strptime(date_string, format)
            return True
        except ValueError:
            return False
        
@require_GET
def overall_metrics(request):
    start_date_str = request.GET.get('start')
    end_date_str = request.GET.get('end')
    if not start_date_str or not end_date_str:
        #missing params
        return JsonResponse({'error': settings.MESSAGES['ERR_MISSING_DATES']}, status = 400)

    if not is_valid_date_format(start_date_str, '%Y-%m-%d'):
        return JsonResponse({'error': settings.MESSAGES['ERR_INVALID_DATES']}, status = 400)

    if not is_valid_date_format(end_date_str, '%Y-%m-%d'):
        return JsonResponse({'error': settings.MESSAGES['ERR_INVALID_DATES']}, status = 400)

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    if start_date > end_date:
        return JsonResponse({'error': settings.MESSAGES['ERR_INVALID_RANGE_DATES']}, status = 400)
    
    sale_service_instance = sale_service.SaleService()
    response = sale_service_instance.overall_metrics(start_date, end_date)
    if 'error' in response:
        return JsonResponse(response, status = 400)
    return JsonResponse(response, status=200)