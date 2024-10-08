I have added another code as "fft-v1" in which i have marked the peaks for the signal(frequency domain) and also found some literature on how to find the fundametal frequency, harmonics and noise. HOPE IT HELPS!!!

#####Identifying Fundamental Frequencies, Harmonics, and Noise

Fundamental Frequencies:
Definition: The fundamental frequency is the lowest frequency produced by a vocal tract or sound source. In speech, this corresponds to the pitch of the voice.
How to Identify:
Fundamental frequencies are typically the first prominent peaks in the spectrum (lowest frequency peaks).
In vowels, the fundamental frequency (F0) is often between 85 Hz to 255 Hz for human speech (lower for males, higher for females).
In your frequency spectrum plot, the first strong peak in this range is likely the fundamental frequency of the vowel being spoken.
Harmonics:
Definition: Harmonics are multiples of the fundamental frequency. If your fundamental frequency is F0, harmonics will appear at 2×F0, 3×F0, and so on.
How to Identify:
Once you’ve identified the fundamental frequency, look for peaks at integer multiples of this frequency (2×F0, 3×F0, etc.).
These harmonics will often show up as smaller peaks at regular intervals after the fundamental peak.
Example: If F0 is 150 Hz, expect harmonics at 300 Hz, 450 Hz, 600 Hz, etc.
Noise:
Definition: Noise is unwanted or random signal components that do not correspond to a harmonic structure. It can be broadband (spread over many frequencies) and often occupies the higher frequency range in speech signals.
How to Identify:
Broad, low-amplitude components in the frequency spectrum, especially above 10kHz, are often considered noise.
Unlike harmonics, noise does not appear at regular intervals.
In speech, noise might also appear as a “smearing” of frequencies, as opposed to distinct peaks.
Tip: Pay attention to the frequency ranges above 3kHz for high-frequency noise, which is often associated with sibilant consonants (like "s" and "sh").
Example of the Process:
Let's assume you're analyzing a spoken vowel and you have plotted the frequency spectrum:

Look for the first strong peak in the spectrum (around 85–255 Hz). This is likely the fundamental frequency.
Check for peaks at multiples of this frequency. For example, if the fundamental frequency is 150 Hz, look for peaks at 300 Hz, 450 Hz, etc. These are harmonics.
Identify noise by examining the high-frequency range (above 10 kHz). If there are no distinct peaks and the spectrum is broad and flat, this is likely noise.
