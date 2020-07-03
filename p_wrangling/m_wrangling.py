import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
from p_acquisition import m_acquisition as mac
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

def get_job_titles(url, json_acum=[]):
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
    country = country_codes[['Country']].drop_duplicates()
    code = country_codes[['country_code']].drop_duplicates()
    country_codes = pd.merge(country, code, left_index=True, right_index=True)

    return country_codes


def merge_data(arguments, url):
    db_tables = mac.tables_to_df(arguments)
    job_titles = job_titles_to_DataFrame(url)
    country_names = get_country_names()

    print("Creating final DataFrame")
    main_df = pd.merge(db_tables, job_titles, on='normalized_job_code', how='left')
    print("...")
    print("...")
    print("Adding Job titles to final DataFrame")
    print("...")
    print("...")
    main_df2 = pd.merge(main_df, country_names, on='country_code', how='left')
    print("...")
    print("...")
    print("Adding country names to final DataFrame")
    print("...")
    print("...")
    # db_df.merge()

    return main_df2


def clean_data(arguments, url):
    main_df = merge_data(arguments, url)
    main_df.columns = ['Education_level', 'Full_time_job', 'Living area',
                       'Age', 'Gender', 'Children', 'Age_group',
                       'Question_basicincome_awareness','Question_basicincome_vote',
                       'Question_basicincome_effect', 'Question_basicincome_argumentsfor',
                       'Question_basicincome_argumentsagainst', 'Job_title', 'Country']

    percentage = [100 / len(main_df) for e in range(len(main_df))]
    quantity = [1 for e in range(len(main_df))]

    main_df['Quantity'] = quantity
    main_df['Percentage'] = percentage

    sub_df = main_df[['Age_group', 'Job_title', 'Country', 'Quantity', 'Percentage']]

    return sub_df
