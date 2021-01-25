import matplotlib as mpl, numpy as np, pandas as pd
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

# Setup figure
plt.figure(figsize=(5,3))
plt.title('Pulses Required for Target BER')
plt.xlabel('Mean Pulses Required')
plt.ylabel('Bit Error Rate (\%)')
colors = iter(plt.rcParams['axes.prop_cycle'].by_key()['color'][:3]*2)
styles = iter(['-']*3 + ['--']*3)
labels = iter(['ISPP', 'FPPV', 'RDCF']*2)

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
        data['success'] = data['success'].astype(bool) & (data['npulses'] <= maxpulses)
        data['npulses'] = data['npulses'].clip(upper=maxpulses)
        pulses.append(data['npulses'].mean())
        bers.append(1-data['success'].mean())
    bers = np.array(bers)*100
    plt.distplot(data['npulses'])
    plt.show()
