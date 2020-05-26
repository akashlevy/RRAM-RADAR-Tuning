import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt


# Load data
datas = []
names = ['addr', 'nreads', 'nsets', 'nresets', 'rf', 'if', 'rlo', 'rhi', 'success', 'attempts1', 'attempts2']
for step in np.arange(0.01, 0.16, 0.01):
    data = pd.read_csv('data/ispp-%.2f-5-26-20.csv' % step, delimiter='\t', names=names, index_col=False)
    data['npulses'] = data['nsets'] + data['nresets']
    data['stepsize'] = step
    rlos = data['rlo'].unique()
    data['bin'] = data['rlo'].apply(lambda x: np.where(rlos == x)[0][0])
    datas.append(data)
data = pd.concat(datas)
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


# ISPP Mean Step
grouped = data.groupby(['stepsize'])
npulses = grouped['npulses']
npulses_mean = npulses.mean()
print npulses_mean
npulses_std = npulses.std()
print npulses_std
npulses_mean.plot.bar(title='ISPP: Mean Pulses vs. Step Size', figsize=(4,3), yerr=npulses_std)
plt.xlabel('Step Size')
plt.ylabel('Mean Pulses Required')
plt.tight_layout()
plt.savefig('figs/ispp-mean-pulses-step.eps')
plt.show()

# ISPP Mean Resets
grouped = data.groupby(['stepsize'])
nresets = grouped['nresets']
nresets_mean = nresets.mean()
print nresets_mean
nresets_std = nresets.std()
print nresets_std
nresets_mean.plot.bar(title='ISPP: Mean Resets vs. Step Size', figsize=(4,3), yerr=nresets_std)
plt.xlabel('Step Size')
plt.ylabel('Mean Resets Required')
plt.tight_layout()
plt.savefig('figs/ispp-mean-resets-step.eps')
plt.show()

# ISPP Mean Success Rate
grouped = data.groupby(['stepsize'])
success = grouped['success']
success_mean = success.mean()
print success_mean
success_mean.plot.bar(title='ISPP: Success Rate vs. Step Size', figsize=(4,3))
plt.xlabel('Step Size')
plt.ylabel('Success Rate')
plt.tight_layout()
plt.savefig('figs/ispp-mean-success-step.eps')
plt.show()


# ISPP Mean Step
grouped = data[data['stepsize'] == 0.01].groupby(['bin'])
npulses = grouped['npulses']
npulses_mean = npulses.mean()
npulses_std = npulses.std()
npulses_mean.plot.bar(title='ISPP: Mean Pulses per Level', figsize=(4,3), yerr=npulses_std)
plt.xlabel('Level Number')
plt.ylabel('Mean Pulses Required')
plt.tight_layout()
plt.savefig('figs/ispp-mean-pulses-beststep-bin.eps')
plt.show()

# ISPP Mean Resets
grouped = data[data['stepsize'] == 0.01].groupby(['bin'])
nresets = grouped['nresets']
nresets_mean = nresets.mean()
nresets_std = nresets.std()
nresets_mean.plot.bar(title='ISPP: Mean Resets per Level', figsize=(4,3), yerr=nresets_std)
plt.xlabel('Level Number')
plt.ylabel('Mean Resets Required')
plt.tight_layout()
plt.savefig('figs/ispp-mean-resets-beststep-bin.eps')
plt.show()

# ISPP Mean Success Rate
grouped = data[data['stepsize'] == 0.01].groupby(['bin'])
success = grouped['success']
success_mean = success.mean()
print success_mean
success_mean.plot.bar(title='ISPP: Success Rate per Level', figsize=(4,3))
plt.xlabel('Level Number')
plt.ylabel('Success Rate')
plt.tight_layout()
plt.savefig('figs/ispp-mean-success-beststep-bin.eps')
plt.show()