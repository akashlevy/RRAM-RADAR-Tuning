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
    means, stds = means[means < 80e3], stds[means < 80e3]
    pareto = pg.non_dominated_front_2d(points=zip(1/means, stds))
    pmeans, pstds = means[pareto], stds[pareto]
    print pd.concat([pmeans, pstds], axis=1)
    fit1 = np.polyfit(np.log(pmeans[means < 5e3]), np.log(pstds[means < 5e3]), 1)
    fit2 = np.polyfit(np.log(pmeans[means > 5e3]), np.log(pstds[means > 5e3]), 1)
    plt.figure(figsize=(4, 3))
    plt.title('Final Resistance $\\sigma$ vs. $\\mu$')
    plt.xlabel('Mean Resistance ($\\Omega$)')
    plt.ylabel('Stdev. Resistance ($\\Omega$)')
    plt.xlim(3e3, 80e3)
    plt.ylim(50, 80e3)
    plt.loglog(means, stds, '.', label="PW: %dns\nBL voltage: varied\nWL voltage: varied" % pw, color='0.2')
    plt.loglog(means[pareto], stds[pareto], '.', color='red', label="Pareto optimal conds")
    x = np.exp(np.linspace(np.log(4e3), np.log(5.5e3)))
    plt.loglog(x, np.exp(fit1[0] * np.log(x) + fit1[1]), '--', color='green', label="Low resistance fit")
    x = np.exp(np.linspace(np.log(5.5e3), np.log(80e3)))
    plt.loglog(x, np.exp(fit2[0] * np.log(x) + fit2[1]), '--', color='blue', label="High resistance fit")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Print results
    for x in np.linspace(4e3, 80e3, num=80-4+1):
        fit = fit1 if x < 5.5e3 else fit2
        print np.exp(fit[0] * np.log(x) + fit[1])

    # # Stdev vs mean
    # plt.title('Norm. Dev. Resistance vs. Mean Final Resistance @ PW = %sns' % pw)
    # plt.xlabel('Mean Resistance (ohm)')
    # plt.ylabel('Norm. Dev. Resistance (ohm)')
    # plt.xlim(0, 50e3)
    # plt.ylim(0, 1)
    # plt.scatter(means, normdevs)
    # plt.show()
