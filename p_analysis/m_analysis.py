import pandas as pd


def analyze(df):
    grouped = df.groupby(['Country', 'Age_group', 'Job_title']).sum().reset_index()
    results = grouped.sort_values('Quantity', ascending=False)
    return results


def country_filter(pais, csv):
    df_filtrado = csv[csv['Country'] == pais].reset_index()

    return df_filtrado
