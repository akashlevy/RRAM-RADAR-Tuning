import matplotlib as mpl, numpy as np, pandas as pd, pygmo as pg
import matplotlib.pyplot as plt

'''Smooth using filter'''
def smooth(y, box_pts=7):
    box = np.ones(box_pts) / box_pts
    return np.concatenate((y[:box_pts/2], np.convolve(y, box, mode='valid'), y[-box_pts/2+1:]))

#data = pd.read_csv('wl-sweep-5-25-20.csv', delimiter='\t', names=['addr', 'pw', 'blv', 'wlv', 'ri', 'rf'])
data = pd.read_csv('set-sweep-5-1-20.csv', delimiter='\t', names=['addr', 'pw', 'blv', 'wlv', 'ri', 'rf'])
data = data[data['ri'] > 60e3]
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

# Remove outliers
def is_outlier(s):
    lower_limit = s.mean() - (s.std() * 2)
    upper_limit = s.mean() + (s.std() * 2)
    return ~s.between(lower_limit, upper_limit)
data = data[~data.groupby(['blv','wlv'])['rf'].apply(is_outlier)]

# Set up variables
grouped = data[(data['blv'] == 1.5) | (data['blv'] == 2) | (data['blv'] == 2.5) | (data['blv'] == 3)]
grouped = grouped.groupby(['wlv', pd.cut(grouped['blv'], np.arange(1.4, 3.1, 0.1))])

# Means of final resistance
rf = grouped['rf']
means = rf.mean()/1000.
stds = rf.std()/1000.

# Plot
means.unstack().plot(title='ISPP WL Voltage Sweep', logy=False, xlim=(2.2, 2.5), ylim=(0, 1e2), linewidth=2, figsize=(4,3)) #, yerr=stds.unstack(), elinewidth=0.5)
plt.xlabel('WL Voltage (V)')
plt.ylabel('Mean Resistance (k$\\Omega$)')
plt.legend(["%.1f" % n for n in np.arange(1.5, 3.5, 0.5)], title='BLV (V)')
plt.tight_layout()
plt.savefig('ispp-sweep.eps')
plt.show()

# Set up variables
grouped = data[(data['wlv'] == 2.48) | (data['wlv'] == 2.43) | (data['wlv'] == 2.4) | (data['wlv'] == 2.35) | (data['wlv'] == 2.29) | (data['wlv'] == 2.26) | (data['wlv'] == 3)]
grouped = grouped.groupby(['blv', pd.cut(grouped['wlv'], np.arange(2, 3.1, 0.01))])

# Means of final resistance
rf = grouped['rf']
means = rf.mean()/1000.
stds = rf.std()/1000.

# Plot
means.unstack().plot(title='SET BL Voltage Sweep', logy=False, xlim=(1.5, 3), ylim=(0, 70), linewidth=2, figsize=(4,3)) #, yerr=stds.unstack(), elinewidth=0.5)
plt.xlabel('BL Voltage (V)')
plt.ylabel('Mean Resistance (k$\\Omega$)')
#plt.legend(["%.1f" % n for n in np.arange(2.5, 3.1, 0.1)], title='WLV (V)', ncol=2)
plt.tight_layout()
plt.savefig('bl-sweep.eps')
plt.show()
