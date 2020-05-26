import matplotlib as mpl, numpy as np, pandas as pd, pygmo as pg
import matplotlib.pyplot as plt

'''Smooth using filter'''
def smooth(y, box_pts=7):
    box = np.ones(box_pts) / box_pts
    return np.concatenate((y[:box_pts/2], np.convolve(y, box, mode='valid'), y[-box_pts/2+1:]))

data = pd.read_csv('set-sweep-5-1-20.csv', delimiter='\t', names=['addr', 'pw', 'blv', 'wlv', 'ri', 'rf'])
data = data[data['ri'] > 60e3]
data = data[data['blv'] == 1.5]
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
grouped = data.groupby(['wlv', pd.cut(data["pw"], np.arange(0, 1000, 100))])

# Means of final resistance
rf = grouped['rf']
means = rf.mean()/1000.
stds = rf.std()/1000.

# Derivative and smoothing
# pts = means.unstack().values
# grads = np.gradient(pts, axis=0)/0.01
# xs = [[2.12,2.28],[1.88,1.98],[1.78,1.88]]
# xsi = [(int(round((n1-1.5)*100)), int(round((n2-1.5)*100))) for n1, n2 in xs]
# gradpw = [grads[xsi[i][0]:xsi[i][1],i].mean() for i in range(3)]
# print gradpw
# midsi = [(xsi[i][0] + xsi[i][1])/2 for i in range(3)]
# mids = [(xs[i][0] + xs[i][1])/2 for i in range(3)]
# pt = [pts[midsi[i],i] for i in range(3)]
# ys = [(gradpw[i] * (x[0] - mids[i]) + pt[i], gradpw[i] * (x[1] - mids[i]) + pt[i]) for i,x in enumerate(xs)]

# Plot
means.unstack().plot(title='SET Pulse Width: WL Voltage Sweep', logy=False, xlim=(1.7, 2.6), ylim=(0, 1.8e2), linewidth=2, figsize=(4,3)) #, yerr=stds.unstack(), elinewidth=0.5)
# plt.plot(xs[0], ys[0], ':', linewidth=3)
# plt.plot(xs[1], ys[1], ':', linewidth=3)
# plt.plot(xs[2], ys[2], ':', linewidth=3)
plt.xlabel('WL Voltage (V)')
plt.ylabel('Mean Resistance (k$\\Omega$)')
plt.tight_layout()
plt.savefig('figs/bl-sweep.eps')
plt.show()

