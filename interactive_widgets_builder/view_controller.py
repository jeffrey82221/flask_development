import copy

from interactive_widgets_builder.view_factory import ViewFactory
from table_info_extractor.toy_db_info_initialize import ToyDB

from interactive_widgets_builder.view_parameters import ParaHolder


class ViewController():
  # template ipython widget embedding

  def __init__(self, platform='flask'):
    assert platform == 'flask' or platform == 'jupyter'
    self.platform = platform
    self.dropdown_titles = ['Role', 'PM', 'Member']
    self._options_for_each_dropdown_titles = {
        'Role': ['Admin', 'PM', 'Member'],
        'PM': ToyDB.project_list,
        'Member': ToyDB.unique_members
    }
    self.view_factory = ViewFactory()
    self.entry_dropdown_title = 'Role'
    self.view_para_holder = ParaHolder(self.response_by_altering_view)

  def _get_reordered_option_list(self, dropdown_title, selected_result):

    options = copy.copy(
        self._options_for_each_dropdown_titles[dropdown_title])
    options.remove(selected_result)
    return [selected_result] + options

  def entry(self):
    self.view_para_holder.set_parameters(
        titles=[self.entry_dropdown_title],
        options_collection={
            'Role': self._options_for_each_dropdown_titles[self.entry_dropdown_title]
        },
        ipywidget=None
    )
    if self.platform == 'jupyter':
      self.view_para_holder.display_ipywidgets()

  def response_by_altering_view(self, request):

    # clear_output(wait=True)
    if 'Role' in request.values.keys():
      if request.values['Role'] == 'PM':
        self.view_para_holder.set_parameters(
            titles=['Role', 'PM'],
            options_collection={
                'Role': self._get_reordered_option_list('Role', 'PM'),
                'PM': self._options_for_each_dropdown_titles['PM']
            },
            ipywidget=None
        )
      elif request.values['Role'] == 'Member':
        self.view_para_holder.set_parameters(
            titles=['Role', 'Member'],
            options_collection={
                'Role': self._get_reordered_option_list('Role', 'Member'),
                'Member': self._options_for_each_dropdown_titles['Member']
            },
            ipywidget=None
        )
      else:  # Role: Admin
        self.view_para_holder.set_parameters(
            titles=['Role'],
            options_collection={
                'Role': self._get_reordered_option_list('Role', 'Admin')
            },
            ipywidget=self.view_factory.build_view('all')
        )
    else:
      if 'PM' in request.values.keys():
        selected_project = request.values['PM']
        self.view_para_holder.set_parameters(
            titles=['Role', 'PM'],
            options_collection={
                'Role': self._get_reordered_option_list('Role', 'PM'),
                'PM': self._get_reordered_option_list('PM', selected_project)
            },
            ipywidget=self.view_factory.build_view('project', selected_project)
        )
        # print("Show PM Table View for", project)

      elif 'Member' in request.values.keys():
        selected_member = request.values['Member']
        self.view_para_holder.set_parameters(
            titles=['Role', 'Member'],
            options_collection={
                'Role': self._get_reordered_option_list('Role', 'Member'),
                'Member': self._get_reordered_option_list('Member', selected_member)
            },
            ipywidget=self.view_factory.build_view('member', selected_member)
        )
      else:
        print("Error: no such selection...")
    if self.platform == 'jupyter':
      self.view_para_holder.display_ipywidgets()
