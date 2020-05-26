import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt


# Load data
names = ['addr', 'pw', 'blv', 'wlv', 'ri', 'rf']
stepsize = 0.01
data = pd.read_csv('data/set-sweep-fine-step-%.2f-5-26-20.csv' % stepsize, delimiter='\t', names=names)
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


# Set up variables
data = data[data['blv']*10 % 1 <= 1e-9]
grouped = data.groupby(['blv', pd.cut(data['wlv'], np.arange(2, 3, 0.01))])

# Means of final resistance
rf = grouped['rf']
medians = rf.median()/1000.
stds = rf.std()/1000.

# Plot
ax = medians.unstack().plot(title='Fine SET BL Sweep (Range 1-6)', logy=False, xlim=(1.6, 3.3), ylim=(0, 50), linewidth=2, figsize=(4,3)) #, yerr=stds.unstack(), elinewidth=0.5)
plt.xlabel('BL Voltage (V)')
plt.ylabel('Median Resistance (k$\\Omega$)')
plt.legend([2.25, 2.3, 2.36, 2.41, 2.46, 2.53], title='WL Voltage (V)', ncol=2, columnspacing=1, labelspacing=0.3, handletextpad=0.5, borderpad=0.2)
plt.tight_layout()
plt.savefig('figs/fine-set-sweep.eps')
plt.show()
