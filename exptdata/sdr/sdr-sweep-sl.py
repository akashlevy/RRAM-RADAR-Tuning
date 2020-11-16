import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


# Filter parameters
maxpulses = 50000


# Load data
bpc = 3
datas = []
names = ['addr', 'nreads', 'nsets', 'nresets', 'rf', 'if', 'rlo', 'rhi', 'success', 'attempts1', 'attempts2']
#steps = np.arange(0.02, 0.221, 0.04)
#starts = np.arange(0.0, 1.01, 0.2)
steps = np.arange(0.02, 0.301, 0.04)
starts = np.arange(0.0, 1.21, 0.4)
#steps = np.arange(0.1, 0.401, 0.05)
#starts = np.arange(0, 1.21, 0.4)
# steps = np.arange(0.02, 0.201, 0.02)
# starts = np.arange(0, 0.151, 0.05)
#steps = np.arange(0.1, 0.421, 0.08)
#starts = np.arange(0, 1.2, 0.2)
for step in steps:
    for start in starts:
        #fname = 'data/3bpc/sl-opt-1/sdr-wl0.070-bl0.04-0.40-sl%.2f-%.2f-7-24-20.csv' % (step,start)
        fname = 'data/3bpc/sl-opt-2/sdr-wl0.070-bl3.00-2.00-sl%.2f-%.2f-7-24-20.csv' % (step,start)
        #fname = 'data/2bpc/sl-opt-1/sdr-wl0.100-bl0.10-0.40-sl%.2f-%.2f-7-24-20.csv' % (step,start)
        #fname = 'data/2bpc/sl-opt-2/sdr-wl0.100-bl5.00-5.00-sl%.2f-%.2f-7-24-20.csv' % (step,start)
        #fname = 'data/2bpc/sl-opt-1/sdr-wl0.100-bl5.00-5.00-sl%.2f-%.2f-7-24-20.csv' % (step,start)
        print fname
        data = pd.read_csv(fname, delimiter='\t', names=names, index_col=False)
        data['npulses'] = data['nsets'] + data['nresets'] - 1
        data['stepsize'] = step
        data['start'] = start
        rlos = data['rlo'].unique()
        data['bin'] = data['rlo'].apply(lambda x: np.where(rlos == x)[0][0])
        data = data[data['bin'] != (2**bpc - 1)]
        datas.append(data)
data = pd.concat(datas)

#ignore = [8613, 8614, 8616, 8627, 8628, 8644, 8650, 8651, 8659, 8660, 8678, 8686, 8695, 8713, 8715, 8739, 8746, 8751, 8767, 8778, 8780, 8791, 8817, 8818, 8833, 8846, 8848]
ignore = [9248, 9292]
#ignore = [39705, 39722, 39750, 39751,  39781, 39785, 39808, 39810, 39883, 39911]
#ignore = [48276]
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
for l in range(2**bpc - 1):
    fig = plt.figure()
    ax = Axes3D(fig)
    plt.locator_params(axis='x', nbins=6)
    plt.locator_params(axis='y', nbins=6)
    ax.set_title('VSL Start/Step Tuning (Range %d)' % (l), fontsize=20)
    ax.set_xlabel('SL Step Size (V)', fontsize=15)
    ax.set_ylabel('SL Start Voltage (V)', fontsize=15)
    ax.set_zlabel('Mean Pulses Required', fontsize=15)
    d = data[data['bin'] == l].groupby(['stepsize', 'start'])['npulses'].mean()
    grid = np.meshgrid(steps, starts)
    print d.unstack()
    print d.min(), d.idxmin()
    ax.plot_surface(grid[0], grid[1], d.unstack().T)
    plt.show()

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_title('VSL Start/Step Optimization (Range %d)' % (l), fontsize=20)
    ax.set_xlabel('SL Step Size (V)', fontsize=15)
    ax.set_ylabel('SL Start Voltage (V)', fontsize=15)
    ax.set_zlabel('Success Rate', fontsize=15)
    d = data[data['bin'] == l].groupby(['stepsize', 'start'])['success'].mean()
    grid = np.meshgrid(steps, starts)
    print d.unstack()
    print d.max(), d.idxmax()
    ax.plot_surface(grid[0], grid[1], d.unstack().T)
    plt.show()
