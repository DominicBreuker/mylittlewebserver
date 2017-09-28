from pyramid.config import Configurator
from pyramid.response import Response


def hello_world(request):
    return Response('Hi from Pyramid!\n', content_type='text/plain')

config = Configurator()
config.add_route('default', '/')
config.add_view(hello_world, route_name='default')
app = config.make_wsgi_app()
