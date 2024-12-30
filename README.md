Pedalboard project
===

# Version 1 - soundcard-based
```
@startuml soundboardBased

package "pedalboard" {
  "entrée pb" --> [pédal #1]
  [pédal #1] --> [pédal #2]
  [pédal #2] --> [looper]
  [looper] --> sortie_pb : "Signal traité"
}

node "Audient EVO 8" {
  "XLR IN (1)" --> [EVO 8] : "Signal micro"
  "INST IN (2)" --> [EVO 8] : "Signal guitare"
  [EVO 8] --> "OUT (mon 1)" : "Signal préamplifié"
}

node "Ampli" {
  "entrée ampli" --> [réglages]
  [réglages] --> "Haut Parleur"
}

[micro] --> "XLR IN (1)" : "Signal du micro"
"entrée guitare" --> "INST IN (2)" : "Signal de la guitare"
"OUT (mon 1)" --> "entrée pb"
sortie_pb --> "entrée ampli"
"Haut Parleur" --> audience

@enduml
```

# Version 2 - standalone
```
@startuml standalone


component "Ampli" {
  portin "entrée inst"
  "entrée inst" --> [réglages]
  [réglages] --> "Haut Parleur"
}


node "Triton Audio - FetHead" {

}

package "pedalboard" {
    component "BOSS LS-2" {
      portin "RETURN A"
      portin "RETURN B"
      portout "OUTPUT"
      "RETURN A" --> [switch]
      "RETURN B" --> [switch]
      [switch] --> "OUTPUT"
    }
  [pitch pedals] --> [tone producing pedals]
  [tone producing pedals] --> [tone modifying pedals]
  [tone modifying pedals] --> [sound copying pedals]
  [sound copying pedals] --> [ambience pedals]
  [ambience pedals] --> [looper pedals]
}

cloud audience{
}

[micro SHURE Beta 58A] -0-> "Triton Audio - FetHead"
 "Triton Audio - FetHead" --> "RETURN A" : "Signal du micro préamplifié"
"entrée guitare" --> "RETURN B" : "Signal de la guitare"
"OUTPUT" --> [pitch pedals]
[looper pedals] --> "entrée inst"
"Haut Parleur" ..> audience

@enduml
```



