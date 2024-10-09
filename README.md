# Digital Signal Processing (DSP) Assignment 1

## Task Breakdown

### Task 1: Audio Signal Analysis
- **Loaded** audio samples into Python.
- **Plotted** the audio signals in both the time domain (amplitude vs. time) and the frequency domain (frequency vs. amplitude in dB).

### Task 2: Analyzing the Frequency Spectrum
- **Fundamental Frequency**: Identified the fundamental frequency as **167.9 Hz** from the frequency domain plot. 
- **Harmonics**: Found harmonics at **335.8 Hz** and **503.7 Hz**. Higher harmonics had significantly lower amplitudes.
- **Noise**: Frequencies above **10kHz** were identified as containing noise, particularly in the higher harmonics and sibilants.

### Task 3: Improving Voice Quality
- **Objective**: Enhance the audio quality by reducing noise while preserving the essential voice frequencies.
- **High-Pass Filter**: Applied a high-pass filter with a cutoff frequency of **1500 Hz**, but it reduced both noise and some of the voice, making it sound less natural.
- **Band-Pass Filter**: Applied a band-pass filter with a low cut of **300 Hz** and a high cut of **3000 Hz**. This filter preserved the fundamental frequency and harmonics, while reducing both low-frequency and high-frequency noise. The result was a clearer voice with less distortion compared to the high-pass filter.

#### Key Observations:
- The **band-pass filter** produced better results than the high-pass filter because it preserved more of the natural voice frequencies while still reducing unwanted noise.
- Fine-tuning the cutoff frequencies was crucial for maintaining the balance between noise reduction and voice clarity.

### Task 4: Aural Exciter Simulation
- **Next Step**: Simulate an aural exciter by applying a non-linearity function like `tanh()` to enhance the voice and combine the result with the original audio signal.

