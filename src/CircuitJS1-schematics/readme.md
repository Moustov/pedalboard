Pure hardware-based effects - Schematics
===

> The schematics are viewed with Falstad's Circuit Simulator version 3.1.3js.
> Original by Paul Falstad: http://www.falstad.com/
> GitHub link to report issues and view source code: https://github.com/pfalstad/circuitjs1
>
> To visualize them, you may use https://www.falstad.com/circuit/circuitjs.html

# [Bazz fuss](bazz%20fuss.txt)
"Bazz fuss" : https://home-wrecker.com/bazz.html
This is a diode + NPN transistor-based fuzz 
![bazz fuss](bazz%20fuss.png)

# [bazz fuss 2 pot](bazz%20fuss%202%20pot.txt)
![bazz fuss 2 pot](bazz%20fuss%202%20pot%20-%20IC.png)
## Config #1
![bazz fuss 2 pot](bazz%20fuss%202%20pot%20-%20c1.png)
## Config #2
![bazz fuss 2 pot](bazz%20fuss%202%20pot%20-%20c2.png)
## Config #3
![bazz fuss 2 pot](bazz%20fuss%202%20pot%20-%20c3.png)

# [Basic fuzz](basic%20fuzz.txt)
![basic fuzz](basic%20fuzz.png)

# [Buzz box](buzz%20box.txt)
"Buzz box" : https://home-wrecker.com/bazz.html
![Buzz box](buzz%20box.png)

# [Fuzz 3pot](fuzz%203pot.txt)
![fuzz 3pot](fuzz%203pot.png)

# [M effect v5](M%20effect%20v5.txt)
![M effect v5](M%20effect%20v5.png)

# [M-bell effect](M-bell%20effect.txt)
![M-bell effect](M-bell%20effect.png)

# My fuzz
From 'bazz fuss 2 pot': the upper potentiometer is fixed to 7.5 / 2.5 kΩ

````text
$ 1 0.000002834467120181406 173.42552219524063 77 10 62 5e-11
v -576 240 -432 240 0 1 100 5 0 0 0.5
c -432 240 -320 240 4 0.000009999999999999999 3.310460035643831 0.001 0
t -320 240 -224 240 0 1 -0.5608311946173936 -1.7421645737618074 100 default
d -224 176 -320 176 2 1N4148
r 64 304 64 256 0 330
v -576 80 -224 80 0 0 40 5 0 0 0.5
w -576 240 -576 80 0
w -320 240 -320 176 0
g -224 256 -224 304 0 0
g -576 240 -576 272 0 0
c -224 224 -128 224 4 0.000009999999999999999 -3.628969949410923 0.001 0
w -224 224 -224 176 0
g 64 304 64 336 0 0
O -32 224 48 144 0 0
w -224 176 -176 176 0
w -128 224 -32 224 0
174 -32 224 144 256 5 10000 0.5594 Resistance
g 160 224 160 256 0 0
g -128 80 -128 112 0 0
r -176 128 -176 176 0 1000
r -224 80 -176 128 0 6800
r -224 80 -128 80 0 2700
x -261 273 -209 276 4 15 2N3904
x -294 164 -242 167 4 15 1N4148
o 13 16 0 4098 10 0.1 0 3 0 0 0 3
````
![my fuzz](my%20fuzz.png)

