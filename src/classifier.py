
import numpy
from scipy.io import wavfile

filename = "wav/A_440.wav"

Fs = 44100
Tend = 5
maxInt16 = 2**15 - 1

t = numpy.linspace(0, Tend, Tend * Fs)
out = numpy.sin(2 * numpy.pi * 440.0 * t)
wavfile.write(filename, Fs, numpy.int16(out * maxInt16))
