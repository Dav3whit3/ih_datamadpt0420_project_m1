import pandas as pd
from sqlalchemy import create_engine


def connection(db_path):
    print(f'Connecting to {db_path}')
    db_connection = create_engine(f'sqlite:////{db_path}')

    return db_connection


def sql_query_to_df(table, data_base):
    select_all_query = pd.read_sql_query(f'SELECT * FROM {table}', data_base)
    return select_all_query


def tables_to_df(db_path):
    data_base = connection(db_path)
    table_names = data_base.table_names()

    df_list = []

    for table in table_names:
        sql_query = sql_query_to_df(table, data_base)
        df_list.append(sql_query)

    return df_list
