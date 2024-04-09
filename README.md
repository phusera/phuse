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

Simpler Version:

```python
from phuse import route, run

@route('/')
def index():
    return '<b>Hello World! I am using Phuse!</b>!'

run(host='localhost', port=8080)
```

# HTTP REQUEST METHODS
The HTTP protocol defines several request methods (sometimes referred to as “verbs”) for different tasks. GET is the default for all routes with no other method specified. These routes will match GET requests only. To handle other methods such as POST, PUT, DELETE or PATCH, add a method keyword argument to the route() decorator or use one of the five alternative decorators: get(), post(), put(), delete() or patch().

The POST method is commonly used for HTML form submission. This example shows how to handle a login form using POST:

```python
from phuse import get, post, request # or route

@get('/login') # or @route('/login')
def login():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
    '''

@post('/login') # or @route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        return "<p>Your login information was correct.</p>"
    else:
        return "<p>Login failed.</p>"
```

In this example the /login URL is linked to two distinct callbacks, one for GET requests and another for POST requests. The first one displays a HTML form to the user. The second callback is invoked on a form submission and checks the login credentials the user entered into the form. The use of Request.forms is further described in the Request Data section.

# ROUTING STATIC FILES
Static files such as images or CSS files are not served automatically. You have to add a route and a callback to control which files get served and where to find them:

```python
from phuse import static_file
@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='/path/to/your/static/files')

```
The static_file() function is a helper to serve files in a safe and convenient way (see Static Files).
This example is limited to files directly within the /path/to/your/static/files directory because the <filename> wildcard won’t match a path with a slash in it. To serve files in subdirectories, change the wildcard to use the path filter:

```python
@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='/path/to/your/static/files')

```
Be careful when specifying a relative root-path such as root='./static/files'. The working directory (./) and the project directory are not always the same.

# ERROR PAGES
If anything goes wrong, Bottle displays an informative but fairly plain error page. You can override the default for a specific HTTP status code with the error() decorator:

```python
from phuse import error
@error(404)
def error404(error):
    return 'Nothing here, sorry'

```

From now on, 404 File not Found errors will display a custom error page to the user. The only parameter passed to the error-handler is an instance of HTTPError. Apart from that, an error-handler is quite similar to a regular request callback. You can read from request, write to response and return any supported data-type except for HTTPError instances.

Error handlers are used only if your application returns or raises an HTTPError exception (abort() does just that). Changing Request.status or returning HTTPResponse won’t trigger the error handler.

# HTTP ERRORS AND REDIRECTS
The abort() function is a shortcut for generating HTTP error pages.

```python
from phuse import route, abort
@route('/restricted')
def restricted():
    abort(401, "Sorry, access denied.")
```
To redirect a client to a different URL, you can send a 303 See Other response with the Location header set to the new URL. redirect() does that for you:

```python
from phuse import route, redirect
@route('/wrong/url')
def wrong():
    redirect("/right/url")

```

# Response Header

Response headers such as Cache-Control or Location are defined via Response.set_header(). This method takes two parameters, a header name and a value. The name part is case-insensitive:

```python
@route('/wiki/<page>')
def wiki(page):
    response.set_header('Content-Language', 'en')
    ...
```

Most headers are unique, meaning that only one header per name is send to the client. Some special headers however are allowed to appear more than once in a response. To add an additional header, use Response.add_header() instead of Response.set_header():

```
response.set_header('Set-Cookie', 'name=value')
response.add_header('Set-Cookie', 'name2=value2')
```
Please note that this is just an example. If you want to work with cookies, read ahead.

# COOKIES

A cookie is a named piece of text stored in the user’s browser profile. You can access previously defined cookies via Request.get_cookie() and set new cookies with Response.set_cookie():

```python
@route('/hello')
def hello_again():
    if request.get_cookie("visited"):
        return "Welcome back! Nice to see you again"
    else:
        response.set_cookie("visited", "yes")
        return "Hello there! Nice to meet you"

```
The Response.set_cookie() method accepts a number of additional keyword arguments that control the cookies lifetime and behavior. Some of the most common settings are described here:

max_age: Maximum age in seconds. (default: None)
expires: A datetime object or UNIX timestamp. (default: None)
domain: The domain that is allowed to read the cookie. (default: current domain)
path: Limit the cookie to a given path (default: /)
secure: Limit the cookie to HTTPS connections (default: off).
httponly: Prevent client-side javascript to read this cookie (default: off, requires Python 2.7 or newer).
same_site: Disables third-party use for a cookie. Allowed attributes: lax and strict. In strict mode the cookie will never be sent. In lax mode the cookie is only sent with a top-level GET request.
If neither expires nor max_age is set, the cookie expires at the end of the browser session or as soon as the browser window is closed. There are some other gotchas you should consider when using cookies:

Cookies are limited to 4 KB of text in most browsers.
Some users configure their browsers to not accept cookies at all. Most search engines ignore cookies too. Make sure that your application still works without cookies.
Cookies are stored at client side and are not encrypted in any way. Whatever you store in a cookie, the user can read it. Worse than that, an attacker might be able to steal a user’s cookies through XSS vulnerabilities on your side. Some viruses are known to read the browser cookies, too. Thus, never store confidential information in cookies.
Cookies are easily forged by malicious clients. Do not trust cookies.

# Signed Cookies

As mentioned above, cookies are easily forged by malicious clients. Bottle can cryptographically sign your cookies to prevent this kind of manipulation. All you have to do is to provide a signature key via the secret keyword argument whenever you read or set a cookie and keep that key a secret. As a result, Request.get_cookie() will return None if the cookie is not signed or the signature keys don’t match:

```python
@route('/login')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        response.set_cookie("account", username, secret='some-secret-key')
        return template("<p>Welcome {{name}}! You are now logged in.</p>", name=username)
    else:
        return "<p>Login failed.</p>"

@route('/restricted')
def restricted_area():
    username = request.get_cookie("account", secret='some-secret-key')
    if username:
        return template("Hello {{name}}. Welcome back.", name=username)
    else:
        return "You are not logged in. Access denied."

```
In addition, Phuse automatically pickles and unpickles any data stored to signed cookies. This allows you to store any pickle-able object (not only strings) to cookies, as long as the pickled data does not exceed the 4 KB limit.
