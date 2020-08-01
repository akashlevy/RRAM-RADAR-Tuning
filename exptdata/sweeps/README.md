# Sweeps

## The Sweep Types

### Fine SET Sweep

This is when the VWL is held fixed and the VBL is swept upwards. A coarse SET pulse is applied, and then the VWL is held at the same voltages used by FPPV.

### Fine RESET Sweep

This is when the VWL is held fixed and the VSL is swept upwards. The resistance starts from the LRS.

### ISPP WL Sweep

ISPP WL sweep holds the VBL fixed and the VWL is swept upwards. The resistance starts from the HRS.

### RESET WL Sweep

RESET WL sweep holds the VSL fixed and the VWL is swept upwards. The resistance starts from the LRS.

### FPPV WL Sweep

FPPV WL sweep is the same as ISPP WL sweep, except there is a reset between each step to emulate starting from HRS (range 7).

## Sweep Augmentation

In order to prevent premature cell burnout, when the resistance is too low or high, the sweep is stopped in the NI program. In order to compensate for this, augment-sweep-{type}.py will take a sweep and fill in the missing low/high resistances by copying the last value.

## Sigma-Mu

Looks at how the mean and standard deviation of resistance are related at every BL/WL/SL combination. Can produce a fit curve for doing sigma-based allocation.
