import matplotlib as mpl, numpy as np, pandas as pd, pygmo as pg
import matplotlib.pyplot as plt

chipnum = 1
if chipnum == 1:
    data = pd.read_csv('data/set-sweep-wl-200pw-7-16-20.csv', delimiter='\t', names=['addr', 'pw', 'blv', 'wlv', 'ri', 'rf']) # chip1
if chipnum == 2:
    data = pd.read_csv('data/set-sweep-wl-inner-chip2-6-15-20.csv', delimiter='\t', names=['addr', 'pw', 'blv', 'wlv', 'ri', 'rf']) # chip2
data = data[data['pw'] == 200]
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
    vs = list(reversed([2.2, 2.3, 2.55, 2.7, 2.85, 3.15, 3.3])) # chip1
if chipnum == 2:
    vs = list(reversed([2.28, 2.33, 2.38, 2.44, 2.52, 2.55])) # chip2
vis = [int(round((v-1.5)/0.01)) for v in vs]
rs = [pts[vi] for vi in vis]
data = zip(range(7), vs, rs)
print data

# Plot WL voltage and selections
medians.plot(title='FPPV WL Voltage Selection', logy=False, xlim=(2, 3.5), ylim=(0, 40), linewidth=2, figsize=(4,3))
for i, v, r in data:
    ha = 'left' if i != 1 else 'center'
    ha = ha if i != 0 else 'right'
    plt.annotate('Range %i: %.2fV' % (i,v), xy=(v, r), xytext=(v, (i+1)*5 if i != 0 else 2), arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=1, headlength=1, linestyle='dotted'), fontsize=10, horizontalalignment=ha, verticalalignment='center')
plt.xlabel('WL Voltage (V)')
plt.ylabel('Median Resistance (k$\\Omega$)')
leg = plt.legend([''], handletextpad=0.5, borderpad=0.2)
leg.set_title(title='VBL=2V\nPW=200ns', prop={'size': 11})
plt.tight_layout()
plt.savefig('figs/fppv-wl-sweep.eps')
plt.show()
