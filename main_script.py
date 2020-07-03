
import argparse
from p_acquisition import m_acquisition
from p_wrangling import m_wrangling as mwr
from p_analysis import m_analysis as man
from p_reporting import m_reporting as mre
from p_wrangling import m_wrangling as mwr

def argument_parser():
    parser = argparse.ArgumentParser(description = 'Set chart type')
    parser.add_argument("-dp", "--db_path", help="Introduce a path to a data base", required=True)
    args = parser.parse_args()
    return args


def main(some_args):
    print("Starting data analysis process!")

    list_of_df = m_acquisition.tables_to_df(arguments.db_path)
    clean = mwr.clean_data(list_of_df)
    mre.dash_report(clean)

    print("Process finished!")


if __name__ == '__main__':
    arguments = argument_parser()
    main(arguments)



