from psychopy import visual, core, event, monitors              # pip install psychopy
import numpy as np                                              # pip install numpy
import pandas as pd                                             # pip install pandas
import random                                                   # pip install random
import os                                                       # pip install os

# Settings
MONITOR_USER = 'Elias'

# Time constants
FIXATION_DURATION = 1
MAX_DECISION_TIME = 3

# Difficulty constants
COHERENCE_EASY = 0.5
COHERENCE_DIFFICULT = 0.2

# Trial length
N_TRIALS_BLOCK1 = 5
N_TRIALS_BLOCK2 = 5
TIME_BLOCK3 = 30
TIME_BLOCK4 = 30
TIME_MAIN = 30

# Minimum required accuracy
MINIMUM_ACCURACY_BLOCK1 = 0.85
MINIMUM_ACCURACY_BLOCK2 = 0.70

# Monitor settings
if MONITOR_USER == 'Stef':
    monitor = monitors.Monitor('Stef', width=30, distance=40) 
    monitor.setSizePix((1920, 1200))
elif MONITOR_USER == 'Yenthe':
    monitor = monitors.Monitor('Yenthe', width=40, distance=50) 
    monitor.setSizePix((2560, 1440))
else:
    print('Monitor not found. Please add monitor settings.')
    core.quit()

# Keys
keys_decision = ['c', 'n', 'escape']
keys_confidence = ['1', '2', '3', '8', '9', '0', 'escape']
keys_instruction = ['space', 'escape']

# Stimuli
win = visual.Window(fullscr=True, color="black", units="deg", monitor=monitor)
fix = visual.TextStim(win, text="+", color='white')
correct = visual.TextStim(win, text="Juist!", color='green')
error = visual.TextStim(win, text="Fout...", color='red')
space = visual.TextStim(win, text="Druk op spatie om door te gaan", color='white', pos=(0, -7))
dotMotion = visual.DotStim(win, units='deg', nDots=120, fieldShape='circle', dotSize=5, color='white', speed=0.1, signalDots='same', noiseDots='direction', dotLife=5, fieldSize=16)

# Instructions
instructions_confidence = visual.ImageStim(win, image='Images/Instructions-Confidence.png', pos=(0, 0), size=(30, 17))
instruction_1 = visual.ImageStim(win, image='Images/Instructions-1.png', pos=(0, 0), size=(30, 17))
instruction_2 = visual.ImageStim(win, image='Images/Instructions-2.png', pos=(0, 0), size=(30, 17))
instruction_3 = visual.ImageStim(win, image='Images/Instructions-3.png', pos=(0, 0), size=(30, 17))
instruction_4 = visual.ImageStim(win, image='Images/Instructions-4.png', pos=(0, 0), size=(30, 17))
instruction_5 = visual.ImageStim(win, image='Images/Instructions-5.png', pos=(0, 0), size=(30, 17))
instruction_6 = visual.ImageStim(win, image='Images/Instructions-6.png', pos=(0, 0), size=(30, 17))

# Trial
def trial(coherence, correct_answer, askConfidence, giveFeedback, timePunishment_decision, timePunishment_confidence):

    # Set dotMotion parameters
    dotMotion.coherence = coherence
    if correct_answer == 'c':
        dotMotion.dir = 180
    elif correct_answer == 'n':
        dotMotion.dir = 0

    # Confidence mapping
    key_mapping = {'1': 1, '2': 2, '3': 3, '8': 4, '9': 5, '0': 6}

    # Draw fixation
    fix.draw()
    win.flip()
    core.wait(FIXATION_DURATION)
    event.clearEvents()

    # Draw stimulus
    while True:
        dotMotion.draw()
        win.flip()
        keys = event.getKeys(keyList=keys_decision)
        if len(keys) > 0:
            response_decision = keys[0]
            break

    # Check response
    if response_decision == 'escape':
        win.close()
        core.quit()    
    elif response_decision == correct_answer:
        if giveFeedback:
            correct.draw()
            win.flip()
            core.wait(1)
        accuracy = 1
    else:
        if giveFeedback:
            error.draw()
            win.flip()
            core.wait(1)
        accuracy = 0
    
    # Ask confidence
    event.clearEvents()
    if askConfidence:
        while True:
            instructions_confidence.draw()
            win.flip()
            keys = event.getKeys(keyList=keys_confidence)
            if len(keys) > 0:
                response_key = keys[0]
                response_confidence = key_mapping[response_key]
                break
        if response_confidence == 'escape':
            win.close()
            core.quit()

    # Time punishment
    timePunishment = 0
    if accuracy == 0:
        timePunishment += timePunishment_decision
    if askConfidence and accuracy == 0:
        timePunishment += timePunishment_confidence[int(response_confidence)-1]
    if askConfidence and accuracy == 1:
        timePunishment += timePunishment_confidence[6-int(response_confidence)]

    # Show time punishment
    if timePunishment > 0:
        punishmentIndicator = visual.TextStim(win, text="Straftijd: " + str(timePunishment), color='white')
        punishmentIndicator.draw()
        win.flip()

    core.wait(timePunishment)

    return accuracy

    
# Block 1

instruction_1.draw()
space.draw()
win.flip()
event.waitKeys(keyList=keys_instruction)

mean_accuracy = 0
while mean_accuracy < MINIMUM_ACCURACY_BLOCK1:

    mean_accuracy = 0

    for trial_number in range(N_TRIALS_BLOCK1):

        correct_answer = random.choice(['c', 'n'])
        trial_accuracy = trial(coherence=COHERENCE_EASY, correct_answer=correct_answer, giveFeedback=True, askConfidence=False, timePunishment_decision=0, timePunishment_confidence = [0, 0, 0, 0, 0, 0])

        mean_accuracy += trial_accuracy

    mean_accuracy = mean_accuracy / N_TRIALS_BLOCK1

# Block 2

instruction_2.draw()
space.draw()
win.flip()
event.waitKeys(keyList=keys_instruction)

mean_accuracy = 0
while mean_accuracy < MINIMUM_ACCURACY_BLOCK2:

    mean_accuracy = 0

    for trial_number in range(N_TRIALS_BLOCK2):

        correct_answer = random.choice(['c', 'n'])
        trial_accuracy = trial(coherence=COHERENCE_DIFFICULT, correct_answer=correct_answer, giveFeedback=True, askConfidence=False, timePunishment_decision=0, timePunishment_confidence = [0, 0, 0, 0, 0, 0])

        mean_accuracy += trial_accuracy

    mean_accuracy = mean_accuracy / N_TRIALS_BLOCK2

# Block 3

instruction_3.draw()
space.draw()
win.flip()
event.waitKeys(keyList=keys_instruction)

score = 0
timer = core.Clock()

while timer.getTime() < TIME_BLOCK3:

    correct_answer = random.choice(['c', 'n'])
    trial_accuracy = trial(coherence=COHERENCE_EASY, correct_answer=correct_answer, giveFeedback=False, askConfidence=False, timePunishment_decision=1, timePunishment_confidence = [0, 0, 0, 0, 0, 0])

    score += trial_accuracy

scoreIndicator = visual.TextStim(win, text="Score: " + str(score), color='white')
scoreIndicator.draw()
win.flip()
core.wait(2)

# Block 4

instruction_4.draw()
space.draw()
win.flip()
event.waitKeys(keyList=keys_instruction)

score = 0
timer = core.Clock()

while timer.getTime() < TIME_BLOCK4:

    correct_answer = random.choice(['c', 'n'])
    trial_accuracy = trial(coherence=COHERENCE_DIFFICULT, correct_answer=correct_answer, giveFeedback=False, askConfidence=True, timePunishment_decision=1, timePunishment_confidence = [0, 0.2, 0.4, 0.6, 0.8, 1])

    score += trial_accuracy

scoreIndicator = visual.TextStim(win, text="Score: " + str(score), color='white')
scoreIndicator.draw()
win.flip()
core.wait(2)

# Main task 1

instruction_5.draw()
space.draw()
win.flip()
event.waitKeys(keyList=keys_instruction)

score = 0
timer = core.Clock()

while timer.getTime() < TIME_MAIN:

    correct_answer = random.choice(['c', 'n'])
    trial_accuracy = trial(coherence=COHERENCE_DIFFICULT, correct_answer=correct_answer, giveFeedback=False, askConfidence=True, timePunishment_decision=2, timePunishment_confidence = [0, 0.2, 0.4, 0.6, 0.8, 1])

    score += trial_accuracy

# Main task 2

instruction_6.draw()
space.draw()
win.flip()
event.waitKeys(keyList=keys_instruction)

score = 0
timer = core.Clock()

while timer.getTime() < TIME_MAIN:

    correct_answer = random.choice(['c', 'n'])
    trial_accuracy = trial(coherence=COHERENCE_DIFFICULT, correct_answer=correct_answer, giveFeedback=False, askConfidence=True, timePunishment_decision=1, timePunishment_confidence = [0, 0.4, 0.8, 1.2, 1.6, 2])

    score += trial_accuracy

# Main task 3

instruction_6.draw()
space.draw()
win.flip()
event.waitKeys(keyList=keys_instruction)

score = 0
timer = core.Clock()

while timer.getTime() < TIME_MAIN:

    correct_answer = random.choice(['c', 'n'])
    trial_accuracy = trial(coherence=COHERENCE_DIFFICULT, correct_answer=correct_answer, giveFeedback=False, askConfidence=True, timePunishment_decision=2, timePunishment_confidence = [0, 0.2, 0.4, 0.6, 0.8, 1])

    score += trial_accuracy

# Main task 4

instruction_6.draw()
space.draw()
win.flip()
event.waitKeys(keyList=keys_instruction)

score = 0
timer = core.Clock()

while timer.getTime() < TIME_MAIN:

    correct_answer = random.choice(['c', 'n'])
    trial_accuracy = trial(coherence=COHERENCE_DIFFICULT, correct_answer=correct_answer, giveFeedback=False, askConfidence=True, timePunishment_decision=1, timePunishment_confidence = [0, 0.4, 0.8, 1.2, 1.6, 2])

    score += trial_accuracy