# Note about files and experiments

## File format

writetest{n}.csv: experiment n write data
readtest{n}-prebake.csv: experiment n read data after writing, before baking
readtest{n}-postbake.csv: experiment n read data after writing and baking

## Relaxation Experiments:

relaxation-{pre/post}bake.csv: programmed 32 conductance levels from 17.5-250 uS, more precisely (17.5-25, 25-32.5, ..., 242.5-250, 250-inf), 80C for 30 minutes

## 3bpc Experiments

Experiment 1: 4.3 kOhm, 40-60 conductance writing, no adjustments, 80C for 30 minutes, 0.9% BER
Experiment 2: 4.3 kOhm, 45-55 conductance writing, no adjustments, 100C for 30 minutes, 2% BER, problems with level 5
Experiment 3: 4.3 kOhm, 45-55 conductance writing, adjusted level 5, 100C for 30 minutes, 0.5% BER
Experiment 4: 4.3 kOhm, 45-55 conductance writing, no additional adjustments, 120C for 30 minutes, 1.5% BER, problems with level 5-6
Experiment 5: 4.3 kOhm, 45-55 conductance writing, adjusted level 6 to be 35-45 conductance writing, 0.9% BER
Experiment 6: 4.3 kOhm, 45-55 conductance writing, adjustments as before + SBA adjustments, 0.5% BER, BEST RESULT!
Experiment 7: 4.3 kOhm, 45-55 conductance writing, all same as expt 6, 5k endurance cycles, 10% BER

## 2bpc Experiments
Experiment 1: 5 kOhm, SBA allocated conductance for both read/write, 157C for 30 minutes, 11.5% BER, problems with levels 1-3
Experiment 2: 5 kOhm, same as above (fixed conductance to be 40-60 with small adjustments), 127C for 30 minutes, 2.7% BER, problems with ranges 2 and 3 mostly
Experiment 3: 5 kOhm, same as above except pure 40-60, 127C for 30 minutes, 1.26% BER, problems with ranges 1 and 2 mostly
Experiment 4: 5 kOhm, same as above except read range reduced to 5.1 kOhm, SBA write range allocation, 127C for 30 minutes
Experiment 5: 5 kOhm, same as above except SBA write range allocation modified to be closer to 40-60 conductance for range 1, 0.3% BER
