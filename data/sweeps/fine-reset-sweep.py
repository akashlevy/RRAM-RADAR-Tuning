import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt


# Load data
names = ['addr', 'pw', 'slv', 'wlv', 'ri', 'rf']
stepsize = 0.01
data = pd.read_csv('data/reset-sweep-fine-step-%.2f-5-26-20.csv' % stepsize, delimiter='\t', names=names)
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
data = data[~data.groupby(['slv','wlv'])['rf'].apply(is_outlier)]

# Set up variables
grouped = data[data['wlv'] == 4]
grouped = grouped.groupby(['slv', pd.cut(grouped['addr'], np.arange(1450,1469,1))])

# Means of final resistance
rf = grouped['rf']
means = rf.mean()/1000.
stds = rf.std()/1000.

# Plot
ax = means.unstack().plot(title='Fine RESET SL Sweep', logy=False, xlim=(1, 2.2), ylim=(0, 60), linewidth=2, figsize=(4,3)) #, yerr=stds.unstack(), elinewidth=0.5)
plt.xlabel('SL Voltage (V)')
plt.ylabel('Mean Resistance (k$\\Omega$)')
#plt.legend(['WLV=4V'])
plt.gca().get_legend().remove()
plt.tight_layout()
plt.savefig('figs/fine-reset-sweep.eps')
plt.show()
