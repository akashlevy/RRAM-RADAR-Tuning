import itertools
import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

# Flipper
def flip(items, ncol):
    return itertools.chain(*[items[i::ncol] for i in range(ncol)])

# LaTEX quality figures 
mpl.rcParams.update(
    {
    'text.usetex': True,
    'pgf.texsystem': 'lualatex',
    'pgf.rcfonts': True,
    }
)
plt.rc('font', family='serif', serif='Times', size=13)

# Load data
names = ['bpc', 'temp', 'time', 'ber']
data = pd.read_csv('data/ber-time-temp.csv', delimiter=',', names=names, skiprows=[0])
data['temp'] = data['temp'] - 273 # convert to Celsius
data['ber'] = data['ber'] * 100 # convert to percent

# Plot sigma-mu
plt.figure(figsize=(4,3))
plt.ylim(1e-1, 100)
plt.title('Est. Relaxation BER vs. Time')
for group, gdata in data.groupby(['bpc','temp']):
    print group
    print gdata
    gdata.plot(x='time', y='ber', marker='x', ax=plt.gca(), logx=True, logy=True, label='%sbpc@$%s^{\circ}$C' % group)
handles, labels = plt.gca().get_legend_handles_labels()
plt.legend(flip(handles, 3), flip(labels, 3), columnspacing=0.8, handletextpad=0.2, borderpad=0.2, prop={'size': 8.5}, ncol=3, handlelength=1.4)
plt.plot([3.154e+8,3.154e+8], [5e-2,100], 'r--')
plt.text(4e+8, 15, '10yrs', color='r', fontsize=8.5)
xlim = (1e4, plt.gca().get_xlim()[1])
plt.plot(list(xlim), [1,1], 'b--')
plt.text(2e4, 1.1, '1\% BER', color='b', fontsize=8.5)
plt.plot(list(xlim), [0.3,0.3], 'b--')
plt.text(2e4, 0.35, '0.3\% BER', color='b', fontsize=8.5)
plt.gca().set_xlim(xlim)
plt.xlabel('Time (s)')
plt.ylabel('Bit Error Rate (\%)')
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%s'))
plt.tight_layout()
plt.savefig('figs/ber-time-temp.eps')
plt.show()