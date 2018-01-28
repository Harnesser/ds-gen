* Op-Amp in Inverting Amplifier Configuration Transient Sim
* to be included in auto-gen file

* Required
* .param vdd={VDD}
* .param vss={VSS}
* .param rload={RLOAD}
* .param cload={CLOAD}
* .lib {LIBPATH} {LIBNAME}
* .include 'opampwrapper.sp'

* set the input common mode voltage to mid-way between the supplies
.param vcm={ (vdd + vss ) / 2 }
.csparam vcm={vcm}

* Supply Lines
Vdd vdd 0 DC='vdd'
Vss vss 0 DC='vss'
Vmisc vmisc vss DC='vdd'

* Inputs
vinp ip 0 DC='vcm' ACMAG=1.0V ACPHASE=0.0

* Load 
*Cload op 0 C='cload'
*Rload op 0 R='rload'

* Feedback to put it in inverting amplifier configuration
Vfb op im DC=0V

* Op-Amp Instantiation
Xdut vdd vss vmisc ip im op om opampwrapper

* Control Card
.control

* {KEEPS}

  let delta = 0.010

* Input sweep. Hold im low, and sweep ip
  let vstart = ('vss')
  let vstop = ('vcm' + 1mV)
  dc vinp $&vstart $&vstop 1m

  let dv = deriv(op)
  meas dc v_ref FIND dv at='vcm'
  let bathtub = abs(dv - v_ref) - delta
  meas dc icmr_min WHEN bathtub=0.0 CROSS=LAST

  if 0
    plot op
    plot bathtub
  end

* Report
  echo [MEASURE] : icmr_min : Input Common Mode Minimum : $&icmr_min : V



* Input sweep. Hold im low, and sweep ip
  let vstart = ('vcm' - 1mV)
  let vstop = ('vdd')
  dc vinp $&vstart $&vstop 1m

  let dv = deriv(op)
  meas dc v_ref FIND dv at='vcm'
  let bathtub = abs(dv - v_ref) - delta
  meas dc icmr_max WHEN bathtub=0.0 CROSS=1
 
  if 0  
    plot op
    plot bathtub
  end

* Report
  echo [MEASURE] : icmr_max : Input Common Mode Maximum : $&icmr_max : V


* {PLOTS}
  let vstart = ('vss')
  let vstop = ('vdd')
  dc vinp $&vstart $&vstop 1m

  let i_vdd = -Vdd#branch

  let dv = deriv(op)
  meas dc v_ref FIND dv at='vcm'
  let bathtub = abs(dv - v_ref) - delta

  if 0
    plot v(ip) v(op)
    plot i_vdd
    plot bathtub
  end

  wrdata plot v(ip) v(op) i_vdd bathtub

.endc

.end
