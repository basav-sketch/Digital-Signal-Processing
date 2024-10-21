# Digital Signal Processing (DSP) Assignment 1

## Task Breakdown

### Task 1: Audio Signal Analysis
- **Loaded** audio samples into Python.
- **Plotted** the audio signals in both the time domain (amplitude vs. time) and the frequency domain (frequency vs. amplitude in dB).

### Task 2: Analyzing the Frequency Spectrum
- **Fundamental Frequency**: Identified the fundamental frequency as **167.9 Hz** from the frequency domain plot. 
- **Harmonics**: Found harmonics at **335.8 Hz** and **503.7 Hz**. Higher harmonics had significantly lower amplitudes.
- **Noise**: Frequencies above **10kHz** were identified as containing noise, particularly in the higher harmonics and sibilants.

### Task 3: Voice Quality Improvement
- **Objective**: Improve the quality of the voice by manipulating the frequency bands above 3 kHz.
- **Method**: 
  - Removed the first 0.5 seconds of noise from the audio.
  - Applied a custom smoother filter to the frequency components between 3 kHz and 10 kHz.
  - Manipulated these bands to enhance clarity and richness, making the voice sound perceptually more pleasant and interesting.
- **Considerations**: Compared low-pass and band-pass filters before deciding on a custom solution to comply with assignment requirements. The band-pass filter was most effective, but we could not use it directly, so we developed our own smoother filter.

### Task 4: Voice Enhancement with Aural Exciter
- **Objective**: Enhance the vocal quality by adding brightness and vibrancy through harmonic excitation.
- **Method**: 
  - Used the hyperbolic tangent (`tanh`) function to add a small amount of harmonic distortion to frequency components between 3 kHz and 10 kHz.
  - The excited components were scaled and added back to the original signal.
  - Limited the frequencies to below 10 kHz to avoid unwanted noise.
  - Achieved a balanced, vibrant sound without artificial distortion.
- **Challenges**: Determining the optimal non-linearity and scaling factor for enhancement without compromising natural vocal quality.

### Results:
The audio quality was significantly improved through careful filtering and enhancement techniques, making the voice sound clearer and more vibrant.

### Future Work:
Further tuning of filter parameters and additional enhancements could be explored to refine audio quality even more.

## Usage

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/basav-sketch/Digital-Signal-Processing.git
   cd Digital-Signal-Processing/assignment1
   ```

2. **Run the Python Scripts**:
   - Make sure Python 3 and required libraries (`numpy`, `matplotlib`, etc.) are installed.
   - Run each script from the terminal as follows:
     ```bash
     python3 taskonetwo.py
     python3 taskthree.py
     python3 taskfour.py
     ```

3. **View the Output**:
   - Plots will be displayed for Tasks 1, 2, and 4.
   - Enhanced audio files (`pleasant_and_interesting.wav` and `exited.wav`) will be generated and saved in the working directory.

## Requirements
- **Python 3.x**
- **NumPy** and **Matplotlib** libraries
- **SciPy** for reading and writing WAV files
- **WAV File Format**: All audio files must be in WAV 16-bit format.

## Important Notes
- The code is designed to be platform-independent and tested in Linux (Ubuntu).
- Absolute paths have been avoided to ensure portability.
- No high-level signal processing/filtering commands were used apart from FFT and IFFT.
- Ensure plots (`plt.show()`) are displayed correctly, as missing this step may lead to incomplete outputs.

## Future Work
- **Assignment 2 (FIR Filters)**: Explore FIR filtering for signal manipulation.
- **Assignment 3 (IIR Filters)**: Apply IIR filters to further analyze and process audio signals.

## GitHub Repository
The full code for this assignment, as well as future assignments for FIR and IIR filters, can be found in the GitHub repository: [DSP Lab Assignments](https://github.com/basav-sketch/Digital-Signal-Processing/tree/main).

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements
- **Professor - Rami and Scott**: For guidance throughout the course.
- **Teammates**: For valuable contribution, feedback and discussions during the development process.
