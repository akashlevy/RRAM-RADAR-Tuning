import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt

# Load data
names = ['addr', 'nreads', 'nsets', 'nresets', 'rf', 'if', 'rlo', 'rhi', 'success', 'attempts1', 'attempts2']
data = pd.read_csv('data/infopt/sdr-wl0.06-bl0.80-sl0.30-7.00-6-22-20-11k.csv', delimiter='\t', names=names, index_col=False)
data['npulses'] = data['nsets'] + data['nresets']
#data = pd.read_csv('data/infopt/sdr-wl0.06-bl0.80-sl0.30-7.00-6-22-20-20k.csv', delimiter='\t', names=names, index_col=False)
#print "OverSET:", data[data['nresets'] >= 50].shape
#print "OverRESET:", data[data['nsets'] >= 50].shape

plt.xlim(50, 500)
data = data[data['npulses'] >= 50]
print (7900 * 4 + data['npulses'].sum())/8192
plt.hist(data['npulses'], bins=2000)
plt.show()