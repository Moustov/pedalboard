Pour récupérer le niveau d'un potentiomètre et l'injecter dans le code du looper, on utilise un convertisseur analogique-numérique (CAN), comme le MCP3008, connecté au Raspberry Pi.

# Matériel Nécessaire
* Raspberry Pi Zero
* [MCP3008](https://cdn-shop.adafruit.com/datasheets/MCP3008.pdf) : Un convertisseur analogique-numérique à 8 canaux.
* Potentiomètre logarithmique
* Câbles de connexion
* Breadboard (facultatif)

# Schéma de Connexion

Connecter le MCP3008 au Raspberry Pi :
* VDD (MCP3008) à 3.3V (Raspberry Pi)
* VREF (MCP3008) à 3.3V (Raspberry Pi)
* AGND à GND (Raspberry Pi)
* DGND à GND (Raspberry Pi)
* CLK à GPIO 11 (pin 23)
* DOUT à GPIO 9 (pin 21)
* DIN à GPIO 10 (pin 19)
* CS/SHDN à GPIO 8 (pin 24)

Connecter le Potentiomètre :
* Une extrémité à GND
* L'autre extrémité à 3.3V
* Le curseur (milieu) au pin CH0 (canal 0) du MCP3008.

# Code
```c lines
int readADC(int channel) {
    unsigned char buff[3];
    
    digitalWrite(MCP3008_CS_PIN, LOW); // Activer le MCP3008
    buff[0] = 1; // Start bit
    buff[1] = (8 + channel) << 4; // Configurer le canal
    buff[2] = 0; // Dummy byte

    wiringPiSPIDataRW(0, buff, 3); // Envoyer et recevoir des données
    digitalWrite(MCP3008_CS_PIN, HIGH); // Désactiver le MCP3008

    return ((buff[1] & 3) << 8) + buff[2]; // Récupérer la valeur
}
```