import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


# Filter parameters
maxpulses = 50


# Load data
datas = []
names = ['addr', 'nreads', 'nsets', 'nresets', 'rf', 'if', 'rlo', 'rhi', 'success', 'attempts1', 'attempts2']
steps = np.arange(0.02, 0.74, 0.04)
for step in steps:
        fname = 'data/bl-opt/sdr-wl0.06-bl%.2f-sl0.15-4.00-6-1-20.csv' % step
        data = pd.read_csv(fname, delimiter='\t', names=names, index_col=False)
        data['npulses'] = data['nsets'] + data['nresets'] - 1
        data['stepsize'] = step
        rlos = data['rlo'].unique()
        data['bin'] = data['rlo'].apply(lambda x: np.where(rlos == x)[0][0])
        data = data[data['bin'] != 7]
        datas.append(data)
data = pd.concat(datas)

ignore = [800, 809, 847, 850, 854, 900, 909, 915, 937, 939, 955, 988, 993, 1007, 1014, 1021, 1029]
data = data[~data['addr'].isin(ignore)]

data['success'] = data['success'].astype(bool) & (data['npulses'] <= maxpulses)
data['npulses'] = data['npulses'].clip(upper=maxpulses)
print data


# LaTEX quality figures 
mpl.rcParams.update(
    {
    'text.usetex': True,
    'pgf.texsystem': 'lualatex',
    'pgf.rcfonts': True,
    }
)
plt.rc('font', family='serif', serif='Times', size=13)


# Per-level optimization
for l in range(7):
    d = data[data['bin'] == l].groupby(['stepsize'])['npulses'].mean()
    print d
    print d.min(), d.idxmin()
    plt.figure(figsize=(4,3))
    plt.title('VBL Step Size Optimization (Range %d)' % (l))
    plt.xlabel('BL Step Size (V)')
    plt.ylabel('\# Pulses Required')
    plt.plot(d)
    plt.tight_layout()
    plt.savefig('figs/sdr-bl-opt-range-%d.eps' % (l))
    plt.show()

    d = data[data['bin'] == l].groupby(['stepsize'])['success'].mean()
    print d
    print d.max(), d.idxmax()
    plt.xlabel('BL Step Size (V)')
    plt.ylabel('Success Rate')
    plt.plot(d)
    plt.show()
