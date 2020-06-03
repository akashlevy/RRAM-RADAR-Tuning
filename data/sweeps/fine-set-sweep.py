import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt


# Load data
names = ['addr', 'pw', 'blv', 'wlv', 'ri', 'rf']
stepsize = 0.02
data = pd.read_csv('data/set-sweep-fine-step-0.02-5-31-20.csv', delimiter='\t', names=names)
data = data[data['addr'] == 1455]
data = data[data['blv'] != 2]
#data = data[data['blv'] != 2.02]
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
    lower_limit = s.mean() - (s.std() * 1.5)
    upper_limit = s.mean() + (s.std() * 1.5)
    return ~s.between(lower_limit, upper_limit)
data = data[~data.groupby(['blv','wlv'])['rf'].apply(is_outlier)]

# Set up variables
grouped = data.groupby(['blv', pd.cut(data['wlv'], np.arange(2, 3, 0.01))])

# Means of final resistance
rf = grouped['rf']
means = rf.mean()/1000.
stds = rf.std()/1000.

# Derivative and smoothing
pts = means.unstack().values[:,0]
x1, x2 = (2.04, 2.22)
xsi = (int(round((x1-2.02)/stepsize)), int(round((x2-2.02)/stepsize)))
y1, y2 = pts[xsi[0]], pts[xsi[1]]
gradpw = (y2-y1)/(x2-x1)


# Plot
ax = means.unstack().plot(title='Fine SET BL Voltage Sweep', logy=False, xlim=(2, 3), ylim=(0, 60), linewidth=2, figsize=(4,3)) #, yerr=stds.unstack(), elinewidth=0.5)
plt.plot([2*x1-x2, 2*x2-x1], [y1-gradpw*(x2-x1), y2+gradpw*(x2-x1)], 'r:')
plt.annotate('Slope: %.1f k$\\Omega$/V' % gradpw, xy=(x1, y1), xytext=(x1, 54), arrowprops=dict(facecolor='black', shrink=0.1, width=1, headwidth=3, headlength=5), fontsize=11, horizontalalignment='left', verticalalignment='center')
plt.xlabel('BL Voltage (V)')
plt.ylabel('Mean Resistance (k$\\Omega$)')
leg = plt.legend([2.26, 2.31, 2.35, 2.41, 2.47, 2.54], ncol=2, columnspacing=1, handletextpad=0.5, borderpad=0.2, prop={'size': 11})
leg.set_title('WL Voltage (V)', prop = {'size': 11})
plt.tight_layout()
plt.savefig('figs/fine-set-sweep.eps')
plt.show()
