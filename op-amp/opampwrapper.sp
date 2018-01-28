.subckt opampwrapper vdd vss vmisc ip im op om
* vdd - op-amp supply voltage
* vss - op-amp negative or gnd rail
* vmisc - supply for any bias ccts
* ip - positive input
* im - negative input
* op - positive output
* om - negative output

* bias generators, etc
Xbias vmisc vss ...

* Amplifier under test
Xamp vdd vss ...

.ends
