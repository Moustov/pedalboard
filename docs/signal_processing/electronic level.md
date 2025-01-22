²Signals caracteristics
===
# Signal types
## Musical Instrument Signal
* **Signal Type**: Generally analog ([amplitude modulation](https://en.m.wikipedia.org/wiki/Amplitude_modulation)).
* **Signal Level**:
  * *Electric Guitar*: Approximately -10 dBV to -20 dBV.
  * *Microphone*: Typically around -60 dBV to -40 dBV (for dynamic microphones).
* **Impedance**:
  * *Guitar*: About 10 kΩ to 20 kΩ (high impedance).
  * *Microphone*: Ranges from 150 Ω to 600 Ω (low impedance).
* **Frequency Response**:
        Varies by instrument, typically from 20 Hz to 20 kHz for acoustic instruments.
* **Signal Characteristics**:
        Can exhibit significant dynamic range variations, with peaks during loud play.
        Often requires a preamplifier to boost the signal level before further processing.

![guitar electric levels](guitar%20signal%20level.png)

This signal shows something around +/- 100mV

To handle such signal, sound cards such as
* M-Audio M-Track Duo
* Behringer UMC22
Those cards are audio USB "class compliant".

The other way is to use a DAC/ADC Raspberry hat for signal processing, with some preamp to adjust electric levels.

## Hi-Fi Audio Signal
* **Signal Type**: Generally analog (amplitude modulation), but can also be digital (in modern systems).
* **Signal Level**:
  * *Line Level*: Approximately +4 dBu for professional equipment and -10 dBV for consumer equipment.
* *Impedance**:
        Hi-Fi Equipment: Ranges from about 1 kΩ to 10 kΩ (high impedance for inputs).
* **Frequency Response**:
        Typically from 20 Hz to 20 kHz, but can extend to 40 kHz or more for high-fidelity systems.
* *Signal Characteristics**:
        Less subject to extreme dynamic range variations.
        Designed for faithful sound reproduction, with a high signal-to-noise ratio.

![audio electric levels](audio%20signal%20level%20-%20RCA.png)

The signal sent on a jack 3.5mm (headphones) shows something around +/- 8V

To handle such signal, Raspberry cards such as [Hifiberry DAC+ ADC](https://www.hifiberry.com/docs/data-sheets/datasheet-dac-adc/).
This reference has been chosen since it provides:
- both Analog to digital and digital to analog converters (ADC + DAC)
- 24 bits + 192 kHz sampling characteristics
- compatibility with [Rasperry OS](https://www.raspbian.org/) (Raspberry Pi Linux kernel of at least version 4.19.60) and [sounddevice](https://pypi.org/project/sounddevice/) python library or [PortAudio](https://www.portaudio.com/) for C code

# Signal transformation
Here are some specific electronic component references that can be used for converting between instrument signals and Hi-Fi signals:
   * **TL072**: A low-noise JFET-input operational amplifier, commonly used in audio applications. Good for general applications, but may have slightly lower performance in terms of noise and distortion compared to the OPA2134PA.
   * **OPA2134**: A high-performance audio op-amp suitable for preamplification. Ideal for high-fidelity audio applications, with wider bandwidth and lower harmonic distortion.

## Theory
![Basic configurations](ampli.jpg)

To transform a mic signal into a guitar level signal, we shoud use a "Non-Inverting Amplifier":

![Non-Inverting Amplifier](https://upload.wikimedia.org/wikipedia/commons/4/44/Op-Amp_Non-Inverting_Amplifier.svg)

With 
> $Vout = Vin(1+{R1 \over R2})$

## Real life schema
Filters are usually inserted between IC and IO:
![OA IRL](https://www.electrical4u.com/wp-content/uploads/What-is-a-Non-Inverting-Amplifier.png?ezimgfmt=rs%3Adevice%2Frscb38-1)
(www.electrical4u.com)

Thus, with an OA such as TI's [OPA2134PA](https://www.ti.com/lit/ds/symlink/opa2134.pdf), the schema would be:
![OPA2134PA schema](OPA2134PA_schema.png)

To adapt the signal level of a dynamic microphone (approximately -60 dBV to -40 dBV) to the level of a guitar signal (approximately -10 dBV to -20 dBV), you will need to increase the gain of your amplifier. Here’s how you can determine the values of R1 and R2.

### Gain calculation

1. **Signal Levels**:
   - Microphone: -60 dBV to -40 dBV
   - Guitar: -10 dBV to -20 dBV

2. **Level Difference**:
   - To adapt the microphone signal to the highest guitar level (-10 dBV), you will need a gain of around 50 dB (since 50 dB corresponds to a ratio of 100,000 times in voltage).

#### Required Gain

To convert -60 dBV to -10 dBV, the difference is 50 dB. In terms of gain:

> $Gain = 10^{50 \over 20}$ ~ 100 

which means _100 times_


#### Gain Formula
For a non-inverting amplifier:
> $A = 1 + {R1 \over R2}$

### Choosing Values
To achieve a gain of 100:
> $100 = 1 + {R1 \over R2}$

This means:
> ${R1 \over R2} = 99$

#### Example Values

- If you choose **R2 = 1 kΩ**:
  - Then R1 = 99 kΩ (you can use a nearby resistance, like 100 kΩ).

- If you choose **R2 = 10 kΩ**:
  - Then R1 = 990 kΩ (you can use a [combination of resistors](https://phys.libretexts.org/Bookshelves/University_Physics/University_Physics_(OpenStax)/University_Physics_II_-_Thermodynamics_Electricity_and_Magnetism_(OpenStax)/10%3A_Direct-Current_Circuits/10.03%3A_Resistors_in_Series_and_Parallel) to achieve this value).

### High-pass filters
You could note the INPUT is plugged to a condensor (C1) with its other pin plugged to resistors (R3 or R4).
These are typically [High-pass filters](https://en.wikipedia.org/wiki/High-pass_filter).
![High-pass filter](https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/CR_high_pass_filter.svg/440px-CR_high_pass_filter.svg.png)

To cut frequencies under 20Hz, the classic formulae is 
> $Fc = {1 \over (2 \pi R C)}$

 
Which can be implemented with 
* R = 80 kΩ
* C = 100 nF

Similarly, a [low-pass filter](https://en.wikipedia.org/wiki/Low-pass_filter) could be added to cut frequencies higher than 20 kHz with the same calculation.
![Low-pass filter](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/1st_Order_Lowpass_Filter_RC.svg/500px-1st_Order_Lowpass_Filter_RC.svg.png)

### Peak detector
To avoid overloading the signal and reaching inadmissible voltages, a [VOLTAGE LEVEL DETECTOR](https://www.researchgate.net/publication/280728100_Op-Amp_Application_Circuits_practice_1) could be involved.

### Gain control
To adjust the gain, since a non-inverting amplifier configuration will be used, we will simply apply the formula

> $Vout = Vin * (1+{R1 \over R2})$
 
Therefore, if a logarithmic potentiometer is put instead of a fixed resistor, the Vout will be adjusted. 
 
### EQ
To fine tune the signal, an equalizer may be added:
![6 bands EQ](https://www.next.gr/uploads/3/6%252BGraphic%252BEqualiser%252BCircuit%252B741%252BOp-Amp.jpg)

(check [here](https://schematicblog.blogspot.com/2011/08/6-graphic-equaliser-circuit-741-op-amp.html) for the BOM)
### Power Supply
To generate both +9V and -9V from a single +9V power supply, you can use a few different methods. Here’s a common approach using an **inverting voltage regulator** or a **virtual ground** circuit.

#### Using an Inverting Voltage Regulator (LM7909)

##### 1. **Components Needed**:
   - Oscillator (LM555 or similar) to generate a cyclic signal
   - Voltage Regulator (LM7909 or similar) to regulate the signal
   - Capacitors (typically 0.33 µF and 1 µF for stability)
   - +9V Power Supply

see example [here](https://theorycircuit.com/ic-555-ic-741/9v-dual-power-supply-from-3v/)
![example](https://theorycircuit.com/wp-content/uploads/2019/09/9V-dual-power-supply-circuit.png)

##### 2. **[TC1044SCPA](https://www.farnell.com/datasheets/129144.pdf) based circuit**
This IC is a "charge pump DC-TO-DC voltage converter" which integrates both oscillator and voltage regulator. 
 
![TC1044SCPA](https://preview.redd.it/c673rojl58q91.jpg?width=750&format=pjpg&auto=webp&s=febe27b96f6bb92c587cb881071a9e9ddb12a241)

## See also  
> To discover more on signal transformation watch this tutorial :
> * https://www.youtube.com/watch?v=Lfus8ew0udY
> * https://fr.wikipedia.org/wiki/Montages_de_base_de_l%27amplificateur_op%C3%A9rationnel
> * http://mawy33.free.fr/cours%20sup/32-008%20%C3%A9l%C3%A9ctrocin%C3%A9tique%20imp%C3%A9dance%20entr%C3%A9e%20sortie.pdf
> * https://forum.arduino.cc/t/guitar-input-with-op-amp-not-giving-output/1081889/13
>
> the most advanced work on this is probably https://electronics.stackexchange.com/questions/607840/best-way-to-reduce-hf-noise-in-oma2134-op-amp-preamp-circuit/610271#610271
> 
> ![sample](preamp.jpg)


## General Components

   * Resistors: Use standard 1/4W or 1/8W resistors for creating attenuators and filters (e.g., 1kΩ, 10kΩ).
   * Capacitors: Ceramic or electrolytic capacitors for filtering applications (e.g., 10µF, 100nF).
