import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


# Filter parameters
maxpulses = 50000


# Load data
datas = []
names = ['addr', 'nreads', 'nsets', 'nresets', 'rf', 'if', 'rlo', 'rhi', 'success', 'attempts1', 'attempts2']
steps = np.arange(0.02, 0.301, 0.04)
starts = np.arange(0, 1.21, 0.4)
for step in steps:
    for start in starts:
        fname = 'data/bl-opt/sdr-wl0.070-bl%.2f-%.2f-sl0.14-2.00-7-24-20.csv' % (step,start)
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


# Ignore bad cells
ignore = []
data = data[~data['addr'].isin(ignore)]


# Success rate
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
    plt.locator_params(axis='x', nbins=6)
    plt.locator_params(axis='y', nbins=6)
    ax.set_title('VBL Step Size Optimization (Range %d)' % (l), fontsize=20)
    ax.set_xlabel('BL Step Size (V)', fontsize=15)
    ax.set_ylabel('BL Start Voltage (V)', fontsize=15)
    ax.set_zlabel('\# Pulses Required', fontsize=15)
    d = data[data['bin'] == l].groupby(['stepsize', 'start'])['npulses'].mean()
    grid = np.meshgrid(steps, starts)
    print d.unstack()
    print d.min(), d.idxmin()
    ax.plot_surface(grid[0], grid[1], d.unstack().T)
    plt.show()

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_title('VBL Step Size Optimization (Range %d)' % (l), fontsize=20)
    ax.set_xlabel('BL Step Size (V)', fontsize=15)
    ax.set_ylabel('BL Start Voltage (V)', fontsize=15)
    ax.set_zlabel('Success Rate', fontsize=15)
    d = data[data['bin'] == l].groupby(['stepsize', 'start'])['success'].mean()
    grid = np.meshgrid(steps, starts)
    print d.unstack()
    print d.max(), d.idxmax()
    ax.plot_surface(grid[0], grid[1], d.unstack().T)
    plt.show()
