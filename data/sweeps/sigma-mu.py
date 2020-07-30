import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt

# Load data and filter
data = pd.read_csv('data/set-sweep-wl-deeper-7-3-20.csv', delimiter='\t', names=['addr', 'pw', 'blv', 'wlv', 'ri', 'rf'])
data = data[data['wlv'] >= 2.44]
data = data[data['wlv'] <= 3]

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

# Group data
grouped = data.groupby(['blv','wlv'])
means = grouped['rf'].median()
stds = grouped['rf'].std()
print means
print stds

# Polynomial fit to pareto front
n = 1
fit = np.polyfit(means, np.log(stds), n)
print tuple(fit)
print np.exp(fit)
x = np.linspace(4e3, 1e3)
y = np.exp(fit[1] + fit[0]*x)

# Stdev vs median
plt.figure(figsize=(4, 3))
plt.title('Final Resistance $\\sigma$ vs. mean')
plt.xlabel('Mean Resistance ($\\Omega$)')
plt.ylabel('Stdev. Resistance ($\\Omega$)')
plt.plot(means, stds, '.', label="PW: 100ns\nBL voltage: 2V\nWL voltage: varied", color='0.2')
plt.plot(x, y, '--', color='green', label="Fit curve")
plt.legend()
plt.tight_layout()
plt.savefig('figs/sigma-mu.eps')
plt.show()