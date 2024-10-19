import numpy as np
from scipy.io import wavfile
from scipy.io.wavfile import write

# Load the original audio file
file_path = '/home/basav/DSP/Digital-Signal-Processing/Assignment_1_FFT/audio files/orig.wav'
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

# Step 7: Inverse FFT to return to time domain after smoothing
improved_audio_data = np.fft.ifft(filtered_fft_data_cleaned)
improved_audio_data_real = np.real(improved_audio_data)

# Normalize the final output
def normalize_signal(signal):
    max_amplitude = np.max(np.abs(signal))
    return signal / max_amplitude if max_amplitude != 0 else signal

final_improved_audio_data_normalized = normalize_signal(improved_audio_data_real)

# Save the final improved audio
output_file_improved = "pleasant_and_interesting.wav"
write(output_file_improved, sampling_rate, np.int16(final_improved_audio_data_normalized * 32767))

print("Improved audio saved as 'pleasant_and_interesting.wav'")