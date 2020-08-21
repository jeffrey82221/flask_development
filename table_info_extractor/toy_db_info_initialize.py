# project_list = ['recommendation_system','computer_vision','credit_card']
# people_id_list = ['21375', '12345', '54345', '35634', '23543', '98467', '58576', '48765']
# feature_table_list = ['rs_1', 'rs_2', 'rs_3', 'cv_1', 'cv_2', 'cc_1', 'cc_2']
from itertools import chain
class ToyDB():

    project_members_info = {
        'recommendation_system': ['21375', '12345', '54345'],
        'computer_vision': ['54345', '35634', '23543'],
        'credit_card': ['35634', '23543', '98467', '58576', '48765']
    }
    project_tables_info = {
        'recommendation_system': ['rs_1', 'rs_2', 'rs_3'],
        'computer_vision': ['cv_1', 'cv_2'],
        'credit_card': ['cc_1', 'cc_2']
    }
    table_members_info = {
        'rs_1': ['21375', '12345', '58576'],
        'rs_2': ['12345', '54345', '58576'],
        'rs_3': ['21375', '12345', '54345', '48765'],
        'cv_1': ['54345'],
        'cv_2': ['35634', '23543'],
        'cc_1': ['35634', '23543', '98467'],
        'cc_2': ['23543', '98467', '58576', '48765'],
    }
    table_size_info = {
        'rs_1': 21,
        'rs_2': 30,
        'rs_3': 34,
        'cv_1': 100,
        'cv_2': 145,
        'cc_1': 4,
        'cc_2': 5
    }
    table_idle_time_info = {
        'rs_1': 1.5,
        'rs_2': 4.2,
        'rs_3': 1.2,
        'cv_1': 13.2,
        'cv_2': 23.2,
        'cc_1': 4.4,
        'cc_2': 5.3
    }

    member_tables_info = {}
    for table, members in table_members_info.items():
        for member in members:
            if member in member_tables_info:
                member_tables_info[member].add(table)
            else:
                member_tables_info[member] = set([table])

    for member, tables in member_tables_info.items():
        member_tables_info[member] = list(tables)

    project_list = list(project_members_info.keys())
    table_list = list(table_members_info.keys())

    unique_members = list(set(
        chain(*(list(project_members_info.values()) + list(table_members_info.values())))
    ))
