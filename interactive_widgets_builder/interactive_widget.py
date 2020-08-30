import ipywidgets as widgets
from ipywidgets import HBox, interactive


class _Request():
    def __init__(self, values):
        self.values = values


class _InteractiveDropdown():
    def _pass_info(self, selected_result):
        self._selected_result = selected_result

    def __init__(self, title, options):
        self._title = title
        self._options = options
        self._dropdown = widgets.Dropdown(
            options=self._options,
            description=self._title + ':',
            disabled=False)
        self._selected_result = None
        self._interactive_dropdown = interactive(
            self._pass_info,
            selected_result=self._dropdown)

    def get_widget(self):
        return self._interactive_dropdown

    def get_selected_result(self):
        return self._selected_result


class SelectionView():
    def _submit(self, b):
        selected_result = self._interactive_dropdown.get_selected_result()
        values = {}
        values[self._title] = selected_result
        self._response_func(_Request(
            values
        ))

    def __init__(self, title, options, response_func):
        self._title = title
        self._interactive_dropdown = _InteractiveDropdown(title, options)
        self._button = widgets.Button(
            value=False,
            description='Enter',
            disabled=False,
            button_style='',
            tooltip='Description',
            icon='Enter'
        )
        self._button.on_click(self._submit)
        self._response_func = response_func

    def get_widget(self):
        return HBox([self._interactive_dropdown.get_widget(), self._button])
