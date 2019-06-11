from alice_wsgi.templates import jinja_render_template
from alice_wsgi.views import ClassView
from example_app.blog import blog


class Index(ClassView):

    def get(self, *path_vars, **query):
        return jinja_render_template(blog.jinja, 'index.html')
