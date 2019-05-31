# -*- coding: utf-8 -*-

from jinja2 import Template


def render_string(template_str: str, *args, **kwargs) -> str:
    template = Template(template_str)
    return template.render(*args, **kwargs)


def render_template(template_path: str, *args, **kwargs) -> str:
    try:
        with open(template_path, 'r') as ft:
            template_str = ft.read()
    except FileNotFoundError as e:
        print(e)
        template_str = 'Template is not found'
    return render_string(template_str, *args, **kwargs)


def jinja_render_template(env: object, template_name: str, *args, **kwargs) -> str:
    template = env.get_template(template_name)
    return template.render(*args, **kwargs)
