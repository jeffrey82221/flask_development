class TableOrganizer():
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
