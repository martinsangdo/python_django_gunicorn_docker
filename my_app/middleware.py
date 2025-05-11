import json
import logging
import time
import uuid
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve

logger = logging.getLogger(__name__)

class JsonRequestLogMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        self.get_response = get_response

    def process_request(self, request):
        request.id = uuid.uuid4().hex  # Assign a unique request ID
        request.start_time = time.time()

    def process_response(self, request, response):
        duration = time.time() - request.start_time

        try:
            match = resolve(request.path_info)
            endpoint = match.view_name
            parameters = self._get_request_parameters(request)
        except Exception:
            endpoint = 'unknown'
            parameters = {}

        log_level = 'INFO'
        message = f'Request processed in {duration:.3f} seconds, Status: {response.status_code}'
        response_data = {}

        if response.status_code >= 400:
            log_level = 'WARNING'  # Or 'ERROR'
            try:
                response_content = response.content.decode('utf-8')
                response_data = json.loads(response_content)
                if 'error' in response_data:
                    message += f", Error: {response_data.get('error')}"
                elif 'errors' in response_data: # Handle potential list of errors
                    message += f", Errors: {response_data.get('errors')}"
                else:
                    message += f", Response Body: {response_content[:100]}..." # Log a snippet
            except json.JSONDecodeError:
                message += f", Non-JSON Response Body: {response.content[:100]}..."
            except Exception as e:
                message += f", Error parsing response body: {e}"

        log_data = {
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S%z', time.localtime()),
            'level': log_level,
            'message': message,
            'context': {
                'endpoint': endpoint,
                'request_id': getattr(request, 'id', 'unknown'),
                'parameters': parameters,
                'status_code': response.status_code,
                'response_data': response_data.get('error') if 'error' in response_data else response_data.get('errors') if 'errors' in response_data else response_data if response_data else None,
            }
        }

        if log_level == 'ERROR':
            logger.error(json.dumps(log_data))
        elif log_level == 'WARNING':
            logger.warning(json.dumps(log_data))
        else:
            logger.info(json.dumps(log_data))

        return response

    def process_exception(self, request, exception):
        log_data = {
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S%z', time.localtime()),
            'level': 'ERROR',
            'message': f'Exception: {str(exception)}',
            'context': {
                'endpoint': 'unknown',
                'request_id': getattr(request, 'id', 'unknown'),
                'parameters': self._get_request_parameters(request),
                'error': str(exception),
            }
        }
        logger.error(json.dumps(log_data))
        return None

    def _get_request_parameters(self, request):
        parameters = request.GET.dict()
        if request.method == 'POST' and request.content_type == 'application/json':
            try:
                parameters.update(json.loads(request.body.decode('utf-8')))
            except json.JSONDecodeError:
                parameters['body'] = 'Non-JSON POST body'
        elif request.method == 'POST':
            parameters.update(request.POST.dict())
        return parameters