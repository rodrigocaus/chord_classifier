
from scipy.io import wavfile
import matplotlib.pyplot as plt

from chroma import chromagram_stft
from chroma import chromaplot


filename = "wav/CMajor2.wav"
Fs, data = wavfile.read(filename)

scale, t, Ch = chromagram_stft(data, rate=Fs, winn='gauss')

chromaplot(t, scale, Ch)
plt.show()

