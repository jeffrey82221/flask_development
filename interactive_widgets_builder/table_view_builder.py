from ipywidgets import widgets, GridspecLayout, Layout, Box, Label, VBox
# from ipywidgets.embed import embed_minimal_html
from table_info_extractor.table_rander import TableRanderer


def __plot_cell(description, bold=False):
  if bold:
    return Box([Label(description)],
               layout=Layout(border='solid 2px', width='100%'))
  else:
    return Box([Label(description)],
               layout=Layout(border='solid 1px', width='100%'))


def __plot_head_columns(columns):
  '''
This function plot the header column, which specifying the column name of
the rest of the table rows.
Argument:
 - columns: a list of column names.
'''
  header = GridspecLayout(1, len(columns))
  for j, column in enumerate(columns):
    header[0, j] = __plot_cell(str(column), bold=True)
  return header


def __plot_non_expandable_table_content(table):
  column_count = len(table.columns)
  row_count = len(table)
  grid = GridspecLayout(row_count, column_count)
  for i in range(row_count):
    for j, column in enumerate(table.columns):
      grid[i, j] = __plot_cell(str(table[column][i]))
  vis = grid
  return vis


def __plot_content_row(table, row_index, condition):
  column_count = len(table.columns)

  one_row_grid = GridspecLayout(1, column_count)
  for j, column in enumerate(table.columns):
    one_row_grid[0, j] = __plot_cell(str(table[column][row_index]))
  return one_row_grid


def __plot_project_specific_accordion(project_name):
  # TODO: change condition inside to project_name
  project_specific_table_info = TableRanderer.get_project_specific_table_info(project_name)
  accordion = widgets.Accordion(children=[
      __build_table_widget(project_specific_table_info.reset_index())
  ],
      selected_index=None,
      layout=Layout(border='solid 1px',
                    width='75.5%'))
  accordion.set_title(
      0, 'show info of tables: ' +
      ", ".join(list(project_specific_table_info.index)))
  return accordion


def __plot_project_specific_member_level_accordion(project_name):
  table_info_used_here = TableRanderer.get_project_specific_member_level_table_info(
      project_name)
  accordion = widgets.Accordion(children=[
      __build_table_widget(table_info_used_here.reset_index(),
                           with_subtable=True,
                           current_level='member',
                           next_level='table',
                           previous_condition=project_name)
  ],
      selected_index=None,
      layout=Layout(border='solid 1px',
                    width='99.5%'))
  accordion.set_title(
      0,
      'show info of members: ' + ", ".join(list(table_info_used_here.index)))
  return accordion


def __plot_member_specific_accordion(member_name, project_name=None):
  # [V] change previous_condition to project_name
  # [V] change condition to member_name
  if project_name != None:
    member_specific_table_info = TableRanderer.get_project_member_specific_table_info(
        project_name, member_name)
  else:
    member_specific_table_info = TableRanderer.get_member_specific_table_info(
        member_name)
  accordion = widgets.Accordion(children=[
      __build_table_widget(member_specific_table_info.reset_index())
  ],
      selected_index=None,
      layout=Layout(border='solid 1px',
                    width='75.5%'))
  accordion.set_title(
      0, 'show info of tables: ' +
      ", ".join(list(member_specific_table_info.index)))
  return accordion


def __build_table_widget(
        table,
        with_subtable=False,
        current_level='project',
        next_level='member',
        previous_condition=None  # e.g., the name of the project
):
  '''
Arguments:
 - table: the pandas table that should be plot as table view.
 - with_subtable: true if the table has sub-tables; o.w., false.
    (should be false if current_level == 'table')
 - current_level: the table level, 'project', 'member', or 'table'.
 - next_level: the level of the sub table. (should be 'member' or 'table')
 - previous_condition: the name of the project or member specified.
 Return:
 - an ipywidgets object
'''
  assert current_level == 'project' or current_level == 'member' or current_level == 'table'
  # assert next_level == 'member' or next_level == 'table'
  if current_level == 'table':
    assert with_subtable == False

  column_count = len(table.columns)
  row_count = len(table)
  table['idle_time'] = table['idle_time'].apply(lambda x: round(x, 2))
  # Plot Header

  header = __plot_head_columns(table.columns)
  # Plot Table Content
  if not with_subtable:
    # no sub-table
    vis = __plot_non_expandable_table_content(table)
  else:
    # making sub-table
    grids = []
    for row_index in range(row_count):
      condition = table['name'][row_index]
      # the name of the project, the member, or the table

      one_row_grid = __plot_content_row(table, row_index, condition)
      grids.append(one_row_grid)
      if next_level == 'table':
        assert current_level == 'project' or current_level == 'member'
        if current_level == 'project':
          accordion = __plot_project_specific_accordion(
              project_name=condition)
        else:  # member
          accordion = __plot_member_specific_accordion(
              member_name=condition, project_name=previous_condition)

      elif next_level == 'member':  # next-level == 'member'
        assert current_level == 'project'
        accordion = __plot_project_specific_member_level_accordion(
            project_name=condition)

      grids.append(accordion)
    vis = VBox(grids)
  return VBox([header, vis])


# TODO: move the following func to the table_info_extractor package


def fetch_table_info_of_current_level(current_level,
                                      condition, condition_type):

  # fetching the right table
  if current_level == 'project':
    assert condition == None and condition_type == None
    table_info_of_current_level = TableRanderer.get_project_level_table_info()
  elif current_level == 'member':
    if condition == None:
      table_info_of_current_level = TableRanderer.get_member_level_table_info()
    else:
      assert condition_type == 'project'
      table_info_of_current_level = TableRanderer.get_project_specific_member_level_table_info(
          condition)
  else:
    if condition == None:
      table_info_of_current_level = TableRanderer.get_table_info()
    else:
      if type(condition) != tuple:
        assert condition_type == 'member' or condition_type == 'project'
        if condition_type == 'member':
          table_info_of_current_level = TableRanderer.get_member_specific_table_info(
              condition)
        else:  # condition_type == 'project'
          table_info_of_current_level = TableRanderer.get_project_specific_table_info(
              condition)
      else:
        table_info_of_current_level = TableRanderer.get_project_member_specific_table_info(
            condition[0], condition[1])
  return table_info_of_current_level


# top


def build_top_table_widget(current_level='project',
                           with_subtable=True,
                           next_level='member',
                           condition=None,
                           condition_type=None):
  '''
Argument:
  - current_level : the level ('project', 'member', or 'table') we
    focused on in to top view
  - with_subtable: whether or not the table can be expand for checking
    the table information of lower levels.
  - next_level: the level of the sub-table
  - condition: whether this table is conditioned on a specific project or member
    (if both type is conditioned, sent in a tuple where the first
     element the project and the second the member.)
  - condition_type: the type of the condition ("project" or "member")
Return:
  - an ipywidgets object
'''
  #
  if current_level == 'project' and with_subtable:
    assert next_level != 'project'
  if current_level == 'member' and with_subtable:
    assert next_level != 'project' and next_level != 'member'
  if current_level == 'table':
    with_subtable = False
    next_level = None
  table_info_of_current_level = fetch_table_info_of_current_level(
      current_level, condition, condition_type)
  # building widget from the table
  table_widget = __build_table_widget(
      table_info_of_current_level.reset_index(),
      with_subtable=with_subtable,
      current_level=current_level,
      next_level=next_level)
  return table_widget


'''
build_table_widget(
    current_level = 'project',
    with_subtable = False)
build_table_widget(
    current_level = 'member',
    with_subtable = True,
    next_level = 'table')
build_table_widget(
    current_level = 'member',
    with_subtable = False
    )
build_table_widget(
    current_level = 'table',
    with_subtable = False)
# Project Specific
build_table_widget(
    current_level = 'member',
    with_subtable = True,
    next_level = 'table',
    condition = 'recommendation_system',
    condition_type = 'project'
    )

build_table_widget(
    current_level = 'table',
    with_subtable = False,
    condition = 'recommendation_system',
    condition_type = 'project'
    )
# Member specific
build_table_widget(
    current_level = 'table',
    with_subtable = False,
    condition = '54345',
    condition_type = 'member'
    )
# Project member specific
build_table_widget(
    current_level = 'table',
    with_subtable = False,
    condition = ('recommendation_system','54345'),
    )
'''

# embed_minimal_html('export.html', views=[accordion], title='Widgets export')

# TODO:
# 1. [V] append member list into the title of member-level accordion
# 2. [V] append table names into the titles of table-level accordion
# 3. [V] allow nested: implemented in role_specific_table_view_builder
