import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import butter, filtfilt
from scipy.io.wavfile import write

# Design a band-pass filter
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

# Apply the band-pass filter to the audio signal
def apply_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    filtered_data = filtfilt(b, a, data)
    return filtered_data

# Load the original audio file
file_path = "/home/basav/DSP/Digital-Signal-Processing/Lab 1 test 2.wav"
sampling_rate, audio_data = wavfile.read(file_path)

# Apply the band-pass filter (300 Hz to 3kHz)
lowcut = 300.0  # Low cut-off frequency in Hz
highcut = 3000.0  # High cut-off frequency in Hz
filtered_audio_data_bandpass = apply_bandpass_filter(audio_data, lowcut, highcut, sampling_rate)

# Plot the original and filtered frequency spectra to compare
fft_original = np.fft.fft(audio_data)
fft_filtered_bandpass = np.fft.fft(filtered_audio_data_bandpass)
fft_freq = np.fft.fftfreq(len(fft_original), d=1/sampling_rate)

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
print("Filtered audio saved as 'filtered_bandpass_audio.wav'")

# Now apply the Fourier Transform to the **band-pass filtered** audio
fft_data = np.fft.fft(filtered_audio_data_bandpass)
fft_freq = np.fft.fftfreq(len(fft_data), d=1/sampling_rate)

# Zero out frequencies below 3kHz
fft_data[np.abs(fft_freq) < 3000] = 0

# Optionally boost frequencies above 3kHz
boost_factor = 1.5  # Adjust this factor as needed
fft_data[np.abs(fft_freq) >= 3000] *= boost_factor

# Apply Inverse FFT to get the modified audio signal back
enhanced_audio_data = np.fft.ifft(fft_data)

# Normalize the enhanced audio
enhanced_audio_data = enhanced_audio_data.real / np.max(np.abs(enhanced_audio_data), axis=0)  # Keep real part

# Save the enhanced audio
output_exciter_path = "/home/basav/DSP/Digital-Signal-Processing/enhanced_audio_fft.wav"
write(output_exciter_path, sampling_rate, np.int16(enhanced_audio_data * 32767))  # Convert back to 16-bit PCM
print("Enhanced audio saved as 'enhanced_audio_fft.wav'")
