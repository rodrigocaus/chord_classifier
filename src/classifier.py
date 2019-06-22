
from scipy.io import wavfile
import matplotlib.pyplot as plt

from chroma import chromagram_stft
from chroma import chromaplot

def get_note_list(data, rate=1.0, winlen=2048, scale='sharp', winn='ret'):
    scale, t, Ch = chromagram_stft(data, rate=rate, winlen=winlen, scale=scale, winn=winn)

    result = []

    for c in range(len(Ch[0])):
        notes = Ch[:,c]
        notes_formatted = []
        for i in range(len(notes)):
            notes_formatted.append((notes[i], i))

        notes_formatted.sort(key=lambda x: x[0], reverse=True)
        for i in range(3):
            note = notes_formatted[i][1]
            j = i+1
            while j < 5:
                if notes_formatted[j][1] == note + 1 or notes_formatted[j][1] == note - 1 or \
                (note == 0 and notes_formatted[j][1] == 11):
                    del notes_formatted[j]
                else:
                    j += 1

        notes_result = [scale[note[1]] for note in notes_formatted][:3]
        notes_result.sort()
        result.append(notes_result)
        
    return result


def gen_chords(chromas):
    '''
            Generates triad chords as a dictionary like C:['C','E','G'].
            
            Args:
                    chromas: array of chromas.
            Return:
                    chords: dictionary of Major, Minor, Diminished and Augmented chords.

    '''

    chords = {}
    for c in range(len(chromas)):
        # Major chords (C, C#, D, ..., B)
        chords[chromas[c]+chromas[(c+4)%len(chromas)]+chromas[(c+7)%len(chromas)]] = chromas[c]
        # Minor chords (Cm, C#m, Dm, ..., Bm)
        chords[chromas[c]+chromas[(c+3)%len(chromas)]+chromas[(c+7)%len(chromas)]] = chromas[c]+'m'
        # Diminished chords (Cd, C#d, Dd, ..., Bd)
        chords[chromas[c]+chromas[(c+3)%len(chromas)]+chromas[(c+6)%len(chromas)]] = chromas[c]+'d'
        # Augmented chords (C+, C#+, D+, ..., B+)
        chords[chromas[c]+chromas[(c+4)%len(chromas)]+chromas[(c+8)%len(chromas)]] = chromas[c]+'+'

    return chords
