import numpy as np
from scipy.io import wavfile
from scipy.io.wavfile import write

# Load the improved audio file
file_path = '/home/basav/DSP/Digital-Signal-Processing/Assignment_1_FFT/audio files/pleasant_and_interesting.wav'
sampling_rate, audio_data = wavfile.read(file_path)

# Step 1: Perform FFT on the cleaned full audio
fft_data_cleaned = np.fft.fft(audio_data)
fft_freq_cleaned = np.fft.fftfreq(len(fft_data_cleaned), d=1/sampling_rate)

# Step 2: Apply Aural Exciter using a non-linearity (tanh) in the 3kHz to 10kHz range
def apply_aural_exciter(fft_data, fft_freq, exciter_range=(3000, 10000)):
    exciter_band = (np.abs(fft_freq) >= exciter_range[0]) & (np.abs(fft_freq) <= exciter_range[1])
    excited_fft_data = np.zeros_like(fft_data)  # Start with zeros
    excited_fft_data[exciter_band] = np.tanh(fft_data[exciter_band])  # Apply non-linearity only to this band
    return excited_fft_data

# Apply the exciter to the FFT data (only between 3kHz and 10kHz)
exciter_range = (3000, 10000)  # Frequency range for the exciter
excited_fft_data = apply_aural_exciter(fft_data_cleaned, fft_freq_cleaned, exciter_range)

# Step 3: Add the excited frequencies back to the original signal
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

# Step 4: Inverse FFT to return to time domain after excitation and enhancement
final_enhanced_audio_data = np.fft.ifft(limited_enhanced_fft_data)
final_enhanced_audio_data_real = np.real(final_enhanced_audio_data)

# Normalize the final output
def normalize_signal(signal):
    max_amplitude = np.max(np.abs(signal))
    return signal / max_amplitude if max_amplitude != 0 else signal

final_enhanced_audio_data_normalized = normalize_signal(final_enhanced_audio_data_real)

# Save the final enhanced audio
output_file_enhanced = "exited.wav"
write(output_file_enhanced, sampling_rate, np.int16(final_enhanced_audio_data_normalized * 32767))

print("Final enhanced audio saved as 'exited.wav'")
