import os
from django.core.asgi import get_asgi_application
from fastapi_app import app as fastapi_app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest_api.settings')

# Get the Django ASGI application
django_asgi_app = get_asgi_application()


# Custom ASGI app to route between Django and FastAPI
class CustomASGIApp:
    def __init__(self, django_app, fastapi_app):
        self.django_app = django_app
        self.fastapi_app = fastapi_app

    async def __call__(self, scope, receive, send):
        if scope['path'].startswith('/fastapi'):
            scope['path'] = scope['path'][8:]  # Remove '/fastapi' prefix
            await self.fastapi_app(scope, receive, send)
        else:
            await self.django_app(scope, receive, send)


application = CustomASGIApp(django_asgi_app, fastapi_app)
