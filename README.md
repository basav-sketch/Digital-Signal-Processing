# Digital Signal Processing (DSP) Assignment

## Task Breakdown

### Task 1: Audio Signal Analysis
- Loaded audio samples into Python.
- Plotted the audio signals in both the time domain (amplitude vs. time) and the frequency domain (frequency vs. amplitude in dB).

### Task 2: Analyzing the Frequency Spectrum
#### Fundamental Frequencies
- **Definition**: The lowest frequency in a signal, typically found in human speech between 85 Hz to 255 Hz.
- **How to Identify**: The first prominent peak in the frequency spectrum (F0).

#### Harmonics
- **Definition**: Multiples of the fundamental frequency.
- **How to Identify**: Look for peaks at integer multiples of the fundamental frequency.

#### Noise
- **Definition**: Random signals spread across frequencies, often present above 10 kHz.
- **How to Identify**: Broad, low-amplitude components in the higher frequency range.

#### Tuning Peak Detection (`height` parameter)
- The `height` parameter in peak detection adjusts the minimum threshold for peak magnitude:
  - **Low height** detects more peaks, including minor fluctuations (potential noise).
  - **High height** detects only prominent peaks but may miss some real signals.
  - Recommended to fine-tune this based on the signal being analyzed.

### Task 3: Improving Voice Quality
- To be completed...

### Task 4: Aural Exciter Simulation
- To be completed...
