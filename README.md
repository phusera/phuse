<p align="center">
  <img src="ext/phuse_logo.jpeg"/>
</p>


# Phuse: Python Web Framework
How to pronounce: 'Fous'

Phuse is a fast, simple and lightweight WSGI micro web-framework for Python. It is distributed as a single file module and has no dependencies other than the Python Standard Library.

Routing: Requests to function-call mapping with support for clean and dynamic URLs.
Templates: Fast and pythonic *built-in template engine* and support for mako, jinja2 and cheetah templates.
Utilities: Convenient access to form data, file uploads, cookies, headers and other HTTP-related metadata.
Server: Built-in HTTP development server and support for paste, fapws3, bjoern, Google App Engine, cherrypy or any other WSGI capable HTTP server.


## Python implementation

https://github.com/phusera/phuse/assets/101386337/b2f1f56e-9736-4f9e-9b4e-81ec03dd1366

![Alt](https://repobeats.axiom.co/api/embed/e2fed0b6f396da4e8ffc6c3e562656ac025a369d.svg "Repobeats analytics image")

# Install
Install the latest stable release using ```pip install phuse``` Phuse runs on Python 2.7 and 3.6+

# Example: "Hello localhost!" with Phuse

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

# REQUEST DATA

Cookies, HTTP header, HTML <form> fields and other request data is available through the global request object. This special object always refers to the current request, even in multi-threaded environments where multiple client connections are handled at the same time:

```python
from phuse import request, route, template

@route('/hello')
def hello():
    name = request.cookies.username or 'Guest'
    return template('Hello {{name}}', name=name)
```

The request object is a subclass of BaseRequest and has a very rich API to access data. We only cover the most commonly used features here, but it should be enough to get started.


# FILE UPLOADS
To support file uploads, we have to change the <form> tag a bit. First, we tell the browser to encode the form data in a different way by adding an enctype="multipart/form-data" attribute to the <form> tag. Then, we add <input type="file" /> tags to allow the user to select a file. Here is an example:

```python
<form action="/upload" method="post" enctype="multipart/form-data">
  Category:      <input type="text" name="category" />
  Select a file: <input type="file" name="upload" />
  <input type="submit" value="Start upload" />
</form>
```
Phuse stores file uploads in BaseRequest.files as FileUpload instances, along with some metadata about the upload. Let us assume you just want to save the file to disk:

```python
@route('/upload', method='POST')
def do_upload():
    category   = request.forms.get('category')
    upload     = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.png','.jpg','.jpeg'):
        return 'File extension not allowed.'

    save_path = get_save_path_for_category(category)
    upload.save(save_path) # appends upload.filename automatically
    return 'OK'
```

FileUpload.filename contains the name of the file on the clients file system, but is cleaned up and normalized to prevent bugs caused by unsupported characters or path segments in the filename. If you need the unmodified name as sent by the client, have a look at FileUpload.raw_filename.

The FileUpload.save method is highly recommended if you want to store the file to disk. It prevents some common errors (e.g. it does not overwrite existing files unless you tell it to) and stores the file in a memory efficient way. You can access the file object directly via FileUpload.file. Just be careful.


# WSGI ENVIRONMENT
Each BaseRequest instance wraps a WSGI environment dictionary. The original is stored in BaseRequest.environ, but the request object itself behaves like a dictionary, too. Most of the interesting data is exposed through special methods or attributes, but if you want to access WSGI environ variables directly, you can do so:

```python
@route('/my_ip')
def show_ip():
    ip = request.environ.get('REMOTE_ADDR')
    # or ip = request.get('REMOTE_ADDR')
    # or ip = request['REMOTE_ADDR']
    return template("Your IP is: {{ip}}", ip=ip)
```

# TEMPLATES

Phuse comes with a fast and powerful built-in template engine called SimpleTemplate Engine. To render a template you can use the template() function or the view() decorator. All you have to do is to provide the name of the template and the variables you want to pass to the template as keyword arguments. Here’s a simple example of how to render a template:

```python
@route('/hello')
@route('/hello/<name>')
def hello(name='World'):
    return template('hello_template', name=name)
```
This will load the template file hello_template.tpl and render it with the name variable set. Bottle will look for templates in the ./views/ folder or any folder specified in the bottle.TEMPLATE_PATH list.

The view() decorator allows you to return a dictionary with the template variables instead of calling template():

```python
@route('/hello')
@route('/hello/<name>')
@view('hello_template')
def hello(name='World'):
    return dict(name=name)
```
## Syntax

The template syntax is a very thin layer around the Python language. Its main purpose is to ensure correct indentation of blocks, so you can format your template without worrying about indentation. Follow the link for a full syntax description: SimpleTemplate Engine

Here is an example template:

```python
%if name == 'World':
    <h1>Hello {{name}}!</h1>
    <p>This is a test.</p>
%else:
    <h1>Hello {{name.title()}}!</h1>
    <p>How are you?</p>
%end
```
## Caching

Templates are cached in memory after compilation. Modifications made to the template files will have no affect until you clear the template cache. Call bottle.TEMPLATES.clear() to do so. Caching is disabled in debug mode.

# AUTO RELOADING
During development, you have to restart the server a lot to test your recent changes. The auto reloader can do this for you. Every time you edit a module file, the reloader restarts the server process and loads the newest version of your code.

```python
from phuse import run
run(reloader=True)
```
How it works: the main process will not start a server, but spawn a new child process using the same command line arguments used to start the main process. All module-level code is executed at least twice! Be careful.

The child process will have os.environ['PHUSE_CHILD'] set to True and start as a normal non-reloading app server. As soon as any of the loaded modules changes, the child process is terminated and re-spawned by the main process. Changes in template files will not trigger a reload. Please use debug mode to deactivate template caching.

The reloading depends on the ability to stop the child process. If you are running on Windows or any other operating system not supporting signal.SIGINT (which raises KeyboardInterrupt in Python), signal.SIGTERM is used to kill the child. Note that exit handlers and finally clauses, etc., are not executed after a SIGTERM.
