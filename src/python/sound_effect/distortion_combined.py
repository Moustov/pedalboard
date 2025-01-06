import numpy as np
import soundfile as sf

def soft_clipping(signal, gain=5.0):
    signal = signal * gain
    return np.tanh(signal)

def overdrive(signal, gain=5.0, threshold=0.5):
    signal = signal * gain
    return np.clip(signal, -threshold, threshold)

def fuzz(signal, gain=5.0):
    signal = signal * gain
    return np.sign(signal) * (np.abs(signal) ** 2)

def apply_distortion(signal, type='soft', gain=5.0, threshold=0.3):
    if type == 'soft':
        return soft_clipping(signal, gain)
    elif type == 'overdrive':
        return overdrive(signal, gain, threshold)
    elif type == 'fuzz':
        return fuzz(signal, gain)
    else:
        raise ValueError("Type de distorsion non reconnu.")

# Charger un fichier audio
input_file = 'input_audio.wav'  # Remplacez par le chemin de votre fichier audio
output_file = 'output_distortion.wav'

# Lire le fichier audio
signal, sample_rate = sf.read(input_file)

# Appliquer un effet de distorsion
distorted_signal = apply_distortion(signal, type='fuzz', gain=5.0)

# Sauvegarder le résultat
sf.write(output_file, distorted_signal, sample_rate)