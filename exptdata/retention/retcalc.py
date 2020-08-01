import numpy as np

# Constants
Ea = 2.25 # eV
kB = 8.617333262E-5 # eV/K
month2sec = 2.628e6

t0_fn = lambda tf, T: tf * np.exp(-Ea / (kB * T)) # s
T_fn = lambda tf, t0: Ea / (kB * np.log(tf/t0)) # K
tf_fn = lambda T, t0: t0 * np.exp(-Ea / (kB * T)) # s

'''
Computes an equivalent retention time or temperature (tf2 or T2)
based on the reference retention time and temperature and specification
of one of the targets
'''
def equivalent_tf_T(tf1, T1, tf2=None, T2=None):
    t0 = t0_fn(tf1, T1)
    if tf2 is not None and T2 is not None:
        raise Exception('Both time and temperature target specified!')
    elif tf2 is not None:
        T2 = T_fn(tf2, t0)
        return T2
    elif T2 is not None:
        tf2 = tf_fn(T2, t0)
        return tf2
    else:
        raise Exception('Either time or temperature target must be specified!')

if __name__ == "__main__":
    targets = [
        (10 * 12 * month2sec, 273 + 25, 30 * 60), # 10 years retention at RT (25C), 30 min bake
        (10 * 12 * month2sec, 273 + 40, 30 * 60), # 10 years retention at 40C, 30 min bake
        (10 * 12 * month2sec, 273 + 65, 30 * 60), # 10 years retention at 65C, 30 min bake
        (10 * 12 * month2sec, 273 + 85, 30 * 60), # 10 years retention at 85C, 30 min bake
        (3 * month2sec, 273 + 70, 30 * 60), # 3 months retention at 70C, 30 min bake
        (3 * month2sec, 273 + 85, 30 * 60), # 3 months retention at 85C, 30 min bake
        ]
    for target in targets:
        tf1, T1, tf2 = target
        T2 = equivalent_tf_T(tf1, T1, tf2)
        if tf1 >= 12 * month2sec:
            nums = (tf1/(month2sec*12), T1-273, tf2/60, tf2%60, T2-273)
            print('For %s years @ %sC: bake for %sm %ss @ %.3fC' % nums)
        else:
            nums = (tf1/month2sec, T1-273, tf2/60, tf2%60, T2-273)
            print('For %s months @ %sC: bake for %sm %ss @ %.3fC' % nums)