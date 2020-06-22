import pandas as pd
from sqlalchemy import create_engine

# acquisition functions

def conection(path):
    db_connection = create_engine(f'sqlite:////{path}')

    return db_connection


def table_names():
    table_names = db_connection.table_names()

    return table_names


def sql_query_to_df(table):
    select_all_query = pd.read_sql_query(f'SELECT * FROM {table}', db_connection)

    return select_all_query


def tables_to_df():
    df_list = []
    for table in table_names():
        sql_query = sql_query_to_df(table)
        df_list.append(sql_query)

    return df_list

tables_to_df()

"""
def acquire():
    data = pd.read_csv('./data/raw/vehicles.csv')
    return data
"""