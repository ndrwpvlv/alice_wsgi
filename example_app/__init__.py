from alice_wsgi import Alice
from example_app.config import Config

app = Alice(Config)

from example_app.views import Index
from example_app.blog import blog

app.router.add_route('/', Index, ('GET', 'POST'))
app.router.add_route('/<str:text>/<int:id>/<float:number>/', Index, ('GET', 'POST'))
app.router.add_redirect('/contacts/', '/', 302)

app.router.add_section(blog)
