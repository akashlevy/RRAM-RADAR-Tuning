import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt


# Load data
names = ['addr', 'pw', 'bslv', 'wlv', 'ri', 'rf']
stepsize = 0.05


# LaTEX quality figures 
mpl.rcParams.update(
    {
    'text.usetex': True,
    'pgf.texsystem': 'lualatex',
    'pgf.rcfonts': True,
    }
)
plt.rc('font', family='serif', serif='Times', size=13)


# Function for removing outliers
def is_outlier(s):
    lower_limit = s.mean() - (s.std() * 2.5)
    upper_limit = s.mean() + (s.std() * 2.5)
    return ~s.between(lower_limit, upper_limit)


# Do for each type of sweep
fnames = [
    'data/reset-sweep-sl-200ns-step-0.05-9-21-20-augment.csv',
    'data/reset-sweep-wl-200ns-step-0.05-9-21-20-augment.csv',
    'data/set-sweep-bl-200ns-step-0.05-9-21-20-augment.csv',
    'data/set-sweep-wl-200ns-step-0.05-9-21-20-augment.csv'
]
groupvars = ['bslv', 'wlv', 'bslv', 'wlv']
labels = ['VSL (RESET)', 'VWL (RESET)', 'VBL (SET)', 'VWL (SET)']
xs = [(0.75, 0.8), (2.3, 2.35), (0.75, 0.8), (2.05, 2.1)]
for fname, groupvar, label, (x1, x2) in zip(fnames, groupvars, labels, xs):
    # Load data
    data = pd.read_csv(fname, delimiter='\t', names=names)

    # Remove outliers
    data = data[~data.groupby(groupvar)['rf'].apply(is_outlier)]

    # Set up variables
    grouped = data.groupby(groupvar)

    # Means of final resistance
    rf = grouped['rf']
    means = rf.mean()/1000.
    stds = rf.std()/1000.

    # Derivative and smoothing
    pts = means.values
    xsi = (int(round((x1-0)/stepsize)), int(round((x2-0)/stepsize)))
    y1, y2 = pts[xsi[0]], pts[xsi[1]]
    gradpw = (y2-y1)/(x2-x1)
    print label, gradpw

    # Plot 
    ax = means.plot(label=label, logy=False, xlim=(0, 3), ylim=(4, 8), linewidth=2, figsize=(4,3))
    #plt.annotate('Slope: %.1f k$\\Omega$/V' % gradpw, xy=((x1+x2)/2, 6.5 if y1 > 6 else 5.5), xytext=(x1-0.2, y1+1 if y1 > 6 else y1-1), arrowprops=dict(facecolor='black', shrink=0.1, width=1, headwidth=3, headlength=5), fontsize=9, horizontalalignment='center', verticalalignment='center')
    #plt.plot([2*x1-x2, 2*x2-x1], [y1-gradpw*(x2-x1), y2+gradpw*(x2-x1)], 'm:', linewidth=2, zorder=10)

# Save to file
plt.title('Resistance Tuning Curves at 6 k$\\Omega$')
plt.xlabel('Tuning Knob Voltage (V)')
plt.ylabel('Mean Resistance (k$\\Omega$)')
#leg = plt.legend(columnspacing=1, handletextpad=0.5, borderpad=0.2, prop={'size': 9})
#leg.set_title(title='Tuning Knob', prop={'size': 11})
plt.tight_layout()
plt.savefig('figs/combined-sweep.eps')
plt.savefig('figs/combined-sweep.pdf')
plt.show()
