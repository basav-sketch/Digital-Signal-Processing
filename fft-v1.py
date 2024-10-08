import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# Step 1: Load the audio file
file_path = "/home/basav/DSP/Digital-Signal-Processing/Lab 1 test 2.wav"  # Updated file path
sampling_rate, audio_data = wavfile.read(file_path)

# Step 2: Normalize the audio data to be between -1 and +1
audio_data = audio_data / np.max(np.abs(audio_data), axis=0)

# Step 3: Create a time axis
time = np.linspace(0, len(audio_data) / sampling_rate, num=len(audio_data))

# Step 4: Plot the time-domain signal
plt.figure(figsize=(10, 6))
plt.plot(time, audio_data)
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.title('Time Domain Signal')
plt.grid(True)
plt.show()

# Step 5: Perform the FFT (Fast Fourier Transform)
fft_data = np.fft.fft(audio_data)
fft_freq = np.fft.fftfreq(len(fft_data), d=1/sampling_rate)

# Step 6: Plot the frequency-domain signal
plt.figure(figsize=(10, 6))
plt.plot(fft_freq, 20 * np.log10(np.abs(fft_data)))  # Using dB scale
plt.xlim(0, 20000)  # Limiting the frequency range to 20kHz
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude [dB]')
plt.title('Frequency Domain Signal')
plt.grid(True)
plt.show()

from scipy.signal import find_peaks

# Perform FFT (reusing the code from Task 1)
fft_data = np.fft.fft(audio_data)
fft_freq = np.fft.fftfreq(len(fft_data), d=1/sampling_rate)

# Only keep positive frequencies
positive_frequencies = fft_freq[:len(fft_freq)//2]
positive_magnitude = np.abs(fft_data[:len(fft_data)//2])

# Find peaks in the frequency domain
peaks, _ = find_peaks(positive_magnitude, height=0.1)  # Adjust height threshold as needed

# Plot Frequency Spectrum with Peaks Marked
plt.figure(figsize=(10, 6))
plt.plot(positive_frequencies, 20*np.log10(positive_magnitude))
plt.plot(positive_frequencies[peaks], 20*np.log10(positive_magnitude[peaks]), "x")
plt.xlim(0, 20000)  # Focus on frequencies up to 20kHz
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude [dB]')
plt.title('Frequency Domain Signal with Peaks')
plt.grid(True)
plt.show()

# Print the identified peak frequencies
print("Peak Frequencies (Hz):", positive_frequencies[peaks])
