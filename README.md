# MyLittleWebServer

[![Code Climate](https://codeclimate.com/github/DominicBreuker/mylittlewebserver.png)](https://codeclimate.com/github/DominicBreuker/mylittlewebserver)

tiny little change...

Simple implementation of a web server.
Written in Python.
Not meant for any production use, only for (self-)educational purposes.
Written in Python and supports:
- HTTP connections only, no HTTPS
- Python WSGI applications
- Parallel request handling with `fork`

Heavily inspired by these blog posts, but with slightly different design: Let's build a web server [part 1](https://ruslanspivak.com/lsbaws-part1/) [part 2](https://ruslanspivak.com/lsbaws-part2/) and [part 3](https://ruslanspivak.com/lsbaws-part3/)

## Usage

All dependencies are managed with Docker.
If you have Docker installed, run `bin/build.sh` from project root and the image is built.
After that, `bin/run.sh <cmd>` starts various modes of the server:
- `bin/run.sh http`: starts a simple web server responding with hello world on every request
- `bin/run.sh wsgi_example`: starts a WSGI server with a dummy WSGI app serving hello world
- `bin/run.sh flask`: starts a hello world flask app connected through WSGI
- `bin/run.sh pyramid`: starts a hello world pyramid app connected through WSGI
- `bin/run.sh django`: starts a hello world django app connected through WSGI
- `bin/run.sh shell`: drops you into a shell inside the container (e.g., to inspect the processes there with `ps auxf`)

While running a server, use `bin/request.sh` to launch many requests against it fast to see if the web server can handle them.

## Code overview

The code has very simple structure:
- Basic web server: In `src/http_server.py`, you find two classes. `HttpServer` binds a socket, receives HTTP requests and sends responses crafted by a callback. `HttpRequestParser` is used by `HttpServer` to read HTTP headers and bodys.
- Forking web server: In `src/http_fork_server.py`, `HttpForkServer` extents `HttpServer` by handling each request in a seperate process and sets up signal handlers to clean up the processes afterwards.
- WSGI server: In `src/wsgi_server.py`, a class `WsgiServer` is defined which implementes the WSGI interface. It can use either of the HTTP servers. Seperate classes `WsgiRequestParser` and `WsgiResponse` handle request parsing and response construcion respectively.
- WSGI loader: `src/wsgi_app_start.py` defines a loader for WSGI apps. See `bin/run.sh` for usage examples.

Besides these main files, various hello world apps exist to test if they can be used with the servers:
- Flask: defined in `src/flask_app.py
- Pyramid: defined in `src/pyramid_app.py`
- Django: defined in `src/django_src/*` and loaded through `src/django_app.py`
