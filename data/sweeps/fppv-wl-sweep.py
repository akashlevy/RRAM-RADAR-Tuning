import matplotlib as mpl, numpy as np, pandas as pd, pygmo as pg
import matplotlib.pyplot as plt

chipnum = 1
if chipnum == 1:
    data = pd.read_csv('data/set-sweep-wl-deeper-7-3-20.csv', delimiter='\t', names=['addr', 'pw', 'blv', 'wlv', 'ri', 'rf']) # chip1
if chipnum == 2:
    data = pd.read_csv('data/set-sweep-wl-inner-chip2-6-15-20.csv', delimiter='\t', names=['addr', 'pw', 'blv', 'wlv', 'ri', 'rf']) # chip2
data = data[data['pw'] == 100]
data = data[data['blv'] == 2]
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
    lower_limit = s.mean() - (s.std() * 2)
    upper_limit = s.mean() + (s.std() * 2)
    return ~s.between(lower_limit, upper_limit)
data = data[~data.groupby(['blv','wlv'])['rf'].apply(is_outlier)]

# Set up variables
grouped = data.groupby(['wlv'])

# Medians of final resistance
rf = grouped['rf']
medians = rf.median()/1000.
stds = rf.std()/1000.
print medians
medians.to_csv('results/fppv%s.csv' % chipnum)

pts = medians.values
if chipnum == 1:
    vs = list(reversed([2.26, 2.31, 2.36, 2.41, 2.47, 2.53])) # chip1
if chipnum == 2:
    vs = list(reversed([2.28, 2.33, 2.38, 2.44, 2.52, 2.55])) # chip2
vis = [int(round((v-2)/0.01)) for v in vs]
rs = [pts[vi] for vi in vis]
data = zip(range(1,7), vs, rs)
print data

# Plot WL voltage and selections
medians.plot(title='FPPV WL Voltage Selection', logy=False, xlim=(2.2, 3), ylim=(0, 60), linewidth=2, figsize=(4,3))
for i, v, r in data[:5]:
    plt.annotate('Range %i: %.2fV' % (i,v), xy=(v, r), xytext=(v, r+5*i), arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=1, headlength=1, linestyle='dotted'), fontsize=10, horizontalalignment='left', verticalalignment='center')
plt.annotate('Range %i: %.2fV' % (6,vs[5]), xy=(vs[5], rs[5]), xytext=(vs[5], rs[5]+20), arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=1, headlength=1, linestyle='dotted'), fontsize=10, horizontalalignment='left', verticalalignment='center')
plt.xlabel('WL Voltage (V)')
plt.ylabel('Median Resistance (k$\\Omega$)')
leg = plt.legend([''], handletextpad=0.5, borderpad=0.2)
leg.set_title(title='VBL=2V\nPW=100ns', prop={'size': 11})
plt.tight_layout()
plt.savefig('figs/fppv-wl-sweep.eps')
plt.show()
