Audio libs in python
===

There are several audio libraries in Python that offer advanced features for sound processing, 
including effects such as distortion, reverberation, filtering and much more. 
Here are some of the most popular and powerful libraries:

# Real-time processing

## SoundDevice

SoundDevice is a library for playing and recording sound in real time. It is often used with NumPy for audio processing.

    Features: Real-time audio playback and recording.
    Installation :
    bash

    pip install sounddevice

## PyAudio

PyAudio is a library that provides bindings for PortAudio, enabling real-time audio recording and playback.

    Features: Real-time audio recording and playback.
    Installation :
    bash

    pip install pyaudio

# Non real-time processing

## Librosa

Librosa is a popular library for audio and music analysis. It provides tools for signal processing and musical feature extraction.

    Features: signal processing, feature extraction, visualization, etc.
    Installation :
    bash

    pip install librosa

## PyDub

PyDub is an easy-to-use library for manipulating audio files. It supports several formats and allows simple operations such as cutting, merging and applying effects.

    Features: Simple manipulation of audio files, format conversion, application of effects.
    Installation :
    bash

    pip install pydub

## SciPy

SciPy, in particular its sub-module scipy.signal, offers tools for filtering and signal processing. You can also use it to apply transformations such as convolution and filtering.

    Features: signal processing, digital filters, transformations.
    Installation :
    bash

    pip install scipy


## TensorFlow and PyTorch

These machine learning libraries can also be used for audio processing, particularly for advanced applications such as audio synthesis, source separation and audio classification.

    Features: deep learning models for audio processing.
    Installation :
    bash

    pip install tensorflow
    # or
    pip install torch

## Soundfile

Soundfile is a simple, efficient library for reading and writing audio files in a variety of formats.

    Features: Reads and writes audio files.
    Installation :
    bash

    pip install soundfile
