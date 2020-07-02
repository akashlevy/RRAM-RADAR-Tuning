import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define CB size
cbsize = 32

# Load data
names = ['addr', 'nreads', 'nsets', 'nresets', 'rf', 'if', 'rlo', 'rhi', 'success', 'attempts1', 'attempts2']
data = pd.read_csv('data/writeispp.csv', delimiter='\t', names=names, index_col=False)
rlos = data['rlo'].unique()
print sorted(rlos)
data['bin'] = data['rlo'].apply(lambda x: np.where(rlos == x)[0][0])
data['rf'] = data['rf']/1000
data['g'] = 1/data['rf']

ranges = range(32)

# Conductance plot
plt.xlim(0, 0.3)
for i in ranges:
    rdata = data[data['bin'] == i]
    print i
    sns.distplot(rdata['g'],kde=False)
plt.show()

# Resistance plot
plt.xlim(0, 60)
for i in ranges:
    rdata = data[data['bin'] == i]
    print i
    sns.distplot(rdata['rf'],kde=False)
plt.show()


# Load data
names = ['rf']
data = pd.read_csv('data/readisppbake.csv', delimiter='\t', names=names, index_col=False)
data['rf'] = data['rf']/1000
data['g'] = 1/data['rf']
data['bin'] = ( data.index + data.index / cbsize ) % 32
print data

ranges = [0, 3, 5, 8, 12, 16, 20, 31]

# Conductance plot
for i in ranges:
    plt.xlim(0, 0.3)
    rdata = data[data['bin'] == i]
    print i
    sns.distplot(rdata['g'],kde=False, bins=int(np.ceil((rdata['g'].max() - rdata['g'].min())/0.002)))
plt.show()

# Resistance plot
plt.xlim(0, 60)
for i in ranges:
    rdata = data[data['bin'] == i]
    print i
    sns.distplot(rdata['rf'],kde=False, bins=5)
plt.show()


# Plot sigmas
data.groupby('bin')