import pandas as pd
import argparse
from p_acquisition import m_acquisition as mac
from p_analysis import m_analysis as man
from p_reporting import m_reporting as mre
from p_wrangling import m_wrangling as mwr
import webbrowser


def argument_parser():
    parser = argparse.ArgumentParser(description = 'Set chart type')
    parser.add_argument("-dp", "--db_path", help="Introduce a path to a data base", required=False)
    parser.add_argument("-r", "--ruta", help="Introduce ruta de destino para el csv", required=True)
    args = parser.parse_args()
    return args


def main(some_args):
    print(some_args)
    print("Starting data analysis process!")

    #list_of_df = mac.tables_to_df(some_args.db_path)
    clean = mwr.clean_data()
    csv = man.analyze(clean)
    mre.export(csv, some_args.ruta)
    webbrowser.open_new_tab('http://127.0.0.1:8050/')
    mre.dash_report(clean)

    print("Process finished!")


if __name__ == '__main__':
    arguments = argument_parser()
    main(arguments)



