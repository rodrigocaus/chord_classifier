import matplotlib.pyplot as plt
import numpy as np
from scipy import fftpack
from scipy import signal
import math


def chromagram_stft(data, rate=1.0, winlen=2048, scale='sharp', winn='flat'):
    '''
            Calculates the chromagram of an audio sample.

                Args:
                        data: array of time series of an audio sample.
                        rate: sample frequency of 'data'.
                        wilen: lenght of segment of FFT.
						scale: type of chroma-scale (sharp, flat or number)
                        winn: type of window (flat, gauss)

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

        while center*(1.0 + devfreq) < fmax and center*(1.0 + devfreq) < 20e3:
            loidx = center*(1.0 - devfreq)
            loidx = math.ceil((len(f) - 1)*(loidx - f[0])/(fmax - f[0]))
            upidx = center*(1.0 + devfreq)
            upidx = math.floor((len(f) - 1)*(upidx - f[0])/(fmax - f[0]))
            winfilter = np.zeros(shape=spectrum.shape)
            
            if winn == 'gauss':
                # Gaussian window inst
                sigma = (upidx - loidx + 1.0)/6.0
                mu = (len(f) - 1)*(center - f[0])/(fmax - f[0])

                for i in range(upidx - loidx + 1):
                    winfilter[loidx+i] = __gaussian(loidx + i, mu, sigma)
            else:
                winfilter[loidx:upidx] = 1.0

            chromagram[chromaidx, timeidx] += np.dot(spectrum, winfilter)
            chromaidx = (chromaidx + 1) % 12
            centeridx += 1
            center = 27.5*np.power(2, centeridx/12)

        if sum(chromagram[:, timeidx]) > 0:
            chromagram[:, timeidx] /= sum(chromagram[:, timeidx])

        if scale == 'sharp':
            chromas = np.array(['C', 'C#', 'D', 'D#', 'E', 'F',
                                'F#', 'G', 'G#', 'A', 'A#', 'B'])
        elif scale == 'flat':
            chromas = np.array(['C', 'Db', 'D', 'Eb', 'E', 'F',
                                'Gb', 'G', 'Ab', 'A', 'Bb', 'B'])
        else:
            chromas = np.array([i for i in range(12)])

    return chromas, t, chromagram


def chromaplot(t, scale, chroma):
    ax = plt.imshow(chroma, cmap='hot', interpolation=None, extent=[
        t[0], t[len(t)-1], -0.5, len(scale)-0.5], origin='lower', aspect='auto')
    plt.yticks(
        ticks=[i for i in range(len(scale))], labels=scale)
    return ax

def __gaussian(x, mu, sig):
    return (1.0/(sig*np.sqrt(2.0*np.pi)))*np.exp(((x-mu)/sig)**2/(-2.0))