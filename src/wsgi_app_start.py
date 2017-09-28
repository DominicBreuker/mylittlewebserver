import sys
from wsgi_server import WsgiServer


def parse_args():
    if len(sys.argv) < 2:
        print("Provide a WSGI application as first arg (module:application)")
        sys.exit(1)
    app_path = sys.argv[1]

    if len(sys.argv) >= 3:
        host = sys.argv[2]
    else:
        host = "0.0.0.0"

    if len(sys.argv) >= 4:
        port = int(sys.argv[3])
    else:
        port = 8080

    return app_path, host, port


if __name__ == '__main__':
    app_path, host, port = parse_args()
    module, application = app_path.split(':')
    application = getattr(__import__(module), application)
    server = WsgiServer(host, port)
    server.serve(application)
