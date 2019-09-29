# Currently, just major, and all of the modes.
import copy

# For printing out notes
NOTE_NAMES = 'C C# D D# E F F# G G# A A# B'.split()

# We are using integer notation to find the notes and scales.
NOTE_NUMS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

# An array of the scale/mode forumlas, major and on, for easier programming.
MODE_FORMS = [[2,4,5,7,9,11,12],
              [2,3,5,7,9,10,12],
              [1,3,5,7,8,10,12],
              [2,4,6,7,9,11,12],
              [2,4,5,7,9,10,12],
              [2,3,5,7,8,10,12],
              [1,3,5,6,8,10,12]
]
# An array of mode names, for easier programming.
MODE_NAMES = ["Major",
              "Dorain",
              "Phygrian",
              "Lydian",
              "Mixolydian",
              "Natural Minor",
              "Locrian"
]

ALL_SCALES = {
}
ALL_SCALES_NAME = {
}
ALL_SCALES_SETS = {
}

def note_name(n): return NOTE_NAMES[n % 12]

def createScales():
    sN = 0 # sN stands for start note, this is the note that we are beginning
           # the scale with.
    tL = [] # tL is tempList, we will be storing the scale in here, to be moved
            # to the dictionary.
    
    # range of 12, for all the keys.
    # This is the Dorian Mode.
    modeNum = 0
    for modeNum in range(len(MODE_NAMES) - 1):
        for sN in range(12):
            tL.append(sN%12)
            # We are using the MODE_FORMS array to get the steps for the scales.
            tL.append((sN+MODE_FORMS[modeNum][0])%12)
            tL.append((sN+MODE_FORMS[modeNum][1])%12)
            tL.append((sN+MODE_FORMS[modeNum][2])%12)
            tL.append((sN+MODE_FORMS[modeNum][3])%12)
            tL.append((sN+MODE_FORMS[modeNum][4])%12)
            tL.append((sN+MODE_FORMS[modeNum][5])%12)
            tL.append((sN+MODE_FORMS[modeNum][6])%12)
            ALL_SCALES[NOTE_NAMES[sN % 12], MODE_NAMES[modeNum]] = tL
            # moving the start note e.g. C -> C#    
            sN += 1
            tL = []
        modeNum += 1

def createScalesName():
    sN = 0 # sN stands for start note, this is the note that we are beginning
           # the scale with.
    tL = [] # tL is tempList, we will be storing the scale in here, to be moved
            # to the dictionary.
    
    # range of 12, for all the keys.
    # This is the Dorian Mode.
    modeNum = 0
    for modeNum in range(len(MODE_NAMES) - 1):
        for sN in range(12):
            tL.append(note_name(sN))
            # We are using the MODE_FORMS array to get the steps for the scales.
            tL.append((note_name(sN+MODE_FORMS[modeNum][0])))
            tL.append((note_name(sN+MODE_FORMS[modeNum][1])))
            tL.append((note_name(sN+MODE_FORMS[modeNum][2])))
            tL.append((note_name(sN+MODE_FORMS[modeNum][3])))
            tL.append((note_name(sN+MODE_FORMS[modeNum][4])))
            tL.append((note_name(sN+MODE_FORMS[modeNum][5])))
            tL.append((note_name(sN+MODE_FORMS[modeNum][6])))
            ALL_SCALES_NAME[NOTE_NAMES[sN % 12], MODE_NAMES[modeNum]] = tL
            # moving the start note e.g. C -> C#    
            sN += 1
            tL = []
        modeNum += 1
        
createScales()
createScalesName()

#This is a second set, which contains sets instead of list to compare our notes to.
ALL_SCALES_SETS = copy.deepcopy(ALL_SCALES)
for x in ALL_SCALES_SETS:
    ALL_SCALES_SETS[x] = set(ALL_SCALES[x])
