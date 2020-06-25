import pandas as pd
from sqlalchemy import create_engine

# Functions in visual order


def tables_to_df(arguments):
    db_path = arguments
    data_base = connection(db_path)
    table_names = data_base.table_names()
    print(f"Obtaining tables from data base provided")
    print("...")
    print("...")

    df_list = []

    for table in table_names:
        sql_query = sql_query_to_df(table, data_base)
        print(f"Converting {table} table into data frame")
        df_list.append(sql_query)

    return df_list


def connection(db_path):
    print(f'Connecting to {db_path}')
    print("...")
    print("...")
    db_connection = create_engine(f'sqlite:////{db_path}', pool_pre_ping=True)

    return db_connection


def sql_query_to_df(table, data_base):
    select_all_query = pd.read_sql_query(f'SELECT * FROM {table}', data_base)
    return select_all_query


def get_json(url, json_acum=[], calls=0):
    print(f'Getting info from {url}')
    response = requests.get(url)
    json = response.json()
    json_acum.append(json[:-1])

    link = json[-1]['links'][2]['href']

    next_link = f'{root}{link}'

    if calls <= 5:
        get_json(next_link, json_acum, calls + 1)

    jobs_df = pd.DataFrame(json_acum[0])

    return jobs_df


