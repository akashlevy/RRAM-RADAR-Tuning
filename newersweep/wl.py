import matplotlib as mpl, numpy as np, pandas as pd, pygmo as pg
import matplotlib.pyplot as plt

data = pd.read_csv('sweep-4-14-20.csv', delimiter='\t', names=['addr', 'pw', 'blv', 'wlv', 'ri', 'rf'])
data = data[data['ri'] > 60e3]
data = data[data['blv'] == 3.3]
data = data[data['pw'] == 100]
print data

# LaTEX quality figures 
mpl.rcParams.update(
    {
    'text.usetex': True,
    'pgf.texsystem': 'lualatex',
    'pgf.rcfonts': True,
    }
)
plt.rc('font', family='serif', serif='Times')

# Set up variables
grouped = data.groupby(['wlv'])

# Means of final resistance
means = grouped['rf'].mean()
stds = grouped['rf'].std()
means.plot(title='WL Voltage Sweep', logy=False, xlim=(1.8, 3), ylim=(1e3, 1.6e5), yerr=stds, linewidth=2, elinewidth=0.5, figsize=(4,3))
plt.xlabel('WL Voltage (V)')
plt.ylabel('Mean Resistance (ohm)')
plt.legend(['100ns', '200ns', '300ns'])
plt.tight_layout()
plt.show()
