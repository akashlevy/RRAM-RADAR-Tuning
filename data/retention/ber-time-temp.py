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

SEC_TO_YEAR = 3.17098e-8

# Load data
names = ['bpc', 'temp', 'time', 'ber']
data = pd.read_csv('data/ber-time-temp.csv', delimiter=',', names=names, skiprows=[0])
data['temp'] = data['temp'] - 273 # convert to Celsius
data['ber'] = data['ber'] * 100 # convert to percent
data['time'] = data['time'] * SEC_TO_YEAR # convert to years
data = data[data['temp'] == 65]

# Plot sigma-mu
plt.figure(figsize=(4,3))
plt.ylim(1e-1, 30)
plt.title('Est. Relaxation BER vs. Time')
for group, gdata in data.groupby(['bpc','temp']):
    print group
    print gdata
    gdata.plot(x='time', y='ber', marker='x', ax=plt.gca(), logx=True, logy=True, label='%sbpc@$%s^{\circ}$C' % group)
handles, labels = plt.gca().get_legend_handles_labels()
plt.legend(flip(handles, 3), flip(labels, 3), columnspacing=0.8, handletextpad=0.2, borderpad=0.2, prop={'size': 8.5}, ncol=3, handlelength=1.4)
plt.plot([3.154e+8 * SEC_TO_YEAR, 3.154e+8 * SEC_TO_YEAR], [4e-2,100], 'r--')
plt.text(1.7e8 * SEC_TO_YEAR, 10, '10yrs', color='r', fontsize=9)
plt.xlim(1, 400)
xlim = plt.gca().get_xlim()
plt.plot(list(xlim), [1,1], 'b--')
plt.text(4e7 * SEC_TO_YEAR, 1.1, '1\% BER Target', color='b', fontsize=9)
plt.plot(list(xlim), [0.3,0.3], 'b--')
plt.text(4e7 * SEC_TO_YEAR, 0.33, '0.3\% BER Target', color='b', fontsize=9)
plt.gca().set_xlim(xlim)
plt.xlabel('Time (years)')
plt.ylabel('Bit Error Rate (\%)')
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%d'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%s'))
plt.tight_layout()
plt.savefig('figs/ber-time-temp.eps')
plt.show()