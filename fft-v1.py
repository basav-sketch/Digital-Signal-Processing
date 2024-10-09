import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import spectrogram
from scipy.signal import butter, filtfilt
from scipy.io.wavfile import write

# TASK - 1 - LOADING THE WAV FILE AND PLOTTING GRAPHS

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

# TASK - 2 - APPLY FOURIER TRANSFORM (FFT) AND FIND FUNDAMENTAL FREQ., HARMONICS AND NOISE

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

# Plot Frequency Spectrum with Peaks Marked for finding fundamental freq. (85-255HZ)
plt.figure(figsize=(10, 6))
plt.plot(positive_frequencies, 20*np.log10(positive_magnitude))
plt.plot(positive_frequencies[peaks], 20*np.log10(positive_magnitude[peaks]), "x")
plt.xlim(0, 255)  # Focus on frequencies up to 20kHz
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude [dB]')
plt.title('Frequency Domain Signal with Peaks')
plt.grid(True)
plt.show()

# Print the identified peak frequencies
print("Peak Frequencies (Hz):", positive_frequencies[peaks])

# Compute the spectrogram (frequency vs. time)
frequencies, times, Sxx = spectrogram(audio_data, fs=sampling_rate)

# Plot the spectrogram
plt.figure(figsize=(10, 6))
plt.pcolormesh(times, frequencies, 10 * np.log10(Sxx), shading='gouraud')
plt.colorbar(label='Intensity [dB]')
plt.ylim(0, 5000)  # Focus on lower frequencies (up to 5kHz)
plt.xlabel('Time [s]')
plt.ylabel('Frequency [Hz]')
plt.title('Spectrogram (Frequency vs. Time)')
plt.show()

# TASK - 3 - IMPROVING VOICE QUALITY

# Design a band-pass filter 
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

# Apply the band-pass filter to the audio signal
def apply_bandpass_filter(data, lowcut,highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    filtered_data = filtfilt(b, a, data)
    return filtered_data

# Apply the filter to the audio signal
lowcut = 300.0  # Low cut-off frequency in Hz
highcut = 3000.0  # High cut-off frequency in Hz
filtered_audio_data_bandpass = apply_bandpass_filter(audio_data, lowcut, highcut, sampling_rate)

# Plot the original and filtered frequency spectra to compare
fft_original = np.fft.fft(audio_data)
fft_filtered_bandpass = np.fft.fft(filtered_audio_data_bandpass)

# Plot original audio frequency spectrum
plt.figure(figsize=(10, 6))
plt.plot(fft_freq[:len(fft_freq)//2], 20 * np.log10(np.abs(fft_original[:len(fft_original)//2])), label="Original Audio")
plt.plot(fft_freq[:len(fft_freq)//2], 20 * np.log10(np.abs(fft_filtered_bandpass[:len(fft_filtered_bandpass)//2])), label="Filtered Audio (Band-pass)", linestyle='--')
plt.xlim(0, 20000)  # Show up to 20kHz
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude [dB]')
plt.title('Frequency Domain: Original vs. Band-pass Filtered')
plt.legend()
plt.grid(True)
plt.show()

# Save the filtered band-pass audio to a new file
output_bandpass_path = "/home/basav/DSP/Digital-Signal-Processing/filtered_bandpass_audio.wav"
write(output_bandpass_path, sampling_rate, np.int16(filtered_audio_data_bandpass * 32767))  # Convert back to 16-bit PCM


# You can now play the audio using any media player
print("Filtered audio saved as 'filtered_bandpass_audio.wav'")
