import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
from p_acquisition import m_acquisition as mac


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


def job_titles_to_DataFrame():
    url = 'http://api.dataatwork.org/v1/jobs?limit=500'
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


def merge_data(list_of_df):
    db_tables = list_of_df
    job_titles = job_titles_to_DataFrame()
    country_names = get_country_names()

    print("Creating final DataFrame")
    db_job_df = pd.merge(db_tables, job_titles, on='normalized_job_code', how='left')

    print("Adding Job titles to final DataFrame")

    main_df = pd.merge(db_job_df, country_names, on='country_code', how='left')

    print("Adding country names to final DataFrame")
    print("...")
    print("...")
    main_df = main_df[[
        'dem_education_level', 'dem_full_time_job', 'rural', 'age', 'gender', 'dem_has_children', 'age_group',
        'question_bbi_2016wave4_basicincome_awareness', 'question_bbi_2016wave4_basicincome_vote',
        'question_bbi_2016wave4_basicincome_effect', 'question_bbi_2016wave4_basicincome_argumentsfor',
        'question_bbi_2016wave4_basicincome_argumentsagainst', 'normalized_job_title', 'Country', 'country_code']]

    main_df.columns = ['Education_level', 'Full_time_job', 'Living area',
                       'Age', 'Gender', 'Children', 'Age_group',
                       'Question_basicincome_awareness', 'Question_basicincome_vote',
                       'Question_basicincome_effect', 'Question_basicincome_argumentsfor',
                       'Question_basicincome_argumentsagainst', 'Job_title', 'Country', 'Country_code']
    return main_df.to_csv('/home/david/Documents/ih_datamadpt0420_project_m1/data/processed/main_df.csv')


def clean_data():
    # merge_data(df)
    main_df = pd.read_csv('/home/david/Documents/learning_repositories/ih_datamadpt0420_project_m1/data/processed/main_df.csv')

    percentage = [100 / len(main_df) for e in range(len(main_df))]
    quantity = [1 for e in range(len(main_df))]

    main_df['Quantity'] = quantity
    main_df['Percentage'] = percentage
    main_df[['Percentage']] = main_df[['Percentage']].applymap('{:,.2f}'.format)
    main_df['Percentage'] = main_df['Percentage'].astype(float)
    sub_df = main_df[['Age_group', 'Job_title', 'Country', 'Quantity', 'Percentage']]

    return sub_df
