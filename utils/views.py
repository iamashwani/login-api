from django.http import JsonResponse

def error_404(request, exception):
    message = ("user not found")

    response = JsonResponse(data={'status': False, 'message' : message,})
    response.status_code = 404
    return response

def error_500(request):
    message = ("The endpoint is not found it on us")

    response = JsonResponse(data={'status': False,'message' : message,})
    response.status_code = 500
    return response