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
.param vcm={ (vdd + vss) / 2 }
.csparam vcm={vcm}


* Supply Lines
Vdd vdd 0 DC='vdd'
Vss vss 0 DC='vss'
Vmisc vmisc 0 DC='vdd'

* Inputs
vinp ip 0 DC='vcm' ACMAG=1.0V ACPHASE=0
*vinn im 0 DC='vcm' ACMAG=0.0V ACPHASE=0

* Load 
Cload op 0 C='cload'
*Rload op 0 R='rload'

* Feedback
Rf op im R=100meg
Cf im 0 C=10u

* Op-Amp Instantiation
Xdut vdd vss vmisc ip im op om opampwrapper

* Control Card
.control

* {KEEPS}

* Frequency Sweep
  ac dec 10 1 1G

* DC Gain
  meas ac dc_gain find vdb(op) at=1
  set dc_gain = "$&dc_gain"

* Unity Gain Frequency
  meas ac f_unity when vdb(op)=0.0
  set f_unity = "$&f_unity"

* 3dB Frequency
  let bw_mag = dc_gain - 3.0
  set bw_mag = "$&bw_mag"
  echo $bw_mag
  meas ac f_3db when vdb(op)=bw_mag
  set f_3db = "$&f_3db"

* Phase Margin
  meas ac ph_unity_rads find vp(op) at=f_unity
  let phase_margin_deg = ( ph_unity_rads * 180 / 3.1416 ) - (-180.0)
  settype phase phase_margin_deg
  set phase_margin_deg = "$&phase_margin_deg"

* {PLOTS}
  let vph_deg = vp(op) * 180 / 3.1416
  settype phase vph_deg
  wrdata plot vdb(op) vph_deg

  if 0 
    plot vdb(op)
    plot vph_deg
  end

* Report
  echo [MEASURE] : dc_gain : DC Gain : $dc_gain : dBV
  echo [MEASURE] : f_3db : 3dB Frequency : $f_3db : Hz
  echo [MEASURE] : f_0db : Unity Gain Frequency : $f_unity : Hz
  echo [MEASURE] : phase_margin : Phase Margin : $phase_margin_deg : deg

.endc

.end
