from ipywidgets import widgets
from ipywidgets.embed import embed_minimal_html

from table_info_extractor.table_rander import TableRanderer

from interactive_widgets_builder.table_randerer_interface import TableOrganizer
from interactive_widgets_builder.table_view_builder import TableViewBuilder


class ViewFactory():
  def __init__(self):
    self.view_types = ['all', 'project', 'member']
    self.randerer_flows = {
        'all-1': [
            TableRanderer.get_project_level_table_info,
            TableRanderer.get_project_specific_member_level_table_info,
            TableRanderer.get_project_member_specific_table_info
        ],
        'all-2': [
            TableRanderer.get_member_level_table_info,
            TableRanderer.get_member_specific_table_info
        ],
        'all-3': [TableRanderer.get_table_info],
        'project-1': [
            TableRanderer.get_project_specific_member_level_table_info,
            TableRanderer.get_project_member_specific_table_info
        ],
        'project-2': [TableRanderer.get_project_specific_table_info],
        'member': [TableRanderer.get_member_specific_table_info]
    }
    self.level_names_config = {
        'all-1': ['project', 'member', 'table'],
        'all-2': ['member', 'table'],
        'all-3': ['table'],
        'project-1': ['member', 'table'],
        'project-2': ['table'],
        'member': ['table']
    }
    self.mode_of_each_view_type = {
        'all': ['all-1', 'all-2', 'all-3'],
        'project': ['project-1', 'project-2'],
        'member': ['member']
    }

  def build_view(self, view_type, condition=None, platform='jupyter'):
    randerer_flow_keys = self.mode_of_each_view_type[view_type]
    table_widget_list = []
    for i, key in enumerate(randerer_flow_keys):
      tvb = TableViewBuilder(
          TableOrganizer(table_randerers=self.randerer_flows[key],
                         level_names=self.level_names_config[key]))
      table_widget = tvb.build_table_widget(
          conditions=[condition] if condition else [])
      table_widget_list.append(table_widget)
    tab_nest = widgets.Tab()
    tab_nest.children = table_widget_list
    for i, key in enumerate(randerer_flow_keys):
      tab_nest.set_title(
          i, '{level_name}-level information'.format(
              level_name=self.level_names_config[key][0]))
    if platform == 'flask':
      temp_file_name = '{view_type}.html'.format(view_type=view_type)
      embed_minimal_html(temp_file_name,
                         views=[tab_nest],
                         title='DB Information')
      return open(temp_file_name).read()
    else:  # platform == jupyter
      return tab_nest


'''def building_admin_view(platform='jupyter'):
  assert platform == 'jupyter' or platform == 'flask'
  tvb = TableViewBuilder(TableOrganizer(
      table_randerers=[
          TableRanderer.get_project_level_table_info,
          TableRanderer.get_project_specific_member_level_table_info,
          TableRanderer.get_project_member_specific_table_info
      ],
      level_names=['project', 'member', 'table']
  ))
  project_level_table_view = tvb.build_table_widget()

  tvb = TableViewBuilder(TableOrganizer(
      table_randerers=[
          TableRanderer.get_member_level_table_info,
          TableRanderer.get_member_specific_table_info
      ],
      level_names=['member', 'table']
  ))
  member_level_table_view = tvb.build_table_widget()
  tvb = TableViewBuilder(TableOrganizer(
      table_randerers=[
          TableRanderer.get_table_info
      ],
      level_names=['table']
  ))
  table_level_view = tvb.build_table_widget()

  tab_nest = widgets.Tab()
  tab_nest.children = [
      project_level_table_view,
      member_level_table_view,
      table_level_view
  ]
  tab_nest.set_title(0, 'project-level information')
  tab_nest.set_title(1, 'member-level information')
  tab_nest.set_title(2, 'table-level information')
  if platform == 'flask':
    embed_minimal_html('db_admin.html', views=[tab_nest], title='DB Admin')
    return open('db_admin.html').read()
  else:  # platform == jupyter
    return tab_nest


def building_pm_view(project_name, platform='jupyter'):
  assert platform == 'jupyter' or platform == 'flask'
  tvb = TableViewBuilder(TableOrganizer(
      table_randerers=[
          TableRanderer.get_project_specific_member_level_table_info,
          TableRanderer.get_project_member_specific_table_info
      ],
      level_names=['member', 'table']
  ))
  member_level_table_view = tvb.build_table_widget(conditions=[project_name])

  tvb = TableViewBuilder(TableOrganizer(
      table_randerers=[
          TableRanderer.get_project_specific_table_info
      ],
      level_names=['table']
  ))
  table_level_view = tvb.build_table_widget(conditions=[project_name])

  tab_nest = widgets.Tab()
  tab_nest.children = [
      member_level_table_view,
      table_level_view
  ]
  tab_nest.set_title(0, 'member-level information')
  tab_nest.set_title(1, 'table-level information')
  if platform == 'flask':
    embed_minimal_html(project_name + '.html', views=[tab_nest], title=project_name)
    return open(project_name + '.html').read()
  else:  # platform == jupyter
    return VBox([Label(value="Project: " + project_name), tab_nest])


def building_member_view(member_name, platform='jupyter'):
  assert platform == 'jupyter' or platform == 'flask'
  tvb = TableViewBuilder(TableOrganizer(
      table_randerers=[
          TableRanderer.get_member_specific_table_info
      ],
      level_names=['table']
  ))
  table_level_view = tvb.build_table_widget(conditions=[member_name])

  tab_nest = widgets.Tab()
  tab_nest.children = [
      table_level_view
  ]
  tab_nest.set_title(0, 'table-level information')
  if platform == 'flask':
    embed_minimal_html(member_name + '.html', views=[tab_nest], title=member_name)
    return open(member_name + '.html').read()
  else:  # platform == jupyter
    return VBox([Label(value="Member: " + member_name), tab_nest])'''
