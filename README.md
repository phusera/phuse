<p align="center">
  <img src="IMG_1295.jpeg"/>
</p>


# Phuse: Python Web Framework
Phuse is a fast, simple and lightweight WSGI micro web-framework for Python. It is distributed as a single file module and has no dependencies other than the Python Standard Library.

Routing: Requests to function-call mapping with support for clean and dynamic URLs.
Templates: Fast and pythonic *built-in template engine* and support for mako, jinja2 and cheetah templates.
Utilities: Convenient access to form data, file uploads, cookies, headers and other HTTP-related metadata.
Server: Built-in HTTP development server and support for paste, fapws3, bjoern, Google App Engine, cherrypy or any other WSGI capable HTTP server.


# Install
Install the latest stable release using```pip install phuse```. Phuse runs on Python 2.7 and 3.6+

# Example: "Hello World" with Phuse

```python
from phuse import route, run, template

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

run(host='localhost', port=8080)
```
