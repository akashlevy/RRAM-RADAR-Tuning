import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt


# Load data
names = ['addr', 'nreads', 'nsets', 'nresets', 'rf', 'if', 'rlo', 'rhi', 'success', 'attempts1', 'attempts2']
data = pd.read_csv('ispp/data/ispp-wl0.04-bl0.05-sl0.30-0.30-5-23-20.csv', delimiter='\t', names=names, index_col=False)
data['npulses'] = data['nsets'] + data['nresets']
rlos = data['rlo'].unique()
data['bin'] = data['rlo'].apply(lambda x: np.where(rlos == x)[0][0])
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

# ISPP Statistics
print 'Mean pulses:', data['npulses'].mean()
print 'Stdev pulses:', data['npulses'].std()
print 'Mean resets:', data['nresets'].mean()
print 'Stdev resets:', data['nresets'].std()
print 'Mean success rate:', data['success'].mean()

# ISPP Mean Step
grouped = data.groupby(['addr'])
npulses = grouped['success']
npulses_mean = npulses.mean()
npulses_mean.plot()
plt.show()

# 894, 992, 1015,       900, 909, 939, 955
