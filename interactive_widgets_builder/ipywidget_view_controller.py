from IPython.display import display, clear_output

import ipywidgets as widgets
from ipywidgets import HBox, VBox, interactive

from table_info_extractor.toy_db_info_initialize import ToyDB
from interactive_widgets_builder.view_factory import ViewFactory


class Request():
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
    ViewController.response_by_altering_view(Request(
        values
    ))

  def __init__(self, title, options):
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

  def get_widget(self):
    return HBox([self._interactive_dropdown.get_widget(), self._button])


class ViewController():
  def __init__():
    self.dropdown_titles = ['Role', 'PM', 'Member']
    self._options_for_each_dropdown_titles = {
        'Role': ['Admin', 'PM', 'Member'],
        'PM': ToyDB.project_list,
        'Member': ToyDB.unique_members
    }
    self.view_factory = ViewFactory()
    self.entry_dropdown_title = 'Role'

  def entry(self):
    sv = SelectionView(
        self.entry_dropdown_title,
        self._options_for_each_dropdown_titles[self.entry_dropdown_title]
    )
    widget = sv.get_widget()
    return widget

  def _get_reordered_option_list(self, dropdown_title, selected_result):
    import copy
    options = copy.copy(self._options_for_each_dropdown_titles[dropdown_title])
    options.remove(selected_result)
    return [selected_result] + options

  def response_by_altering_view(self, request):
    import copy
    clear_output(wait=True)
    if 'Role' in request.values.keys():
      if request.values['Role'] == 'PM':
        sv1 = SelectionView(
            'Role',
            self._get_reordered_option_list('Role', 'PM')
        )
        sv2 = SelectionView(
            'PM',
            self._options_for_each_dropdown_titles['PM']
        )
        widget = VBox([
            sv1.get_widget(),
            sv2.get_widget()])
      elif request.values['Role'] == 'Member':
        sv1 = SelectionView(
            'Role',
            self._get_reordered_option_list('Role', 'Member')
        )
        sv2 = SelectionView(
            'Member',
            self._options_for_each_dropdown_titles['Member']
        )
        widget = VBox([
            sv1.get_widget(),
            sv2.get_widget()
        ])
      else:  # Role: Admin
        sv = SelectionView(
            'Role',
            self._options_for_each_dropdown_titles['Role']
        )
        widget = VBox([
            sv.get_widget(),
            self.view_factory.build_view('all')
        ])
        # print("Show Admin Table View")

    else:
      if 'PM' in request.values.keys():
        selected_project = request.values['PM']
        sv1 = SelectionView(
            'Role',
            self._get_reordered_option_list('Role', 'PM')
        )
        sv2 = SelectionView(
            'PM',
            self._get_reordered_option_list('PM', selected_project)
        )
        widget = VBox([
            sv1.get_widget(),
            sv2.get_widget(),
            self.view_factory.build_view('project', selected_project)
        ])
        # print("Show PM Table View for", project)

      elif 'Member' in request.values.keys():
        selected_member = request.values['Member']
        sv1 = SelectionView(
            'Role',
            self._get_reordered_option_list('Role', 'Member')
        )
        sv2 = SelectionView(
            'Member',
            self._get_reordered_option_list('Member', selected_member)
        )
        widget = VBox([
            sv1.get_widget(),
            sv2.get_widget(),
            self.view_factory.build_view('member', selected_member)
        ])
        # print("Show Member Table View for", member)
    display(widget)
