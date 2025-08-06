import os
import sys

# Add your project directory to Python path
project_home = '/home/yourusername/soyang-festival-backend'  # PythonAnywhere에서 실제 경로로 변경
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'soyang_festival_backend.settings_pythonanywhere'

# Import Django and initialize
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
