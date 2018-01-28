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
Vmisc vmisc 0 DC='vdd'

* Inputs
vcm  cm 0 DC='vcm'
vinp ip cm DC=0
vinn im cm DC=0

* Load 
*Cload op 0 C='cload'
*Rload op 0 R='rload'


* Op-Amp Instantiation
Xdut vdd vss vmisc ip im op om opampwrapper

* Control Card
.control

* {KEEPS}

* Input sweep. Hold im low, and sweep ip
  let vstart=(0-'vcm')
  let vstop=(0+'vcm')
  dc vinp $&vstart $&vstop 1m
  run

* Minimum Output Voltage
  let voutmin = vecmin( v(op) )

* Maximum Output Voltage
  let voutmax = vecmax( v(op) )

* {PLOTS}
  wrdata plot v(op)-'vcm'

  if 0 
    plot v(ip) v(op)
    plot deriv(op)
    plot xdut.vbias3 xdut.vbias4
    plot v.xdut.vmeas#branch
    plot v.xdut.xamp.vmeas0#branch v.xdut.xamp.vmeas1#branch
  end

* Report
  echo [MEASURE] : voutmin : Minimum Output Voltage : $&voutmin : V
  echo [MEASURE] : voutmax : Maximum Output Voltage : $&voutmax : V
.endc

.end
