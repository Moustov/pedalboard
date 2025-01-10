import numpy as np
import sounddevice as sd

# Parameters
# sample_rate: The number of samples per second (standard CD quality is 44100 Hz).
sample_rate = 44100  # Sample rate in Hz
# delay_times: A list of delay times in seconds for creating multiple voices.
delay_times = [0.01, 0.015, 0.02]  # Delay times in seconds for multiple voices
# depth: The maximum pitch modulation depth in seconds.
depth = 0.002  # Depth of pitch modulation in seconds
# rate: The frequency of the LFO that modulates the pitch.
rate = 0.5  # Rate of modulation in Hz

# Audio buffer
buffer_size = 1024
buffer = np.zeros(buffer_size)


def audio_callback(indata, outdata, frames, time, status):
    if status:
        print(status)

    # Generate LFO for pitch modulation
    t = np.arange(frames) / sample_rate
    lfo = depth * np.sin(2 * np.pi * rate * t)

    # Apply chorus effect
    outdata[:] = indata  # Start with original signal
    for delay in delay_times:
        delay_samples = int(delay * sample_rate)
        modulated_indices = np.clip(np.arange(frames) + (lfo * sample_rate).astype(int), 0, frames - 1)
        delayed_signal = np.roll(indata, delay_samples, axis=0)
        outdata += delayed_signal[modulated_indices]  # Add delayed signal with modulation

    # Normalize output to avoid clipping
    outdata /= (len(delay_times) + 1)


# Start streaming
with sd.Stream(callback=audio_callback, channels=1, samplerate=sample_rate):
    print("Press Ctrl+C to stop.")
    try:
        while True:
            sd.sleep(1000)
    except KeyboardInterrupt:
        print("Stopped.")