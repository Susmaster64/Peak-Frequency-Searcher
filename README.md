# README

This program is named "APPTFIFPWAOMCMFTFAUYARMMTFPTSWTALPF". It stands for "A Python Program That Finds Important Frequencies With The FFT and Finds Their Peaks Whilst Accounting For Overtones by Calculating the Fundamental Frequency Utilizing the YIN Algorithm and Removing the Mathematical Multiples Then Finally Passing the Sound Wave Through a Low Pass Filter".

The program aims to seek out notable frequencies in an audio file using the Fast Fourier Transform (FFT) and identify their pinnacles while considering their overtones by computation of the fundamental frequency by means of the YIN Algorithm. It removes the mathematical multiples and conducts the sound wave through a Low Pass Filter.

## Installation and Dependencies

This program requires the following libraries to be installed:

    -librosa
    - argparse
    - numpy
    - scipy.fftpack
    - scipy.signal
    - pydub
    - soundfile

## Usage

To run the program, you need to pass in a command-line argument that specifies the filename of the audio file that you want to analyze. The program will then output a list of the most notable frequencies in the specified audio file.

For example:

`python main.py path/to/audio/file.wav`

You can also specify the following optional arguments:

    -n, --num_peaks: The number of peaks to find (default: 5)
    -l, --freq_lower: The lower bound of the range to find peaks in (default: 27.5Hz - A0)
    -u, --freq_upper: The upper bound of the range to find peaks in (default: 14080Hz - A9)
    -fl, --fun_freq_lower: The lower bound of the range to find fundamental frequencies to remove overtones (default: 27.5Hz - A0)
    -fu, --fun_freq_upper: The upper bound of the range to find fundamental frequencies to remove overtones (default: 14080Hz - A9)
    -r, --num_overtones: How many overtones to remove (default: 10000)
    -L, --low_pass_filter: Whether to use the low pass filter (default: false)
    -M, --mathamatical_overtone_pass: Whether to use the mathematical overtone removal pass (default: false)
    
## Output

The program outputs the peak frequencies it finds along side with the fundamental frequency.
It will output the overtone removed wav and the low pass filter wav.

For example:

`python Main.py -n 10 -L -M temp.wav`

Returns:

    The first fundemental frequency found in the set range was: 568.7892261302085 Hz

    Peak 1: 330.32 Hz (E4+4)
    Peak 2: 65.71 Hz (C2+8)
    Peak 3: 130.55 Hz (C3-3)
    Peak 4: 258.47 Hz (C4-21)
    Peak 5: 780.67 Hz (G5-7)
    Peak 6: 197.14 Hz (G3+10)
    Peak 7: 388.14 Hz (G4-17)
    Peak 8: 658.88 Hz (E5-1)
    Peak 9: 989.19 Hz (B5+2)
    Peak 10: 525.70 Hz (C5+8)


