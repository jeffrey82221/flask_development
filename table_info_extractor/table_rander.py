from table_info_extractor.toy_db_info_initialize import ToyDB
import pandas as pd
table_info = pd.DataFrame([ToyDB.table_list,
                           [ToyDB.table_size_info[table_name] for table_name in ToyDB.table_list],
                           [ToyDB.table_idle_time_info[table_name] for table_name in ToyDB.table_list]
                           ]).T
table_info.columns = ['name', 'size', 'idle_time']
table_info.set_index('name', inplace=True)

'''
Project Level Table Info
'''
project_table_sizes = []
project_average_idle_times = []
project_table_counts = []
for project in ToyDB.project_list:
    tables = ToyDB.project_tables_info[project]
    total_size = table_info.loc[tables]['size'].sum()
    average_idle_time = table_info.loc[tables]['idle_time'].mean()
    project_table_counts.append(len(tables))
    project_table_sizes.append(total_size)
    project_average_idle_times.append(average_idle_time)

#
project_level_table_info = pd.DataFrame([
    ToyDB.project_list,
    project_table_sizes,
    project_average_idle_times,
    project_table_counts
]).T
project_level_table_info.columns = ['name', 'size', 'idle_time', 'count']
project_level_table_info.set_index('name', inplace=True)
project_level_table_info
# add members and tables tags
'''
Member Level Table Info
- general
'''

member_table_sizes = []
member_average_idle_times = []
member_table_counts = []
for member in ToyDB.unique_members:
    tables = ToyDB.member_tables_info[member]
    total_size = table_info.loc[tables]['size'].sum()
    average_idle_time = table_info.loc[tables]['idle_time'].mean()
    member_table_counts.append(len(tables))
    member_table_sizes.append(total_size)
    member_average_idle_times.append(average_idle_time)

#
member_level_table_info = pd.DataFrame([
    ToyDB.unique_members,
    member_table_sizes,
    member_average_idle_times,
    member_table_counts
]).T
member_level_table_info.columns = [
    'name',
    'size',
    'idle_time',
    'count'
]
member_level_table_info.set_index('name', inplace=True)
member_level_table_info

# TODO: add table and project tags

'''
 - project-specific (input: project)
'''
# 1. limit the members in member_tables_info to only those
# in the project.


def get_project_specific_member_level_table_info(target_project):
    # target_project = 'credit_card'
    members_of_the_project = ToyDB.project_members_info[target_project]
    project_specific_member_tables_info = dict(
        (member, ToyDB.member_tables_info[member])
        for member in members_of_the_project
    )
    # 2. limit the tables to only those belong to the project
    project_specific_tables = ToyDB.project_tables_info[target_project]
    project_specific_table_info = table_info.loc[
        project_specific_tables
    ]

    # 3. obtain project-specific member-level table
    member_table_sizes = []
    member_average_idle_times = []
    member_table_counts = []
    for member in members_of_the_project:
        tables = project_specific_member_tables_info[member]
        tables = list(set(tables) & set(project_specific_tables))
        total_size = project_specific_table_info.loc[tables]['size'].sum()
        average_idle_time = project_specific_table_info.loc[tables]['idle_time'].mean()
        member_table_counts.append(len(tables))
        member_table_sizes.append(total_size)
        member_average_idle_times.append(average_idle_time)
    #
    member_level_table_info = pd.DataFrame([
        members_of_the_project,
        member_table_sizes,
        member_average_idle_times,
        member_table_counts
    ]).T
    member_level_table_info.columns = [
        'name',
        'size',
        'idle_time',
        'count'
    ]
    member_level_table_info.set_index('name', inplace=True)
    return member_level_table_info
# TODO: add table tags
# get_project_specific_member_level_table_info('computer_vision')


'''
Table Info
- project-specific
'''


def get_project_specific_table_info(target_project):
    tables = ToyDB.project_tables_info[target_project]
    return table_info.loc[tables]


# get_project_specific_table_info('credit_card')
'''
- member-specific
'''


def get_member_specific_table_info(target_member):
    tables = ToyDB.member_tables_info[target_member]
    return table_info.loc[tables]


# get_member_specific_table_info(unique_members[1])
'''
- project-member-specific
'''


def get_project_member_specific_table_info(target_project, target_member):
    assert target_member in ToyDB.project_members_info[target_project]
    tables = set(ToyDB.project_tables_info[target_project]) & set(ToyDB.member_tables_info[target_member])
    return table_info.loc[tables]
