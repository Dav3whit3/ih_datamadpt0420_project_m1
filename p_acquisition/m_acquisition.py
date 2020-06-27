import pandas as pd
from sqlalchemy import create_engine
import requests

# Functions in visual order


def merge_data():
    #db_df.merge()
    pass


def tables_to_df(arguments):  # Exec number 1
    db_path = arguments
    data_base = db_connection(db_path)
    table_names = data_base.table_names()
    print(f"Obtaining tables from data base provided")
    print("...")
    print("...")

    df_list = []

    for table in table_names:
        sql_query = sql_query_to_df(table, data_base)
        print(f"Converting {table} table into data frame")
        df_list.append(sql_query)

    db_df = pd.DataFrame(df_list[0])
    for df in df_list[1:]:
        db_df = db_df.merge(df, left_on='uuid', right_on='uuid')

    return db_df


def db_connection(db_path):
    print(f'Connecting to {db_path}')
    print("...")
    print("...")
    connection = create_engine(f'sqlite:////{db_path}')
    return connection


def sql_query_to_df(table, data_base):
    select_all_query = pd.read_sql_query(f'SELECT * FROM {table}', data_base)
    return select_all_query


def get_job_titles(url, json_acum=[]):
    print(f'Getting info from {url}')
    response = requests.get(url)
    json = response.json()
    json_acum.append(json[:-1])

    root = 'http://api.dataatwork.org/v1'
    link = json[-1]['links'][2]['href']

    next_link = f'{root}{link}'

    if next_link:
        get_job_titles(next_link, json_acum)

    jobs_df = []
    for result in json_acum:
        jobs_df.extend(result)

    return pd.DataFrame(jobs_df)


