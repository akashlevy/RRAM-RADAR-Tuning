import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('sweep-4-14-20.csv', delimiter='\t', names=['addr', 'pw', 'blv', 'wlv', 'ri', 'rf'])
data = data[data['ri'] > 50e3]
pwdata = data[data['pw'] == 100]

# LaTEX quality figures 
mpl.rcParams.update(
    {
    'text.usetex': True,
    'pgf.texsystem': 'lualatex',
    'pgf.rcfonts': True,
    }
)
plt.rc('font', family='serif', serif='Times')

# Plot
def is_outlier(s):
    lower_limit = s.mean() - (s.std() * 2)
    upper_limit = s.mean() + (s.std() * 2)
    return ~s.between(lower_limit, upper_limit)
#pwdata = pwdata[~pwdata.groupby('wlv')['rf'].apply(is_outlier)]
grouped = pwdata.groupby('wlv')
means = grouped['rf'].mean()
stds = grouped['rf'].std()
means, stds = means[means < 40e3], stds[means < 40e3]

# Stdev vs mean
plt.figure(figsize=(4, 3))
plt.title('Final Resistance $\\sigma$ vs. $\\mu$')
plt.xlabel('Mean Resistance ($\\Omega$)')
plt.ylabel('Stdev. Resistance ($\\Omega$)')
plt.plot(means, stds, '.', label="PW: 100ns\nBL voltage: 3.3V\nWL voltage: varied", color='0.2')
fit = np.polyfit(means, stds, 4)
print tuple(fit)
x = np.linspace(4e3, 4e4)
y = list(np.sum(np.array([fit[4-i] * x**i for i in range(5)]), axis=0))
plt.plot(x, y, '--', color='green'), #label="Fit: $\\sigma = %.3f\mu%.0f$" % tuple(fit))
plt.legend()
plt.tight_layout()
plt.savefig('sigma-mu.eps')
plt.show()
