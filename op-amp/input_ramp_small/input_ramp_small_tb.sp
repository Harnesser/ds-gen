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
vicm cm 0 DC='vcm'
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
  let vstart=(0-5mV)
  let vstop=(0+5mV)
  dc vinp $&vstart $&vstop 1u
  run

* DC Open-loop Gain
* take the derivative of the output voltage wrt the input voltage
* the maximum of this is the DC gain
  let op_deriv = deriv(op)
  let a_oldc = vecmax(op_deriv)

* Offset
* ideally, when the input is Vcm, the output should be Vcm too.
* find the input voltage for which the output voltage is Vcm.
* this voltage, minus the Vcm, is the offset
  meas dc vi_off find v(ip) when v(op)='vcm'
  let v_off = ( vi_off - 'vcm' )

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
  echo [MEASURE] : a_oldc :  DC Open-loop Gain : $&a_oldc : 
  echo [MEASURE] : v_off  :  Offset : $&v_off : V
.endc

.end
