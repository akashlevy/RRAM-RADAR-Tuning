import matplotlib as mpl, numpy as np, pandas as pd, pygmo as pg
import matplotlib.pyplot as plt

data = pd.read_csv('data/set-sweep-wl-inner-5-26-20.csv', delimiter='\t', names=['addr', 'pw', 'blv', 'wlv', 'ri', 'rf'])
#data = data[data['pw'] == 100]
#data = data[data['ri'] > 60e3]
#data = data[data['ri'] < 100e3]
#data = data[data['blv'] == 1.5]
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
medians.plot(title='WL Voltage Sweep', logy=False, xlim=(2.2, 2.7), ylim=(0, 80), linewidth=2, figsize=(4,3))
plt.xlabel('WL Voltage (V)')
plt.ylabel('Median Resistance (k$\\Omega$)')
plt.legend([''], title='BLV=1.5V, PW=100ns')
plt.tight_layout()
plt.savefig('wl.eps')
plt.show()
