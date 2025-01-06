import numpy as np
import sounddevice as sd


def soft_clipping(signal, gain=5.0, depth=0.5):
    """Applique un effet de soft clipping à un signal audio."""
    signal = signal * gain
    return np.tanh(depth * signal)


def audio_callback(indata, outdata, frames, time, status):
    """
    Fonction de rappel pour traiter le signal audio en temps réel.
    Cette fonction est appelée en continu par le flux audio. Elle reçoit des données audio en entrée (indata),
    applique l'effet de distorsion, et envoie le signal traité à la sortie (outdata).
    """
    if status:
        print(status)

    # Appliquer l'effet de distorsion
    outdata[:] = soft_clipping(indata, gain=5.0, depth=0.7)


# Configurer les paramètres audio
samplerate = 44100  # Fréquence d'échantillonnage

# sd.Stream crée un flux audio qui lit l'entrée et écrit la sortie. Vous pouvez spécifier le nombre de canaux
# (1 pour mono, 2 pour stéréo) et la fréquence d'échantillonnage.

# Démarrer le flux audio
with sd.Stream(callback=audio_callback, channels=1, samplerate=samplerate):
    print("Appuyez sur Ctrl+C pour arrêter le flux.")
    try:
        sd.sleep(1000000)  # Garder le flux ouvert pendant 1 million de millisecondes
    except KeyboardInterrupt:
        print("Arrêt du flux.")