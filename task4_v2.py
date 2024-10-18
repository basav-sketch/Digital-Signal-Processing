import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.io.wavfile import write

# Load the filtered and cleaned audio (from previous step)
file_path = "/home/basav/DSP/Digital-Signal-Processing/FINAL_cleaned_audio.wav"
sampling_rate, cleaned_audio_data = wavfile.read(file_path)

# Step 1: Isolate high frequencies (e.g., above 3 kHz)
def isolate_high_frequencies(signal, fft_freq, cutoff=3000):
    fft_signal = np.fft.fft(signal)
    high_freq_indices = np.abs(fft_freq) > cutoff
    isolated_high_freq = np.zeros_like(fft_signal)
    isolated_high_freq[high_freq_indices] = fft_signal[high_freq_indices]
    return isolated_high_freq

# Step 2: Apply non-linearity (tanh)
def apply_nonlinearity(signal):
    return np.tanh(signal)

# Step 3: Combine the processed high frequencies with the original signal
def combine_with_original(original_signal, processed_high_freq):
    ifft_processed = np.fft.ifft(processed_high_freq).real
    # Combine the two signals
    combined_signal = original_signal + ifft_processed
    # Normalize to avoid clipping
    return combined_signal / np.max(np.abs(combined_signal))

# Fourier Transform of the cleaned audio
fft_cleaned = np.fft.fft(cleaned_audio_data)
fft_freq = np.fft.fftfreq(len(cleaned_audio_data), d=1/sampling_rate)

# Isolate high frequencies (above 3kHz)
isolated_high_freq = isolate_high_frequencies(cleaned_audio_data, fft_freq, cutoff=3000)

# Apply tanh non-linearity to enhance the high frequencies
enhanced_high_freq = apply_nonlinearity(isolated_high_freq)

# Combine the enhanced high frequencies with the original audio
aural_excited_audio = combine_with_original(cleaned_audio_data, enhanced_high_freq)

# Normalize and save the final audio with aural exciter effect
aural_excited_audio_normalized = aural_excited_audio / np.max(np.abs(aural_excited_audio))
output_excited_audio = "aural_excited_audio.wav"
write(output_excited_audio, sampling_rate, np.int16(aural_excited_audio_normalized * 32767))

print("Aural Excited audio saved as 'aural_excited_audio.wav'")

# Plotting the frequency spectrum before and after Aural Excitation
plt.figure(figsize=(10, 6))

# Plot original cleaned audio spectrum
plt.subplot(2, 1, 1)
plt.plot(fft_freq[:len(fft_freq)//2], 20 * np.log10(np.abs(fft_cleaned[:len(fft_cleaned)//2])), label="Cleaned Audio")
plt.title("Cleaned Audio Frequency Spectrum")
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude [dB]')
plt.grid(True)

# Plot aural excited audio spectrum
fft_excited = np.fft.fft(aural_excited_audio_normalized)
plt.subplot(2, 1, 2)
plt.plot(fft_freq[:len(fft_freq)//2], 20 * np.log10(np.abs(fft_excited[:len(fft_excited)//2])), label="Aural Excited Audio", color='orange')
plt.title("Aural Excited Audio Frequency Spectrum")
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude [dB]')
plt.grid(True)

plt.tight_layout()
plt.show()