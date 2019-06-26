import json
import classifier
from scipy.io import wavfile

def exact_precision(chords, expected_chords):
    '''
        Compare chords and returns percentage of correct notes

        Args:
            chords: list of gotten notes
            expected_chords: list o notes to compare

        Returns:
            percentage between 0 and 1
    '''
    correct_chords = 0
    
    for c in range(min(len(expected_chords['chords']), len(chords))):
        if expected_chords['chords'][c] == chords[c]:
            correct_chords += 1
    
    return correct_chords/min(len(expected_chords['chords']), len(chords))

def near_precision(chords, expected_chords):
    '''
        Compare chords and returns percentage of correct notes
        It gives the current points:
            3. correct chord
            2. correct chord but wrong quality
            1. chord is near expected
            0. otherwise

        Args:
            chords: list of gotten notes
            expected_chords: list o notes to compare

        Returns:
            percentage between 0 and 1
    '''
    correct_chords = 0
    
    for c in range(min(len(expected_chords['chords']), len(chords))):
        expected_chord = expected_chords['chords'][c]
        chord = chords[c]
        
        # Same chord and quality
        if expected_chord == chord:
            correct_chords += 3
            continue
            
        # Removing 'm', 'd' or '+' from end
        if expected_chord[-1] == 'm' or \
           expected_chord[-1] == 'd' or \
           expected_chord[-1] == '+':
            expected_chord = expected_chord[:-1]
            
        if chord[-1] == 'm' or \
           chord[-1] == 'd' or \
           chord[-1] == '+':
            chord = chord[:-1]
        
        #  Same chord but different quality
        if expected_chord == chord:
            correct_chords += 2
            continue
        
        # Near chord
        if scales.indexof(expected_chord[c]) == scales.indexof(chord)-1 or \
           scales.indexof(expected_chord[c]) == scales.indexof(chord)+1 or \
           (scales.indexof(expected_chord[c]) == 0 and chord == 11) or \
           (scales.indexof(expected_chord[c]) == 11 and chord == 0):
            correct_chords += 1
            continue
    
    return correct_chords/(min(len(expected_chords['chords']), len(chords))*3)

def print_precisions(sample):
    '''
        Prints precisions using `exact_precision` and `near_precision` functions

        Args:
            sample: file name without extension
    '''
    # Get the chords groups
    Fs, data = wavfile.read('../wav/{}.wav'.format(sample), 44100)
    scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    note_groups = classifier.get_note_list(data, rate=Fs)
    note_strings = classifier.chord_to_string(note_groups, scale)
    
    # Get the expected chords
    file = '../tabs/{}.json'.format(sample)
    with open(file) as json_file:
        expected_chords = json.load(json_file)
        
        # Using our algorithm to get precisions
        window = int((Fs/1024)*expected_chords['time_step'])
        chords = classifier.compress_result(note_strings, window=window)

        # Starts comparing
        exact_percentage = exact_precision(chords, expected_chords)
        print('The exact precision is {0:.2f}%'.format(exact_percentage*100))
        near_percentage = exact_precision(chords, expected_chords)
        print('The near precision is {0:.2f}%'.format(near_percentage*100))
