import pandas as pd
from sqlalchemy import create_engine

# Functions in visual order


def tables_to_df(arguments):  # Exec number 1
    db_path = arguments
    data_base = db_connection(db_path)
    table_names = data_base.table_names()
    print(f"Obtaining tables from data base provided")

    df_list = []

    for table in table_names:
        sql_query = sql_query_to_df(table, data_base)
        print(f"Converting '{table}' table into data frame")
        df_list.append(sql_query)

    db_df = pd.DataFrame(df_list[0])
    for df in df_list[1:]:
        db_df = db_df.merge(df, left_on='uuid', right_on='uuid')

    print("Merging all DataFrames...")

    return db_df


def db_connection(db_path):
    print(f'Connecting to data base {db_path}')

    connection = create_engine(f'sqlite:////{db_path}')
    return connection


def sql_query_to_df(table, data_base):
    select_all_query = pd.read_sql_query(f'SELECT * FROM {table}', data_base)
    return select_all_query

