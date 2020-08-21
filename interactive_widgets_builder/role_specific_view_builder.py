from table_info_extractor.toy_db_info_initialize import *
from table_info_extractor.table_rander import *
from interactive_widgets_builder.table_view_builder import build_top_table_widget

from ipywidgets import widgets, VBox, Label
from ipywidgets.embed import embed_minimal_html


def building_db_admin_html_view(platform='jupyter'):
  assert platform == 'jupyter' or platform == 'flask'
  project_level_table_view = build_top_table_widget(
      current_level='project',
      with_subtable=True,
      next_level='member')
  member_level_table_view = build_top_table_widget(
      current_level='member',
      with_subtable=True,
      next_level='table')
  table_view = build_top_table_widget(
      current_level='table')
  tab_nest = widgets.Tab()
  tab_nest.children = [
      project_level_table_view,
      member_level_table_view,
      table_view
  ]
  tab_nest.set_title(0, 'project-level information')
  tab_nest.set_title(1, 'member-level information')
  tab_nest.set_title(2, 'table-level information')
  if platform == 'flask':
    embed_minimal_html('db_admin.html', views=[tab_nest], title='DB Admin')
    return open('db_admin.html').read()
  else:  # platform == jupyter
    return tab_nest


def building_db_pm_html_view(project_name, platform='jupyter'):
  assert platform == 'jupyter' or platform == 'flask'
  '''project_level_table_view = build_table_widget(
      current_level = 'project',
      with_subtable = True,
      next_level = 'member')'''
  member_level_table_view = build_top_table_widget(
      current_level='member',
      with_subtable=True,
      next_level='table',
      condition=project_name,
      condition_type='project')

  table_view = build_top_table_widget(
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


def building_db_member_html_view(member_name, platform='jupyter'):
  assert platform == 'jupyter' or platform == 'flask'
  table_view = build_top_table_widget(
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
