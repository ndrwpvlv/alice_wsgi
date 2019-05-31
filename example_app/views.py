from alice_wsgi.templates import jinja_render_template
from alice_wsgi.views import ClassView
from example_app import app


class Index(ClassView):

    def get(self, *path_vars, **query):
        return jinja_render_template(app.jinja, 'index.html', path_vars=path_vars or None, query=query or None)

    def post(self, *path_vars, **query):
        return jinja_render_template(app.jinja, 'index_post.html', path_vars=path_vars or None, query=query or None)
