import numpy as np
import matplotlib.pyplot as plt

# Function to calculate FIR filter coefficients
def Filter_coeff(fs, highpass_cutoff, bandstop_start, bandstop_stop):
    delta_f = highpass_cutoff  # Frequency resolution in Hz
    M = fs // delta_f  # Filter order
    if M % 2 == 0:
        M += 1  # Ensure odd number of coefficients for symmetry
    n = np.arange(-M // 2, M // 2 + 1)  # Sample indices
    highpass_cutoff /= fs  # Normalize cutoff frequencies
    bandstop_start /= fs
    bandstop_stop /= fs
    
    # Sinc function for highpass and bandstop filters
    h_highpass = np.where(n == 0, 1 - 2 * highpass_cutoff, -2 * highpass_cutoff * np.sinc(2 * highpass_cutoff * n))
    h_bandstop = np.where(n == 0, 1 - (2 * bandstop_start - 2 * bandstop_stop),
                          2 * bandstop_start * np.sinc(2 * bandstop_start * n) - 2 * bandstop_stop * np.sinc(2 * bandstop_stop * n))
    
    # Combine filters without windowing
    coefficients_nowindow = np.convolve(h_highpass, h_bandstop, mode="same")
    
    # Apply Blackman window
    coefficients_windowed = coefficients_nowindow * np.blackman(len(coefficients_nowindow))
    coefficients_windowed /= np.sum(coefficients_windowed)  # Normalize
    
    # Plot coefficients vs. sample index
    plt.figure(figsize=(10, 6))
    plt.stem(coefficients_windowed, basefmt=" ", linefmt="b-", markerfmt="bo")
    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude")
    plt.title("FIR Filter Coefficients (After Windowing)")
    plt.grid()
    plt.savefig("Filter_Coefficients_Sample_Index.svg", format="svg")
    plt.show()

    # Frequency-domain visualization
    fft_nowindow = np.abs(np.fft.fft(coefficients_nowindow, n=2048))
    fft_windowed = np.abs(np.fft.fft(coefficients_windowed, n=2048))
    freqs = np.fft.fftfreq(len(fft_nowindow), d=1/fs)

    # Subplots for frequency domain comparison
    plt.figure(figsize=(12, 6))

    # Without windowing
    plt.subplot(1, 2, 1)
    plt.plot(freqs[:len(fft_nowindow)//2], 20 * np.log10(fft_nowindow[:len(fft_nowindow)//2]), label="No Window")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (dB)")
    plt.title("Frequency Response (No Window)")
    plt.grid()
    plt.legend()

    # With windowing
    plt.subplot(1, 2, 2)
    plt.plot(freqs[:len(fft_windowed)//2], 20 * np.log10(fft_windowed[:len(fft_windowed)//2]), label="Blackman Window")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (dB)")
    plt.title("Frequency Response (With Window)")
    plt.grid()
    plt.legend()

    plt.tight_layout()
    plt.savefig("Filter_Frequency_Comparison.svg", format="svg")
    plt.show()

    return coefficients_windowed


# FIR Filter Class
class FIRfilter:
    def __init__(self, coefficients):
        self.ntaps = len(coefficients)
        self.coefficients = coefficients
        self.buffer = np.zeros(self.ntaps)

    def dofilter(self, v):
        self.buffer = np.roll(self.buffer, 1)  # Circular buffer
        self.buffer[0] = v
        return np.dot(self.buffer, self.coefficients)


# Filter signals sample-by-sample
def filter_signal(signal, fir_filter):
    return [fir_filter.dofilter(sample) for sample in signal]


# Load signals
noisy_signal_file = "/home/basav/DSP/Digital-Signal-Processing/Assignment_2_FIR/Noisy_ECG_1000Hz_9.dat"
clean_signal_file = "/home/basav/DSP/Digital-Signal-Processing/Assignment_2_FIR/Lying_ECG_1000Hz_9.dat"
ecg_noisy_signal = np.loadtxt(noisy_signal_file)
ecg_clean_signal = np.loadtxt(clean_signal_file)

# Filter parameters
fs = 1000
highpass_cutoff = 1
bandstop_start = 45
bandstop_stop = 55

# Calculate FIR coefficients
coefficients = Filter_coeff(fs, highpass_cutoff, bandstop_start, bandstop_stop)

# Initialize FIR filter
fir_filter = FIRfilter(coefficients)

# Filter noisy and clean signals
filtered_noisy_ecg = filter_signal(ecg_noisy_signal, fir_filter)
filtered_clean_ecg = filter_signal(ecg_clean_signal, fir_filter)

# Plot the original and filtered noisy ECG signals
plt.figure(figsize=(12, 8))
plt.subplot(2, 1, 1)
plt.plot(ecg_noisy_signal, label="Original Noisy ECG", color="blue")
plt.xlabel("Time (samples)")
plt.ylabel("Amplitude (mV)")
plt.title("Original Noisy ECG Signal")
plt.grid()
plt.legend()
plt.subplot(2, 1, 2)
plt.plot(filtered_noisy_ecg, label="Filtered Noisy ECG", color="red")
plt.xlabel("Time (samples)")
plt.ylabel("Amplitude (mV)")
plt.title("FIR_Filtered Noisy ECG Signal")
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()

# Plot the original and filtered clean ECG signals
plt.figure(figsize=(12, 8))
plt.subplot(2, 1, 1)
plt.plot(ecg_clean_signal, label="Original Clean ECG", color="green")
plt.xlabel("Time (samples)")
plt.ylabel("Amplitude (mV)")
plt.title("Original Clean ECG Signal")
plt.grid()
plt.legend()
plt.subplot(2, 1, 2)
plt.plot(filtered_clean_ecg, label="Filtered Clean ECG", color="red")
plt.xlabel("Time (samples)")
plt.ylabel("Amplitude (mV)")
plt.title("FIR_Filtered Clean ECG Signal")
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()
