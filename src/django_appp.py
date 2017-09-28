import sys
sys.path.insert(0, './django_app')
from django_app import wsgi


app = wsgi.application
