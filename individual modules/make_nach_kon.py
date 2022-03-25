import  pandas as pd
import numpy as np
import argparse
import pathlib

parser = argparse.ArgumentParser('Разделим MASSIV.csv на два файла с начальными и конечными значениями измерений.')
parser.add_argument('-p', '--path', help = 'path to directory', type=str)
parser.add_argument('-i', '--interval', help = 'minutes on temperature', type=int)
args = parser.parse_args()

def split_massiv_to_kon_nach(path, interval):

    file_path = sorted(pathlib.Path(path).glob('MASS*.csv'))[0]
    df = pd.read_csv(file_path , sep=';', decimal=',')
    df.columns = ['p2', 'fx', 'fy', 'fz', 'twy', 'twz']
    nach = [] #pd.DataFrame()
    kon = [] #pd.DataFrame()

    fx_nach = fx_kon = []
    fy_nach = fy_kon = []
    fz_nach = fz_kon = []

    for i in range(0, len(df), interval):
        nach.append(df.iloc[i])
        if i:
            kon.append(df.iloc[i-2])
    kon.append(df.loc[len(df)-1])
    df_kon = pd.DataFrame(kon)
    df_nach = pd.DataFrame(nach)

    df_kon.to_csv(path + 'kon.csv')
    df_nach.to_csv(path + 'nach.csv')


if __name__ == '__main__':
    split_massiv_to_kon_nach(args.path, args.interval)
