import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import lstsq
import argparse

parser = argparse.ArgumentParser('Рассчитаем коэфициенты')
parser.add_argument('-p', '--path', help = 'path to directory', type=str)
args = parser.parse_args()

def make_koefficients(data, polynomal_degree = 3, path = args.path, name = 'nach'):
    M = data['p2'].to_numpy()[:, np.newaxis]**[i for i in range(polynomal_degree+1)]
    p, res, rnk, s = lstsq(M, data['fx'].to_numpy()[:])
    with open(path + 'koef.txt', 'a') as f:
        print(name, p, file =f)
    x = np.linspace(data['p2'].iloc[0], data['p2'].iloc[-1], 100)
    y = sum([p[i]*x**i for i in range(polynomal_degree+1)])
    return x,y


if __name__ == '__main__':
    data = pd.read_csv(args.path)
    x,y = make_koefficients(data)
    plt.plot(x,y)
    plt.show()
