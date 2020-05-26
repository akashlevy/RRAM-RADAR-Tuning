import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt

# Load data and filter
data = pd.read_csv('data/cycling-5-1-20.csv', delimiter='\t', header=None).transpose()
print data
setr = data.iloc[2:601:2,:]/1000
print setr
print 'Maximum SET Resistance: %s kOhm' % setr.min().max()

# LaTEX quality figures
mpl.rcParams.update(
    {
    'text.usetex': True,
    'pgf.texsystem': 'lualatex',
    'pgf.rcfonts': True,
    }
)
plt.rc('font', family='serif', serif='Times')

# Plot cycling data
data.iloc[550:,:5].plot(logy=True, figsize=(4,3))
plt.title('Cell Cycling')
plt.xlabel('Pulse Number')
plt.ylabel('Resistance (k$\Omega$)')
plt.tight_layout()
plt.savefig('figs/cycle.eps')
plt.show()
