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
In this task, we aimed to enhance the quality of the voice recorded in the audio file by manually designing a filter and using Fourier Transform techniques.

### Manual High-Pass Filter
- **Custom Filter Design**: We created a manual high-pass filter to remove frequencies below 3kHz and retain the essential vocal frequencies.
- **Boosting Frequencies**: Frequencies between 1kHz and 3kHz were boosted to enhance vocal clarity.

#### Key Steps:
1. **Fourier Transform**: Applied to the original audio signal to analyze the frequency components.
2. **Manual Filtering**: Frequencies below 3kHz were set to zero to eliminate unwanted noise.
3. **Enhancement**: Frequencies in the range of 1kHz to 3kHz were amplified to improve clarity.
4. **Inverse Fourier Transform**: Converted the filtered data back to the time domain.
5. **Output**: Saved the enhanced audio as `enhanced_audio_manual_highpass.wav`.

## Task 4: Aural Exciter Simulation
This task involved simulating an aural exciter effect by applying non-linearity to specific frequency ranges.

### Key Steps:
1. **High-Frequency Isolation**: Isolated frequencies between 3kHz and 10kHz for enhancement.
2. **Non-Linearity Application**: The `tanh` function was applied to enhance the presence of high frequencies.
3. **Combining Signals**: The enhanced high-frequency signal was combined with the original audio signal.
4. **Output**: Saved the resulting audio with the aural exciter effect as `aural_exciter_effect.wav`.

### Results:
The audio quality was significantly improved through careful filtering and enhancement techniques, making the voice sound clearer and more vibrant.

### Future Work:
Further tuning of filter parameters and additional enhancements could be explored to refine audio quality even more.