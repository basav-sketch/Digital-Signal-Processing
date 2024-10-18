import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.io.wavfile import write

# Load the original audio file
file_path = "Lab 1 test 2.wav"
sampling_rate, audio_data = wavfile.read(file_path)

# Step 1: Isolate the first half second (where the noise is present)
half_second_samples = int(0.5 * sampling_rate)
first_half_second = audio_data[:half_second_samples]

# Step 2: Perform FFT on the first half second
fft_first_half = np.fft.fft(first_half_second)

# Step 3: Set the frequency components of the noise to zero
fft_first_half_cleaned = np.zeros_like(fft_first_half)  # Zero out all frequency components

# Step 4: Perform Inverse FFT to get back the time-domain signal (cleaned-up first half second)
cleaned_first_half_second = np.real(np.fft.ifft(fft_first_half_cleaned))

# Step 5: Reconstruct the full audio by combining cleaned first half with the rest of the audio
cleaned_audio_data = np.concatenate((cleaned_first_half_second, audio_data[half_second_samples:]))

# Step 6: Perform FFT on the cleaned full audio
fft_data_cleaned = np.fft.fft(cleaned_audio_data)
fft_freq_cleaned = np.fft.fftfreq(len(fft_data_cleaned), d=1/sampling_rate)

# Custom smoother filter for frequencies between 3kHz and 10kHz with smooth transition
def smooth_transition_filter(fft_freq, cutoff_low, cutoff_high):
    mask = np.ones_like(fft_freq)  # Start by keeping all frequencies
    transition_band = (np.abs(fft_freq) > cutoff_low) & (np.abs(fft_freq) <= cutoff_high)
    mask[transition_band] = (cutoff_high - np.abs(fft_freq[transition_band])) / (cutoff_high - cutoff_low)
    return mask

# Apply the smooth filter (for frequencies between 3kHz and 10kHz)
cutoff_low = 3000  # 3kHz
cutoff_high = 10000  # 10kHz
filter_mask_cleaned = smooth_transition_filter(fft_freq_cleaned, cutoff_low, cutoff_high)
filtered_fft_data_cleaned = fft_data_cleaned * filter_mask_cleaned

# Step 7: Apply Aural Exciter using a non-linearity (tanh) in the 3kHz to 10kHz range
def apply_aural_exciter(fft_data, fft_freq, exciter_range=(3000, 10000)):
    exciter_band = (np.abs(fft_freq) >= exciter_range[0]) & (np.abs(fft_freq) <= exciter_range[1])
    excited_fft_data = np.zeros_like(fft_data)  # Start with zeros
    excited_fft_data[exciter_band] = np.tanh(fft_data[exciter_band])  # Apply non-linearity only to this band
    return excited_fft_data

# Apply the exciter to the smooth-filtered FFT data (only between 3kHz and 10kHz)
exciter_range = (3000, 10000)  # Frequency range for the exciter
excited_fft_data = apply_aural_exciter(filtered_fft_data_cleaned, fft_freq_cleaned, exciter_range)

# Step 8: Add the excited frequencies back to the original signal
scaling_factor = 0.3  # Scale the excited data to add a smaller amount to the original
enhanced_fft_data = fft_data_cleaned + scaling_factor * excited_fft_data  # Add back the enhanced frequencies

# Optional: limit the frequency band post-excitation (but ensure frequencies up to 10kHz are preserved)
def limit_frequency_band(fft_data, fft_freq, limit_range=(85, 10000)):
    limited_fft_data = np.copy(fft_data)
    limit_band = (np.abs(fft_freq) > limit_range[1])  # Only limit frequencies above 10kHz
    limited_fft_data[limit_band] = 0  # Zero out frequencies above 10kHz
    return limited_fft_data

# Apply frequency limitation if needed (limiting frequencies above 10kHz)
limited_enhanced_fft_data = limit_frequency_band(enhanced_fft_data, fft_freq_cleaned, limit_range=(85, 10000))

# Step 9: Inverse FFT to return to time domain after excitation and enhancement
final_enhanced_audio_data = np.fft.ifft(limited_enhanced_fft_data)
final_enhanced_audio_data_real = np.real(final_enhanced_audio_data)

# Normalize the final output
def normalize_signal(signal):
    max_amplitude = np.max(np.abs(signal))
    return signal / max_amplitude if max_amplitude != 0 else signal

final_enhanced_audio_data_normalized = normalize_signal(final_enhanced_audio_data_real)

# Save the final cleaned and enhanced audio
output_file_enhanced = "10filteraddedfinal_enhanced_audio_same.wav"
write(output_file_enhanced, sampling_rate, np.int16(final_enhanced_audio_data_normalized * 32767))

# Plot final enhanced audio in time domain
time_axis_full = np.linspace(0, len(cleaned_audio_data) / sampling_rate, len(cleaned_audio_data))
plt.figure(figsize=(10, 6))
plt.plot(time_axis_full, final_enhanced_audio_data_normalized)
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.title('Final Enhanced Audio - Time Domain')
plt.grid()
plt.savefig('final_enhanced_time_domain.svg', format='svg')
plt.show()

# Plot final enhanced audio in frequency domain
final_enhanced_fft = np.fft.fft(final_enhanced_audio_data_normalized)
plt.figure(figsize=(10, 6))
plt.plot(fft_freq_cleaned[:len(fft_freq_cleaned)//2], 20 * np.log10(np.abs(final_enhanced_fft[:len(final_enhanced_fft)//2])))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude (dB)')
plt.title('Final Enhanced Audio - Frequency Domain')
plt.grid()
plt.savefig('final_enhanced_frequency_domain.svg', format='svg')
plt.show()

print("Final enhanced audio saved as '10filteraddedfinal_enhanced_audio_same.wav'")
