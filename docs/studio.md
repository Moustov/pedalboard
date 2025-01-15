Studio Configuration
===

# Version 1 - soundcard-based
```plantuml
@startuml soundboardBased

package "Pedalboard" {
  "Pedalboard IN" --> [pedal #1]
  [pedal #1] --> [pedal #2]
  [pedal #2] --> [looper]
  [looper] --> "Pedalboard OUT" : "(processed signal)"
}

node "Audient EVO 8" {
  portin "EVO8 IN (1)"
  portin "EVO8 IN (2)"
  portout "EVO8 OUT (mon 1)"
  "EVO8 IN (1)" --> [EVO 8] 
  "EVO8 IN (2)" --> [EVO 8]
  [EVO 8] --> "EVO8 OUT (mon 1)" : "(preamped sig. - instr. level)"
}

node "Amplifier" {
  "amp. IN" --> [settings]
  [settings] --> "Speaker"
}

[Microphone] --> "EVO8 IN (1)" : "(mic level)"
"Guitar" --> "EVO8 IN (2)" : "(instr. level)"
"EVO8 OUT (mon 1)" --> "Pedalboard IN"
"Pedalboard OUT" --> "amp. IN"
"Speaker" ..> audience

@enduml
```

# Version 2 - standalone
```plantuml
@startuml standalone


component "Amplifier" {
  portin "Amplifier IN - inst"
  "Amplifier IN - inst" --> [settings]
  node "Speaker"
  [settings] --> "Speaker"
}

package "Pedalboard" {
    component "Joyo Line Selector" {
      portin "INPUT"
      portin "RETURN A"
      portin "RETURN B"
      portout "OUTPUT"
      portout "SEND A"
      portout "SEND B"
      "INPUT" --> [switch]
      "RETURN A" --> [switch]
      "RETURN B" --> [switch]
      [switch] --> "OUTPUT"
      [switch] --> "SEND A"
      [switch] --> "SEND B"
    }
  [pitch pedals] --> [tone producing pedals]
  [tone producing pedals] --> [tone modifying pedals]
  [tone modifying pedals] --> [sound copying pedals]
  [sound copying pedals] --> [ambience pedals]
  [ambience pedals] --> [looper pedals]
}
node "Guitar" 
actor audience

[micro SHURE Beta 58A] --> "RETURN A": "(dyn. mic. signal)"
[micro Prodipe ST-1MK2] --> "RETURN B": "(cond. mic. signal)"
"Guitar" --> "INPUT" : "(instr. level)"
"OUTPUT" --> [pitch pedals]
[looper pedals] --> "Amplifier IN - inst"
"Speaker" ..> audience

@enduml
```



