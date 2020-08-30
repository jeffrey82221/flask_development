import json
from IPython.display import display, clear_output

from jinja2 import Template
from ipywidgets.embed import embed_data
from ipywidgets import VBox

from interactive_widgets_builder.interactive_widget import (
    SelectionView
)


class ParaHolder():
    def _convert_ipywidget_to_jinja_parameters(self, ipywidget=None):
        if ipywidget == None:
            return {'manager_state': None, 'widget_views': [None]}
        else:
            data = embed_data(views=[ipywidget])
            manager_state = json.dumps(data['manager_state'])
            widget_views = [
                json.dumps(view_spec) for view_spec in data['view_specs']
            ]
            return {
                'manager_state': manager_state,
                'widget_views': widget_views
            }

    def __init__(self, response_func):
        self.response_func = response_func
        self.titles = None
        self.options_collection = None
        self.ipywidget = None

    def set_parameters(self, titles, options_collection, ipywidget):
        self.titles = titles
        self.options_collection = options_collection
        self.ipywidget = ipywidget

    def render_template(self):
        html_name = "selection_view.html"
        template = Template(open('templates/' + html_name).read())
        rendered_template = template.render(
            titles=self.titles,
            options_collection=self.options_collection,
            ipywidget_info=self._convert_ipywidget_to_jinja_parameters(
                self.ipywidget))
        return rendered_template

    def display_ipywidgets(self):
        clear_output(wait=True)
        views = []
        for title in self.titles:
            sv = SelectionView(title, self.options_collection[title],
                               self.response_func)
            views.append(sv.get_widget())
        if self.ipywidget:
            views.append(self.ipywidget)
        display(VBox(views))
