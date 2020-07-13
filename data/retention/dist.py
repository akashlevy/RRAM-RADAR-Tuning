import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import product


# LaTEX quality figures 
mpl.rcParams.update(
    {
    'text.usetex': True,
    'pgf.texsystem': 'lualatex',
    'pgf.rcfonts': True,
    }
)
plt.rc('font', family='serif', serif='Times', size=13)


# Define CB size
cbsize = 32

# # Load data
# names = ['addr', 'nreads', 'nsets', 'nresets', 'rf', 'if', 'rlo', 'rhi', 'success', 'attempts1', 'attempts2']
# data = pd.read_csv('data/writeispp-testrange.csv', delimiter='\t', names=names, index_col=False)
# rlos = data['rlo'].unique()
# print sorted(rlos)
# data['bin'] = data['rlo'].apply(lambda x: np.where(rlos == x)[0][0])
# data['rf'] = data['rf']/1000
# data['g'] = 1/data['rf']

# ranges = range(32)

# # Conductance plot
# plt.xlim(0, 0.3)
# for i in ranges:
#     rdata = data[data['bin'] == i]
#     print i
#     sns.distplot(rdata['g'],kde=False)
# plt.show()

# # Resistance plot
# plt.xlim(0, 60)
# for i in ranges:
#     rdata = data[data['bin'] == i]
#     print i
#     sns.distplot(rdata['rf'],kde=False)
# plt.show()

for expt, pp, bpc in product(range(1, 7+1), ['pre','post'], (2,3)):
    # Get resistance and conductance bounds for plots
    nranges = 2**bpc
    if bpc == 2:
        Rmins = np.array([0.0001, 5.38, 6.93, 18])
        Rmaxs = np.array([5.1, 6.48, 14, 10000])
    if bpc == 3:
        Rmins = np.array([0.0001, 4.38, 4.84, 5.42, 6.16, 7.19, 9.23, 35])
        Rmaxs = np.array([4.3, 4.75, 5.3, 6.01, 6.99, 8.9, 25, 10000])
    Gmaxs = 1 / Rmins
    Gmins = 1 / Rmaxs

    # Load data
    names = ['rf']
    try:
        data = pd.read_csv('data/readtest%dbpc%d-%sbake.csv' % (bpc, expt, pp), delimiter='\t', names=names, index_col=False)
    except IOError as e:
        print("Skipping:", e)
        continue
    data['rf'] = data['rf']/1000
    data['g'] = 1/data['rf']
    data['bin'] = ( data.index + data.index / cbsize ) % nranges
    print data

    ranges = range(2**bpc)

    # Conductance plot
    plt.figure(figsize=(6, 4))
    plt.title('Conductance Distribution P%s-bake' % pp[1:])
    for i in ranges:
        plt.xlim(0, 0.28)
        if i == 6:
            plt.ylim(0, 500)
        rdata = data[data['bin'] == i]
        color = sns.color_palette()[i]
        sns.distplot(rdata['g'], kde=True, label='Range %d' % i)
        plt.axvline(Gmins[i], -0.1, 0.2, color=color)
        plt.axvline(Gmaxs[i], -0.1, 0.2, color=color)
    plt.xlabel('Conductance (uS)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.tight_layout()
    plt.savefig('figs/dist%d-%dbpc-g-%sbake.png' % (expt, bpc, pp))
    #plt.show()

    # Resistance plot
    plt.figure(figsize=(6, 4))
    plt.title('Resistance Distribution P%s-bake' % pp[1:])
    #plt.gca().set_xscale('log')
    for i in ranges:
        plt.xlim(4, 20)
        rdata = data[data['bin'] == i]
        color = sns.color_palette()[i]
        sns.distplot(rdata['rf'], kde=True, label='Range %d' % i)
        plt.axvline(Rmins[i], -0.1, 0.2, color=color)
        plt.axvline(Rmaxs[i], -0.1, 0.2, color=color)
    plt.xlabel('Resistance (k$\\Omega$)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.tight_layout()
    plt.savefig('figs/dist%d-%dbpc-r-%sbake.png' % (expt, bpc, pp))
    #plt.show()

    for i in range(2**bpc):
        bindata = data[data['bin'] == i]
        g = bindata['g']/1000
        g.to_csv('results/g_%dbpc-expt%d-%s_range%d.csv' % (bpc, expt, pp, i), index=False, float_format='%.15f')
