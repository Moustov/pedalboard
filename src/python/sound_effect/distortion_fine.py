import numpy as np
import soundfile as sf


def soft_clipping(signal, gain=5.0, depth=0.5):
    """
    Applique un soft clipping à un signal audio.

    :param signal: Le signal audio d'entrée.
    :param gain: Gain appliqué au signal.
    :param depth: Profondeur de la distorsion.
    :return: Le signal audio avec l'effet de soft clipping appliqué.
    """
    signal = signal * gain

    # Utiliser une fonction non linéaire pour le clipping
    clipped_signal = np.tanh(depth * signal)

    return clipped_signal


def apply_distortion(signal, gain=5.0, depth=0.5):
    """
    Applique une distorsion au signal audio avec contrôle du gain et de la profondeur.

    :param signal: Le signal audio d'entrée.
    :param gain: Gain appliqué au signal.
    :param depth: Profondeur de la distorsion.
    :return: Le signal audio distordu.
    """
    return soft_clipping(signal, gain, depth)


# Charger un fichier audio
input_file = 'input_audio.wav'  # Remplacez par le chemin de votre fichier audio
output_file = 'output_distortion_controlled.wav'

# Lire le fichier audio
signal, sample_rate = sf.read(input_file)

# Appliquer l'effet de distorsion avec contrôle
distorted_signal = apply_distortion(signal, gain=5.0, depth=0.7)

# Sauvegarder le résultat
sf.write(output_file, distorted_signal, sample_rate)