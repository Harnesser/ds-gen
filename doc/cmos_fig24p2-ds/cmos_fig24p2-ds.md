# Datasheet for `cmos_fig24p2`
## Measurements
 
| Measurement | Min. | Avg. | Max. | Unit |
| --- | --- | --- | --- | --- |
| [Offset][v_off] | -0.000146 | 7.12e-05 | 0.000364 | V |
| [DC Open-loop Gain][a_oldc] | 9.02e+02 | 1e+03 | 1.09e+03 |  |
| [Minimum Output Voltage][voutmin] | 0.000185 | 0.000337 | 0.000554 | V |
| [Maximum Output Voltage][voutmax] | 0.89 | 0.992 | 1.09 | V |
| [3dB Gain Frequency][f_3db] | 9.5e+03 | 1.02e+04 | 1.08e+04 | Hz |
| [Unity Gain Frequency][f_0db] | 9.25e+06 | 9.79e+06 | 1.04e+07 | Hz |
| [DC Gain][dc_gain] | 58.7 | 59.6 | 60.5 | dBV |
| [Phase Margin][phase_margin] | 93.6 | 94.7 | 95.9 | deg |
| [Input Common Mode Minimum][icmr_min] | 0.381 | 0.403 | 0.423 | V |
| [Input Common Mode Maximum][icmr_max] | 0.747 | 0.882 | 1.01 | V |
 

## Regression: VT Analysis of offset or something


Number of testcases: 9


| Parameter | Values |
| --- | --- |
| Supply Voltage | 0.9; 1.0; 1.1 |
| Temperature | 0; 25; 80 |

## Configuration
  
   [v_off]: input_ramp_small/input_ramp_small-ds.html#v_off "Offset"
   [a_oldc]: input_ramp_small/input_ramp_small-ds.html#a_oldc "DC Open-loop Gain"
   [voutmin]: input_ramp_large/input_ramp_large-ds.html#voutmin "Minimum Output Voltage"
   [voutmax]: input_ramp_large/input_ramp_large-ds.html#voutmax "Maximum Output Voltage"
   [f_3db]: open_loop_freq/open_loop_freq-ds.html#f_3db "3dB Gain Frequency"
   [f_0db]: open_loop_freq/open_loop_freq-ds.html#f_0db "Unity Gain Frequency"
   [dc_gain]: open_loop_freq/open_loop_freq-ds.html#dc_gain "DC Gain"
   [phase_margin]: open_loop_freq/open_loop_freq-ds.html#phase_margin "Phase Margin"
   [icmr_min]: input_common_mode_range/input_common_mode_range-ds.html#icmr_min "Input Common Mode Minimum"
   [icmr_max]: input_common_mode_range/input_common_mode_range-ds.html#icmr_max "Input Common Mode Maximum"