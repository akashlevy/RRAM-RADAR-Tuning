import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt


# Load data
names = ['addr', 'pw', 'blv', 'wlv', 'ri', 'rf']
stepsize = 0.02
data = pd.read_csv('data/wl-set-sweep-5-29-20.csv', delimiter='\t', names=names)
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
grouped = data[data['blv'] == 2]
grouped = grouped.groupby(['wlv'])

# Medians of final resistance
rf = grouped['rf']
medians = rf.median()/1000.
stds = rf.std()/1000.

# Derivative and smoothing
pts = medians.values
print pts
x1, x2 = (2.28, 2.32)
xsi = (int(round((x1-2)/stepsize)), int(round((x2-2)/stepsize)))
print xsi
y1, y2 = pts[xsi[0]], pts[xsi[1]]
print y1, y2
gradpw = (y2-y1)/(x2-x1)
print gradpw

# Plot
ax = medians.plot(title='WL Voltage Sweep', logy=False, xlim=(2.26, 2.55), ylim=(0, 60), linewidth=2, figsize=(4,3)) #, yerr=stds.unstack(), elinewidth=0.5)
plt.plot([2*x1-x2, x2], [y1-gradpw*(x2-x1), y2], 'r:')
plt.annotate('Slope: %.1f k$\\Omega$/V' % gradpw, xy=(x1, y1), xytext=(2.35, 55), arrowprops=dict(facecolor='black', shrink=0.1, width=1, headwidth=3, headlength=5), fontsize=11, horizontalalignment='center', verticalalignment='center')
plt.xlabel('WL Voltage (V)')
plt.ylabel('Median Resistance (k$\\Omega$)')
leg = plt.legend([''], columnspacing=1, handletextpad=0.5, borderpad=0.2, prop={'size': 11})
leg.set_title(title='BLV=2V, PW=100ns', prop={'size': 11})
plt.tight_layout()
plt.savefig('figs/ispp-wl-sweep.eps')
plt.show()
