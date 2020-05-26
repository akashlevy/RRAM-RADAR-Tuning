import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


# Filter parameters
maxpulses = 40


# Load data
datas = []
names = ['addr', 'nreads', 'nsets', 'nresets', 'rf', 'if', 'rlo', 'rhi', 'success', 'attempts1', 'attempts2']
steps = np.arange(0.05, 0.85, 0.05)
starts = np.arange(0.5, 2.25, 0.25)
for step in steps:
    for start in starts:
        fname = 'data/sl-opt/sdr-wl0.06-bl0.40-sl%.2f-%.2f-5-20-20.csv' % (step,start)
        data = pd.read_csv(fname, delimiter='\t', names=names, index_col=False)
        data['npulses'] = data['nsets'] + data['nresets']
        data['stepsize'] = step
        data['start'] = start
        rlos = data['rlo'].unique()
        data['bin'] = data['rlo'].apply(lambda x: np.where(rlos == x)[0][0])
        datas.append(data)
data = pd.concat(datas)

#data['success'] = data['success'].astype(bool) & (data['npulses'] <= maxpulses)
#data['npulses'] = data['npulses'].clip(upper=maxpulses)
print data


# LaTEX quality figures 
mpl.rcParams.update(
    {
    'text.usetex': True,
    'pgf.texsystem': 'lualatex',
    'pgf.rcfonts': True,
    }
)
plt.rc('font', family='serif', serif='Times')


# Per-level optimization
for l in range(8):
    fig = plt.figure()
    ax = Axes3D(fig)
    d = data[data['bin'] == l].groupby(['stepsize', 'start'])['npulses'].mean()
    grid = np.meshgrid(steps, starts)
    print d.unstack()
    print d.min(), d.idxmin()
    ax.plot_surface(grid[0], grid[1], d.unstack().T)
    plt.show()

    fig = plt.figure()
    ax = Axes3D(fig)
    d = data[data['bin'] == l].groupby(['stepsize', 'start'])['success'].mean()
    grid = np.meshgrid(steps, starts)
    print d.unstack()
    print d.min(), d.idxmin()
    ax.plot_surface(grid[0], grid[1], d.unstack().T)
    plt.show()


# SDR Mean Step
grouped = data.groupby(['stepsize'])
npulses = grouped['npulses']
npulses_mean = npulses.mean()
print npulses_mean
npulses_std = npulses.std()
print npulses_std
npulses_mean.plot.bar(title='SDR: Mean Pulses vs. Step Size', figsize=(4,3), yerr=npulses_std)
plt.xlabel('Step Size')
plt.ylabel('Mean Pulses Required')
plt.tight_layout()
plt.savefig('sdr-mean-pulses-step.eps')
plt.show()


# SDR Mean Success Rate
grouped = data.groupby(['stepsize'])
success = grouped['success']
success_mean = success.mean()
print success_mean
success_mean.plot.bar(title='SDR: Success Rate vs. Step Size', figsize=(4,3))
plt.xlabel('Step Size')
plt.ylabel('Success Rate')
plt.tight_layout()
plt.savefig('sdr-mean-success-step.eps')
plt.show()
