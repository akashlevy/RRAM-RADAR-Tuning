import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt


# Load data
names = ['addr', 'pw', 'blv', 'wlv', 'ri', 'rf']
stepsize = 0.01
fname = 'data/set-sweep-bl-200ns-perlev-7-23-20'
data = pd.read_csv(fname + '.csv', delimiter='\t', names=names)
for i, row in data.iterrows():
    if i != 0 and row['blv'] == 0:
        row = data.iloc[i-1].copy()
        while row['blv'] < 4:
            row['blv'] = row['blv'] + stepsize
            #print row
            data = data.append(row, ignore_index=True)
            #print data.iloc[-1]
        print i
data.to_csv(fname + '-augment.csv', sep='\t', index=False, header=False, float_format='%g')