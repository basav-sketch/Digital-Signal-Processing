import numpy as np
import matplotlib.pyplot as plt

class FIR_filter:
    def __init__(self, coefficients):
        self.ntaps = len(coefficients)
        self.coefficients = coefficients
        self.buffer = np.zeros(self.ntaps)

    def filter(self, v):
        self.buffer = np.roll(self.buffer, 1)
        self.buffer[0] = v
        return np.dot(self.buffer, self.coefficients)

    def lms(self, error, mu=0.01):
        self.coefficients += error * mu * self.buffer

def Filter_coeff(fs, highpass_cutoff, bandstop_start, bandstop_stop):
    delta_f = highpass_cutoff
    M = fs // delta_f
    if M % 2 == 0:
        M += 1
    n = np.arange(-M // 2, M // 2 + 1)
    highpass_cutoff /= fs
    bandstop_start /= fs
    bandstop_stop /= fs

    h_highpass = np.where(n == 0, 1 - 2 * highpass_cutoff, -2 * highpass_cutoff * np.sinc(2 * highpass_cutoff * n))
    h_bandstop = np.where(n == 0, 1 - (2 * bandstop_start - 2 * bandstop_stop),
                          2 * bandstop_start * np.sinc(2 * bandstop_start * n) - 2 * bandstop_stop * np.sinc(2 * bandstop_stop * n))
    coefficients_nowindow = np.convolve(h_highpass, h_bandstop, mode="same")
    coefficients_windowed = coefficients_nowindow * np.blackman(len(coefficients_nowindow))
    coefficients_windowed /= np.sum(coefficients_windowed)
    return coefficients_windowed

# Parameters
fs = 1000
NTAPS = 1000
LEARNING_RATE = 0.001
fnoise = 50

# Load ECG data
noisy_ecg = np.loadtxt("/home/basav/DSP/Digital-Signal-Processing/Assignment_2_FIR/Noisy_ECG_1000Hz_9.dat")
clean_ecg = np.loadtxt("/home/basav/DSP/Digital-Signal-Processing/Assignment_2_FIR/Lying_ECG_1000Hz_9.dat")

# DC component estimation
dc_component_noisy = 0.1
dc_component_clean = 0.1

# FIR Filter Coefficients
fir_coefficients = Filter_coeff(fs, 1, 45, 55)

# Apply FIR Filtering
fir_filter = FIR_filter(fir_coefficients)
fir_filtered_noisy = [fir_filter.filter(sample) for sample in noisy_ecg]
fir_filtered_clean = [fir_filter.filter(sample) for sample in clean_ecg]

# LMS Filtering
def apply_lms_filter(ecg_signal, reference_noise, ntaps, learning_rate):
    lms_filter = FIR_filter(np.zeros(ntaps))
    lms_filtered_signal = np.empty_like(ecg_signal)
    for i in range(len(ecg_signal)):
        noise_estimation = lms_filter.filter(reference_noise[i])
        error = ecg_signal[i] - noise_estimation
        lms_filter.lms(error, learning_rate)
        lms_filtered_signal[i] = error
    return lms_filtered_signal

# Generate Reference Noise
reference_noise_noisy = np.sin(2.0 * np.pi * fnoise / fs * np.arange(len(noisy_ecg))) + dc_component_noisy
reference_noise_clean = np.sin(2.0 * np.pi * fnoise / fs * np.arange(len(clean_ecg))) + dc_component_clean

# Apply LMS Filtering
lms_filtered_noisy = apply_lms_filter(noisy_ecg, reference_noise_noisy, NTAPS, LEARNING_RATE)
lms_filtered_clean = apply_lms_filter(clean_ecg, reference_noise_clean, NTAPS, LEARNING_RATE)

# DC Components
dc_fir_noisy = np.mean(fir_filtered_noisy)
dc_lms_noisy = np.mean(lms_filtered_noisy)
dc_fir_clean = np.mean(fir_filtered_clean)
dc_lms_clean = np.mean(lms_filtered_clean)

# Plotting
def plot_fir_lms_comparison(original, fir_filtered, lms_filtered, title_prefix, filename_prefix, sample_limit=30000):
    plt.figure(figsize=(12, 8))

    # FIR Filtered
    plt.subplot(2, 1, 1)
    plt.plot(original[:sample_limit], label="Original Signal", alpha=0.6, color="blue")
    plt.plot(fir_filtered[:sample_limit], label="FIR Filtered Signal", color="green")
    plt.title(f"{title_prefix}: FIR Filtered Signal")
    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid()

    # LMS Filtered
    plt.subplot(2, 1, 2)
    plt.plot(original[:sample_limit], label="Original Signal", alpha=0.6, color="blue")
    plt.plot(lms_filtered[:sample_limit], label="LMS Filtered Signal", color="red")
    plt.title(f"{title_prefix}: LMS Filtered Signal")
    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.savefig(f"{filename_prefix}.svg", format="svg")
    plt.show()

def plot_single_heartbeat(ecg_signal, fs, title, filename, window=0.5):
    """
    Plot a zoomed-in view of a single heartbeat around an R-peak.
    """
    from scipy.signal import find_peaks
    peaks, _ = find_peaks(ecg_signal, height=0.5, distance=fs//2)
    r_peak_idx = peaks[0]
    half_window_samples = int(window * fs / 2)
    start_idx = max(0, r_peak_idx - half_window_samples)
    end_idx = min(len(ecg_signal), r_peak_idx + half_window_samples)
    heartbeat_window = ecg_signal[start_idx:end_idx]
    time_window = np.arange(start_idx, end_idx) / fs
    plt.figure(figsize=(10, 6))
    plt.plot(time_window, heartbeat_window, label="Zoomed Heartbeat", color="blue")
    plt.axvline(r_peak_idx / fs, color="red", linestyle="--", label="R-Peak")
    plt.title(title)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True)
    plt.savefig(filename, format="svg")
    plt.show()

# Plot for Noisy ECG
plot_fir_lms_comparison(noisy_ecg, fir_filtered_noisy, lms_filtered_noisy, "Noisy ECG Signal", "Comparison_Noisy_ECG")
plot_single_heartbeat(fir_filtered_noisy, fs, "Zoomed-in ECG Traces of One Heartbeat (Noisy ECG)", "Zoomed_Heartbeat_Noisy_ECG.svg")

# Plot for Clean ECG
plot_fir_lms_comparison(clean_ecg, fir_filtered_clean, lms_filtered_clean, "Clean ECG Signal", "Comparison_Clean_ECG")
plot_single_heartbeat(fir_filtered_clean, fs, "Zoomed-in ECG Traces of One Heartbeat (FIR_filtered Clean ECG)", "Zoomed_Heartbeat_Clean_ECG.svg")

# Frequency Domain Plot
def plot_frequency_domain(fir_filtered, lms_filtered, fs, title_prefix, filename_prefix):
    # FFT for FIR Filtered Signal
    fft_fir = np.fft.fft(fir_filtered)
    fft_freq = np.fft.fftfreq(len(fft_fir), d=1/fs)
    fft_fir_magnitude = 20 * np.log10(np.abs(fft_fir[:len(fft_fir)//2]))

    # FFT for LMS Filtered Signal
    fft_lms = np.fft.fft(lms_filtered)
    fft_lms_magnitude = 20 * np.log10(np.abs(fft_lms[:len(fft_lms)//2]))

    # Plot the results
    plt.figure(figsize=(14, 10))

    # FIR Filtered Frequency Domain
    plt.subplot(2, 1, 1)
    plt.plot(fft_freq[:len(fft_freq)//2], fft_fir_magnitude, label="FIR Filtered Signal", color="green")
    plt.title(f"{title_prefix}: FIR Filtered in Frequency Domain")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Magnitude [dB]")
    plt.grid()
    plt.legend()

    # LMS Filtered Frequency Domain
    plt.subplot(2, 1, 2)
    plt.plot(fft_freq[:len(fft_freq)//2], fft_lms_magnitude, label="LMS Filtered Signal", color="red")
    plt.title(f"{title_prefix}: LMS Filtered in Frequency Domain")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Magnitude [dB]")
    plt.grid()
    plt.legend()

    plt.tight_layout()
    plt.savefig(f"{filename_prefix}.svg", format="svg")
    plt.show()

# Plot for Noisy ECG Frequency Domain
plot_frequency_domain(
    fir_filtered_noisy,
    lms_filtered_noisy,
    fs,
    "Noisy ECG Signal",
    "Frequency_Domain_Noisy_ECG"
)

# Plot for Clean ECG Frequency Domain
plot_frequency_domain(
    fir_filtered_clean,
    lms_filtered_clean,
    fs,
    "Clean ECG Signal",
    "Frequency_Domain_Clean_ECG"
)

# DC Component Output
print("DC Components:")
print(f"FIR Filter (Noisy ECG): {dc_fir_noisy}")
print(f"LMS Filter (Noisy ECG): {dc_lms_noisy}")
print(f"FIR Filter (Clean ECG): {dc_fir_clean}")
print(f"LMS Filter (Clean ECG): {dc_lms_clean}")