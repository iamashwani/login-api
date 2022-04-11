# myapp/context_processors.py
from django.conf import settings


def extra_context(request):
    return {'base_url': settings.BASE_URL}