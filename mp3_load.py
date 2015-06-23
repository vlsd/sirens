# I think audioread is a standard part of python

from audioread import audio_open
from numpy import ndarray, frombuffer, asarray


class AudioObject(ndarray):
    def __new__(cls, input_array, sample_rate=22050):
        obj = asarray(input_array).view(cls)
        obj.sample_rate = sample_rate
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return
        self.sample_rate = getattr(obj, 'sample_rate', 22050)

    @property
    def seconds(self):
        return len(self)/float(self.sample_rate)

    def to_file(self, filename):
        raise NotImplementedError

def load_audio_from_file(filename):
    # load the audio data from the file
    temp = bytearray()
    sr = 0
    with audio_open(filename) as audio:
        sr = audio.samplerate
        nchannels = audio.channels
    
        # chunk size can be specified with 'block_samples' (default 1024):
        for chunk in audio.read_data():
            temp.extend(chunk)

    data = frombuffer(temp, dtype='<i2').reshape(-1, nchannels)[:,0]   
    return AudioObject(data, sample_rate=sr)

