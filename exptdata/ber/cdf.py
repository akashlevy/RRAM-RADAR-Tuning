import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

# Chip number and bpc
chipnum = 1
bpc = 2

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
plt.figure(figsize=(5,3))
plt.title('Pulse Count CDF (%dbpc)' % bpc)
plt.xlabel('Mean Pulse Count')
plt.ylabel('CDF (\%)')
colors = iter(plt.rcParams['axes.prop_cycle'].by_key()['color'][:3]*2)
styles = iter(['-']*3 + ['--']*3)
labels = iter(['ISPP', 'FPPV', 'RADAR']*2)

# Load data
names = ['addr', 'nreads', 'nsets', 'nresets', 'rf', 'if', 'rlo', 'rhi', 'success', 'attempts1', 'attempts2']
if chipnum == 1:
    if bpc == 2:
        fnames = ['../ispp/data/2bpc/ispp-4wl-eval-chip1-8-5-20.csv', '../fppv/data/2bpc/fppv-4wl-eval-chip1-8-7-20.csv', '../sdr/data/2bpc/sdr-4wl-eval-chip1-8-7-20.csv', '../ispp/data/2bpc/ispp-4wl-eval-chip1-8k-8-9-20.csv', '../fppv/data/2bpc/fppv-4wl-eval-chip1-8k-8-9-20.csv', '../sdr/data/2bpc/sdr-4wl-eval-chip1-8k-8-9-20.csv']
    if bpc == 3:
        fnames = ['../ispp/data/3bpc/ispp-4wl-eval-chip1-7-19-20.csv', '../fppv/data/3bpc/fppv-4wl-eval-chip1-7-31-20.csv', '../sdr/data/3bpc/sdr-4wl-eval-chip1-7-30-20.csv', '../ispp/data/3bpc/ispp-4wl-eval-chip1-8k-7-31-20.csv', '../fppv/data/3bpc/fppv-4wl-eval-chip1-8k-7-31-20.csv', '../sdr/data/3bpc/sdr-4wl-eval-chip1-8k-7-31-20.csv']
if chipnum == 2:
    if bpc == 2:
        fnames = ['../ispp/data/2bpc/ispp-4wl-eval-chip2-8-9-20.csv', '../fppv/data/2bpc/fppv-4wl-eval-chip2-8-9-20.csv', '../sdr/data/2bpc/sdr-4wl-eval-chip2-8-9-20.csv', '../ispp/data/2bpc/ispp-4wl-eval-chip2-8k-8-9-20.csv', '../fppv/data/2bpc/fppv-4wl-eval-chip2-8k-8-9-20.csv', '../sdr/data/2bpc/sdr-4wl-eval-chip2-8k-8-9-20.csv']
    if bpc == 3:
        fnames = ['../ispp/data/3bpc/ispp-4wl-eval-chip2-8-9-20.csv', '../fppv/data/3bpc/fppv-4wl-eval-chip2-8-9-20.csv', '../sdr/data/3bpc/sdr-4wl-eval-chip2-8-9-20.csv', '../ispp/data/3bpc/ispp-4wl-eval-chip2-8k-8-9-20.csv', '../fppv/data/3bpc/fppv-4wl-eval-chip2-8k-8-9-20.csv', '../sdr/data/3bpc/sdr-4wl-eval-chip2-8k-8-9-20.csv']
for i, fname in enumerate(fnames):
    # Load and process/filter data
    data = pd.read_csv(fname, delimiter='\t', names=names, index_col=False)
    data['npulses'] = data['nsets'] + data['nresets'] - 1
    rlos = data['rlo'].unique()
    data['bin'] = data['rlo'].apply(lambda x: np.where(rlos == x)[0][0])
    data = data[data['bin'] != (2**bpc - 1)]

    # Sweep maxpulses
    pulses = []
    bers = []
    for maxpulses in sorted(data['npulses'].unique(), reverse=True):
        pdata = data[data['npulses'] <= maxpulses]
        pulses.append(maxpulses)
        bers.append(len(pdata)/len(data))
    bers = np.array(bers)*100
    plt.plot(pulses, bers, color=next(colors), linestyle=next(styles), label=next(labels))

# Plot BER
if bpc == 2:
    plt.xlim(0, 100)
    plt.ylim(90, 100)
if bpc == 3:
    plt.xlim(0, 100)
    plt.ylim(0, 100)
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%d'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%d'))
handles, labels = plt.gca().get_legend_handles_labels()
leg1 = plt.legend(handles[:3], labels[:3], ncol=1, columnspacing=1, handletextpad=0.5, borderpad=0.2, prop={'size': 10}, loc='upper left', bbox_to_anchor=(1.02, 1), title='Before cycling')
plt.gca().add_artist(leg1)
leg2 = plt.legend(handles[3:6], labels[3:6], ncol=1, columnspacing=1, handletextpad=0.5, borderpad=0.2, prop={'size': 10}, loc='lower left', bbox_to_anchor=(1.02, 0), title='After 8k cycles')
plt.tight_layout()
plt.savefig('figs/cdf.eps', bbox_extra_artists=[leg1, leg2], bbox_inches='tight')
plt.savefig('figs/cdf.pdf', bbox_extra_artists=[leg1, leg2], bbox_inches='tight')
plt.savefig('figs/cdf.png', bbox_extra_artists=[leg1, leg2], bbox_inches='tight')
