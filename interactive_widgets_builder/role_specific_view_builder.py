from ipywidgets import widgets, VBox, Label
from ipywidgets.embed import embed_minimal_html

from table_info_extractor.table_rander import TableRanderer

from interactive_widgets_builder.table_randerer_interface import TableOrganizer
from interactive_widgets_builder.table_view_builder import TableViewBuilder


def building_admin_view(platform='jupyter'):
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
  '''project_level_table_view = build_table_widget(
      current_level = 'project',
      with_subtable = True,
      next_level = 'member')'''
  tvb = TableViewBuilder()
  member_level_table_view = tvb.build_top_table_widget(
      current_level='member',
      with_subtable=True,
      next_level='table',
      condition=project_name,
      condition_type='project')

  table_view = tvb.build_top_table_widget(
      current_level='table',
      with_subtable=False,
      condition=project_name,
      condition_type='project')

  tab_nest = widgets.Tab()
  tab_nest.children = [
      member_level_table_view,
      table_view
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
  tvb = TableViewBuilder()
  table_view = tvb.build_top_table_widget(
      current_level='table',
      with_subtable=False,
      condition=member_name,
      condition_type='member'
  )

  tab_nest = widgets.Tab()
  tab_nest.children = [
      table_view
  ]
  tab_nest.set_title(0, 'member-level information')
  tab_nest.set_title(1, 'table-level information')
  if platform == 'flask':
    embed_minimal_html(member_name + '.html', views=[tab_nest], title=member_name)
    return open(member_name + '.html').read()
  else:  # platform == jupyter
    return VBox([Label(value="Member: " + member_name), tab_nest])
