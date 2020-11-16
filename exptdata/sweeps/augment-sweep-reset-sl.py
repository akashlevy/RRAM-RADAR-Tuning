import matplotlib as mpl, numpy as np, pandas as pd
import matplotlib.pyplot as plt


# Load data
names = ['addr', 'pw', 'slv', 'wlv', 'ri', 'rf']
stepsize = 0.05
fname = 'data/reset-sweep-sl-200ns-step-%.2f-9-21-20' % stepsize
data = pd.read_csv(fname + '.csv', delimiter='\t', names=names).to_dict('records')
for i, row in enumerate(data):
    if i != 0 and row['slv'] == 0:
        row = data[i-1]
        while row['slv'] < 4:
            row = row.copy()
            row['slv'] = row['slv'] + stepsize
            data.append(row)
        print i
data = pd.DataFrame.from_records(data, columns=names)
data.to_csv(fname + '-augment.csv', sep='\t', index=False, header=False, float_format='%g')