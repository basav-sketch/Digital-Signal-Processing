from scipy.io.wavfile import read
samplerate, data = read('Lab 1 test 2.wav')

import numpy as np
data2 = data/32768
duration = len(data2)/samplerate
time = np.arange(0,duration,1/samplerate) #time vector

import matplotlib.pyplot as plt
plt.plot(time,data2)
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.title('Lab 1 Test 2.wav')
plt.show()

fft_signal = np.fft.fft(data2)

frequencies = np.fft.fftfreq(len(fft_signal), d=1/samplerate)

magnitude = np.abs(fft_signal)

positive_frequencies = frequencies[:len(frequencies) // 2]
positive_magnitude = magnitude[:len(magnitude) // 2]
positive_magnitude[positive_magnitude == 0] = 1e-10
magnitude_dB = 20 * np.log10(positive_magnitude)

plt.plot(positive_frequencies,magnitude_dB)
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude [dB]')
plt.title('Signal in Frequency Domain')
plt.grid(True)
plt.show()