
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import spectrogram
from scipy.io.wavfile import write

# Read the audio file at the beginning
file_path = "/home/basav/Downloads/P.wav"  # Replace with the actual path to the letter's audio file
letter_name = "P"  # Replace with the corresponding letter name
output_file = "processed_letter_EE.wav"  # Replace with the output file name
spectrogram_svg_file = "spectrogram_P.pdf"

# Load the audio file
sampling_rate, audio_data = wavfile.read(file_path)

# Function to process the audio, perform FFT, plot frequency domain, spectrogram, and save the processed file
def process_audio_letter(audio_data, sampling_rate, letter_name, output_file):
    # Perform FFT on the audio data
    fft_data = np.fft.fft(audio_data)
    fft_freqs = np.fft.fftfreq(len(fft_data), d=1/sampling_rate)
    
    # Take the absolute values of the FFT to get the magnitude spectrum
    fft_magnitude = np.abs(fft_data)

  

    # Plot the spectrogram
    f, t, Sxx = spectrogram(audio_data, fs=sampling_rate)
    plt.figure(figsize=(10, 6))
    plt.pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud')
    plt.ylabel('Frequency (Hz)')
    plt.xlabel('Time (s)')
    plt.title(f'Spectrogram of {letter_name}')
    plt.colorbar(label='Amplitude (dB)')
    plt.ylim(0, 20000)  # Limit to 20kHz for clarity
    plt.show()

    # Save the spectrogram as an SVG file
    plt.savefig(spectrogram_svg_file, format='pdf')

    # Inverse FFT to convert back to time domain (after processing in frequency domain)
    processed_audio_data = np.fft.ifft(fft_data)
    processed_audio_data_real = np.real(processed_audio_data)

    # Normalize the final output
    def normalize_signal(signal):
        max_amplitude = np.max(np.abs(signal))
        return signal / max_amplitude if max_amplitude != 0 else signal

    normalized_audio_data = normalize_signal(processed_audio_data_real)

    # Save the final processed and normalized audio to a file
    write(output_file, sampling_rate, np.int16(normalized_audio_data * 32767))

    print(f"Final processed audio saved as '{output_file}'")

# Call the function with loaded audio
process_audio_letter(audio_data, sampling_rate, letter_name, output_file)