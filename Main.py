from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

if __name__ == '__main__':
    config = Configurator()
    config.set_authentication_policy(AuthTktAuthenticationPolicy("hcms2017", hashalg='sha512'))
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.add_route('home', '/')
    config.add_route('upload', '/upload')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('json', '/json')
    config.add_route('user', '/user/{id}')
    config.add_route('points','/points/{id}/{amount}')
    config.add_route('photo', '/photo/{id}')
    config.add_route('rate', '/rate/{id}/{rate}')
    config.add_route('leaderboard', '/leaderboard')
    config.add_route('gallery', '/gallery')
    config.include('pyramid_chameleon')
    config.scan('views')
    config.add_static_view(name='static', path='static')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()