import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt


# Load data
names = ['addr', 'pw', 'slv', 'wlv', 'ri', 'rf']
stepsize = 0.02
fname = 'data/reset-sweep-fine-step-0.02-6-7-20'
data = pd.read_csv(fname + '.csv', delimiter='\t', names=names)
for i, row in data.iterrows():
    if i != 0 and row['slv'] == 0:
        row = data.iloc[i-1].copy()
        while row['slv'] < 3:
            row['slv'] = row['slv'] + 0.02
            #print row
            data = data.append(row, ignore_index=True)
            #print data.iloc[-1]
        print i
data.to_csv(fname + '-augment.csv', sep='\t', index=False, header=False, float_format='%g')