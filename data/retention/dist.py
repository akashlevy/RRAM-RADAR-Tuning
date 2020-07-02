import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define CB size
cbsize = 16

# Load data
names = ['addr', 'nreads', 'nsets', 'nresets', 'rf', 'if', 'rlo', 'rhi', 'success', 'attempts1', 'attempts2']
data = pd.read_csv('data/writeispp.csv', delimiter='\t', names=names, index_col=False)
data = data[data['rlo'] != 5260.0]
data = data[data['rlo'] != 5560.0]
data = data[data['rlo'] != 5880.0]
rlos = data['rlo'].unique()
print sorted(rlos)
data['bin'] = data['rlo'].apply(lambda x: np.where(rlos == x)[0][0])
#data['bin'] = 7 - ( data.index + data.index / cbsize ) % 8 + (data.index % 768) / 256 * 8
data['rf'] = data['rf']/1000
data['g'] = 1/data['rf']
#data = data.tail(1024)

# Conductance plot
plt.xlim(0, 0.25)
for i in range(20):
    rdata = data[data['bin'] == i]
    print i
    sns.distplot(rdata['g'],kde=False)
plt.show()

# Resistance plot
plt.xlim(0, 60)
for i in range(20):
    rdata = data[data['bin'] == i]
    print i
    sns.distplot(rdata['rf'],kde=False)
plt.show()


# Load data
names = ['rf']
data = pd.read_csv('data/readispp.csv', delimiter='\t', names=names, index_col=False)
data['rf'] = data['rf']/1000
data['g'] = 1/data['rf']
data = data.head(768*200)
data = data.tail(768)
data['bin'] = 7 - ( data.index + data.index / cbsize ) % 8 + (data.index % 768) / 256 * 8
print data

# Conductance plot
for i in [19, 17, 15, 13, 11, 8, 5, 0]:
    plt.xlim(0, 0.25)
    rdata = data[data['bin'] == i]
    print i
    sns.distplot(rdata['g'],kde=False)
plt.show()

# Resistance plot
plt.xlim(0, 60)
for i in [19, 17, 15, 13, 11, 8, 5, 0]:
    rdata = data[data['bin'] == i]
    print i
    sns.distplot(rdata['rf'],kde=False)
plt.show()
