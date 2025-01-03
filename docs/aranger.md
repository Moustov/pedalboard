Aranger
===

The Aranger is a module used share a tempo between  
  * looper modules to ease loop synching
  * time effect pedals such as a delay, flanger, tremolo, drum simulator, ...
It also gathers mixed volumes from loopers


```plantuml
@startuml
title Aranger

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

component Aranger
component Looper1
component Looper2
component "time effect pedal #1"
component "time effect pedal #2"

Guitar -->  "any pedal"
Mic -->  "any pedal"
"any pedal" --> "time effect pedal #1"
"time effect pedal #1" --> "time effect pedal #2": gen. sound
"time effect pedal #2" --> Looper1 : gen. sound
"time effect pedal #2" --> "other pedal" : gen. sound
"other pedal" --> Looper1 : gen. sound
Looper1 --> Looper2 : pass thru
Looper1 --> Aranger : gen. sound
Looper2 --> Aranger : gen. sound
Aranger --> "time effect pedal #1" : beat
Aranger --> "time effect pedal #2" : beat
Aranger --> Looper2 : beat
Aranger --> Looper1 : beat
Aranger =====> Amplifier : full sound
@enduml
```

