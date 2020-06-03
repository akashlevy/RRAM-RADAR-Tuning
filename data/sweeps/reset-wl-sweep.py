import matplotlib as mpl, numpy as np, pandas as pd, pygmo as pg
import matplotlib.pyplot as plt

stepsize = 0.02
data = pd.read_csv('data/reset-sweep-wl-%.2f-5-31-20.csv' % stepsize, delimiter='\t', names=['addr', 'pw', 'slv', 'wlv', 'ri', 'rf'])
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
plt.rc('font', family='serif', serif='Times', size=13)

# Set up variables
grouped = data.groupby(['wlv'])

# Means of final resistance
rf = grouped['rf']
means = rf.mean()/1000.
stds = rf.std()/1000.

# Derivative and smoothing
pts = means.values
print pts
x1, x2 = (3, 3.14)
xsi = (int(round((x1-2)/stepsize)), int(round((x2-2)/stepsize)))
print xsi
y1, y2 = pts[xsi[0]], pts[xsi[1]]
print y1, y2
gradpw = (y2-y1)/(x2-x1)
print gradpw

# Plot
means.plot(title='Fine RESET WL Voltage Sweep', logy=False, xlim=(2.5, 3.5), ylim=(0, 60), linewidth=2, figsize=(4,3))
plt.plot([2*x1-x2, x2+0.1], [y1-gradpw*(x2-x1), y2+0.1*gradpw], 'r:', linewidth=2)
plt.annotate('Slope: %.1f k$\\Omega$/V' % gradpw, xy=(x1, y1), xytext=(2.8, 25), arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=3, headlength=5), fontsize=11, horizontalalignment='center', verticalalignment='center')
plt.xlabel('WL Voltage (V)')
plt.ylabel('Mean Resistance (k$\\Omega$)')
leg = plt.legend([''], columnspacing=1, handletextpad=0.5, borderpad=0.2, prop={'size': 11})
leg.set_title(title='VSL=2.5V, PW=100ns', prop={'size': 11})
plt.tight_layout()
plt.savefig('figs/wl-reset.eps')
plt.show()
