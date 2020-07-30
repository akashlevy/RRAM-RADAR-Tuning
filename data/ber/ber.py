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
fig, ax = plt.subplots(figsize=(4,3))
plt.title('Pulses Required for Target Error')
plt.xlabel('Mean Pulses Required')
plt.ylabel('Error (\%)')
plt.tight_layout()

# Load data
names = ['addr', 'nreads', 'nsets', 'nresets', 'rf', 'if', 'rlo', 'rhi', 'success', 'attempts1', 'attempts2']
if chipnum == 1:
    #fnames = ['../ispp/data/ispp-4wl-eval-chip1-6-6-20.csv', '../fppv/data/fppv-4wl-eval-chip1-6-6-20.csv', '../fppv/data/fppv-4wl-eval-chip1-6-6-20.csv', '../sdr/data/infopt/sdr-infopt-4wl-eval-chip1-6-8-20.csv']
    fnames = ['../ispp/data/ispp-4wl-eval-chip1-7-19-20.csv', '../fppv/data/fppv-wl0.070-bl5.80-sl0.30-0.30-7-19-20.csv', '../sdr/data/bl-opt/sdr-wl0.070-bl0.10-0.00-sl0.14-2.00-7-24-20.csv']
if chipnum == 2:
    fnames = ['../ispp/data/ispp-4wl-eval-chip2-6-17-20.csv', '../fppv/data/fppv-4wl-eval-chip2-6-17-20.csv', '../fppv/data/fppv-4wl-eval-chip2-6-17-20.csv', '../sdr/data/infopt/sdr-infopt-4wl-eval-chip2-6-17-20.csv', '../sdr/data/infopt/sdr-wl0.06-bl0.80-sl0.30-7.00-6-22-20-1k.csv', '../sdr/data/infopt/sdr-wl0.06-bl0.80-sl0.30-7.00-6-22-20-6k.csv', '../sdr/data/infopt/sdr-wl0.06-bl0.80-sl0.30-7.00-6-22-20-11k.csv', '../sdr/data/infopt/sdr-wl0.06-bl0.80-sl0.30-7.00-6-22-20-20k.csv', '../sdr/data/infopt/sdr-wl0.06-bl0.80-sl0.30-7.00-6-22-20.csv', '../ispp/data/ispp-wl0.06-bl0.80-sl0.30-7.00-6-22-20.csv']
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
    for maxpulses in range(5000, 0, -1):
        data['success'] = data['success'].astype(bool) & (data['npulses'] <= maxpulses)
        data['npulses'] = data['npulses'].clip(upper=maxpulses)
        pulses.append(data['npulses'].mean())
        bers.append(1-data['success'].mean())
    bers = np.array(bers)*100
    plt.semilogy(pulses, bers)

    # Create labels
    argerr = np.argmin(np.abs(bers - 1))
    print fname
    print pulses[argerr], bers[argerr]
    print pulses[argerr-1], bers[argerr-1]
    if i != 1:
        plt.annotate('%.2f' % pulses[argerr-1], xy=(pulses[argerr-1], bers[argerr-1]), xytext=(pulses[argerr-1]-20, 2), arrowprops=dict(facecolor='black', shrink=0.1, width=1, headwidth=3, headlength=5), fontsize=11, horizontalalignment='center', verticalalignment='center')

# Plot BER
plt.semilogy([0, 150], [1, 1], ':')
plt.legend(['ISPP', 'FPPV', 'SDCFC'], ncol=1, columnspacing=1, handletextpad=0.5, borderpad=0.2, prop={'size': 10})
plt.xlim(0, 150)
plt.ylim(0.5, 100)
ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
plt.tight_layout()
plt.show()
