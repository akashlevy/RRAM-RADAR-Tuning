import matplotlib as mpl, numpy as np, pandas as pd, pygmo as pg
import matplotlib.pyplot as plt

data = pd.read_csv('map_expt4.csv', delimiter='\t', names=['addr', 'pw', 'blv', 'wlv', 'ri', 'rf'])
data = data[data['ri'] > 80e3]
#data = data[data['addr'] == 184]

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
for pw in data.pw.unique():
    if pw not in [200.]:
        continue
    pwdata = data[data['pw'] == pw]
    #grouped = pwdata.groupby(['blv', pd.cut(pwdata["wlv"], np.arange(2, 5, 0.2))])
    grouped = pwdata.groupby(['blv', 'wlv'])
    
    # # Means of final resistance
    means = grouped['rf'].mean()
    # means.unstack().plot(title='Mean Final Resistance @ PW = %sns' % pw, logy=False, yerr=grouped['rf'].std().unstack(), ylim=(1e3, 1e5))
    # plt.xlabel('BL Voltage (V)')
    # plt.ylabel('Mean Resistance (ohm)')
    # plt.show()

    stds = grouped['rf'].std()
    # stds.unstack().plot(title='Stdev Final Resistance @ PW = %sns' % pw, logy=False, ylim=(1e3, 1e5))
    # plt.xlabel('BL Voltage (V)')
    # plt.ylabel('Stdev Resistance (ohm)')
    # plt.show()
    
    # # Norm. dev. of resistance
    # normdevs = stds/means
    # normdevs.unstack().plot(title='Norm. Dev. Final Resistance @ PW = %sns' % pw, logy=True)
    # plt.xlabel('BL Voltage (V)')
    # plt.ylabel('Norm. Dev. Resistance (ohm)')
    # plt.show()

    # Stdev vs mean
    means, stds = means[means < 75e3], stds[means < 75e3]
    means, stds = means[means != 78116.337500], stds[means != 78116.337500]
    means, stds = means[means != 4004.749500], stds[means != 4004.749500]
    means, stds = means[means != 4187.557000], stds[means != 4187.557000]
    means, stds = means[means != 4813.380000], stds[means != 4813.380000]
    means, stds = means[means != 4575.902500], stds[means != 4575.902500]
    means, stds = means[means != 5376.480000], stds[means != 5376.480000]
    means, stds = means[(means < 4666.735000) | (means > 4666.737000)], stds[(means < 4666.735000) | (means > 4666.737000)]
    means, stds = means[(means < 16078.410666) | (means > 16078.410668)], stds[(means < 16078.410666) | (means > 16078.410668)]
    pareto = pg.non_dominated_front_2d(points=zip(-means, stds))
    pmeans, pstds = means[pareto], stds[pareto]
    print pd.concat([pmeans, pstds], axis=1)
    plt.figure(figsize=(4, 3))
    plt.title('Final Resistance $\\sigma$ vs. $\\mu$')
    plt.xlabel('Mean Resistance ($\\Omega$)')
    plt.ylabel('Stdev. Resistance ($\\Omega$)')
    plt.xlim(3e3, 80e3)
    plt.ylim(10, 80e3)
    plt.loglog(means, stds, '.', label="PW: %dns\nBL voltage: varied\nWL voltage: varied" % pw, color='0.2')
    plt.loglog(means[pareto], stds[pareto], '.', color='red', label="Pareto optimal conditions")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # # Stdev vs mean
    # plt.title('Norm. Dev. Resistance vs. Mean Final Resistance @ PW = %sns' % pw)
    # plt.xlabel('Mean Resistance (ohm)')
    # plt.ylabel('Norm. Dev. Resistance (ohm)')
    # plt.xlim(0, 50e3)
    # plt.ylim(0, 1)
    # plt.scatter(means, normdevs)
    # plt.show()
