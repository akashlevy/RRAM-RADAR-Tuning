import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt


# Load data
names = ['addr', 'nreads', 'nsets', 'nresets', 'rf', 'if', 'rlo', 'rhi', 'success', 'attempts1', 'attempts2']
data = pd.read_csv('sdr/data/sl-opt/sdr-wl0.070-bl0.04-0.40-sl0.22-1.00-7-24-20.csv', delimiter='\t', names=names, index_col=False)
data['npulses'] = data['nsets'] + data['nresets']
rlos = data['rlo'].unique()
data['bin'] = data['rlo'].apply(lambda x: np.where(rlos == x)[0][0])
data = data[data['bin'] != 7]
print data[data['success'] == 0]


ignore = [8641,8813,8823]
data = data[~data['addr'].isin(ignore)]


# LaTEX quality figures 
mpl.rcParams.update(
    {
    'text.usetex': True,
    'pgf.texsystem': 'lualatex',
    'pgf.rcfonts': True,
    }
)
plt.rc('font', family='serif', serif='Times', size=13)

# ISPP Statistics
print 'Mean pulses:', data['npulses'].mean()
print 'Stdev pulses:', data['npulses'].std()
print 'Mean resets:', data['nresets'].mean()
print 'Stdev resets:', data['nresets'].std()
print 'Mean success rate:', data['success'].mean()

# ISPP Mean Step
grouped = data.groupby(['addr'])
npulses = grouped['npulses']
npulses_mean = npulses.mean()
npulses_mean.plot()
plt.show()

addr = data.groupby(['addr'])['npulses'].mean()
#addr = addr[addr > 0.8]
addr = addr[addr > 200]
addr.to_csv('badaddrs.csv')
