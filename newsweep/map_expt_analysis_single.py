import matplotlib as mpl, numpy as np, pandas as pd, pygmo as pg
import matplotlib.pyplot as plt

data = pd.read_csv('sweep-main.csv', delimiter='\t', names=['addr', 'pw', 'blv', 'wlv', 'ri', 'rf'])
data = data[data['ri'] > 60e3]
data = data[data['blv'] >= 3.8]
print data

# TODO: make pwl fit to optimal condition based on binned minimums

# LaTEX quality figures 
mpl.rcParams.update(
    {
    'text.usetex': True,
    'pgf.texsystem': 'lualatex',
    'pgf.rcfonts': True,
    }
)
plt.rc('font', family='serif', serif='Times')

# PW/WL/BL plots
for pw in data.pw.unique():
    pwdata = data[data['pw'] == pw]
    if pw == 100:
        pwdata = pwdata[pwdata['wlv'] >= 1.9]
        pwdata = pwdata[pwdata['wlv'] <= 2.6]
    if pw == 200:
        pwdata = pwdata[pwdata['wlv'] >= 1.7]
        pwdata = pwdata[pwdata['wlv'] <= 2.3]
        continue
    grouped = pwdata.groupby(['wlv', pd.cut(pwdata["addr"], np.arange(1, 12, 1))])
    
    # Means of final resistance
    means = grouped['rf'].mean()
    means.unstack().plot(title='Mean Final Resistance @ PW = %sns' % pw, logy=False, ylim=(1e3, 1.5e5)) #, yerr=grouped['rf'].std().unstack())
    plt.xlabel('WL Voltage (V)')
    plt.ylabel('Mean Resistance (ohm)')
    plt.show()
