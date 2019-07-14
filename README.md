# Tiny bottle app with trivial CORS examples

https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS

## What is this?

Two Bottle applications in a tiny Python file. HTML/JS is served from
port 8000, some toy resources are served on port 9000.

Visit http://localhost:8000 and open your developer console to observe
and inspect the pre-flight requests.

The HTML/JS will do XmlHttpRequests to the "resources" served via
port 9000. Requests to `http://localhost:9000/resource/any` should work,
while `http://localhost:9000/resource/foo.example.com` is restricted
via `Access-Control-Allow-Origin` to only be accessed from foo.example.com.

**Do not use this as an example of how to actually implement CORS.**

## Run

    $ python3 -m venv venv
    $ pip install -r requirements.txt
    $ python cors-example.py
