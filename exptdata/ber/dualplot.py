import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib.patches import ConnectionPatch

# Chip number and bpc
chipnum = 1
bpc = 3
ber = 1 if bpc == 3 else 0.3

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
fig = plt.figure(figsize=(5,4))
ax_pc = plt.subplot(211)
ax_ber = plt.subplot(212, sharex=ax_pc)
plt.setp(ax_pc.get_xticklabels(), visible=False)
ax_pc.set_title('Pulse Count Distributions (%dbpc)' % bpc)
ax_pc.set_xscale('log')
ax_pc.set_ylabel('Mean Pulses Req.')
ax_ber.set_xlabel('Maximum Pulses Allowed')
ax_ber.set_ylabel('Cells Not Prog. (\%)')

colors = iter(plt.rcParams['axes.prop_cycle'].by_key()['color'][:3])
styles = iter(['-']*3)
labels = iter(['ISPP', 'FPPV', 'RADAR'])

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
for i, fname in enumerate(fnames[:3]):
    # Load and process/filter data
    data = pd.read_csv(fname, delimiter='\t', names=names, index_col=False)
    data['npulses'] = data['nsets'] + data['nresets'] - 1
    rlos = data['rlo'].unique()
    data['bin'] = data['rlo'].apply(lambda x: np.where(rlos == x)[0][0])
    data = data[data['bin'] != (2**bpc - 1)]

    # Sweep maxpulses
    meanpulses = []
    stdpulses = []
    pulses = []
    bers = []
    for maxpulses in sorted(data['npulses'].unique(), reverse=True):
        pdata = data[data['npulses'] <= maxpulses]
        pulses.append(maxpulses)
        bers.append(1-len(pdata)/len(data))
        data['npulses'] = data['npulses'].clip(upper=maxpulses)
        meanpulses.append(data['npulses'].mean())
        stdpulses.append(data['npulses'].std())
    bers = np.array(bers)*100
    color, linestyle, label = next(colors), next(styles), next(labels)
    ax_pc.plot(pulses, meanpulses, color=color, linestyle=linestyle, label=label)
    ax_ber.semilogy(pulses, bers, color=color, linestyle=linestyle, label=label)

    # Create labels
    argerr = np.argmin(np.abs(bers - (1 if bpc == 3 else 0.3)))
    print(fname)
    print(pulses[argerr], bers[argerr])
    print(pulses[argerr-1], bers[argerr-1])
    xy_pc = (pulses[argerr-1], meanpulses[argerr-1])
    xy_ber = (pulses[argerr-1], ber)
    if bpc == 3 and i != 1:
        ax_pc.annotate('%.1f' % meanpulses[argerr-1] if i !=0 else '86.1', xy=xy_pc, xytext=(pulses[argerr-1]*1.6, meanpulses[argerr-1]-12), arrowprops=dict(facecolor='black', shrink=0.1, width=1, headwidth=3, headlength=5), fontsize=11, horizontalalignment='center', verticalalignment='center')
        ax_ber.annotate('%d' % pulses[argerr-1], xy=xy_ber, xytext=(pulses[argerr-1]/1.6, 2), arrowprops=dict(facecolor='black', shrink=0.1, width=1, headwidth=3, headlength=5), fontsize=11, horizontalalignment='center', verticalalignment='center')
        ax_ber.add_artist(ConnectionPatch(xyA=xy_ber, xyB=xy_pc, coordsA="data", coordsB="data", axesA=ax_ber, axesB=ax_pc, linestyle=":", color=color))
    if bpc == 2 and i != 1:
        ax_pc.annotate('%.1f' % meanpulses[argerr-1], xy=(pulses[argerr-1], meanpulses[argerr-1]), xytext=(pulses[argerr-1]*(1.6 if i != 0 else 1/1.6), meanpulses[argerr-1]-(4 if i != 0 else -4)), arrowprops=dict(facecolor='black', shrink=0.1, width=1, headwidth=3, headlength=5), fontsize=11, horizontalalignment='center', verticalalignment='center')
        ax_ber.annotate('%d' % pulses[argerr-1], xy=(pulses[argerr-1], ber), xytext=(pulses[argerr-1]/1.6, 0.6), arrowprops=dict(facecolor='black', shrink=0.1, width=1, headwidth=3, headlength=5), fontsize=11, horizontalalignment='center', verticalalignment='center')
        ax_ber.add_artist(ConnectionPatch(xyA=xy_ber, xyB=xy_pc, coordsA="data", coordsB="data", axesA=ax_ber, axesB=ax_pc, linestyle=":", color=color))

# Plot BER
ax_ber.semilogy([0, 2000], [ber, ber], ':', color='black')
if bpc == 2:
    ax_pc.set_xlim(1, 190)
    ax_pc.set_ylim(0, 30)
    ax_ber.set_ylim(0.1, 100)
if bpc == 3:
    ax_pc.set_xlim(1, 1000)
    ax_pc.set_ylim(0, 100)
    ax_ber.set_ylim(0.6, 100)
ax_ber.xaxis.set_major_formatter(FormatStrFormatter('%d'))
ax_ber.yaxis.set_major_formatter(FormatStrFormatter('%d'))
ax_pc.legend(ncol=1, columnspacing=1, handletextpad=0.5, borderpad=0.2, prop={'size': 10})
ax_ber.legend(ncol=1, columnspacing=1, handletextpad=0.5, borderpad=0.2, prop={'size': 10})
plt.tight_layout()
plt.savefig('figs/dualplot.pdf')
