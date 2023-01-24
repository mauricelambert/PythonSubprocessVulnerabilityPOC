from wsgiref.simple_server import make_server
from subprocess import Popen, DEVNULL
from os.path import basename
from sys import executable
from os import environ

del environ['COMSPEC']  # force environment without COMSPEC

def app(environ, start_response):
    method = environ["REQUEST_METHOD"]
    print('[*] New request, method:', method)
    if method == "GET":
        process = Popen("myprogram", shell=True, stderr=DEVNULL)
        process.communicate()
        print('[+] Process exit code:', process.returncode)
        status = "200 OK"
        content = b"GET OK"
    elif method == "POST":
        status = "200 OK"
        content = b"File uploaded successfully."
        content_length = environ.get("CONTENT_LENGTH", "0")
        if content_length.isdigit():
            filename = basename(environ["PATH_INFO"])
            with open(filename, 'wb') as file:
                file.write(environ["wsgi.input"].read(int(content_length)))
            print('[+] New file written:', filename)
        else:
            status = "400 Bad Request"
            content = b'Invalid Content-Length header.'
    else:
        status = "400 Bad Request"
        content = b"Only GET and POST methods allowed."
    start_response(status, [('Content-type', 'text/plain')])
    return (content,)

with make_server('127.0.0.1', 8000, app) as httpd:
    print('[*] Serving HTTP on 127.0.0.1 port 8000 (http://127.0.0.1:8000/) ...')
    httpd.serve_forever()