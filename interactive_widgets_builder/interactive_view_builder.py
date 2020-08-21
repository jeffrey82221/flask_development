from IPython.display import display, clear_output

import ipywidgets as widgets
from ipywidgets import HBox, VBox, interactive

from table_info_extractor.toy_db_info_initialize import *
from interactive_widgets_builder.role_specific_view_builder import (
    building_db_admin_html_view,
    building_db_pm_html_view,
    building_db_member_html_view)


class __DropdownRecorder():
  def __init__(self):
    self.selected_result = None

  def func(self, x):
    self.selected_result = x


class __ButtonReactor():
  def __init__(self, title, dropdown_recorder, output_widget, table_widget_builders):
    self.selected_role = None
    self.title = title
    self.dropdown_recorder = dropdown_recorder
    self.output_widget = output_widget
    self.table_widget_builders = table_widget_builders

  def on_button_clicked(self, b):
    if self.title == 'Role':
      if self.dropdown_recorder.selected_result == 'Admin':
        with self.output_widget:
          clear_output(wait=True)
          display(self.table_widget_builders['Admin']())
      elif self.dropdown_recorder.selected_result == 'PM':
        with self.output_widget:
          clear_output(wait=True)
          display(get_selection_view(title='PM', options=project_list))
        self.selected_role = 'PM'
      else:
        with self.output_widget:
          clear_output(wait=True)
          display(
              get_selection_view(title='Member', options=unique_members))
        self.selected_role = 'Member'
    else:
      with self.output_widget:
        clear_output(wait=False)
        print("showing table infos for " +
              self.dropdown_recorder.selected_result)
        display(self.table_widget_builders[self.selected_role](
            self.dropdown_recorder.selected_result))


def get_selection_view(
        title='Role',
        options=['Admin', 'PM', 'Member'],
        table_widget_builders={
            'Admin': building_db_admin_html_view,
            'PM': building_db_pm_html_view,
            'Member': building_db_member_html_view
        }):
  dropdown_recorder = __DropdownRecorder()

  dropdown = widgets.Dropdown(options=options,
                              description=title + ':',
                              disabled=False)

  interactive_dropdown = interactive(
      dropdown_recorder.func,
      x=dropdown)

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
  button_reactor = __ButtonReactor(
      title,
      dropdown_recorder,
      output_widget,
      table_widget_builders
  )

  button.on_click(button_reactor.on_button_clicked)
  return VBox([HBox([interactive_dropdown, button]), output])


# view = get_selection_view()
# view

# TODO:
# 1. [V] allow forum switching interactivity
# 2. [V] how to remove displayed items interactively:
#      - using clear_output(wait=True)
