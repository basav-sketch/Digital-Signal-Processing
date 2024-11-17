# Assignment 2: Finite Impulse Response (FIR) Filtering and Heartbeat Detection

This document provides a detailed overview of **Assignment 2** for the **Digital Signal Processing** (DSP) course. The focus of this assignment was on designing and implementing FIR filters for ECG signal processing, exploring adaptive filtering using LMS, and implementing heartbeat detection using matched filtering.

## Objectives

1. **Design and Implement FIR Filters**
   - Develop high-pass and band-stop filters to clean ECG signals.
   - Utilize the Blackman window to improve the frequency response of the FIR filter.

2. **Apply FIR Filters to ECG Signals**
   - Use the designed FIR filter on noisy ECG data and compare the output with clean ECG data.

3. **Adaptive LMS Filtering**
   - Implement an adaptive LMS filter to remove noise and compare its performance to FIR filtering.

4. **Heartbeat Detection**
   - Detect heartbeats in the filtered ECG data using matched filtering and calculate the momentary heart rate (BPM).

## Task Details

### Task 1: FIR Filter Design

**Objective**: Design a combined high-pass and band-stop FIR filter using the sinc function.

- **High-pass Filter**: Developed using a sinc function to remove low-frequency components from the ECG signal.
- **Band-stop Filter**: Designed to eliminate 50 Hz power-line interference.
- **Windowing**: Applied a Blackman window to the filter to reduce side lobes and improve filter performance.
- **Normalization**: The filter coefficients were normalized to ensure unity gain in the passband.

**Visualizations**:
- Impulse response plots of the filter before and after applying the Blackman window.
- Frequency response of the filter to evaluate its performance in attenuating unwanted frequencies.

### Task 2: Apply FIR Filter

**Objective**: Apply the FIR filter to both noisy and clean ECG signals.

- **Implementation**: The noisy ECG signal was filtered using the designed FIR filter.
- **Comparison**: Time-domain and frequency-domain plots were used to compare the filtered noisy ECG signal against the clean ECG reference.

**Visualizations**:
- Time-domain plots of the original noisy signal, clean signal, and FIR-filtered signal.
- Frequency-domain plots to analyze the effectiveness of the filter.

### Task 3: Adaptive LMS Filtering

**Objective**: Implement an adaptive LMS filter to further clean the noisy ECG signal.

- **LMS Filter**: Initialized with zero coefficients and adaptively updated based on the error between the noisy ECG signal and a reference noise signal.
- **Reference Noise**: A 50 Hz sinusoidal reference signal with a DC component was used.
- **Comparison**: The LMS-filtered ECG signal was compared with the FIR-filtered output to understand the differences in their performance.

**Visualizations**:
- Time-domain and frequency-domain comparisons of FIR-filtered and LMS-filtered signals.
- A zoomed-in plot of one heartbeat to show if the ECG waveform components (P, QRS, T waves) remained intact after filtering.

### Task 4: Heartbeat Detection

**Objective**: Use matched filtering to detect R-peaks in the filtered ECG and calculate the heart rate.

- **Matched Filtering**: A template was selected from the clean ECG data, and its time-reversed version was used as the matched filter coefficients.
- **Peak Detection**: The filtered ECG signal was processed to enhance R-peaks, followed by using `scipy.signal.find_peaks()` to detect the peaks.
- **Heart Rate Calculation**: The time intervals between consecutive R-peaks were used to calculate the momentary heart rate in BPM.

**Visualizations**:
- Comparison between the ECG template and the matched filter coefficients.
- Filtered ECG signal with detected R-peaks highlighted.
- Momentary heart rate (BPM) plotted over time.

## Results and Observations

### FIR vs. LMS Filtering

- **FIR Filter**: Demonstrated strong performance in removing baseline wander and 50 Hz power-line interference while preserving the morphology of the ECG signal.
- **LMS Filter**: Successfully adapted to remove noise, but required careful tuning of the learning rate. In some cases, LMS filtering slightly affected the integrity of the ECG waveform.

### Heartbeat Detection

- The matched filter effectively enhanced R-peaks, leading to accurate detection of heartbeats.
- Calculated BPM values were consistent with expected physiological ranges, demonstrating successful detection.

## Repository Structure

- **Assignment_2_FIR/**
  - **FIR assignment.pdf**: The report detailing the FIR filter design and results.
  - **fir_filtering.py**: Python script for designing and applying FIR filters.
  - **lms_filtering.py**: Python script for implementing LMS filtering.
  - **hr_detect.py**: Python script for detecting heartbeats and calculating BPM.
  - **Noisy_ECG_1000Hz_9.dat**: Noisy ECG data used for filtering.
  - **Lying_ECG_1000Hz_9.dat**: Clean ECG data used as reference.

## Running the Code

1. **FIR Filter Design and Application**
   ```bash
   python fir_filtering.py
   ```
   - This script designs the FIR filter and applies it to the noisy ECG data, generating relevant plots.

2. **LMS Filtering**
   ```bash
   python lms_filtering.py
   ```
   - This script implements adaptive LMS filtering to remove noise from the ECG data.

3. **Heartbeat Detection**
   ```bash
   python hr_detect.py
   ```
   - This script uses matched filtering to detect R-peaks and calculates momentary BPM.

## Conclusion

This assignment demonstrated the effectiveness of FIR and LMS filtering in the context of biomedical signal processing. FIR filters were found to be effective in removing specific frequency components while maintaining ECG signal integrity, whereas LMS filters provided adaptive capabilities but required careful parameter tuning. Matched filtering proved highly effective for detecting heartbeats and calculating heart rates, providing accurate physiological measurements.

## Contact

For any questions or discussions, feel free to reach out via GitHub or email.
