#! /usr/bin/env python
######################################################################
# FindScale.py - A console based scale finder.
# Requires numpy and pyaudio.
######################################################################

import numpy as np
import pyaudio
import sounddevice as sd

######################################################################
# ALl Scales is a homemade script that can genrate all scales and their modes
## MORE TO ALL TO THIS SCRIPT: PENETONIC, HARMONIC MINOR, MEDOLDIC MINOR ##
import AllScales
######################################################################
# Feel free to play with these numbers. Might want to change NOTE_MIN
# and NOTE_MAX especially for guitar/bass. Probably want to keep
# FRAME_SIZE and FRAMES_PER_FFT to be powers of two.

NOTE_MIN = 40       # E2 These are midi values
NOTE_MAX = 76       # E5 
FSAMP = 22050       # Sampling frequency in Hz
FRAME_SIZE = 2048   # How many samples per frame?
FRAMES_PER_FFT = 16 # FFT takes average across how many frames?
SOUND_CUTOFF = 5    # Used to make sure dead silence is not read in.
DURATION = 1       # The number of seconds we get to play the notes.
soundLevel = 0
######################################################################
# Derived quantities from constants above. Note that as
# SAMPLES_PER_FFT goes up, the frequency step size decreases (so
# resolution increases); however, it will incur more delay to process
# new sounds.

SAMPLES_PER_FFT = FRAME_SIZE*FRAMES_PER_FFT
FREQ_STEP = float(FSAMP)/SAMPLES_PER_FFT

######################################################################
# For printing out notes
NOTE_NAMES = 'C C# D D# E F F# G G# A A# B'.split()

# We are using integer notation to find the notes and scales.
NOTE_NUMS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

# We are using this to hold all currently known scales.
ALL_SCALES = AllScales.ALL_SCALES
ALL_SCALES_NAMES = AllScales.ALL_SCALES_NAME
ALL_SCALES_SETS = AllScales.ALL_SCALES_SETS
SubScalesWithNames ={}
# A set used to store the notes played by user.
scaleNotes = []
scaleNotesSet = set()
######################################################################
# These three functions are based upon this very useful webpage:
# https://newt.phys.unsw.edu.au/jw/notes.html

def freq_to_number(f): return 69 + 12*np.log2(f/440.0)
def number_to_freq(n): return 440 * 2.0**((n-69)/12.0)
# The original function included the note number, with a decimal point, unecessary for this project.
def note_name(n): return NOTE_NAMES[n % 12]
# Homemade function that returns num from name.
def note_num(n): return NOTE_NUMS[n % 12]
######################################################################
# A wonderful function from: https://github.com/arupiot/Sound-level-meter/blob/master/slm.py
# This is popped into the sound device function, Stream, and runs for a little bit.
# The function was changed to return, rather than print, the decibel value.
def return_sound(indata, outdata, frames, time, status):
    volume_norm = np.linalg.norm(indata)*10
    if (int(volume_norm)) > SOUND_CUTOFF:
        if note_name(n0) not in scaleNotes:
            scaleNotes.append(note_name(n0))
            scaleNotesSet.add(note_num(n0))
            subSets = [ss for ss in ALL_SCALES_SETS.values() if scaleNotesSet.issubset(ss)]
            
            for (k,v) in ALL_SCALES_SETS.items():
                for i in range(len(subSets)):
                    if(subSets[i].issubset(v)):
                        SubScalesWithNames[k] = ALL_SCALES_NAMES[k]
            print(scaleNotes)
            print(SubScalesWithNames)
            SubScalesWithNames.clear()
######################################################################
# Ok, ready to go now.
# Get min/max index within FFT of notes we care about.
# See docs for numpy.rfftfreq()
def note_to_fftbin(n): return number_to_freq(n)/FREQ_STEP
imin = max(0, int(np.floor(note_to_fftbin(NOTE_MIN-1))))
imax = min(SAMPLES_PER_FFT, int(np.ceil(note_to_fftbin(NOTE_MAX+1))))

# Allocate space to run an FFT. 
buf = np.zeros(SAMPLES_PER_FFT, dtype=np.float32)
num_frames = 0

# Initialize audio
stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,
                                channels=1,
                                rate=FSAMP,
                                input=True,
                                frames_per_buffer=FRAME_SIZE)

stream.start_stream()

# Create Hanning window function
window = 0.5 * (1 - np.cos(np.linspace(0, 2*np.pi, SAMPLES_PER_FFT, False)))

# Print initial text
print ('sampling at', FSAMP, 'Hz with max resolution of', FREQ_STEP, 'Hz')

# As long as we are getting data:
while stream.is_active():

    # Shift the buffer down and new data in
    buf[:-FRAME_SIZE] = buf[FRAME_SIZE:]
    buf[-FRAME_SIZE:] = np.frombuffer(stream.read(FRAME_SIZE), np.int16)

    # Run the FFT on the windowed buffer
    fft = np.fft.rfft(buf * window)

    # Get frequency of maximum response in range
    freq = (np.abs(fft[imin:imax]).argmax() + imin) * FREQ_STEP

    # Get note number and nearest note
    n = freq_to_number(freq)
    n0 = int(round(n))

    # Console output once we have a full buffer
    num_frames += 1
    with sd.Stream(callback=return_sound):
        sd.sleep(DURATION * 80)
