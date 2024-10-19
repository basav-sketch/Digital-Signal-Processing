import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.io.wavfile import write

# TASK - 1 - LOADING THE WAV FILE AND PLOTTING GRAPHS

# Load the original audio file
file_path = '/home/basav/DSP/Digital-Signal-Processing/Assignment_1_FFT/audio files/orig.wav'
sampling_rate, audio_data = wavfile.read(file_path)

# Normalize the audio data to be between -1 and +1
audio_data = audio_data / np.max(np.abs(audio_data), axis=0)

# Create a time axis
time = np.linspace(0, len(audio_data) / sampling_rate, num=len(audio_data))

# Plot original audio signal in time domain
plt.figure(figsize=(10, 6))
plt.plot(time, audio_data)
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.title('Original Audio Signal - Time Domain')
plt.grid()
plt.savefig('original_time_domain_plot.svg', format='svg')
plt.show()

# Plot the audio signal in the frequency domain
# Perform Fourier Transform
audio_fft = np.fft.fft(audio_data)
frequencies = np.fft.fftfreq(len(audio_fft), d=1/sampling_rate)

# Use only the positive frequencies
positive_freqs = frequencies[:len(frequencies)//2]
positive_fft = audio_fft[:len(audio_fft)//2]

# Convert amplitude to dB
amplitude_db = 20 * np.log10(np.abs(positive_fft))

# Plot the frequency domain with log axis for both freq. and ampliitude
plt.figure(figsize=(10, 6))
plt.plot(positive_freqs, amplitude_db, label='Frequency Spectrum')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude (dB)')
plt.title('Original Audio Signal - Frequency Domain')
plt.grid()
plt.savefig('original_frequency_domain_plot.svg', format='svg')
plt.show()

# TASK - 2 - APPLY FOURIER TRANSFORM (FFT) AND FIND FUNDAMENTAL FREQ., HARMONICS AND NOISE

# Plot the frequency domain representation and mark the fundamental frequency and harmonics range
plt.figure(figsize=(10, 6))
plt.plot(positive_freqs, amplitude_db, label='Frequency Spectrum')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude (dB)')
plt.title('Audio Signal in Frequency Domain')
plt.grid()

# Mark the fundamental frequency
fundamental_freq = 168.174
fundamental_amplitude = 20 * np.log10(np.abs(positive_fft[np.argmin(np.abs(positive_freqs - fundamental_freq))]))
plt.plot(fundamental_freq, fundamental_amplitude, 'ro', label='Fundamental Frequency (168.174 Hz)')

# Mark the harmonics range (assumed to be from 2x to 5x of the fundamental frequency)
harmonics_range_start = 2 * fundamental_freq
harmonics_range_end = 5 * fundamental_freq
plt.axvspan(harmonics_range_start, harmonics_range_end, color='yellow', alpha=0.3, label='Harmonics Range')

# Mark the harmonics in the harmonics range
harmonics_freqs = [fundamental_freq * i for i in range(2, 6)]
for harmonic_freq in harmonics_freqs:
    if harmonics_range_start <= harmonic_freq <= harmonics_range_end:
        harmonic_amplitude = 20 * np.log10(np.abs(positive_fft[np.argmin(np.abs(positive_freqs - harmonic_freq))]))
        plt.plot(harmonic_freq, harmonic_amplitude, 'rx', label=f'Harmonic Frequency ({harmonic_freq:.2f} Hz)')

# Mark the noise bands (assumed to be high-frequency bands and low-frequency bands that do not contribute to the perceived sound)
# Noise typically resides in frequencies below 85 Hz and above 8 kHz
low_noise_band_end = 85  # 85 Hz
high_noise_band_start = 8000  # 8 kHz
plt.axvspan(positive_freqs[0], low_noise_band_end, color='red', alpha=0.2, label='Low-Frequency Noise Band < 85Hz')
plt.axvspan(high_noise_band_start, max(positive_freqs), color='red', alpha=0.2, label='High-Frequency Noise Band > 8KHz')

plt.legend()
plt.savefig('frequency_domain_plot.svg', format='svg')
plt.show()
