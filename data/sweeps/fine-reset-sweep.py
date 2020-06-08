import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt


# Load data
names = ['addr', 'pw', 'slv', 'wlv', 'ri', 'rf']
stepsize = 0.02
data = pd.read_csv('data/reset-sweep-fine-step-0.02-6-7-20-augment.csv', delimiter='\t', names=names)


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
    lower_limit = s.mean() - (s.std() * 2)
    upper_limit = s.mean() + (s.std() * 2)
    return ~s.between(lower_limit, upper_limit)
data = data[~data.groupby(['slv','wlv'])['rf'].apply(is_outlier)]

# Set up variables
#data = data[data['slv']*1000 % 1 <= 1e-9]
#data = data[data['wlv'] == 4]
grouped = data.groupby('slv')

# Means of final resistance
rf = grouped['rf']
means = rf.mean()/1000.
stds = rf.std()/1000.

# Derivative and smoothing
pts = means.values
print pts
x1, x2 = (1.6, 1.82)
xsi = (int(round((x1-0)/stepsize)), int(round((x2-0)/stepsize)))
print xsi
y1, y2 = pts[xsi[0]], pts[xsi[1]]
print y1, y2
gradpw = (y2-y1)/(x2-x1)
print gradpw

# Plot
ax = means.plot(title='Fine RESET SL Voltage Sweep', logy=False, xlim=(1, 2.5), ylim=(0, 60), linewidth=2, figsize=(4,3)) #, yerr=stds.unstack(), elinewidth=0.5)
plt.plot([2*x1-x2, 2*x2-x1], [y1-gradpw*(x2-x1), y2+gradpw*(x2-x1)], 'r:', linewidth=2)
plt.annotate('Slope: %.1f k$\\Omega$/V' % gradpw, xy=(x1, y1), xytext=(x1, 50), arrowprops=dict(facecolor='black', shrink=0.1, width=1, headwidth=3, headlength=5), fontsize=11, horizontalalignment='center', verticalalignment='center')
plt.xlabel('SL Voltage (V)')
plt.ylabel('Mean Resistance (k$\\Omega$)')
plt.legend(['VWL=3.5V, PW=100ns'], columnspacing=1, handletextpad=0.5, borderpad=0.2, prop={'size': 11})
plt.tight_layout()
plt.savefig('figs/fine-reset-sweep.eps')
plt.show()
