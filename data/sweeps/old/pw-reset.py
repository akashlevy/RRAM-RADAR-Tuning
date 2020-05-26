import matplotlib as mpl, numpy as np, pandas as pd, pygmo as pg
import matplotlib.pyplot as plt

'''Smooth using filter'''
def smooth(y, box_pts=7):
    box = np.ones(box_pts) / box_pts
    return np.concatenate((y[:box_pts/2], np.convolve(y, box, mode='valid'), y[-box_pts/2+1:]))

data = pd.read_csv('rsweep-4-24-20.csv', delimiter='\t', names=['addr', 'pw', 'slv', 'wlv', 'ri', 'rf'])
data = data[data['ri'] < 10e3]
data = data[data['wlv'] == 4]
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
grouped = data.groupby(['slv', pd.cut(data["pw"], np.arange(0, 1000, 100))])

# Means of final resistance
rf = grouped['rf']
means = rf.mean()/1000.
stds = rf.std()/1000.

# Derivative and smoothing

# Plot
means.unstack().plot(title='RESET Pulse Width: SL Voltage Sweep', logy=False, xlim=(1, 4), ylim=(0, 80), linewidth=2, figsize=(4,3)) #, yerr=stds.unstack(), elinewidth=0.5)
plt.xlabel('SL Voltage (V)')
plt.ylabel('Mean Resistance (k$\\Omega$)')
plt.legend(['100ns', '200ns', '300ns'], title='WLV=4V, PW=')
plt.tight_layout()
plt.savefig('pw-reset.eps')
plt.show()
