import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.io.wavfile import write

# Load the original audio file
file_path = "/home/basav/DSP/Digital-Signal-Processing/Lab 1 test 2.wav"
sampling_rate, audio_data = wavfile.read(file_path)

# Fourier Transform of the original audio signal
fft_data = np.fft.fft(audio_data)
fft_freq = np.fft.fftfreq(len(fft_data), d=1/sampling_rate)

# Create a custom filter in the frequency domain with a smoother transition
def manual_filter_tuned(fft_data, fft_freq, cutoff_low, cutoff_high, boost_factor=2):
    # Copy the FFT data to manipulate
    filtered_fft_data = np.copy(fft_data)

    # Smoother transition: Apply a ramp between cutoff_low and cutoff_high frequencies
    transition_band = (np.abs(fft_freq) >= cutoff_low) & (np.abs(fft_freq) <= cutoff_high)
    
    # Apply smooth reduction in amplitude for frequencies above cutoff_high (reduce noise)
    filtered_fft_data[np.abs(fft_freq) > cutoff_high] = 0
    
    # Boost factor: enhance frequencies between cutoff_low and cutoff_high
    filtered_fft_data[transition_band] *= boost_factor

    return filtered_fft_data

# Parameters
cutoff_low = 3000   # 3kHz, below which we cut frequencies
cutoff_high = 8000  # 8kHz, above which we treat as noise and remove
boost_factor = 3    # Reduced boost factor to avoid distortion

# Apply the tuned manual filter
filtered_fft_data = manual_filter_tuned(fft_data, fft_freq, cutoff_low, cutoff_high, boost_factor)

# Perform Inverse FFT to get back to time domain
filtered_audio_data = np.fft.ifft(filtered_fft_data)

# Normalize the output to avoid clipping
filtered_audio_data = np.real(filtered_audio_data)
filtered_audio_data /= np.max(np.abs(filtered_audio_data))

# Save the enhanced audio
output_exciter_path = "/home/basav/DSP/Digital-Signal-Processing/enhanced_audio_manual_filter_tuned.wav"
write(output_exciter_path, sampling_rate, np.int16(filtered_audio_data * 32767))  # Convert to 16-bit PCM

print("Enhanced audio saved as 'enhanced_audio_manual_filter_tuned.wav'")

# Plotting the frequency spectrum before and after filtering
plt.figure(figsize=(10, 6))

# Plot original frequency spectrum
plt.subplot(2, 1, 1)
plt.plot(fft_freq[:len(fft_freq)//2], 20 * np.log10(np.abs(fft_data[:len(fft_data)//2])), label="Original Spectrum")
plt.xlim(0, 20000)  # Up to 20kHz
plt.title("Original Frequency Spectrum")
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude [dB]')
plt.grid(True)

# Plot filtered frequency spectrum
plt.subplot(2, 1, 2)
plt.plot(fft_freq[:len(fft_freq)//2], 20 * np.log10(np.abs(filtered_fft_data[:len(filtered_fft_data)//2])), label="Filtered Spectrum", color='red')
plt.xlim(0, 20000)  # Up to 20kHz
plt.title("Filtered Frequency Spectrum (Tuned Manual Filter)")
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude [dB]')
plt.grid(True)

# Show plots
plt.tight_layout()
plt.show()