import matplotlib as mpl, numpy as np, pandas as pd, pygmo as pg
import matplotlib.pyplot as plt

# Load data and filter
data = pd.read_csv('data/set-sweep-wl-inner-5-10-20.csv', delimiter='\t', names=['addr', 'pw', 'blv', 'wlv', 'ri', 'rf'])
#data = data[data['ri'] > 60e3]
#data = data[data['rf'] < 150e3]
data = data[data['blv'] > 1.5]
pwdata = data[data['pw'] == 100]

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
pwdata = pwdata[~pwdata.groupby(['blv','wlv'])['rf'].apply(is_outlier)]
grouped = pwdata.groupby(['blv','wlv'])
medians = grouped['rf'].median()
stds = grouped['rf'].std()
medians, stds = medians[medians < 60e3], stds[medians < 60e3]

# Find pareto front
pareto = pg.non_dominated_front_2d(points=zip(-medians, stds))
pmedians, pstds = medians[pareto], stds[pareto]
pmedians.to_csv('pareto-median.csv')

# Polynomial fit to pareto front
n = 3
fit = np.polyfit(medians[pareto], stds[pareto], n)
print tuple(fit)
x = np.linspace(5e3, 5e4)
y = list(np.sum(np.array([fit[n-i] * x**i for i in range(n+1)]), axis=0))

# Stdev vs median
plt.figure(figsize=(4, 3))
plt.title('Final Resistance $\\sigma$ vs. median')
plt.xlabel('Median Resistance ($\\Omega$)')
plt.ylabel('Stdev. Resistance ($\\Omega$)')
plt.plot(medians, stds, '.', label="PW: 100ns\nBL voltage: varied\nWL voltage: varied", color='0.2')
plt.plot(medians[pareto], stds[pareto], '.', color='red', label="Pareto optimal pts")
plt.plot(x, y, '--', color='green', label="Pareto optimal fit")
plt.legend()
plt.tight_layout()
plt.savefig('sigma-median.eps')
plt.show()
