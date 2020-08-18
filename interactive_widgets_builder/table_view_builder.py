from table_info_extractor.toy_db_info_initialize import *
from table_info_extractor.table_rander import *
from ipywidgets.embed import embed_minimal_html
from ipywidgets import widgets, GridspecLayout, Layout, Box, Label, VBox
def __create_expanded_button(description, bold = False):
  if bold:
    return Box([Label(description)],
              layout = Layout(
                border='solid 2px',
                width='100%'))
  else:
    return Box([Label(description)],
              layout = Layout(
                border='solid 1px',
                width='100%'))
def __build_table_widget(
    table,
    with_accordion = False,
    current_level = 'project',
    next_level = 'member',
    previous_condition = None # e.g., the name of the project
    ):
  table['idle_time'] = table['idle_time'].apply(lambda x:round(x,2))
  column_count = len(table.columns)
  row_count = len(table)
  # Plot Header
  header = GridspecLayout(1, column_count)
  for j, column in enumerate(table.columns):
    header[0, j] = __create_expanded_button(
      str(column),bold = True)

  # Plot Table Content
  if not with_accordion:
    # no sub-table
    grid = GridspecLayout(row_count, column_count)
    for i in range(row_count):
        for j, column in enumerate(table.columns):
            grid[i, j] = __create_expanded_button(
              str(table[column][i]))
    vis = grid
  else:
    # making sub-table
    grids = []
    for i in range(row_count):
        condition = table['name'][i] # the name of the project, the member, or the table
        grid = GridspecLayout(1, column_count)
        for j, column in enumerate(table.columns):
            grid[0, j] = __create_expanded_button(
              str(table[column][i]))
        grids.append(grid)
        if next_level == 'table':
          assert current_level == 'project' or current_level == 'member'
          if current_level == 'project':
            project_specific_table_info = get_project_specific_table_info(
                condition
              )
            accordion = widgets.Accordion(children=[
              __build_table_widget(
                  project_specific_table_info.reset_index())],
              selected_index=None,
              layout = Layout(
                  border='solid 1px',
                  width='75.5%'
                )
              )
            table_info_used_here = project_specific_table_info
          else: # member
            if previous_condition != None:
              member_specific_table_info = get_project_member_specific_table_info(
                      previous_condition, condition
                )
            else:
              member_specific_table_info = get_member_specific_table_info(
                      condition
                )
            accordion = widgets.Accordion(children=[
              __build_table_widget(
                  member_specific_table_info.reset_index())],
              selected_index=None,
              layout = Layout(
                  border='solid 1px',
                  width='75.5%'
                )
              )
            table_info_used_here = member_specific_table_info
          accordion.set_title(
              0,
              'show info of tables: ' + ", ".join(list(table_info_used_here.index)))
        elif next_level == 'member': # next-level == 'member'
          assert current_level == 'project'
          table_info_used_here = get_project_specific_member_level_table_info(
            condition)
          accordion = widgets.Accordion(children=[
            __build_table_widget(
                table_info_used_here.reset_index(),
                with_accordion = True,
                current_level = 'member',
                next_level = 'table',
                previous_condition = condition
                )],
            selected_index=None,
            layout = Layout(
                border='solid 1px',
                width='99.5%'
              )
            )
          accordion.set_title(
              0,
              'show info of members: '+ ", ".join(list(table_info_used_here.index)))
        grids.append(accordion)
    vis = VBox(grids)
  return VBox([header,vis])

# top
def build_table_widget(
    current_level = 'project',
    with_accordion = True,
    next_level = 'member',
    condition = None,
    condition_type = None
    ):
  # fetching the right table
  if current_level == 'project':
    if with_accordion:
      assert next_level != 'project'
    assert condition == None and condition_type == None
    table_info_of_current_level = project_level_table_info
  elif current_level == 'member':
    if with_accordion:
      assert next_level != 'project' and next_level != 'member'
    if condition == None:
      table_info_of_current_level = member_level_table_info
    else:
      assert condition_type == 'project'
      table_info_of_current_level = get_project_specific_member_level_table_info(condition)
  else:
    with_accordion = False
    next_level = None
    if condition == None:
      table_info_of_current_level = table_info
    else:
      if type(condition) != tuple:
        assert condition_type == 'member' or condition_type == 'project'
        if condition_type == 'member':
          table_info_of_current_level = get_member_specific_table_info(condition)
        else: # condition_type == 'project'
          table_info_of_current_level = get_project_specific_table_info(condition)
      else:
        table_info_of_current_level = get_project_member_specific_table_info(condition[0], condition[1])
  # building widget from the table
  table_widget = __build_table_widget(
      table_info_of_current_level.reset_index(),
      with_accordion = with_accordion,
      current_level = current_level,
      next_level = next_level
      )
  return table_widget
'''
build_table_widget(
    current_level = 'project',
    with_accordion = False)
build_table_widget(
    current_level = 'member',
    with_accordion = True,
    next_level = 'table')
build_table_widget(
    current_level = 'member',
    with_accordion = False
    )
build_table_widget(
    current_level = 'table',
    with_accordion = False)
# Project Specific
build_table_widget(
    current_level = 'member',
    with_accordion = True,
    next_level = 'table',
    condition = 'recommendation_system',
    condition_type = 'project'
    )

build_table_widget(
    current_level = 'table',
    with_accordion = False,
    condition = 'recommendation_system',
    condition_type = 'project'
    )
# Member specific
build_table_widget(
    current_level = 'table',
    with_accordion = False,
    condition = '54345',
    condition_type = 'member'
    )
# Project member specific
build_table_widget(
    current_level = 'table',
    with_accordion = False,
    condition = ('recommendation_system','54345'),
    )
'''

# embed_minimal_html('export.html', views=[accordion], title='Widgets export')

# TODO:
# 1. append member list into the title of member-level accordion
# 2. append table names into the titles of table-level accordion
# 3. allow nested
