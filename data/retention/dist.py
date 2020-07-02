import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define CB size
cbsize = 32
nranges = 8

# Load data
names = ['addr', 'nreads', 'nsets', 'nresets', 'rf', 'if', 'rlo', 'rhi', 'success', 'attempts1', 'attempts2']
data = pd.read_csv('data/writeispp-testrange.csv', delimiter='\t', names=names, index_col=False)
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
data = pd.read_csv('data/readispp-testrange.csv', delimiter='\t', names=names, index_col=False)
data['rf'] = data['rf']/1000
data['g'] = 1/data['rf']
data['bin'] = ( data.index + data.index / cbsize ) % nranges
print data

ranges = range(8) #[1, 3, 5, 7, 10, 13, 18, 31]

# Conductance plot
for i in ranges:
    plt.xlim(0, 0.3)
    rdata = data[data['bin'] == i]
    print i
    sns.distplot(rdata['g'],kde=False)
plt.show()

# Resistance plot
plt.xlim(0, 60)
for i in ranges:
    rdata = data[data['bin'] == i]
    print i
    sns.distplot(rdata['rf'],kde=False, bins=5)
plt.show()


# Plot sigmas
data = data[data['bin'] <= 19]
data = data[data['bin'] > 0]
bindata = data.groupby('bin')
means, stds = bindata['rf'].mean()*1000, bindata['rf'].std()*1000

n = 2
fit = np.polyfit(means, stds, n)
print tuple(fit)
x = np.linspace(4300, 12000)
y = list(np.sum(np.array([fit[n-i] * x**i for i in range(n+1)]), axis=0))

plt.semilogy(means, stds)
plt.semilogy(x, y)
plt.show()