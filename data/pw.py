import matplotlib as mpl, numpy as np, pandas as pd, pygmo as pg
import matplotlib.pyplot as plt

'''Smooth using filter'''
def smooth(y, box_pts=7):
    box = np.ones(box_pts) / box_pts
    return np.concatenate((y[:box_pts/2], np.convolve(y, box, mode='valid'), y[-box_pts/2+1:]))

data = pd.read_csv('sweep-4-14-20.csv', delimiter='\t', names=['addr', 'pw', 'blv', 'wlv', 'ri', 'rf'])
data = data[data['ri'] > 60e3]
data = data[data['blv'] == 3.3]
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
grouped = data.groupby(['wlv', pd.cut(data["pw"], np.arange(0, 1000, 100))])

# Means of final resistance
rf = grouped['rf']
means = rf.mean()/1000.
stds = rf.std()/1000.

# Derivative and smoothing
#result = means.apply(smooth, axis=1)

# Plot
means.unstack().plot(title='SET Pulse Width: WL Voltage Sweep', logy=False, xlim=(1.7, 2.6), ylim=(0, 1.6e2), linewidth=2, figsize=(4,3)) #, yerr=stds.unstack(), elinewidth=0.5)
plt.xlabel('WL Voltage (V)')
plt.ylabel('Mean Resistance (k$\\Omega$)')
plt.legend(['100ns', '200ns', '300ns'], title='BLV=3.3V, PW=')
plt.tight_layout()
plt.savefig('pw.eps')
plt.show()
