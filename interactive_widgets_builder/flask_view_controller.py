import copy
import json

from ipywidgets.embed import embed_data

from interactive_widgets_builder.role_specific_view_builder import (
    building_admin_view,
    building_pm_view,
    building_member_view)
from table_info_extractor.toy_db_info_initialize import ToyDB


class ViewController():
  # template ipython widget embedding
  def __get_ipython_widget_embedding(self,
                                     empty=False,
                                     role='Admin',
                                     condition=None):

    if empty == True:
      return {'manager_state': None, 'widget_views': [None]}
    else:
      assert role == 'Admin' or role == 'PM' or role == 'Member'
      if role == 'Admin':
        view = building_admin_view()
      elif role == 'PM':
        assert condition in self.project_list
        view = building_pm_view(condition)
      else:  # if role == 'Member':
        assert condition in self.unique_members
        view = building_member_view(condition)
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

    from itertools import chain
    self.project_list = ToyDB.project_list  # list(ToyDB.project_members_info.keys())
    self.unique_members = ToyDB.unique_members
    '''
    list(
        set(
            chain(*(list(ToyDB.project_members_info.values()) +
                    list(ToyDB.table_members_info.values())))))
    '''
    self.titles = ['Role']
    self.options_collection = {'Role': ['Admin', 'PM', 'Member']}
    self.ipywidget_info = self.__get_ipython_widget_embedding(empty=True)

  def reordering_option_lists(self, request):
    # aka. moving the selected option to the front
    for title in self.titles:
      selected_value = request.values[title]
      self.options_collection[title].remove(selected_value)
      self.options_collection[title] = [
          selected_value
      ] + self.options_collection[title]

  def _remove_second_selection_dropdown(self):
    del self.options_collection[self.titles[-1]]
    self.titles.pop()

  def _add_second_selection_dropdown(self, role):
    assert len(self.titles) == 1 and self.titles[0] == 'Role'
    assert role == 'PM' or role == 'Member'
    if role == 'PM':
      self.titles.append('PM')
      self.options_collection['PM'] = copy.copy(self.project_list)
    else:  # role == 'Member'
      self.titles.append('Member')
      self.options_collection['Member'] = copy.copy(self.unique_members)

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
          print("In 2.1.2: PM or Member is the new role")
          print("Note: In this case, the old role is always PM or Member")
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
        print("In 2.2: role is not changed")
        self.reordering_option_lists(request)
        if new_role == 'PM':
          print("In 2.2.1: ")
          print("Project " + request.values['PM'] + " selected!")
          self.ipywidget_info = self.__get_ipython_widget_embedding(
              empty=False, role='PM', condition=request.values['PM'])
        else:  # new_role == 'Member'
          print("In 2.2.2: ")
          print("Member " + request.values['Member'] + " selected!")
          self.ipywidget_info = self.__get_ipython_widget_embedding(
              empty=False,
              role='Member',
              condition=request.values['Member'])
