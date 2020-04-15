import matplotlib as mpl, numpy as np, pandas as pd, pygmo as pg
import matplotlib.pyplot as plt

data = pd.read_csv('sweep-4-14-20.csv', delimiter='\t', names=['addr', 'pw', 'blv', 'wlv', 'ri', 'rf'])
data = data[data['ri'] > 60e3]
data = data[data['blv'] == 3.3]
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
#for pw in data.pw.unique():
    #pwdata = data[data['pw'] == pw]
for _ in range(1):
    pwdata = data
    pw = 'bleh'
    # if pw == 100:
    #     pwdata = pwdata[pwdata['wlv'] >= 1.9]
    #     pwdata = pwdata[pwdata['wlv'] <= 2.6]
    # if pw == 200:
    #     pwdata = pwdata[pwdata['wlv'] >= 1.7]
    #     pwdata = pwdata[pwdata['wlv'] <= 2.15]
    # if pw == 300:
    #     pwdata = pwdata[pwdata['wlv'] >= 1.7]
    #     pwdata = pwdata[pwdata['wlv'] <= 2.0]
    grouped = pwdata.groupby(['wlv', pd.cut(pwdata["pw"], np.arange(0, 1000, 100))])
    
    # Means of final resistance
    means = grouped['rf'].mean()
    #means.plot(title='Mean Final Resistance @ PW = %sns' % pw, logy=False, ylim=(1e3, 1.5e5), yerr=grouped['rf'].std())
    means.unstack().plot(title='Mean Final Resistance @ PW = %sns' % pw, logy=False, ylim=(1e3, 1.6e5), yerr=grouped['rf'].std().unstack(), xlim=(1.7,2.6), linewidth=2, elinewidth=0.5)
    plt.xlabel('WL Voltage (V)')
    plt.ylabel('Mean Resistance (ohm)')
    plt.show()
