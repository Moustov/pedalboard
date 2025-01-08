import numpy as np
import sounddevice as sd

# Parameters
#sample_rate: The number of samples per second (standard CD quality is 44100 Hz).
sample_rate = 44100  # Sample rate in Hz
# vibrato_rate: The frequency of the vibrato effect in Hz (how fast the pitch oscillates).
vibrato_rate = 5.0  # Rate of vibrato in Hz
# vibrato_depth_seconds: Controls the time variation in the vibrato effect.
vibrato_depth_seconds = 0.005  # Depth of vibrato in seconds
# The cents_to_freq function converts the vibrato depth from cents to a frequency offset relative to A4 (440 Hz).}
vibrato_depth_cents = 50  # Depth of vibrato in cents




# Convert cents to frequency offset
def cents_to_freq(cents):
    return 440.0 * (2 ** (cents / 1200.0))


# Calculate vibrato depth in frequency
vibrato_depth_freq = cents_to_freq(vibrato_depth_cents) - 440.0

# Audio buffer
buffer_size = 1024
buffer = np.zeros(buffer_size)


def audio_callback(indata, outdata, frames, time, status):
    if status:
        print(status)

    # Generate vibrato effect
    t = np.arange(frames) / sample_rate
    vibrato_offset_cents = vibrato_depth_freq * np.sin(2 * np.pi * vibrato_rate * t)
    vibrato_offset_time = vibrato_depth_seconds * np.sin(2 * np.pi * vibrato_rate * t)

    # Apply vibrato effect
    for i in range(frames):
        # Index Adjustment: The index used to read samples is adjusted based on both the pitch oscillation and the time oscillation. This creates a richer vibrato effect.
        index = int(i + vibrato_offset_cents[i] * sample_rate / 440.0 + vibrato_offset_time[i] * sample_rate)
        index = np.clip(index, 0, buffer_size - 1)  # Prevent index out of bounds
        outdata[i] = indata[index]


# Start streaming
with sd.Stream(callback=audio_callback, channels=1, samplerate=sample_rate):
    print("Press Ctrl+C to stop.")
    try:
        while True:
            sd.sleep(1000)
    except KeyboardInterrupt:
        print("Stopped.")