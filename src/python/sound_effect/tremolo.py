import numpy as np
import sounddevice as sd

# Tremolo parameters
#    depth: Controls how much the amplitude is modulated. A value of 0 means no modulation, while a value of 1 means full modulation.
depth = 0.5  # Depth of modulation (0 to 1)
#    rate: Controls the speed of the modulation in Hertz (Hz). A higher value results in a faster tremolo effect.
rate = 5.0  # Rate of modulation in Hz


def tremolo(signal, samplerate):
    """Applies a tremolo effect to the input signal."""
    # Create a modulation waveform (sine wave)
    modulation = (1 + depth * np.sin(2 * np.pi * rate * np.arange(len(signal)) / samplerate)) / 2
    return signal * modulation


def audio_callback(indata, outdata, frames, time, status):
    """Callback function to process audio signal in real time."""
    if status:
        print(status)

    # Apply the tremolo effect
    outdata[:] = tremolo(indata[:, 0], 44100).reshape(-1, 1)  # Mono


# Configure audio parameters
samplerate = 44100  # Sample rate

# Start the audio stream
with sd.Stream(callback=audio_callback, channels=1, samplerate=samplerate):
    print("Press Ctrl+C to stop the stream.")
    try:
        sd.sleep(1000000)  # Keep the stream open for 1 million milliseconds
    except KeyboardInterrupt:
        print("Stopping the stream.")