import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# FIR_filter class definition
class FIR_filter:
    def __init__(self, coefficients):
        self.ntaps = len(coefficients)
        self.coefficients = coefficients
        self.buffer = np.zeros(self.ntaps)

    def dofilter(self, v):
        # Roll buffer in a circular fashion and insert the new value
        self.buffer = np.roll(self.buffer, 1)
        self.buffer[0] = v

        # Use dot product for efficient filtering
        return np.dot(self.buffer, self.coefficients)

# Load the noisy ECG data 
noisy = np.loadtxt("/home/basav/DSP/Digital-Signal-Processing/Assignment_2_FIR/Noisy_ECG_1000Hz_9.dat")

# Load the clean ECG data
clean = np.loadtxt("/home/basav/DSP/Digital-Signal-Processing/Assignment_2_FIR/Lying_ECG_1000Hz_9.dat")

# Select a shorter, clearer peak as the template (adjust the indices as necessary)
template = clean[15985:16085]  # Best looking stable peak

# Time-reverse the template to make it the matched filter coefficients
matched_coeff = template[::-1]

# Create an instance of FIR_filter with the matched filter coefficients
matched_filter = FIR_filter(coefficients=matched_coeff)

# Filter the noisy ECG signal
filtered_ecg = []
for sample in noisy:
    filtered_output = matched_filter.dofilter(sample)
    filtered_ecg.append(filtered_output)

# Convert the result to a NumPy array for easy plotting
filtered_ecg = np.array(filtered_ecg)

# Square out signal to improve S/N ratio 
filtered_ecg = filtered_ecg * filtered_ecg

# Plot 1: Comparison of ECG Template and Matched Coefficients
plt.figure(figsize=(10, 6))
plt.plot(template, label='ECG Template', color='blue')
plt.plot(matched_coeff, label='Matched Coefficients', color='red')
plt.title("4.a. Comparison of ECG Template and Matched Coefficients")
plt.xlabel("Sample")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)
# Save plot as SVG
plt.savefig("4a_Comparison_ECG_Template_and_Matched_Coefficients.svg", format="svg")
plt.show()

# Plot 2: Filtered ECG Signal
plt.figure(figsize=(10, 6))
plt.plot(filtered_ecg, label='Filtered ECG Signal', color='green')
plt.title("4.b. Filtered ECG Signal (Matched Filter Output)")
plt.xlabel("Sample")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)
# Save plot as SVG
plt.savefig("4b_Filtered_ECG_Signal.svg", format="svg")
plt.show()

# Question 4: Calculate Momentary Heart Rate (BPM) Over Time
# Sampling frequency
fs = 1000  # Hz

# Step 1: Detect R-peaks in the filtered ECG signal
# Use a threshold to find R-peaks, adjust 'height' and 'distance' to match your data
peaks, _ = find_peaks(filtered_ecg, height=0.5, distance=fs/2.5)

# Step 2: Calculate RR intervals and convert them to BPM
# Calculate RR intervals (in samples)
rr_intervals = np.diff(peaks)

# Convert RR intervals to time in seconds
rr_intervals_sec = rr_intervals / fs

# Calculate BPM (beats per minute)
bpm = 60 / rr_intervals_sec

# Step 3: Create a time axis for plotting BPM
# The time values for BPM correspond to the midpoint between two consecutive R-peaks
time_axis = peaks[1:] / fs  # In seconds

# Plot 3: BPM Over Time
plt.figure(figsize=(10, 6))
plt.plot(time_axis, bpm, label='Heart Rate (BPM)', color='blue', marker='o')
plt.title("4.c. Momentary Heart Rate Over Time")
plt.xlabel("Time (seconds)")
plt.ylabel("Heart Rate (BPM)")
plt.legend()
plt.grid(True)
# Save plot as SVG
plt.savefig("4c_Momentary_Heart_Rate_Over_Time.svg", format="svg")
plt.show()

# Plot to Frequency Domain (Noisy Signal - FIR)
filtered_ecg1 = []
fir_instance = FIR_filter(np.zeros(len(filtered_ecg)))

# Perform the FFT (Fast Fourier Transform) for Original Noisy-Signal
fft_data_noisy = np.fft.fft(filtered_ecg)
fft_freq_noisy = np.fft.fftfreq(len(fft_data_noisy), d=1 / fs)

N_noisy = len(filtered_ecg)
xfreq_noisy = fft_freq_noisy[:N_noisy // 2]
yfreq_noisy = np.abs(fft_data_noisy[:N_noisy // 2])

# Plot Original Noisy Signal in frequency-domain signal
plt.figure(figsize=(10, 6))
plt.plot(xfreq_noisy, 20 * np.log10(np.abs(yfreq_noisy)), color='red')  # Using dB scale
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude [dB]')
plt.title('4.d. Match Filtered ECG Signal in Frequency Domain')
plt.grid(True)

# Save plot as SVG
plt.savefig("4d_Match_Filtered_ECG_Frequency_Domain.svg", format="svg")
plt.show()