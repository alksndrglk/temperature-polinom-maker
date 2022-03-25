import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import lstsq
import argparse

parser = argparse.ArgumentParser('Получим коэффициенты и графики для полинома разделенного в определнной температуре.')
parser.add_argument('-p', '--path', help = 'path to directory', type=str)
args = parser.parse_args()

def make_koefficients(
        target_y: pd.DataFrame,
        target_x: pd.DataFrame,
        breakpoint: int = 0,
        degree = 3
        ):
    result = [0, 0]
    M_size = [i for i in range(polynomial_degree + 1)]
    if breakpoint:
        left , right = (0, breakpoint+1), (breakpoint-1,len(target_x))
        start, finish = target_x.iloc[0], target_x.iloc[breakpoint-1]
    else:
        left, right = (0, len(target_x)), 0
        start, finish = target_x.iloc[0], target_x.iloc[-1]
    for k, part in enumerate((left, right)):
        M = target_x.to_numpy()[part[0]:part[1], np.newaxis]**M_size
        p, res, rnk, s = lstsq(M, target_y.to_numpy()[part[0]:part[1]])
        x = np.linspace(start, finish, 300)
        y = sum([p[i]*x**i for i in range(polynomial_degree+1)])
        result[k] = (p)
        plt.plot(x,y)
        if not right:
            break
        start, finish = target_x.iloc[breakpoint-1], target_x.iloc[-1]
    return result

if __name__ == '__main__':

    kon = pd.read_csv(args.path + 'kon.csv')
    nach = pd.read_csv(args.path + 'nach.csv')
    with open(args.path + 'all_koef.txt', 'w') as f:
        for i in ['fx', 'fy', 'fz']: #, 'twy', 'twz']:
            polynomial_degree = 3
            if i.startswith('tw'):
                polynomial_degree = 1
            nach_ = make_koefficients(nach[i], nach['p2'], degree=polynomial_degree)
            kon_ = make_koefficients(kon[i], kon['p2'], degree=polynomial_degree)
            print(f'nach_{i}: {nach_} \nkon_{i}: {kon_}', file = f, sep = '\n')
    plt.show()

