import librosa
import numpy as np
import scipy.fftpack
import scipy.signal
from pydub import AudioSegment
import soundfile as sf
from pydub.effects import low_pass_filter

min_fundamental_frequency = 50    # The lower bound to search for fundemental frequencies in (can not be 0)
max_fundamental_frequency = 500   # The upper bound to search for fundemental frequencies in (can not be 0)

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
audio_file, sr = librosa.load('path/to/your/wav/file', sr=None)

# Compute the frequency spectrum
fft = librosa.stft(audio_file)

# Compute the power spectrum
power_spectrum = np.abs(fft) ** 2

# Compute the spectral centroid
centroid = librosa.feature.spectral_centroid(S=power_spectrum)

# Get the index of the spectral centroid with the highest amplitude
index = np.argmax(centroid)

# Compute the fundamental frequency
fundamental_frequency = librosa.yin(audio_file, min_fundamental_frequency, max_fundamental_frequency, sr=sr)[1]

print('\n')

print('The first fundemental frequency found in your set range was: {} Hz\n'.format(fundamental_frequency))

# Set the number of overtones to remove
num_overtones = 10000

# Remove the overtones
fft_filtered = remove_overtones(fft, fundamental_frequency, num_overtones)

# Compute the inverse FFT to get the filtered audio signal
audio_filtered = librosa.istft(fft_filtered)

# Save the filtered audio to a file
sf.write('audio_filtered.wav', audio_filtered, sr)

# Load audio file
audio = AudioSegment.from_file("audio_filtered.wav", format="wav")

# Filter out fundamental frequency and keep overtones
audio_overtones = low_pass_filter(audio, fundamental_frequency)

# Export audio file
audio_overtones.export("audio_overtones.wav", format="wav")

# Define frequency range to search for peaks in
min_freq = 80
max_freq = 1000

# Load audio file and convert to mono
audio = AudioSegment.from_file("audio_overtones.wav")
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
num_peaks = 5

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

