import numpy as np
import sounddevice as sd

# Flanger parameters
# depth: Controls the modulation depth of the flanger effect.
depth = 0.5  # Modulation depth
# rate: Controls the speed of the modulation in Hertz.
rate = 0.5  # Modulation speed (Hz)
# max_delay: Determines the maximum delay time for the effect in seconds.
max_delay = 0.005  # Maximum delay (seconds)

# Initialize a buffer to store the delayed signal
delay_buffer = np.zeros(int(max_delay * 44100))
write_index = 0


def flanger(signal, samplerate):
    global delay_buffer, write_index

    output = np.zeros_like(signal)

    for i in range(len(signal)):
        # Calculate variable delay
        delay_samples = int(max_delay * (depth * (1 + np.sin(2 * np.pi * rate * i / samplerate))))
        read_index = (write_index - delay_samples) % len(delay_buffer)

        # Mix the original signal with the delayed one
        output[i] = signal[i] + delay_buffer[read_index] * 0.5  # Mix with delayed signal

        # Store the signal in the buffer
        delay_buffer[write_index] = signal[i]
        write_index = (write_index + 1) % len(delay_buffer)

    return output


def audio_callback(indata, outdata, frames, time, status):
    """Callback function to process audio signal in real time."""
    if status:
        print(status)

    # Apply the flanger effect
    outdata[:] = flanger(indata[:, 0], 44100).reshape(-1, 1)  # Mono


# Configure audio parameters
samplerate = 44100  # Sample rate

# Start the audio stream
with sd.Stream(callback=audio_callback, channels=1, samplerate=samplerate):
    print("Press Ctrl+C to stop the stream.")
    try:
        sd.sleep(1000000)  # Keep the stream open for 1 million milliseconds
    except KeyboardInterrupt:
        print("Stopping the stream.")