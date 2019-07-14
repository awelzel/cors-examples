import argparse
import os
import threading

from bottle import Bottle
from bottle import html_escape, redirect, request, response, run, static_file

app = Bottle()
static_app = Bottle()


@static_app.route("/")
def index():
    redirect("index.html")


@static_app.route("/<filepath:path>")
def static_files(filepath):
    return static_file(filepath, root="./static")


@app.route("/resource/any", method=["OPTIONS", "GET", "POST", "PUT"])
def other_resource():
    """
    A resource that is allowed to be accessed from any origin.
    """
    response.add_header("Access-Control-Allow-Origin", "*")
    response.add_header("Access-Control-Allow-Methods", "GET, POST, PUT, OPTIONS")
    response.add_header("Access-Control-Allow-Headers", "Origin, Accept, Content-Type")

    method = html_escape(request.method)
    origin = html_escape(request.headers.get("Origin", "<none>"))
    return "Hello. You came from '{}' with a {}".format(origin, format(method))


@app.route("/resource/foo.example.com", method=["OPTIONS", "GET", "POST", "PUT"])
def foo_example_com():
    """
    A resource only allowed to be accessed from Origin foo.example.com.

    Requested with a GET, the browser will do no preflight request, but
    won't make the response available, because Access-Control-Allow-Origin
    doesn't match localhost:8000.

    Requested with a PUT or POST with non-standard Content-Type, it will
    do a pre-flight and not do the actual request.
    """
    response.add_header("Access-Control-Allow-Origin", "http://foo.example.com")
    response.add_header("Access-Control-Allow-Methods", "GET, POST, PUT, OPTIONS")
    response.add_header("Access-Control-Allow-Headers", "Origin, Accept, Content-Type")

    return "Hello. You're coming from http://foo.example.com?"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--reloader", default=False, action="store_true")
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()
    static_port = 8000
    resources_port = 9000

    def _run_static_app():
        run(static_app, host=args.host, port=static_port)

    # Run static file serving on a separate port in a separate thread.
    if not args.reloader or (args.reloader and "BOTTLE_CHILD" in os.environ):
        static_app_thread = threading.Thread(
            target=_run_static_app,
            daemon=True
        )
        static_app_thread.start()

    run(app, host=args.host, port=resources_port, reloader=args.reloader)
