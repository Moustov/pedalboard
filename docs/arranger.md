Arranger
===

The Arranger is a module used share a tempo between  
  * looper modules to ease loop synching
  * time effect pedals such as a delay, flanger, tremolo, drum simulator, ...
It also gathers mixed volumes from loopers


```plantuml
@startuml
title Arranger

allowmixing

sprite $part [16x16/16] {
FFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFF
FFFFFFFFFF0FFFFF
FFFFFFFFFF00FFFF
FF00000000000FFF
FF000000000000FF
FF00000000000FFF
FFFFFFFFFF00FFFF
FFFFFFFFFF0FFFFF
FFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFF
}

!define RECTANGLE class

component Arranger #lightblue {
  portin "tap tempo in"
  portin "mic tempo in"
  portin "bluetooth tempo in"
  portin "mixer sound in"
  portout "bluetooth tempo out"
  portout "mixed sound out"
  "bluetooth tempo in" --> "beat manager"
  "mic tempo in" --> "beat manager"
  "tap tempo in" --> "beat manager"
  "mixer sound in" --> "mixer" : N inputs
  "mixer" --> "mixed sound out"
  "beat manager" --> "bluetooth tempo out"
}
component Looper1
component Looper2
component "time effect pedal #1"
component "time effect pedal #2"
component Amplifier #red

"Instr." -->  "time effect pedal #1"
"time effect pedal #1" --> "time effect pedal #2": gen. sound
"time effect pedal #2" --> Looper1 : gen. sound
"time effect pedal #2" --> "other pedal" : gen. sound
"other pedal" --> Looper1 : gen. sound
Looper1 --> Looper2 : pass thru
Looper1 --> "mixer sound in" : gen. sound
Looper2 --> "mixer sound in" : gen. sound
"bluetooth tempo out" -..-> "time effect pedal #1" : beat
"bluetooth tempo out" -..-> "time effect pedal #2" : beat
"bluetooth tempo out" -..-> Looper2 : beat
"bluetooth tempo out" -..-> Looper1 : beat
"mixed sound out" =====> Amplifier : full sound
@enduml
```

