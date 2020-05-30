import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt


# Filter parameters
maxpulses = 50


# Load data
names = ['addr', 'nreads', 'nsets', 'nresets', 'rf', 'if', 'rlo', 'rhi', 'success', 'attempts1', 'attempts2']
data = pd.read_csv('data/fppv-eval-4wl-chip1.csv', delimiter='\t', names=names, index_col=False)
data['npulses'] = data['nsets'] + data['nresets']
rlos = data['rlo'].unique()
data['bin'] = data['rlo'].apply(lambda x: np.where(rlos == x)[0][0])
# data = data[data['addr'] != 894]
# data = data[data['addr'] != 900]
# data = data[data['addr'] != 909]
# data = data[data['addr'] != 939]
# data = data[data['addr'] != 955]
# data = data[data['addr'] != 992]
# data = data[data['addr'] != 1015]

data['success'] = data['success'].astype(bool) & (data['npulses'] <= maxpulses)
data['npulses'] = data['npulses'].clip(upper=maxpulses)
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