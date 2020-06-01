import matplotlib as mpl, numpy as np, pandas as pd, pygmo as pg
import matplotlib.pyplot as plt

data = pd.read_csv('data/set-sweep-wl-inner-5-31-20.csv', delimiter='\t', names=['addr', 'pw', 'blv', 'wlv', 'ri', 'rf'])
data = data[data['pw'] == 100]
data = data[data['blv'] == 2]
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
grouped = data.groupby(['wlv'])

# Medians of final resistance
rf = grouped['rf']
medians = rf.median()/1000.
stds = rf.std()/1000.
print medians
medians.to_csv('results/fppv.csv')

pts = medians.values
vs = list(reversed([2.26, 2.31, 2.36, 2.41, 2.47, 2.53]))
vis = [int(round((v-2)/0.01)) for v in vs]
rs = [pts[vi] for vi in vis]
data = zip(range(1,7), vs, rs)
print data

# Plot WL voltage and selections
medians.plot(title='FPPV WL Voltage Selection', logy=False, xlim=(2.2, 2.7), ylim=(0, 60), linewidth=2, figsize=(4,3))

plt.xlabel('WL Voltage (V)')
plt.ylabel('Median Resistance (k$\\Omega$)')
leg = plt.legend([''], handletextpad=0.5, borderpad=0.2)
leg.set_title(title='BLV=1.6V, PW=100ns', prop={'size': 11})
plt.tight_layout()
plt.savefig('figs/fppv-wl-sweep.eps')
plt.show()
