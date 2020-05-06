import matplotlib as mpl, numpy as np, pandas as pd, pygmo as pg
import matplotlib.pyplot as plt

data = pd.read_csv('form-5-1-20.csv', delimiter='\t', names=['addr', 'wlv', 'blv', 'rf', 'success'])
data = data[data['wlv'] == 2]
data = data[data['blv'] >= 2.5]
data = data[data['blv'] <= 4]
data = data[data['rf'] < 15e3]
print data

# LaTEX quality figures 
mpl.rcParams.update(
    {
    'text.usetex': True,
    'pgf.texsystem': 'lualatex',
    'pgf.rcfonts': True,
    }
)
plt.rc('font', family='serif', serif='Times')

# Means of final resistance
rf = data['rf']/1000
rf.hist(figsize=(4,3))
plt.title('Post-FORMing Resistance Distribution')
plt.xlabel('Post-FORMing Resistance (k$\\Omega$)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('form-rf-hist.eps')
plt.show()

# Means of final resistance
blv = data['blv']
blv.hist(figsize=(4,3))
plt.title('FORMing BL Voltage Distribution')
plt.xlabel('BL Voltage (V)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('form-bl-hist.eps')
plt.show()
