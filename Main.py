import librosa
import argparse
import numpy as np
import scipy.fftpack
import scipy.signal
from pydub import AudioSegment
import soundfile as sf
from pydub.effects import low_pass_filter

# The parser (CLI)
parser = argparse.ArgumentParser(
                    prog = 'APPTFIFPWAOMCMFTFAUYARMMTFPTSWTALPF',
                    description = 'APPTFIFPWAOMCMFTFAUYARMMTFPTSWTALPF (A Python Program That Finds Important Frequencies With The FFT and Finds Their Peaks Whilst Accounting For Overtones by Calculating the Fundamental Frequency Utilizing the YIN Algorithm and Removing the Mathematical Multiples Then Finally Passing the Sound Wave Through a Low Pass Filter) attempts to seekth out notable frequencies using the FFT, and identify their pinnacles whilst considering their overtones by computation of the fundamental frequency by means of the YIN Algorithm. It doth then expunge the mathematical multiples and conduct the sound wave through a Low Pass Filter.',
                    epilog = 'Check the README if do not understand.')

parser.add_argument('filename', type=str)

parser.add_argument('-n', '--num_peaks', type=int,
                    default=5,
                    help='How many peaks to find (default: 5')

parser.add_argument('-l','--freq_lower', type=int,
                    default=27.5,
                    help='The lower bound of the range to find peaks (Hz) (default :27.5Hz - A0)')

parser.add_argument('-u','--freq_upper', type=int,
                    default=14080,
                    help='The upper bound of the range to find peaks (Hz) (default :14080Hz - A9)')

parser.add_argument('-fl','--fun_freq_lower', type=int,
                    default=27.5,
                    help='The lower bound of the range to find fundamental frequencies to remove overtones (Hz) (default: 27.5Hz - A0)')

parser.add_argument('-fu', '--fun_freq_upper', type=int,
                    default=14080,
                    help='The upper bound of the range to find fundamental frequencies to remove overtones (Hz) (default: 14080Hz - A9)')

parser.add_argument('-r', '--num_overtones', type=int,
                    default=10000,
                    help='How many overtones to remove (default: 10000)')

parser.add_argument('-L','--low_pass_filter',
                    action='store_true',
                    help='Whether to use the low pass filter (default: false)')

parser.add_argument('-M','--mathamatical_overtone_pass',
                    action='store_true',
                    help='Whether to use the mathamatical overtone removal pass (default: false)')

args = parser.parse_args()


# Reassignment of args to variables
audio_input_path = args.filename # The path to the wav which you wish to find peaks in
min_fundamental_frequency = args.fun_freq_lower    # The lower bound to search for fundemental frequencies in (can not be 0)
max_fundamental_frequency = args.fun_freq_upper   # The upper bound to search for fundemental frequencies in (can not be 0)
num_overtones = args.num_overtones   # Set the number of overtones to remove
min_freq = args.freq_lower   # The upper bound to search for peaks in (can not be 0)
max_freq = args.freq_upper   # The upper bound to search for peaks in (can not be 0)
num_peaks = args.num_peaks   # Number of peaks to find

# Logic to decide the input of the peak finder
if args.low_pass_filter == True and args.mathamatical_overtone_pass == True:
    low_pass_input = 'mathamatical_overtone_pass.wav'
    peak_finder_input = 'audio_low_pass.wav'

elif args.low_pass_filter == True and args.mathamatical_overtone_pass == False:
    low_pass_input = audio_input_path
    peak_finder_input = 'audio_low_pass.wav'

elif args.low_pass_filter == False and args.mathamatical_overtone_pass == True:
    low_pass_input = audio_input_path
    peak_finder_input = 'mathamatical_overtone_pass.wav'

else:
    peak_finder_input = audio_input_path
    low_pass_input = audio_input_path



#-#-#-#-# MATHAMATICAL OVERTONE REMOVAL #-#-#-#-#



# Overtone removal function
def remove_overtones(fft, fundamental_frequency, num_overtones):
    # Compute the overtones
    overtones = np.arange(fundamental_frequency * 2, fundamental_frequency * (num_overtones + 1), fundamental_frequency)

    # Get the frequency bins corresponding to the overtones
    bins = librosa.fft_frequencies(sr=sr, n_fft=fft.shape[0])
    indices = np.searchsorted(bins, overtones)

    # Set the magnitude of the overtones to zero
    fft[indices, :] = 0

    return fft

# Load the audio file
audio_file, sr = librosa.load(audio_input_path, sr=None)

# Compute the frequency spectrum
fft = librosa.stft(audio_file)

# Compute the power spectrum
power_spectrum = np.abs(fft) ** 2

# Compute the spectral centroid
centroid = librosa.feature.spectral_centroid(S=power_spectrum)

# Get the index of the spectral centroid with the highest amplitude
index = np.argmax(centroid)

# Compute the fundamental frequency
fundamental_frequency = librosa.yin(audio_file, fmin=min_fundamental_frequency, fmax=max_fundamental_frequency, sr=sr)[0]

print('\nThe first fundemental frequency found in the set range was: {} Hz\n'.format(fundamental_frequency))

# Remove the overtones
fft_filtered = remove_overtones(fft, fundamental_frequency, num_overtones)

# Compute the inverse FFT to get the filtered audio signal
audio_filtered = librosa.istft(fft_filtered)

# Save the filtered audio to a file
sf.write('mathamatical_overtone_pass.wav', audio_filtered, sr)



#-#-#-#-# LOW PASS FILTER #-#-#-#-#



# Load audio file
audio = AudioSegment.from_file(low_pass_input, format="wav")

# Filter out fundamental frequency and keep overtones
audio_low_pass = low_pass_filter(audio, fundamental_frequency)

# Export audio file
audio_low_pass.export("audio_low_pass.wav", format="wav")



#-#-#-#-# PEAK FINDER #-#-#-#-#



# Load audio file and convert to mono
audio = AudioSegment.from_file(peak_finder_input)
samples = np.array(audio.get_array_of_samples())
samples = np.mean(samples.reshape(-1, audio.channels), axis=1)

# Compute FFT of audio signal
N = len(samples)
window = np.hanning(N)
spectrum = np.abs(scipy.fftpack.fft(window * samples))
frequencies = scipy.fftpack.fftfreq(N, d=1.0/audio.frame_rate)

# Find the indices of the frequencies within the desired range
mask = (frequencies >= min_freq) & (frequencies <= max_freq)

# Find the loudest peaks iteratively
for i in range(num_peaks):
    peaks = scipy.signal.find_peaks(spectrum[mask])[0]
    
    if len(peaks) > 0:
        max_peak_idx = np.argmax(spectrum[mask][peaks])
        max_peak_freq = frequencies[mask][peaks][max_peak_idx]
        note_and_cents = librosa.hz_to_note(max_peak_freq, cents=True)
        
        # Prints the peak frequency, peak number (from loudest to quietest), and the note (with cents deviation)
        print("Peak {}: {:.2f} Hz ({})".format(i+1, max_peak_freq, note_and_cents))
        
        # Remove the loudest peak from the spectrum before searching for the next peak
        spectrum[np.abs(frequencies - max_peak_freq) < 50] = 0
        
    else:
        break
print('\n')
