
import argparse
from p_acquisition import m_acquisition
from p_wrangling import m_wrangling as mwr
from p_analysis import m_analysis as man
from p_reporting import m_reporting as mre


def argument_parser():
    parser = argparse.ArgumentParser(description = 'Set chart type')
    parser.add_argument("-dp", "--db_path", help="Introduce a path to a data base", required=True)
    args = parser.parse_args()
    return args


def main(some_args):
    print("Starting data analysis process!")
    print("...")
    print("...")
    list_of_df = m_acquisition.tables_to_df(arguments.db_path)

### Prueba
    a = 0
    for df in list_of_df:
        a += 1
        df.to_csv(f'/home/david/Downloads/prueba/{a}.csv')
### Prueba

    print("...")
    print("...")
    print("data analysis process finished!")


if __name__ == '__main__':
    arguments = argument_parser()
    main(arguments)



"""
import argparse
from p_acquisition import m_acquisition as mac
from p_wrangling import m_wrangling as mwr
from p_analysis import m_analysis as man 
from p_reporting import m_reporting as mre 

def argument_parser():
    parser = argparse.ArgumentParser(description = 'Set chart type')
    parser.add_argument("-dp", "--db_path", help="Produce a barplot", action="store_true")
    parser.add_argument("-l", "--line", help="Produce a lineplot", action="store_true")
    args = parser.parse_args()
    return args

def main(some_args):
    data = mac.acquire()
    filtered = mwr.wrangle(data, year)
    results = man.analyze(filtered)
    fig = mre.plottidef argument_parser():
    parser = argparse.ArgumentParser(description = 'Set chart type')
    parser.add_argument("-dp", "--db_path", help="Produce a barplot", action="store_true")
    parser.add_argument("-l", "--line", help="Produce a lineplot", action="store_true")
    args = parser.parse_args()
    return argsng_function(results, title, arguments)
    mre.save_viz(fig, title)
    print('========================= Pipeline is complete. You may find the results in the folder ./data/results =========================')

if __name__ == '__main__':
    year = int(input('Enter the year: '))
    title = 'Top 10 Manufacturers by Fuel Efficiency ' + str(year)
    arguments = argument_parser()
    main(arguments)
"""
