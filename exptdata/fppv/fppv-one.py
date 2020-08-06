import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt


# Filter parameters
maxpulses = 500
bpc = 2


# Load data
names = ['addr', 'nreads', 'nsets', 'nresets', 'rf', 'if', 'rlo', 'rhi', 'success', 'attempts1', 'attempts2']
data = pd.read_csv('data/2bpc/fppv-wl0.100-bl6.00-6.00-sl6.00-6.00-7-24-20.csv', delimiter='\t', names=names, index_col=False)
data['npulses'] = data['nsets'] + data['nresets'] - 1
rlos = data['rlo'].unique()
data['bin'] = data['rlo'].apply(lambda x: np.where(rlos == x)[0][0])
data = data[data['bin'] != (2**bpc - 1)]


data['success'] = data['success'].astype(bool) & (data['npulses'] <= maxpulses)
data['npulses'] = data['npulses'].clip(upper=maxpulses)
print data

# data = data[data['addr'] != 3650]
# data = data[data['addr'] != 3557]
# data = data[data['addr'] != 3561]
# data = data[data['addr'] != 3622]
# data = data[data['addr'] != 3637]
# data = data[data['addr'] != 3644]
# data = data[data['addr'] != 3421]
# data = data[data['addr'] != 3482]
# data = data[data['addr'] != 3489]
# data = data[data['addr'] != 3615]
# data = data[data['addr'] != 3603]


# LaTEX quality figures 
mpl.rcParams.update(
    {
    'text.usetex': True,
    'pgf.texsystem': 'lualatex',
    'pgf.rcfonts': True,
    }
)
plt.rc('font', family='serif', serif='Times', size=13)


# FPPV Statistics
print 'Mean pulses:', data['npulses'].mean()
print 'Stdev pulses:', data['npulses'].std()
print 'Mean success rate:', data['success'].mean()

# FPPV Mean Pulses
grouped = data.groupby(['bin'])
npulses = grouped['npulses']
npulses_mean = npulses.mean()
npulses_std = npulses.std()
npulses_mean.plot.bar(title='FPPV: Mean Pulses per Level', figsize=(4,3), yerr=npulses_std)
plt.xlabel('Level Number')
plt.ylabel('Mean Pulses Required')
plt.tight_layout()
plt.savefig('figs/fppv-mean-pulses-bin.eps')
plt.show()

# FPPV Mean Sets
grouped = data.groupby(['bin'])
npulses = grouped['nsets']
npulses_mean = npulses.mean()
npulses_std = npulses.std()
npulses_mean.plot.bar(title='FPPV: Mean Sets per Level', figsize=(4,3), yerr=npulses_std)
plt.xlabel('Level Number')
plt.ylabel('Mean Sets Required')
plt.tight_layout()
plt.savefig('figs/fppv-mean-sets-bin.eps')
plt.show()

# FPPV Mean Resets
grouped = data.groupby(['bin'])
npulses = grouped['nresets']
npulses_mean = npulses.mean()
npulses_std = npulses.std()
npulses_mean.plot.bar(title='FPPV: Mean Resets per Level', figsize=(4,3), yerr=npulses_std)
plt.xlabel('Level Number')
plt.ylabel('Mean Resets Required')
plt.tight_layout()
plt.savefig('figs/fppv-mean-resets-bin.eps')
plt.show()

# FPPV Mean Success Rate
grouped = data.groupby(['bin'])
success = grouped['success']
success_mean = success.mean()
success_mean.plot.bar(title='FPPV: Success Rate per Level', figsize=(4,3))
plt.xlabel('Level Number')
plt.ylabel('Success Rate')
plt.tight_layout()
plt.savefig('figs/fppv-mean-success-bin.eps')
plt.show()