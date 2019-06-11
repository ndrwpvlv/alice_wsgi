from alice_wsgi import Section
from example_app.blog.config import Config

blog = Section('/blog', Config, Config.STATIC_PATH, Config.TEMPLATES_PATH)

from example_app.blog.views import Index

blog.router.add_route('/', Index, ('GET',))
