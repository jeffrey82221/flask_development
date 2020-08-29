from IPython.display import display, clear_output

import ipywidgets as widgets
from ipywidgets import HBox, VBox, interactive

from table_info_extractor.toy_db_info_initialize import ToyDB
from interactive_widgets_builder.view_factory import ViewFactory


class __DropdownRecorder():
  def __init__(self):
    self.selected_result = None

  def pass_info(self, selected_dropdown):
    self.selected_result = selected_dropdown


class __ButtonReactor():
  def __init__(self, title, dropdown_recorder, output_widget):
    self.selected_role = None
    self.title = title
    self.dropdown_recorder = dropdown_recorder
    self.output_widget = output_widget
    self.view_factory = ViewFactory()

  def on_button_clicked(self, b):
    if self.title == 'Role':
      if self.dropdown_recorder.selected_result == 'Admin':
        self.selected_role = None
        with self.output_widget:
          clear_output(wait=True)
          display(self.view_factory.build_view('all'))
        print(self.selected_role)
      elif self.dropdown_recorder.selected_result == 'PM':
        self.selected_role = 'PM'
        with self.output_widget:
          clear_output(wait=True)
          display(
              build_selection_view(title='PM',
                                   options=ToyDB.project_list))
        print(self.selected_role)
      else:
        self.selected_role = 'Member'
        with self.output_widget:
          clear_output(wait=True)
          display(
              build_selection_view(title='Member',
                                   options=ToyDB.unique_members))
        print(self.selected_role)
    else:
      with self.output_widget:
        clear_output(wait=True)
        if self.selected_role == 'Member':
          print(self.selected_role)
          display(
              self.view_factory.build_view(
                  'member', self.dropdown_recorder.selected_result))
        elif self.selected_role == 'PM':
          print(self.selected_role)
          display(
              self.view_factory.build_view(
                  'project', self.dropdown_recorder.selected_result))
        else:
          print('no in the display branch', self.selected_role)


def build_selection_view(title='Role', options=['Admin', 'PM', 'Member']):
  dropdown_recorder = __DropdownRecorder()

  dropdown = widgets.Dropdown(options=options,
                              description=title + ':',
                              disabled=False)

  interactive_dropdown = interactive(dropdown_recorder.pass_info,
                                     selected_dropdown=dropdown)

  output_widget = widgets.Output()

  button = widgets.Button(
      value=False,
      description='Enter',
      disabled=False,
      button_style='',  # 'success', 'info', 'warning', 'danger' or ''
      tooltip='Description',
      icon='Enter'  # (FontAwesome names without the `fa-` prefix)
  )

  # Button Interaction (define as a callback)
  button_reactor = __ButtonReactor(title, dropdown_recorder, output_widget)

  button.on_click(button_reactor.on_button_clicked)
  return VBox([HBox([interactive_dropdown, button]), output_widget])


# view = get_selection_view()
# view

# TODO:
# 1. [V] allow forum switching interactivity
# 2. [V] how to remove displayed items interactively:
#      - using clear_output(wait=True)
