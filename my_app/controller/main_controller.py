from django.http import JsonResponse
from django.db import connection

def health_check(request):
    health_data = {"status": "ok"}
    database_status = "unreachable"

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result and result[0] == 1:
                database_status = "reachable"
    except Exception as e:
        print(f"Database health check failed: {e}")
        health_data["status"] = "error"

    health_data["database"] = database_status
    return JsonResponse(health_data)