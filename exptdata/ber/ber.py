import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

# Chip number
chipnum = 1

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
plt.figure(figsize=(3.5,3))
plt.title('Pulses Required for Target Error')
plt.xlabel('Mean Pulses Required')
plt.ylabel('Error (\%)')
colors = iter(plt.rcParams['axes.prop_cycle'].by_key()['color'][:3]*2)
styles = iter(['-']*3 + ['--']*3)
labels = iter(['ISPP', 'FPPV', 'SDCFC']*2)

# Load data
names = ['addr', 'nreads', 'nsets', 'nresets', 'rf', 'if', 'rlo', 'rhi', 'success', 'attempts1', 'attempts2']
if chipnum == 1:
    fnames = ['../ispp/data/ispp-4wl-eval-chip1-7-19-20.csv', '../fppv/data/fppv-4wl-eval-chip1-7-31-20.csv', '../sdr/data/sdr-4wl-eval-chip1-7-30-20.csv', '../ispp/data/ispp-wl0.070-bl5.00-5.00-sl5.00-5.00-7-24-20.csv', '../ispp/data/ispp-wl0.070-bl5.00-5.00-sl6.00-5.00-7-24-20.csv', '../sdr/data/sdr-wl0.070-bl5.00-5.00-sl5.00-5.00-7-24-20.csv']
for i, fname in enumerate(fnames):
    # Load and process/filter data
    data = pd.read_csv(fname, delimiter='\t', names=names, index_col=False)
    data['npulses'] = data['nsets'] + data['nresets'] - 1
    rlos = data['rlo'].unique()
    data['bin'] = data['rlo'].apply(lambda x: np.where(rlos == x)[0][0])
    data = data[data['bin'] != 7]

    # Sweep maxpulses
    pulses = []
    bers = []
    for maxpulses in sorted(data['npulses'].unique(), reverse=True):
        data['success'] = data['success'].astype(bool) & (data['npulses'] <= maxpulses)
        data['npulses'] = data['npulses'].clip(upper=maxpulses)
        pulses.append(data['npulses'].mean())
        bers.append(1-data['success'].mean())
    bers = np.array(bers)*100
    plt.semilogy(pulses, bers, color=next(colors), linestyle=next(styles), label=next(labels))

    # Create labels
    argerr = np.argmin(np.abs(bers - 1))
    print fname
    print pulses[argerr], bers[argerr]
    print pulses[argerr-1], bers[argerr-1]
    if i not in [1,3,4]:
        plt.annotate('%.2f' % pulses[argerr-1], xy=(pulses[argerr-1], 1), xytext=(pulses[argerr-1]+(10 if i==2 else -10), 2), arrowprops=dict(facecolor='black', shrink=0.1, width=1, headwidth=3, headlength=5), fontsize=11, horizontalalignment='center', verticalalignment='center')

# Plot BER
plt.semilogy([0, 90], [1, 1], ':', color='black')
plt.xlim(0, 90)
plt.xticks(list(plt.xticks()[0]) + [90])
plt.xlim(0, 90)
plt.ylim(0.5, 100)
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%d'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%d'))
handles, labels = plt.gca().get_legend_handles_labels()
leg1 = plt.legend(handles[:3], labels[:3], ncol=1, columnspacing=1, handletextpad=0.5, borderpad=0.2, prop={'size': 10}, loc='upper left', bbox_to_anchor=(1.02, 1), title='Before cycling')
plt.gca().add_artist(leg1)
leg2 = plt.legend(handles[3:6], labels[3:6], ncol=1, columnspacing=1, handletextpad=0.5, borderpad=0.2, prop={'size': 10}, loc='lower left', bbox_to_anchor=(1.02, 0), title='After 8k cycles')
plt.tight_layout()
plt.savefig('figs/ber.eps', bbox_extra_artists=[leg1, leg2], bbox_inches='tight')
plt.savefig('figs/ber.png', bbox_extra_artists=[leg1, leg2], bbox_inches='tight')
