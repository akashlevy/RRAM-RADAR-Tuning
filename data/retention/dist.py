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
nranges = 8


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

Rmins = np.array([0.0001, 4.38, 4.84, 5.42, 6.16, 7.19, 9.23, 35])
Rmaxs = np.array([4.3, 4.75, 5.3, 6.01, 6.99, 8.9, 25, 10000])
Gmaxs = 1 / Rmins
Gmins = 1 / Rmaxs
for expt, pp in product(range(1, 7+1), ['pre','post']):
    # Load data
    names = ['rf']
    data = pd.read_csv('data/readtest%d-%sbake.csv' % (expt, pp), delimiter='\t', names=names, index_col=False)
    data['rf'] = data['rf']/1000
    data['g'] = 1/data['rf']
    data['bin'] = ( data.index + data.index / cbsize ) % nranges
    print data

    ranges = range(8)

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
    plt.savefig('figs/dist%d-g-%sbake.png' % (expt, pp))
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
    plt.savefig('figs/dist%d-r-%sbake.png' % (expt, pp))
    #plt.show()

# # Fit to retention sigma
# # Plot sigmas
# data = data[data['bin'] <= 19]
# data = data[data['bin'] > 0]
# bindata = data.groupby('bin')
# means, stds = bindata['rf'].mean()*1000, bindata['rf'].std()*1000

# n = 2
# fit = np.polyfit(means, stds, n)
# print tuple(fit)
# x = np.linspace(4300, 12000)
# y = list(np.sum(np.array([fit[n-i] * x**i for i in range(n+1)]), axis=0))

# plt.semilogy(means, stds)
# plt.semilogy(x, y)
# plt.show()