import matplotlib.pyplot as plt
import numpy as np
import wave
import scipy.fftpack as fftpack

# Load the audio file
audio_file_path = 'Lab 1 test 2.wav'

with wave.open(audio_file_path, 'r') as wav_file:
    # Extract Raw Audio from Wav File
    n_channels, sample_width, frame_rate, n_frames, _, _ = wav_file.getparams()
    audio_frames = wav_file.readframes(n_frames)

# Convert audio frames to numpy array
audio_signal = np.frombuffer(audio_frames, dtype=np.int16)

# Normalize the audio signal to the range -1 to 1
audio_signal = audio_signal / (2**(8*sample_width-1))

# Create a time axis in seconds
time_axis = np.linspace(0, n_frames / frame_rate, num=n_frames)

# Plot the audio signal in the time domain
plt.figure(figsize=(10, 6))
plt.plot(time_axis, audio_signal)
plt.xlabel('Time (seconds)')
plt.ylabel('Normalized Amplitude')
plt.title('Audio Signal in Time Domain')
plt.grid()
plt.savefig('time_domain_plot.svg', format='svg')
plt.show()

# Plot the audio signal in the frequency domain
# Perform Fourier Transform
audio_fft = np.fft.fft(audio_signal)
frequencies = np.fft.fftfreq(len(audio_fft), d=1/frame_rate)

# Use only the positive frequencies
positive_freqs = frequencies[:len(frequencies)//2]
positive_fft = audio_fft[:len(audio_fft)//2]

# Convert amplitude to dB
amplitude_db = 20 * np.log10(np.abs(positive_fft))

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

# Mark the harmonics in the harmonics range (2x to 5x)
harmonics_freqs = [fundamental_freq * i for i in range(2, 6)]
for harmonic_freq in harmonics_freqs:
    if harmonics_range_start <= harmonic_freq <= harmonics_range_end:
        harmonic_amplitude = 20 * np.log10(np.abs(positive_fft[np.argmin(np.abs(positive_freqs - harmonic_freq))]))
        plt.plot(harmonic_freq, harmonic_amplitude, 'bo', label=f'Harmonic Frequency ({harmonic_freq:.2f} Hz)')

# Mark the noise bands (assumed to be high-frequency bands and low-frequency bands that do not contribute to the perceived sound)
# Noise typically resides in frequencies below 85 Hz and above 8 kHz
low_noise_band_end = 85  # 85 Hz
high_noise_band_start = 8000  # 8 kHz
plt.axvspan(positive_freqs[0], low_noise_band_end, color='red', alpha=0.2, label='Low-Frequency Noise Band')
plt.axvspan(high_noise_band_start, max(positive_freqs), color='red', alpha=0.2, label='High-Frequency Noise Band')

plt.legend()
plt.savefig('frequency_domain_plot.svg', format='svg')
plt.show()