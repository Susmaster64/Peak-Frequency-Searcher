# Peak-Frequency-Searcher
This is a Python script that takes an MP3 file as input and outputs the peak frequencies of the audio, as well as the corresponding notes and cents deviation from A440 tuning. It also allows for searching for peak frequencies within a set frequency range.

## Dependencies

This script requires the following Python libraries:

    -librosa
    -numpy
    -scipy

You can install these dependencies by running the following command:

  `pip install librosa numpy scipy`
  
## Usage
  
  Edit the variables `min_freq` and `maz_freq` to define the frequency to search for peaks in. 
  
  Edit the `"/path/to/your/mp3/file"` in `audio = AudioSegment.from_file("/path/to/your/mp3/file")` to the path to your mp3 file
  
  (WARNING: DO NOT USE OVERLY LARGE MP3 FILES UNLESS YOU ARE CONFIDENT YOUR SYSTEM CAN HANDLE IT.)
