import pandas as pd


# analysis functions

def analyze(df):
    grouped = df.groupby(['Country', 'Age_group', 'Job_title']).sum().reset_index()
    results = grouped.sort_values('Quantity', ascending=False)
    return results
