from IPython.display import display
from table_info_extractor.toy_db_info_initialize import *
from interactive_widgets_builder.role_specific_view_builder import (building_db_admin_html_view,
                                                                    building_db_pm_html_view,
                                                                    building_db_member_html_view)
import ipywidgets as widgets
from ipywidgets import widgets, HBox, VBox, interactive
from IPython.display import clear_output


class __DropdownRecorder():
  def __init__(self):
    self.selected_result = None

  def func(self, x):
    self.selected_result = x


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
  interactive_dropdown = interactive(dropdown_recorder.func, x=dropdown)
  output = widgets.Output()
  button = widgets.Button(
      value=False,
      description='Enter',
      disabled=False,
      button_style='',  # 'success', 'info', 'warning', 'danger' or ''
      tooltip='Description',
      icon='Enter'  # (FontAwesome names without the `fa-` prefix)
  )

  def on_button_clicked(b):
    if title == 'Role':
      if dropdown_recorder.selected_result == 'Admin':
        with output:
          clear_output(wait=True)
          display(table_widget_builders['Admin']())
      elif dropdown_recorder.selected_result == 'PM':
        with output:
          clear_output(wait=True)
          display(get_selection_view(title='PM', options=project_list))
        selected_role = 'PM'
      else:
        with output:
          clear_output(wait=True)
          display(
              get_selection_view(title='Member', options=unique_members))
        selected_role = 'Member'
    else:
      with output:
        clear_output(wait=False)
        print("showing table infos for " +
              dropdown_recorder.selected_result)
        display(table_widget_builders[selected_role](
            dropdown_recorder.selected_result))

  button.on_click(on_button_clicked)
  return VBox([HBox([interactive_dropdown, button]), output])


# view = get_selection_view()
# view

# TODO:
# 1. [V] allow forum switching interactivity
# 2. [V] how to remove displayed items interactively:
#      - using clear_output(wait=True)
