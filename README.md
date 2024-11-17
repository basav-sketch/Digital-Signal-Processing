# Digital Signal Processing (DSP) Assignments

Welcome to the **Digital-Signal-Processing** repository! This repository contains my work for the **DSP** course, where I implemented solutions for assignments related to signal processing. The focus is on understanding and applying fundamental concepts to enhance, filter, and manipulate signals.

## Assignments Overview

### Assignment 1: Fast Fourier Transform (FFT)
In this assignment, I utilized the Fast Fourier Transform (FFT) to analyze the frequency components of an audio signal. Key tasks included:
- Loading an audio file and visualizing it in both time and frequency domains.
- Identifying key features, such as fundamental frequencies and harmonics.
- Improving the quality of the audio signal through frequency domain manipulation, focusing on enhancing the clarity of the voice.

### Assignment 2: Finite Impulse Response (FIR) Filter
The second assignment focused on designing and implementing **Finite Impulse Response (FIR)** filters to process ECG signals. Highlights included:
- **Task 1**: Designing combined high-pass and band-stop FIR filters using the sinc function and applying a Blackman window.
- **Task 2**: Applying the designed FIR filter to noisy ECG signals and comparing the results with the clean ECG signal.
- **Task 3**: Using adaptive LMS filtering for noise removal and comparing the FIR and LMS-filtered signals.
- **Task 4**: Implementing heartbeat detection using matched filtering and calculating the momentary heart rate (BPM).

Each task included detailed visualization and analysis in both time and frequency domains. 

### Moodle Quiz: Infinite Impulse Response (IIR) Filters
Instead of Assignment 3, I completed a **Moodle Quiz** focused on **Infinite Impulse Response (IIR)** filters. The quiz covered:
- Theoretical aspects of IIR filters, including stability, poles, and zeros.
- Comparison between IIR and FIR filters.
- Real-time applications of IIR filters and their advantages in specific scenarios.

## Repository Structure
- **Assignment_1_FFT/**: Contains the code, plots, and audio files used for the FFT analysis, as well as the report summarizing the results.
- **Assignment_2_FIR/**: Includes FIR filter design, implementation scripts, ECG data files, and resulting plots for all tasks.
- **README.md**: This document, providing an overview of the repository.

## Technologies Used
- **Python**: Main programming language for all assignments.
- **NumPy**: Used for numerical computations, including FFT and FIR filter implementation.
- **SciPy**: Employed for advanced signal processing tasks and filter design.
- **Matplotlib**: Used for visualizing signals in both time and frequency domains.

## Getting Started
To run the code for any of the assignments, follow these steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/basav-sketch/Digital-Signal-Processing.git
   ```
2. Navigate to the desired assignment folder.
3. Run the Python scripts using Python 3.

Ensure you have the required Python libraries installed:
```bash
pip install numpy scipy matplotlib
```

## Results and Discussion

### **Assignment 1 (FFT)**
- Visualized the time and frequency domain of an audio signal.
- Enhanced the clarity of the signal by removing unwanted frequency components.
- Demonstrated the significance of FFT in audio signal processing.

### **Assignment 2 (FIR Filtering and Heartbeat Detection)**
- Designed and implemented FIR filters for ECG signal processing.
- Demonstrated the effectiveness of FIR filters in reducing noise in ECG data.
- Compared FIR and LMS filtering techniques, highlighting their strengths and trade-offs.
- Implemented a matched filter for heartbeat detection and calculated momentary heart rates (BPM).

## Future Work
- Extend FIR and LMS filtering techniques to other biomedical signals.
- Explore real-time DSP applications using adaptive filters.
- Experiment with machine learning for automatic filter design and noise classification.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
For any questions or discussions, feel free to reach out via GitHub or email.

Thank you for exploring my **Digital Signal Processing** assignments!
