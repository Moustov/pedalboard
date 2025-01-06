import numpy as np
import sounddevice as sd

# Phaser parameters
# num_stages: The number of filter stages in the phaser. More stages can create a richer effect.
num_stages = 4  # Number of filter stages
# feedback: Controls how much of the output is fed back into the input.
feedback = 0.5  # Feedback amount (0 to 1)
# depth: The modulation depth of the LFO, affecting how pronounced the phasing effect is.
depth = 0.7  # Depth of modulation (0 to 1)
# rate: The speed of the modulation in Hertz.
rate = 0.5  # Modulation rate in Hz

# Initialize filter coefficients and phase
filter_coeffs = np.zeros(num_stages)
phase = 0


def phaser(signal, samplerate):
    global filter_coeffs, phase
    output = np.zeros_like(signal)

    # Create an LFO for modulation
    lfo = (1 + depth * np.sin(2 * np.pi * rate * np.arange(len(signal)) / samplerate)) / 2

    for i in range(len(signal)):
        # Update the filter coefficients based on the LFO
        for j in range(num_stages):
            filter_coeffs[j] = np.sin(phase + j * (np.pi / num_stages))

        # Apply the phaser effect
        temp_signal = signal[i]
        for j in range(num_stages):
            temp_signal += filter_coeffs[j] * output[max(0, i - j)]

        output[i] = temp_signal
        phase += 2 * np.pi * rate / samplerate
        if phase > 2 * np.pi:
            phase -= 2 * np.pi

    return output


def audio_callback(indata, outdata, frames, time, status):
    """Callback function to process audio signal in real time."""
    if status:
        print(status)

    # Apply the phaser effect
    outdata[:] = phaser(indata[:, 0], 44100).reshape(-1, 1)  # Mono


# Start the audio stream
with sd.Stream(callback=audio_callback, channels=1, samplerate=44100):
    print("Press Ctrl+C to stop the stream.")
    try:
        sd.sleep(1000000)  # Keep the stream open for 1 million milliseconds
    except KeyboardInterrupt:
        print("Stopping the stream.")