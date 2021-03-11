import matplotlib as mpl, numpy as np, pandas as pd, seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

# Chip number and bpc
chipnum = 1
bpc = 3

# LaTEX quality figures 
mpl.rcParams.update(
    {
    'text.usetex': True,
    'pgf.texsystem': 'lualatex',
    'pgf.rcfonts': True
    }
)
plt.rc('font', family='serif', serif='Times', size=13)

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



# Setup figure
plt.figure(figsize=(5,3))
plt.title('Pulse Count Distribution')
plt.xlabel('Programming Pulses')
plt.ylabel('Frequency')
colors = iter(plt.rcParams['axes.prop_cycle'].by_key()['color'][:3]*2)
styles = iter(['-']*3 + ['--']*3)
labels = iter(['ISPP', 'FPPV', 'RADAR']*2)

for i, fname in enumerate(fnames):
    # Load and process/filter data
    data = pd.read_csv(fname, delimiter='\t', names=names, index_col=False)
    data['npulses'] = data['nsets'] + data['nresets'] - 1
    rlos = data['rlo'].unique()
    data['bin'] = data['rlo'].apply(lambda x: np.where(rlos == x)[0][0])
    data = data[data['bin'] != (2**bpc - 1)]
    y, binedges = np.histogram(data['npulses'].clip(upper=275), bins=26)
    bincenters = 0.5*(binedges[1:]+binedges[:-1])
    plt.plot(bincenters, y, color=next(colors), linestyle=next(styles), label=next(labels))
plt.xlim(0, 275)
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%d'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%d'))
handles, labels = plt.gca().get_legend_handles_labels()
leg1 = plt.legend(handles[:3], labels[:3], ncol=1, columnspacing=1, handletextpad=0.5, borderpad=0.2, prop={'size': 10}, loc='upper left', bbox_to_anchor=(1.02, 1), title='Before cycling')
plt.gca().add_artist(leg1)
leg2 = plt.legend(handles[3:6], labels[3:6], ncol=1, columnspacing=1, handletextpad=0.5, borderpad=0.2, prop={'size': 10}, loc='lower left', bbox_to_anchor=(1.02, 0), title='After 8k cycles')
plt.tight_layout()
plt.savefig('figs/pulsedist.eps', bbox_extra_artists=[leg1, leg2], bbox_inches='tight')
plt.savefig('figs/pulsedist.pdf', bbox_extra_artists=[leg1, leg2], bbox_inches='tight')
plt.savefig('figs/pulsedist.png', bbox_extra_artists=[leg1, leg2], bbox_inches='tight')