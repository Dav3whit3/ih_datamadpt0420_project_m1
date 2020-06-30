import pandas as pd
from sqlalchemy import create_engine
import requests
import re
from bs4 import BeautifulSoup

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
        print(f"Converting '{table}' table into data frame")
        df_list.append(sql_query)

    db_df = pd.DataFrame(df_list[0])
    for df in df_list[1:]:
        db_df = db_df.merge(df, left_on='uuid', right_on='uuid')
    print("...")
    print("...")
    print("Merging all tables...")
    print("...")
    print("...")
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
    print("...")
    print("...")
    print(f'Getting job titles from API {url}')
    response = requests.get(url)
    json = response.json()
    json_acum.append(json[:-1])

    root = 'http://api.dataatwork.org/v1'

    for elem in json[-1]['links']:
        if elem['rel'] == 'next':
            link = elem['href']
            next_link = f'{root}{link}'
            get_job_titles(next_link, json_acum)
    print("...")
    print("...")

    return json_acum


def job_titles_to_DataFrame(url):
    json = get_job_titles(url)

    jobs_df = []
    for result in json:
        jobs_df.extend(result)

    jobs_df = pd.DataFrame(jobs_df)
    jobs_df.rename(columns={'uuid': 'normalized_job_code'}, inplace=True)

    return jobs_df


def get_country_names():
    url = 'https://www.iban.com/country-codes'
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('tr')

    a = str(items).split('<td>')

    paises = []
    for elem in a[1:]:
        match = re.search('(\w+\s\w+)', elem)
        if match:
            paises.append(re.findall('(\w+\s\w+)', elem))
        else:
            paises.append(re.findall('\w+', elem))

    countries = paises[0::4]
    codes = paises[1::4]

    country_codes = []
    for index, elem in enumerate(countries):
        country_codes.append([elem[0], codes[index][0]])
    country_codes = pd.DataFrame(country_codes, columns=['Country', 'country_code'])

    return country_codes
