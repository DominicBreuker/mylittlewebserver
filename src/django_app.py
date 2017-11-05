import sys
sys.path.insert(0, "./django_src")
from django_src import wsgi


app = wsgi.application
