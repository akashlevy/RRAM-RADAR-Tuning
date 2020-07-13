
import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
ranges = range(cbsize)

# Load data
names = ['rf']
data = pd.read_csv('data/relaxation-postbake.csv', delimiter='\t', names=names, index_col=False)
data['g'] = 1/data['rf']
data['bin'] = ( data.index + data.index / cbsize ) % 32

# Plot sigmas
data = data[data['bin'] != 0]

# Remove outliers
def is_outlier(s):
    lower_limit = s.mean() - (s.std() * 3.5)
    upper_limit = s.mean() + (s.std() * 3.5)
    return ~s.between(lower_limit, upper_limit)
data = data[~data.groupby(['bin'])['g'].apply(is_outlier)]

# Group and compute mean/std
bindata = data.groupby('bin')
means, stds = bindata['g'].mean(), bindata['g'].std()

# 5th-order polynomial fit
n = 5
fit = np.polyfit(list(means) + [0, 0.0003], list(stds) + [0, 0], n)
print tuple(fit)
x = np.linspace(0, 0.0003)
y = np.array(np.sum(np.array([fit[n-i] * x**i for i in range(n+1)]), axis=0))

# Plot sigma-mu
plt.figure(figsize=(4,3))
plt.xlabel('Mean conductance ($\\mu$S)')
plt.ylabel('Stdev. conductance ($\\mu$S)')
plt.title('Relaxation vs. conductance')
plt.plot(means*1e6, stds*1e6, label="Expt")
plt.plot(x*1e6, y*1e6, label="Fit")
plt.legend(title="30min @ 80C")
plt.tight_layout()
plt.savefig('figs/relaxation-sigma-mu.eps')
plt.show()