from ipywidgets import widgets, GridspecLayout, Layout, Box, Label, VBox


class TableRandererOrganizer():
  def __init__(self, table_randerers, level_names):
    '''
    Argument:
     - table_randerers: a list of methods in TableRanderer listed
        from root level to leaf level.
     - level_names: the name of the level from root to leaf,
        e.g., ["group", "schema", "table"]
    '''
    self.table_randerers = table_randerers
    self.level_names = level_names


class TableViewBuilder():
  def __init__(self, table_organizer):
    self._table_organizer = table_organizer

  def __plot_cell(self, description, bold=False):
    if bold:
      return Box([Label(description)],
                 layout=Layout(border='solid 2px', width='100%'))
    else:
      return Box([Label(description)],
                 layout=Layout(border='solid 1px', width='100%'))

  def __plot_head_columns(self, table):
    '''
    This function plot the header column, which specifying the column name of
    the rest of the table rows.
    Argument:
      - columns: a list of column names.
    '''
    header = GridspecLayout(1, len(table.columns))
    for j, column in enumerate(table.columns):
      header[0, j] = self.__plot_cell(str(column), bold=True)
    return header

  def __plot_non_expandable_table_content(self, table):
    column_count = len(table.columns)
    row_count = len(table)
    grid = GridspecLayout(row_count, column_count)
    for i in range(row_count):
      for j, column in enumerate(table.columns):
        grid[i, j] = self.__plot_cell(str(table[column][i]))
    vis = grid
    return vis

  def plot_non_expandable_table(self, table):
    header = self.__plot_head_columns(table)
    content = self.__plot_non_expandable_table_content(table)
    return VBox([header, content])

  def __plot_content_row(self, table, row_index):
    column_count = len(table.columns)

    one_row_grid = GridspecLayout(1, column_count)
    for j, column in enumerate(table.columns):
      one_row_grid[0, j] = self.__plot_cell(str(table[column][row_index]))
    return one_row_grid

  def build_table_widget(
      self,
      randerer_id=0,
      conditions=[]
  ):
    '''
    conditions
    '''
    # Stopping Qiteria: no child-tables anymore
    if randerer_id == len(self._table_organizer.table_randerers) - 1:
      df = self._table_organizer.table_randerers[randerer_id](*conditions)
      return self.plot_non_expandable_table(df.reset_index())
    # Recursion Qiteria: continue to build sub-tables
    else:
      # setup artistic properties:
      if randerer_id != len(self._table_organizer.table_randerers) - 2:
        sub_table_widget_width = '99.5%'
      else:
        sub_table_widget_width = '75.5%'
      # get dataframe properties:
      table_randerer = self._table_organizer.table_randerers[randerer_id]
      df = table_randerer(*conditions)
      # build header:
      header = self.__plot_head_columns(df.reset_index())
      grids = []
      for i in range(len(df)):
        # build one column:
        condition = df.index[i]
        conditions_of_next_level = conditions + [condition]
        one_row_grid = self.__plot_content_row(df.reset_index(), i)
        grids.append(one_row_grid)
        # build the sub-table expansion button:
        sub_table_widget = widgets.Accordion(
            children=[
                self.build_table_widget(
                    randerer_id=randerer_id + 1,
                    conditions=conditions_of_next_level
                )
            ],
            selected_index=None,
            # TODO: fix the width using artistic interface
            layout=Layout(
                border='solid 1px',
                width=sub_table_widget_width)
        )
        sub_table_widget.set_title(0, 'show info of {level_name}s: '.format(
            level_name=self._table_organizer.level_names[randerer_id + 1]
        ) + ", ".join(list(
            self._table_organizer.table_randerers[randerer_id + 1](*conditions_of_next_level).index
        )))
        grids.append(sub_table_widget)
      return VBox([header, VBox(grids)])
