from IPython.display import display, clear_output

import ipywidgets as widgets
from ipywidgets import HBox, VBox, interactive

from table_info_extractor.toy_db_info_initialize import ToyDB
from interactive_widgets_builder.view_factory import ViewFactory


class Request():
  def __init__(self, values):
    self.values = values


class InteractiveDropdown():
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
    self._interactive_dropdown = InteractiveDropdown(title, options)
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


view_factory = ViewFactory()


class ViewController():
  @staticmethod
  def entry():
    sv = SelectionView('Role', ['Admin', 'PM', 'Member'])
    return sv.get_widget()

  @staticmethod
  def response_by_altering_view(request):
    import copy
    clear_output(wait=True)
    if 'Role' in request.values.keys():
      if request.values['Role'] == 'PM':
        sv1 = SelectionView('Role', ['PM', 'Admin', 'Member'])
        sv2 = SelectionView('PM', ToyDB.project_list)
        widget = VBox([
            sv1.get_widget(),
            sv2.get_widget()])
      elif request.values['Role'] == 'Member':
        sv1 = SelectionView('Role', ['Member', 'Admin', 'PM'])
        sv2 = SelectionView('Member', ToyDB.unique_members)
        widget = VBox([
            sv1.get_widget(),
            sv2.get_widget()
        ])
      else:  # Role: Admin
        sv = SelectionView('Role', ['Admin', 'PM', 'Member'])
        widget = VBox([
            sv.get_widget(),
            view_factory.build_view('all')
        ])
        # print("Show Admin Table View")

    else:
      if 'PM' in request.values.keys():
        project = request.values['PM']
        sv1 = SelectionView('Role', ['PM', 'Admin', 'Member'])

        list_here = copy.copy(ToyDB.project_list)
        list_here.remove(project)
        sv2 = SelectionView('PM', [project] + list_here)
        widget = VBox([
            sv1.get_widget(),
            sv2.get_widget(),
            view_factory.build_view('project', project)
        ])
        # print("Show PM Table View for", project)

      elif 'Member' in request.values.keys():
        member = request.values['Member']
        sv1 = SelectionView('Role', ['Member', 'Admin', 'PM'])
        list_here = copy.copy(ToyDB.unique_members)
        list_here.remove(member)
        sv2 = SelectionView('Member', [member] + list_here)
        widget = VBox([
            sv1.get_widget(),
            sv2.get_widget(),
            view_factory.build_view('member', member)
        ])
        # print("Show Member Table View for", member)
    display(widget)
