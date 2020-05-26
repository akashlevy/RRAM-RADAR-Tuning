import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt


# Load data
names = ['addr', 'pw', 'blv', 'wlv', 'ri', 'rf']
stepsize = 0.01
data = pd.read_csv('data/set-sweep-ispp-step-%.2f-5-25-20.csv' % stepsize, delimiter='\t', names=names)
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
ax = means.unstack().plot(title='ISPP WL Voltage Sweep', logy=False, xlim=(2.2, 2.5), ylim=(0, 1e2), linewidth=2, figsize=(4,3)) #, yerr=stds.unstack(), elinewidth=0.5)
plt.xlabel('WL Voltage (V)')
plt.ylabel('Mean Resistance (k$\\Omega$)')
plt.legend(["%.1f" % n for n in np.arange(1.5, 3.5, 0.5)], title='BLV (V)')
plt.tight_layout()
plt.savefig('figs/ispp-wl-sweep.eps')
plt.show()
