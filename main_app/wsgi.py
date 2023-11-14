import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

from main_app.settings import BASE_DIR

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main_app.settings')

application = WhiteNoise(application=get_wsgi_application(),
                         root=os.path.join(BASE_DIR, 'static'))
