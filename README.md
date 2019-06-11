# Alice_WSGI

**Alice_WSGI** is simple wsgi framework. It was made as fourth homework of OTUS Python course. 


## Basic usage
### Basic setup of **Alice_WSGI**
```
from alice_wsgi import Alice
from config import Config

app = Alice(Config)
``` 

**Alice_WSGI** is class based view framework. Basic usage of view class is explained below:
```
from alice_wsgi import ClassView

class View(ClassView):
def get(self, *args, **kwargs):
    return 'It is get'
    
def post(self, *args, **kwargs):
    return 'It is post'
    
def put(self, *args, **kwargs):
    return 'It is put'
    
def patch(self, *args, **kwargs):
    return 'It is patch'
    
def delete(self, *args, **kwargs):
    return 'It is delete'
```
If you need to use custom mime or http response code **View** can be modified:
```
class View(ClassView):
def get(self, *args, **kwargs):
    return 'It is get', 'text/plain', 200
``` 
### Routes
To make route you need to import Views with **router.add_route()** of Alice() instance. **Be careful decorators is implemented as wrappers around based function. Upgrade of it is in ToDo**
```
app.router.add_route('/path/', ViewClass, ('GET','POST', and other allowed methods), (decorators, ))
```
Example:
```
from alice_wsgi import Alice

app = Alice()
app.router.add_route('/', View, ('GET', 'POST', ))
```

### Redirects
Redirects is realized similar as **router.add_route()** method **router.add_redirect()**:
```
app.router.add_redirect('/path/', '/redirect_path/', 302)
```
### Error handlers
Error handlers is implemented as Routes and Redirects:
```
app.router.add_error_handler(error_code, handler_class)
```

## Variables

Alice_WSGI support a receiving of variables values from get or post query and with setup path variables templates.
Be careful if request method is GET Alice_WSGI will parse GET variables, if method POST the query GET variables will be ignored.

### Path templates and variables
Path variables is implemented with path templates. 

Example:
```
app.router.add_route('/user/<int:age>/<float:height>/<str:nickname>/', View, ('GET', ))
``` 
You can setup **int**, **float**, and **str** types. After "**:**" you should enter hint of variable name. 

Basic template for one variable:
```
<int_or_float_or_str:hint>
```

## Templates parsing and rendering
As template render Alice_WSGI use Jinja2. Implemented three methods:
```
import from alice_wsgi.templates render_string, render_template, jinja_render_template

jinja_render_template(env: object, template_name: str, *args, **kwargs) -> str
render_string(template_str: str, *args, **kwargs) -> str
render_template(template_path: str, *args, **kwargs) -> str
```
General methods is:
```
jinja_render_template(env: object, template_name: str, *args, **kwargs) -> str
```
Example:
```
from example_app import app  # Main instance of Alice()
from alice_wsgi.templates import jinja_render_template

class Index(ClassView):
    def get(self, *path_vars, **query):
        return jinja_render_template(app.jinja, 'index.html', path_vars=path_vars or None, query=query or None)
```

## Sections
Sections is useful for creation large applications with modular system. To make section use Section class:
```
section = Section(url_prfix: str, config, static_path: str, templates_path: str)
``` 
Alice class is parent for Section class. Now you can use general Alice methods for section creation.
For registration section use Alice.router.add_section() method.
```
# This is scheme not code
app = Alice(...)
section = Section(...)
app.router.add_section(section)
```
add_section() updates general Alice.router.routes and Alice.router.redirects instance dicts.

## Basic app
Let's make basic app with name example_app:
```
App structure:
/alice_wsgi/
|---/alice_wsgi/
|   | Alice_WSGI package
|   
|---/example_app/
|   |-/static/
|   |-/templates/
|   |-__init__.py
|   |-config.py
|   |-views.py
|
|---/run_wsgi.ini
```

First we need to make **config.py** file with templates and static paths:
```
import os


class Config:
    TEMPLATES_PATH = '{}/templates/'.format(os.path.dirname(os.path.abspath(__file__)))
    STATIC_PATH = '{}/static/'.format(os.path.dirname(os.path.abspath(__file__)))

```
**\_\_init__.py**
```
from alice_wsgi import Alice
from example_app.config import Config

app = Alice(Config)

from example_app.views import Index

app.router.add_route('/', Index, ('GET', 'POST'))
app.router.add_route('/<str:text>/<int:id>/<float:number>/', Index, ('GET', 'POST'))
app.router.add_redirect('/contacts/', '/', 302)

```
**views.py**
```
from alice_wsgi.templates import jinja_render_template
from alice_wsgi.views import ClassView
from example_app import app


class Index(ClassView):

    def get(self, *path_vars, **query):
        return jinja_render_template(app.jinja, 'index.html', path_vars=path_vars or None, query=query or None)

    def post(self, *path_vars, **query):
        return jinja_render_template(app.jinja, 'index_post.html', path_vars=path_vars or None, query=query or None)

```
To run app enter to terminal:
```
uwsgi run_wsgi.ini
```

## Requirements
```
Python 3.5+

Jinja2==2.10.1
MarkupSafe==1.1.1
uWSGI==2.0.18 or gunicorn==19.9.0 or any other wsgi server.
```


## Contributors
Andrei S. Pavlov (https://github.com/ndrwpvlv/)
