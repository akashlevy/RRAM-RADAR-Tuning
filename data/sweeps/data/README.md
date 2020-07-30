# Note about file names

File name format: {set/reset}-sweep-{type}-{date}.csv

## Description of sweep types
- SET sweep with BL inner: this means that BL is swept in the inner loop and WL is swept in the outer loop. RESET is performed between each data point when resistance goes below 60 kOhm.
- SET sweep with WL inner: this means that WL is swept in the inner loop and BL is swept in the outer loop. RESET is performed between each data point when resistance goes below 60 kOhm.
- RESET sweep with SL inner: this means that SL is swept in the inner loop and SL is swept in the outer loop. SET is performed between each data point when resistance goes above 6.5 kOhm.
- RESET sweep with WL inner: this means that WL is swept in the inner loop and BL is swept in the outer loop. SET is performed between each data point when resistance goes above 6.5 kOhm.
- SET sweep ISPP: this means that WL is swept with fixed BL voltage. SET is NOT perofrmed between each data point.
- SET sweep BL fine: this means that BL is swept in the inner loop with provided step size and WL is iterated over the FPPV WL voltages. RESET is NOT performed between each data point.
- RESET sweep SL fine: this means that SL is swept in the inner loop with provided step size and WL is kept fixed (at 4V). SET is NOT performed between each data point.
