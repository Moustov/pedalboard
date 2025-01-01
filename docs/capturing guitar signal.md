Pour traiter un signal en provenance d'un pedalboard de guitare avec un Raspberry Pi Zero, tu auras besoin de matériel spécifique et d'ajustements dans le code. Voici un guide complet :
# Matériel Nécessaire

* Raspberry Pi Zero : Assure-toi d'avoir un modèle Raspberry Pi Zero avec les ports nécessaires.
* Interface Audio USB : Le Raspberry Pi Zero n'a pas d'entrée audio analogique. Il te faudra une interface audio USB compatible qui peut gérer des signaux audio de haute qualité. 
* Câbles Audio :
  * Câble 1/4" TS pour connecter la sortie de ton pedalboard à l'entrée de l'interface audio.
  * Câble USB pour connecter l'interface audio au Raspberry Pi.
* Alimentation : Assure-toi que ton Raspberry Pi est correctement alimenté, surtout si tu utilises des périphériques USB.

## Raspberry Pi Zero
* https://raspberry-projects.com/pi/category/pi-hardware/raspberry-pi-zero

## Interface Audio USB
L'interface USB doit être '[USB Class Compliant](https://wiki.linuxaudio.org/wiki/hardware)'. Cela  signifie qu'elle devrait fonctionner sans pilotes supplémentaires sous Linux (y compris Raspbian).
Voici quelques exemples 
* M-Audio M-Track Duo
* Focusrite Scarlett Solo
* Behringer UMC22

# Code

Voici les modifications à apporter au code pour gérer le signal audio en provenance du pedalboard.

## Configurer l'Interface Audio
Assure-toi que l'interface audio est bien reconnue par le Raspberry Pi. Tu peux vérifier cela avec la commande :
```shell
$ aplay -l
```
Cela devrait te montrer les appareils audio disponibles.