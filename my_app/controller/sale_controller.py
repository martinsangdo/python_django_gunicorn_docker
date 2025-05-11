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

def validate_start_end_date(start_date_str, end_date_str):
    start_date = None
    end_date = None
    if not start_date_str or not end_date_str:
        #missing params
        return settings.MESSAGES['ERR_MISSING_DATES'], start_date, end_date

    if not is_valid_date_format(start_date_str, '%Y-%m-%d'):
        return settings.MESSAGES['ERR_INVALID_DATES'], start_date, end_date

    if not is_valid_date_format(end_date_str, '%Y-%m-%d'):
        return settings.MESSAGES['ERR_INVALID_DATES'], start_date, end_date

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    if start_date > end_date:
        return settings.MESSAGES['ERR_INVALID_RANGE_DATES'], start_date, end_date
    
    return '', start_date, end_date

@require_GET
def overall_metrics(request):
    error, start_date, end_date = validate_start_end_date(request.GET.get('start'), request.GET.get('end'))
    if error != '':
        return JsonResponse({'error': error}, status=400)

    sale_service_instance = sale_service.SaleService()
    response = sale_service_instance.overall_metrics(start_date, end_date)
    if 'error' in response:
        return JsonResponse(response, status = 400)
    return JsonResponse(response, status=200)

@require_GET
def daily_metrics(request):
    error, start_date, end_date = validate_start_end_date(request.GET.get('start'), request.GET.get('end'))
    if error != '':
        return JsonResponse({'error': error}, status=400)

    sale_service_instance = sale_service.SaleService()
    response = sale_service_instance.daily_metrics(start_date, end_date)
    if 'error' in response:
        return JsonResponse(response, status = 400)
    return JsonResponse(response, safe=False, status=200)