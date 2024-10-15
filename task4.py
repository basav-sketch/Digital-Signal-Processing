import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.io.wavfile import write

# Load the original audio file
file_path = "/home/basav/DSP/Digital-Signal-Processing/Lab 1 test 2.wav"
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

# Step 6: Apply the same filtering, boosting, and normalization process to the entire audio
fft_data_cleaned = np.fft.fft(cleaned_audio_data)
fft_freq_cleaned = np.fft.fftfreq(len(fft_data_cleaned), d=1/sampling_rate)

# Custom smoother filter
def smooth_transition_filter(fft_freq, cutoff_low, cutoff_high):
    mask = np.zeros_like(fft_freq)
    mask[np.abs(fft_freq) <= cutoff_low] = 1
    transition_band = (np.abs(fft_freq) > cutoff_low) & (np.abs(fft_freq) <= cutoff_high)
    mask[transition_band] = (cutoff_high - np.abs(fft_freq[transition_band])) / (cutoff_high - cutoff_low)
    return mask

# Apply the filter
cutoff_low = 3000  # 3kHz
cutoff_high = 6000  # 8kHz
filter_mask_cleaned = smooth_transition_filter(fft_freq_cleaned, cutoff_low, cutoff_high)
filtered_fft_data_cleaned = fft_data_cleaned * filter_mask_cleaned

# Manual frequency boost
def manual_frequency_boost(fft_data, fft_freq, boost_range=(85, 4000), boost_factor=2):
    boosted_fft_data = np.copy(fft_data)
    boost_band = (np.abs(fft_freq) >= boost_range[0]) & (np.abs(fft_freq) <= boost_range[1])
    for i in range(len(boosted_fft_data)):
        if boost_band[i]:
            boosted_fft_data[i] *= boost_factor
    return boosted_fft_data

boosted_fft_data_cleaned = manual_frequency_boost(filtered_fft_data_cleaned, fft_freq_cleaned, boost_range=(1000, 4000), boost_factor=1.5)

# Gain boost
def manual_gain_boost(fft_data, boost_factor=1.2):
    return fft_data * boost_factor

boosted_fft_data_cleaned = manual_gain_boost(boosted_fft_data_cleaned, boost_factor=1.2)

# Normalize the final output
def normalize_signal(signal):
    max_amplitude = np.max(np.abs(signal))
    return signal / max_amplitude if max_amplitude != 0 else signal

# Inverse FFT to return to time domain
final_audio_data_cleaned = np.fft.ifft(boosted_fft_data_cleaned)
final_audio_data_cleaned_real = np.real(final_audio_data_cleaned)
final_audio_data_cleaned_normalized = normalize_signal(final_audio_data_cleaned_real)

# Save the final cleaned and enhanced audio
output_file_cleaned = "FINAL_cleaned_audio.wav"
write(output_file_cleaned, sampling_rate, np.int16(final_audio_data_cleaned_normalized * 32767))

print("FINAL cleaned audio saved as 'final_cleaned_audio.wav'")

# Plotting the frequency spectrum before and after cleaning
plt.figure(figsize=(10, 6))

