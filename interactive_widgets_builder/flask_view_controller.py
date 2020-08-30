import copy
import json

from ipywidgets.embed import embed_data

from interactive_widgets_builder.view_factory import ViewFactory
from table_info_extractor.toy_db_info_initialize import ToyDB


class ViewController():
  # template ipython widget embedding
  def _bridge_ipywidget_to_front_parameters(self, view=None):
    if view == None:
      return {'manager_state': None, 'widget_views': [None]}
    else:
      data = embed_data(views=[view])
      manager_state = json.dumps(data['manager_state'])
      widget_views = [
          json.dumps(view_spec) for view_spec in data['view_specs']
      ]
      return {
          'manager_state': manager_state,
          'widget_views': widget_views
      }

  def __init__(self):
    self.dropdown_titles = ['Role', 'PM', 'Member']
    self._options_for_each_dropdown_titles = {
        'Role': ['Admin', 'PM', 'Member'],
        'PM': ToyDB.project_list,
        'Member': ToyDB.unique_members
    }
    self.view_factory = ViewFactory()
    self.titles = ['Role']
    self.entry_dropdown_title = 'Role'
    self.options_collection = {
        'Role': self._options_for_each_dropdown_titles[self.entry_dropdown_title]
    }
    self.ipywidget_info = self._bridge_ipywidget_to_front_parameters()

  def _get_reordered_option_list(self, dropdown_title, selected_result):
    import copy
    options = copy.copy(
        self._options_for_each_dropdown_titles[dropdown_title])
    options.remove(selected_result)
    return [selected_result] + options

  def response_by_altering_view(self, request):
    import copy
    # clear_output(wait=True)
    if 'Role' in request.values.keys():
      if request.values['Role'] == 'PM':
        self.options_collection = {
            'Role': self._get_reordered_option_list('Role', 'PM'),
            'PM': self._options_for_each_dropdown_titles['PM']
        }
        self.titles = ['Role', 'PM']
        widget = None
      elif request.values['Role'] == 'Member':
        self.options_collection = {
            'Role': self._get_reordered_option_list('Role', 'Member'),
            'Member': self._options_for_each_dropdown_titles['Member']
        }
        self.titles = ['Role', 'Member']
        widget = None
      else:  # Role: Admin
        self.options_collection = {
            'Role': self._get_reordered_option_list('Role', 'Admin')
        }
        self.titles = ['Role']
        widget = self.view_factory.build_view('all')

    else:
      if 'PM' in request.values.keys():
        selected_project = request.values['PM']
        self.options_collection = {
            'Role': self._get_reordered_option_list('Role', 'PM'),
            'PM': self._get_reordered_option_list('PM', selected_project)
        }
        self.titles = ['Role', 'PM']
        widget = self.view_factory.build_view('project', selected_project)
        # print("Show PM Table View for", project)

      elif 'Member' in request.values.keys():
        selected_member = request.values['Member']
        self.options_collection = {
            'Role': self._get_reordered_option_list('Role', 'Member'),
            'Member': self._get_reordered_option_list('Member', selected_member)
        }
        self.titles = ['Role', 'Member']
        widget = self.view_factory.build_view('member', selected_member)
      else:
        print("Error: no such selection...")
    self.ipywidget_info = self._bridge_ipywidget_to_front_parameters(
        widget
    )


'''
  def response_by_altering_view(self, request):
    # if there is only the role selection view
    print("Request:")
    print(request.values)
    if ('PM' not in request.values.keys()) and (
            'Member' not in request.values.keys()):
      print("In 1: Not yet showing the second selection dropdown (i.e., that for PM and Member).")
      self.reordering_option_lists(request)
      selected_role = request.values['Role']
      if selected_role == 'Admin':
        print("In 1.1: Selecting Admin as role from the first dropdown list.")
        print("Showing Admin Table View ...")
        self.ipywidget_info = self.__get_ipython_widget_embedding(
            empty=False, role='Admin')
      elif selected_role == 'PM':
        print("In 1.2: Selecting PM as role from the first dropdown list.")
        self._add_second_selection_dropdown('PM')
        self.ipywidget_info = self.__get_ipython_widget_embedding(
            empty=True)
      else:  # selected_role == 'Member'
        print("In 1.3: Selecting Member as role from the first dropdown list.")
        self._add_second_selection_dropdown('Member')
        self.ipywidget_info = self.__get_ipython_widget_embedding(
            empty=True)
    # if there are two selection views
    else:
      print("In 2: A selection made on the second dropdown.")
      assert 'Role' in request.values.keys()
      new_role = request.values['Role']
      old_role = self.options_collection['Role'][0]
      # if role is changed
      if new_role != old_role:
        print("In 2.1: Role is changed.")
        # alter the second selection dropdown
        if new_role == 'Admin':
          print("In 2.1.1: Admin is the new role.")
          self.reordering_option_lists(request)
          self._remove_second_selection_dropdown()
          self.ipywidget_info = self.__get_ipython_widget_embedding(
              empty=False, role='Admin')
        else:
          print("In 2.1.2: PM or Member is the new role.")
          print("Note: In this case, the old role is always PM or Member.")
          assert old_role != 'Admin'
          self.reordering_option_lists(request)
          # if old_role != 'Admin':
          #  print("remove the second dropdown because the original role is not Admin")
          self._remove_second_selection_dropdown()
          self._add_second_selection_dropdown(new_role)
          self.ipywidget_info = self.__get_ipython_widget_embedding(
              empty=True)

      # if role is not changed
      else:
        print("In 2.2: Role remains unchanged.")
        self.reordering_option_lists(request)
        if new_role == 'PM':
          print("In 2.2.1: Project " + request.values['PM'] + " selected.")
          self.ipywidget_info = self.__get_ipython_widget_embedding(
              empty=False, role='PM', condition=request.values['PM'])
        else:  # new_role == 'Member'
          print("In 2.2.2: Member " + request.values['Member'] + " selected.")
          self.ipywidget_info = self.__get_ipython_widget_embedding(
              empty=False,
              role='Member',
              condition=request.values['Member'])
'''
