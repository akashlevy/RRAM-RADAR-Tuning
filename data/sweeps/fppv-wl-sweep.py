import matplotlib as mpl, numpy as np, pandas as pd, pygmo as pg
import matplotlib.pyplot as plt

data = pd.read_csv('data/set-sweep-wl-inner-5-26-20.csv', delimiter='\t', names=['addr', 'pw', 'blv', 'wlv', 'ri', 'rf'])
data = data[data['pw'] == 100]
data = data[data['blv'] == 1.6]
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
grouped = data.groupby(['wlv'])

# Medians of final resistance
rf = grouped['rf']
medians = rf.median()/1000.
stds = rf.std()/1000.

pts = medians.values
vs = reversed([2.26, 2.31, 2.35, 2.41, 2.47, 2.54])
vis = [int(round((v-2.2)/0.01)) for v in vs]
rs = [pts[vi] for vi in vis]
print zip(vs, rs)

# Plot WL voltage and selections
medians.plot(title='FPPV WL Voltage Selection', logy=False, xlim=(2.2, 2.7), ylim=(0, 60), linewidth=2, figsize=(4,3))
plt.xlabel('WL Voltage (V)')
plt.ylabel('Median Resistance (k$\\Omega$)')
leg = plt.legend([''], handletextpad=0.5, borderpad=0.2)
leg.set_title(title='BLV=1.6V, PW=100ns', prop={'size': 11})
plt.tight_layout()
plt.savefig('figs/fppv-wl-sweep.eps')
plt.show()
