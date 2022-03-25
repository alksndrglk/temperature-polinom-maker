import  pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import  lstsq
import argparse

parser = argparse.ArgumentParser('Разделим MASSIV.csv на два файла с начальными и конечными значениями измерений.')
parser.add_argument('-p', '--path', help = 'path to directory with kon&nach', type=str)
args = parser.parse_args()

def draw_graph(path):
    kon = pd.read_csv(path + 'kon.csv')
    nach = pd.read_csv(path + 'nach.csv')

    M_nach = nach['p2'].to_numpy()[:, np.newaxis]**[0,1,2,3]
    p_nach, res_nach, rnk_nach, s_nach = lstsq(M_nach, nach['fx'].to_numpy())
    #print(p_nach)
    xx_nach = np.linspace(0.78, 0.267, 354)
    yy_nach = p_nach[0] + p_nach[1]*xx_nach + p_nach[2]*xx_nach**2 + p_nach[3]*xx_nach**3


    M_kon = kon['p2'].to_numpy()[:, np.newaxis]**[0,1,2,3]
    p_kon, res_kon, rnk_kon, s_kon = lstsq(M_kon, kon['fx'].to_numpy())
    #print(p_kon)
    xx_kon = np.linspace(0.78, 0.267, 354)
    yy_kon = p_kon[0] + p_kon[1]*xx_kon + p_kon[2]*xx_kon**2 + p_kon[3]*xx_kon**3

    plt.plot(nach['p2'], nach['fx'], 'ro', label='nach data')
    plt.plot(xx_nach, yy_nach,'y', label='nach aproxy $a+bP2+cP2^2+dP2^3$')

    plt.plot(kon['p2'], kon['fx'], 'bo', label='kon data')
    plt.plot(xx_kon, yy_kon,'g', label='kon aproxy $a+bP2+cP2^2+dP2^3$')

    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend(framealpha=1, shadow=True)
    plt.grid(alpha=0.25)
    plt.show()
'''
plt.plot(kon['p2'], kon['fx'], 'r')
plt.plot(nach['p2'], nach['fx'], 'b')

plt.show()
'''
if __name__ == '__main__':
    draw_graph(args.path)
