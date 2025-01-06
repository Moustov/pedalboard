import numpy as np
import sounddevice as sd

# Delay parameters
# delay_time: The amount of time (in seconds) to delay the signal.
delay_time = 0.5  # Delay time in seconds
# feedback: Controls how much of the delayed signal is fed back into the input. A value of 0 means no feedback, while a value of 1 means full feedback.
feedback = 0.5     # Feedback level (0 to 1)

# Calculate the number of samples for the delay
samplerate = 44100
delay_samples = int(delay_time * samplerate)

# Initialize the delay buffer
# delay_buffer: is an array created to store the delayed samples. The size of this array is determined by the delay time and the sample rate.
delay_buffer = np.zeros(delay_samples)
write_index = 0

def delay(signal):
    """Applies a delay effect to the input signal."""
    global delay_buffer, write_index
    output = np.zeros_like(signal)

    for i in range(len(signal)):
        # Read from the delay buffer
        delayed_signal = delay_buffer[write_index]

        # Mix the original signal with the delayed signal
        output[i] = signal[i] + delayed_signal * feedback

        # Write the current signal into the delay buffer
        delay_buffer[write_index] = signal[i]

        # Update the write index
        write_index = (write_index + 1) % delay_samples

    return output

def audio_callback(indata, outdata, frames, time, status):
    """Callback function to process audio signal in real time."""
    if status:
        print(status)

    # Apply the delay effect
    outdata[:] = delay(indata[:, 0]).reshape(-1, 1)  # Mono

# Start the audio stream
with sd.Stream(callback=audio_callback, channels=1, samplerate=samplerate):
    print("Press Ctrl+C to stop the stream.")
    try:
        sd.sleep(1000000)  # Keep the stream open for 1 million milliseconds
    except KeyboardInterrupt:
        print("Stopping the stream.")