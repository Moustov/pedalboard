Architecture
===

# Standalone instr. version
The looper can be in different flavors: instrument or microphone.
The mic version should include a 48V phantom power supply.

> __NOTE__
> 
> To spare DAC, Raspberry and extra casing, an input mixer/preamp realised with a simple opamp could be added.

The RaspberryPi component hosts many features :
* managing loops (start, stop, erase, overdub, ...)
* applying sound effects (delay, reverb, distortion, ...)
* generating a metronome beep

```plantuml
@startuml
title Standalone instr. version
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

component Looper {
    portin looper_jack_in
    portout looper_jack_out
    
    RECTANGLE RaspberryPi <<$part>> {
        + Ref part: Raspberry Pi Zero
        + OS: Raspbian        
    }
    
    RECTANGLE DAC/ADC  <<$part>> {
        + Ref part: HifiBerry DAC+ ADC
        + Type: DAC/ADC HiFi
    }
    
    RECTANGLE "instr2Hifi preamp"  <<$part>> {
        + see [**electronic level.md**]
    }
    
    RECTANGLE "hifi2instr preamp"  <<$part>> {
        + see [**electronic level.md**]
    }

    looper_jack_in --> "instr2Hifi preamp"
    "instr2Hifi preamp" --> DAC : HiFi
    DAC --> "hifi2instr preamp" : HiFi
    DAC <--> RaspberryPi : I2S Connexion
    "hifi2instr preamp" --> looper_jack_out : instr.
}

note right of Looper
    Can be adapted to a mic
    with XLR and instr2Hifi preamp settings 
end note

RECTANGLE Guitar  <<$part>> 
RECTANGLE Amplifier  <<$part>>

Guitar -->  looper_jack_in : instr.
note right of Guitar
    Can be a mic
end note
"looper_jack_out" --> Amplifier : instr.

@enduml
```


# Multitrack version
This version enables multitracking that can be run or paused separately.

The connection between loopers modules requires robust mechanical links to firmly chain modules.
The connection can be used to:
* enable a unique link to an amplifier - therefore mixing capabilities must be added to each module
* a [Arranger](arranger.md) could be used to share a tempo between  
  * looper modules to ease loop synching
  * time effect pedals such as a delay, flanger, tremolo, drum simulator, ...

```plantuml
@startuml
title Multitrack version

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

component Looper_channel1 {
    portin looper_jack_in
    portin looper_rca_in
    portout looper_jack_out
    portout looper_rca_out
    
    RECTANGLE RaspberryPi <<$part>> {
        + Ref part: Raspberry Pi Zero
        + OS: Raspbian        
    }
    
    RECTANGLE DAC/ADC  <<$part>> {
        + Ref part: HifiBerry DAC+ ADC
        + Type: DAC/ADC HiFi
    }
    
    RECTANGLE "instr2Hifi preamp"  <<$part>> {
        + see [**electronic level.md**]
    }
    
    RECTANGLE "hifi2instr preamp"  <<$part>> {
        + see [**electronic level.md**]
    }

    RECTANGLE "mixer"  <<$part>> {
        + see [**mixer.md**]
        + potentiometer to define mixing level
    }
    looper_rca_in --> mixer : instr.
    "hifi2instr preamp" --> mixer : instr.
    looper_jack_in --> "instr2Hifi preamp"
    "instr2Hifi preamp" --> DAC : HiFi
    DAC --> "hifi2instr preamp" : HiFi
    DAC <--> RaspberryPi : I2S Connexion
    "hifi2instr preamp" --> looper_jack_out : instr.
}

note right of Looper_channel1
    Can be adapted to a mic
    with XLR and instr2Hifi preamp settings 
end note


component Looper_channel2 {
    portin looper_xlr_in_2
    portin looper_rca_in_2
    portout looper_jack_out_2
    portout looper_rca_out_2
}

RECTANGLE Amplifier  <<$part>>

Guitar -->  looper_jack_in : instr.
note right of Guitar
    Can be a mic
end note
"looper_jack_out" --> Amplifier : instr.

mic --> looper_xlr_in_2
looper_rca_out_2 --> looper_rca_in

@enduml
```


# Wireless version
Beside the pedals before the looper system, both multitracks and [arranger](arranger.md) can communicate through wireless protocols:
* WiFi for the sound: 
  * Bandwidth Required: Approximately 9.216 Mbps for a 24-bit, 192 kHz stereo audio signal.
  * The maximum theoretical data rate for 802.11n can reach up to 600 Mbps on the Raspberry Pi Zero 2 W
* Bluetooth for time synching
  * Maximum Theoretical Bandwidth: Bluetooth 5.0 can achieve data rates of up to 2 Mbps on the Raspberry Pi Zero 2 W

This wireless version would then enable each musician to control their own loops and effects, the arranger could then be split into
* a mixing module (for the sound engineer to control the balance)
* a drum module (for the drummer to set the tempo at start - an internal mic would listen to the sticks start and time signature or something like that...)