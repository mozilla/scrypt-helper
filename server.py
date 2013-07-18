from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

import scrypt

def hello_world(request):
    return Response('Hello %(name)s!' % request.matchdict)


def do_scrypt(request):
    stretched_input = 'stretched_input'
    salt = 'salt'
    key = scrypt.hash(stretched_input, salt, N=64*1024, r=8, p=1,
                      buflen=1*32)
    return Response(key)


if __name__ == '__main__':
    config = Configurator()
    config.add_route('hello', '/hello/{name}')
    config.add_view(hello_world, route_name='hello')
    config.add_route('do_scrypt', '/')
    config.add_view(do_scrypt, route_name='do_scrypt')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()