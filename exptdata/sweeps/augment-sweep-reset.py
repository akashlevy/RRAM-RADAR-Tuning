import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt


# Load data
names = ['addr', 'pw', 'slv', 'wlv', 'ri', 'rf']
stepsize = 0.05
fname = 'data/reset-sweep-wl-200ns-step-0.05-7-30-20'
data = pd.read_csv(fname + '.csv', delimiter='\t', names=names)
for i, row in data.iterrows():
    if i != 0 and row['wlv'] == 2:
        row = data.iloc[i-1].copy()
        while row['wlv'] < 4:
            row['wlv'] = row['wlv'] + stepsize
            #print row
            data = data.append(row, ignore_index=True)
            #print data.iloc[-1]
        print i
data.to_csv(fname + '-augment.csv', sep='\t', index=False, header=False, float_format='%g')