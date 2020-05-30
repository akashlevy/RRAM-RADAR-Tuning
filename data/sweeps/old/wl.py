import matplotlib as mpl, numpy as np, pandas as pd, pygmo as pg
import matplotlib.pyplot as plt

data = pd.read_csv('data/reset-sweep-wl-step-0.01-5-28-20.csv', delimiter='\t', names=['addr', 'pw', 'slv', 'wlv', 'ri', 'rf'])
data = data[data['pw'] == 100]
data = data[data['slv'] == 2.3]
data = data[data['addr'] == 1450]
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

# Means of final resistance
rf = grouped['rf']
medians = rf.median()/1000.
stds = rf.std()/1000.
medians.plot(title='WL Voltage Sweep (10 cells, 20 sweeps/cell)', logy=False, xlim=(3, 4), ylim=(0, 60), linewidth=2, figsize=(4,3))
plt.xlabel('WL Voltage (V)')
plt.ylabel('Median Resistance (k$\\Omega$)')
plt.legend([''], title='SLV=2.3V, PW=100ns')
plt.tight_layout()
plt.savefig('wl.eps')
plt.show()
