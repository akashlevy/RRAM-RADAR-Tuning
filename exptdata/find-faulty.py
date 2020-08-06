import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt



# Load data
bpc = 2
names = ['addr', 'nreads', 'nsets', 'nresets', 'rf', 'if', 'rlo', 'rhi', 'success', 'attempts1', 'attempts2']
data = pd.read_csv('sdr/data/2bpc/sl-opt-1/sdr-wl0.100-bl0.04-2.00-sl0.02-0.20-7-24-20.csv', delimiter='\t', names=names, index_col=False)
data['npulses'] = data['nsets'] + data['nresets']
rlos = data['rlo'].unique()
data['bin'] = data['rlo'].apply(lambda x: np.where(rlos == x)[0][0])
data = data[data['bin'] != (2**bpc - 1)]


# LaTEX quality figures 
mpl.rcParams.update(
    {
    'text.usetex': True,
    'pgf.texsystem': 'lualatex',
    'pgf.rcfonts': True,
    }
)
plt.rc('font', family='serif', serif='Times', size=13)


# Statistics
print 'Mean pulses:', data['npulses'].mean()
print 'Stdev pulses:', data['npulses'].std()
print 'Mean resets:', data['nresets'].mean()
print 'Stdev resets:', data['nresets'].std()
print 'Mean success rate:', data['success'].mean()


# Plot success
grouped = data.groupby(['addr'])
npulses = grouped['success']
npulses_mean = npulses.mean()
npulses_mean.plot()
plt.show()


# Export bad addresses to CSV file
addr = data.groupby(['addr'])['success'].mean()
addr = addr[addr < 0.6]
addr.to_csv('badaddrs.csv')
