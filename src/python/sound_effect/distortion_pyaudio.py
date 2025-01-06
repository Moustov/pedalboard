import pyaudio
import numpy as np

def soft_clipping(signal, gain=5.0, depth=0.5):
    """Applique un effet de soft clipping à un signal audio."""
    signal = signal * gain
    return np.tanh(depth * signal)

# Initialiser PyAudio
p = pyaudio.PyAudio()

# Paramètres audio
chunk = 1024  # Taille du bloc
format = pyaudio.paFloat32  # Format des données
channels = 1  # Mono
rate = 44100  # Fréquence d'échantillonnage

# Ouvrir un flux audio
stream = p.open(format=format, channels=channels, rate=rate, output=True, input=True)

try:
    while True:
        # Lire un bloc de données
        data = stream.read(chunk)
        input_signal = np.frombuffer(data, dtype=np.float32)

        # Appliquer l'effet de distorsion
        output_signal = soft_clipping(input_signal)

        # Écrire le signal traité dans le flux
        stream.write(output_signal.astype(np.float32).tobytes())
except KeyboardInterrupt:
    print("Arrêt du flux.")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()