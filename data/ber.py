import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

# LaTEX quality figures 
mpl.rcParams.update(
    {
    'text.usetex': True,
    'pgf.texsystem': 'lualatex',
    'pgf.rcfonts': True
    }
)
plt.rc('font', family='serif', serif='Times', size=13)

# Setup figure
fig, ax = plt.subplots(figsize=(4,3))
plt.title('Pulses Required for Target Error')
plt.xlabel('Mean Pulses Required')
plt.ylabel('Error (\%)')
plt.tight_layout()

# Load SDR data
names = ['addr', 'nreads', 'nsets', 'nresets', 'rf', 'if', 'rlo', 'rhi', 'success', 'attempts1', 'attempts2']
fnames = ['ispp/data/ispp-eval-wl-6-3-20.csv', 'fppv/data/fppv-test.csv','sdr/data/option1/sdr-eval-wl-6-3-20.csv']
for fname in fnames:
    data = pd.read_csv(fname, delimiter='\t', names=names, index_col=False)
    data['npulses'] = data['nsets'] + data['nresets'] - 1
    rlos = data['rlo'].unique()
    data['bin'] = data['rlo'].apply(lambda x: np.where(rlos == x)[0][0])
    data = data[data['bin'] != 7]

    pulses = []
    bers = []
    for maxpulses in range(200, 0, -1):
        data['success'] = data['success'].astype(bool) & (data['npulses'] <= maxpulses)
        data['npulses'] = data['npulses'].clip(upper=maxpulses)
        pulses.append(data['npulses'].mean())
        bers.append(1-data['success'].mean())
        if maxpulses == 200:
            pulses.append(15)
            bers.append(1-data['success'].mean())
    plt.semilogy(pulses, np.array(bers)*100)

plt.semilogy([0, 15], [1, 1], ':')
plt.legend(['ISPP', 'FPPV', 'SDR'], ncol=1, columnspacing=1, handletextpad=0.5, borderpad=0.2, prop={'size': 11})
plt.xlim(2, 12)
plt.ylim(0.4, 100)
ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
plt.tight_layout()
plt.show()
