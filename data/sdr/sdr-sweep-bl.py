import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


# Filter parameters
maxpulses = 50


# Load data
datas = []
names = ['addr', 'nreads', 'nsets', 'nresets', 'rf', 'if', 'rlo', 'rhi', 'success', 'attempts1', 'attempts2']
steps = np.arange(0.05, 0.5, 0.05)
starts = np.arange(0, 1, 0.2)
for step in steps:
    for start in starts:
        fname = 'data/infopt/bl-opt/sdr-wl0.06-bl0.40-sl%.2f-%.2f-6-6-20.csv' % (step,start)
        print fname
        data = pd.read_csv(fname, delimiter='\t', names=names, index_col=False)
        data['npulses'] = data['nsets'] + data['nresets'] - 1
        data['stepsize'] = step
        data['start'] = start
        rlos = data['rlo'].unique()
        data['bin'] = data['rlo'].apply(lambda x: np.where(rlos == x)[0][0])
        data = data[data['bin'] != 7]
        datas.append(data)
data = pd.concat(datas)

#ignore = [800, 809, 847, 850, 854, 900, 909, 915, 937, 939, 955, 988, 993, 1007, 1014, 1021, 1029]
ignore = [1706, 1707, 1753, 1768, 1774, 1789, 1793, 1794, 1808, 1883]
data = data[~data['addr'].isin(ignore)]

data['success'] = data['success'].astype(bool) & (data['npulses'] <= maxpulses)
data['npulses'] = data['npulses'].clip(upper=maxpulses)


# LaTEX quality figures 
mpl.rcParams.update(
    {
    'text.usetex': True,
    'pgf.texsystem': 'lualatex',
    'pgf.rcfonts': True,
    'axes.labelpad': 7,
    }
)
plt.rc('font', family='serif', serif='Times', size=13)


# Per-level optimization
for l in range(7):
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_title('VSL Step Size Optimization (Range %d)' % (l), fontsize=20)
    ax.set_xlabel('SL Step Size (V)', fontsize=15)
    ax.set_ylabel('SL Start Voltage (V)', fontsize=15)
    ax.set_zlabel('\# Pulses Required', fontsize=15)
    d = data[data['bin'] == l].groupby(['stepsize', 'start'])['npulses'].mean()
    grid = np.meshgrid(steps, starts)
    print d.unstack()
    print d.min(), d.idxmin()
    ax.plot_surface(grid[0], grid[1], d.unstack().T)
    plt.show()

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_title('VSL Step Size Optimization (Range %d)' % (l), fontsize=20)
    ax.set_xlabel('SL Step Size (V)', fontsize=15)
    ax.set_ylabel('SL Start Voltage (V)', fontsize=15)
    ax.set_zlabel('Success Rate', fontsize=15)
    d = data[data['bin'] == l].groupby(['stepsize', 'start'])['success'].mean()
    grid = np.meshgrid(steps, starts)
    print d.unstack()
    print d.max(), d.idxmax()
    ax.plot_surface(grid[0], grid[1], d.unstack().T)
    plt.show()
