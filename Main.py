import librosa
import numpy as np
import scipy.fftpack
import scipy.signal
from pydub import AudioSegment

# Define frequency range to search for peaks in
min_freq = 80
max_freq = 1000

# Load audio file and convert to mono
audio = AudioSegment.from_file("/path/to/your/mp3/file")
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

