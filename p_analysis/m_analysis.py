import pandas as pd


# analysis functions

def analyze(df):
    grouped = df.groupby(['Country', 'Age_group', 'Job_title']).sum().reset_index()
    #results = grouped.sort_values('Combined MPG', ascending=False).head(10)
    return grouped