
from scipy.io import wavfile
import matplotlib.pyplot as plt

import numpy as np
from scipy import fftpack
from scipy import signal
import math


def chromagram_stft(data, rate=1.0, winlen=2048):
    '''
            Calculates the chromagram of an audio sample.

                Args:
                        data: array of time series of an audio sample.
                        rate: sample frequency of 'data'.
                        wilen: lenght of segment of FFT.

                Returns:
                        chromas: array of chroma-scale (C, C#, D, ..., B).
                        t: time scale array.
                        chomagram: ndarray of the chromagram. Last axis is the time scale.
    '''
    f, t, Stf = signal.stft(data, fs=rate, nperseg=winlen)
	# Better results with abs^2
    Stf = np.abs(Stf)**2

    fmax = f[len(f)-1]

    chromagram = np.zeros(shape=(12, len(t)))
    for timeidx in range(len(t)):
        spectrum = Stf[:, timeidx]
        # First frequency is an A at 27.5Hz
        center = 27.5
        # Deviation between chromas
        devfreq = 0.028
        chromaidx = 9
        centeridx = 0

        while center*(1.0 + devfreq) < fmax:
            loidx = center*(1.0 - devfreq)
            loidx = math.ceil((len(f) - 1)*(loidx - f[0])/(fmax - f[0]))
            upidx = center*(1.0 + devfreq)
            upidx = math.floor((len(f) - 1)*(upidx - f[0])/(fmax - f[0]))
            winfilter = np.zeros(shape=spectrum.shape)
            winfilter[loidx:upidx] = 1.0
            chromagram[chromaidx, timeidx] += np.dot(spectrum, winfilter)
            chromaidx = (chromaidx + 1) % 12
            centeridx += 1
            center = 27.5*np.power(2, centeridx/12)

        if sum(chromagram[:, timeidx]) > 0:
            chromagram[:, timeidx] /= sum(chromagram[:, timeidx])

    chromas = np.array(['C', 'C#', 'D', 'D#', 'E', 'F',
                        'F#', 'G', 'G#', 'A', 'A#', 'B'])
    return chromas, t, chromagram


filename = "wav/ChromaticScaleUp.wav"
Fs, data = wavfile.read(filename)

c, t, chroma = chromagram_stft(data, rate=Fs)
plt.pcolormesh(t, c, chroma)
plt.show()
