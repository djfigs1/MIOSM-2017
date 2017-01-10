from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

def hello_world(request):
    return Response('<h1>Hello World!</h1>')

if __name__ == '__main__':
    config = Configurator()
    config.add_route('hello', '/')
    config.include('pyramid_chameleon')
    config.scan('views')
    config.add_static_view(name='static', path='static')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()