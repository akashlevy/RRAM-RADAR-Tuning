import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt


# Load data
names = ['addr', 'pw', 'blv', 'wlv', 'ri', 'rf']
stepsize = 0.05
data = pd.read_csv('data/set-sweep-wl-noreset-200ns-step-0.05-7-30-20-augment.csv', delimiter='\t', names=names)
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
grouped = data[data['blv'] == 2]
grouped = grouped.groupby(['wlv'])

# Means of final resistance
rf = grouped['rf']
means = rf.mean()/1000.
stds = rf.std()/1000.

# Derivative and smoothing
pts = means.values
print pts
x1, x2 = (2.1, 2.15)
xsi = (int(round((x1-1)/stepsize)), int(round((x2-1)/stepsize)))
print xsi
y1, y2 = pts[xsi[0]], pts[xsi[1]]
print y1, y2
gradpw = (y2-y1)/(x2-x1)
print gradpw

# Plot
#title='SET WL Voltage Sweep', 
ax = means.plot(logy=False, xlim=(2, 3), ylim=(0, 15), linewidth=2, figsize=(4,3)) #, yerr=stds.unstack(), elinewidth=0.5)
plt.plot([3*x1-2*x2, 3*x2-2*x1], [y1-2*gradpw*(x2-x1), y2+2*gradpw*(x2-x1)], 'r:')
plt.annotate('Slope: %.1f k$\\Omega$/V' % gradpw, xy=(x1, y1), xytext=(2.6, 8), arrowprops=dict(facecolor='black', shrink=0.1, width=1, headwidth=3, headlength=5), fontsize=11, horizontalalignment='center', verticalalignment='center')
plt.xlabel('WL Voltage (V)')
plt.ylabel('Mean Resistance (k$\\Omega$)')
leg = plt.legend([''], columnspacing=1, handletextpad=0.5, borderpad=0.2, prop={'size': 11})
leg.set_title(title='VBL=2V, PW=200ns', prop={'size': 11})
plt.tight_layout()
plt.savefig('figs/ispp-wl-sweep.eps')
plt.show()
