from psychopy import visual, core, event, monitors, sound       # type: ignore
import numpy as np                                              # type: ignore
import random                                                   # type: ignore

# Settings
MONITOR_USER = 'Elias'
monitor_settings = {
    "Stef": {"width": 30, "distance": 40, "resolution": (1920, 1200)},
    "Yenthe": {"width": 40, "distance": 50, "resolution": (2560, 1440)},
    "Elias": {"width": 30, "distance": 40, "resolution": (1920, 1080)},
}

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
if MONITOR_USER in monitor_settings:
    settings = monitor_settings[MONITOR_USER]
    monitor = monitors.Monitor(MONITOR_USER, width=settings["width"], distance=settings["distance"])
    monitor.setSizePix(settings["resolution"])
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

# Sound
def play_sound(file):
    start_music = sound.Sound('Audio/' + file)
    start_music.play()
    core.wait(start_music.getDuration())

# Confetti streamers
def confetti_streamers(win, duration=5, n_streamers=50, streamer_length=10):
    confetti_positions = np.random.uniform(-20, 20, size=(n_streamers, 2))
    confetti_colors = [np.random.choice(['red', 'blue', 'green', 'yellow', 'white', 'magenta']) for _ in range(n_streamers)]
    confetti_speeds = np.random.uniform(0.05, 0.2, size=n_streamers)
    confetti_directions = np.random.uniform(0, 360, size=n_streamers)
    streamers = [
        [
            visual.Rect(
                win,
                width=0.2,
                height=0.6,
                fillColor=color,
                lineColor=color,
                pos=(pos[0], pos[1])
            ) for _ in range(streamer_length)
        ]
        for pos, color in zip(confetti_positions, confetti_colors)
    ]
    play_sound('confetti.mp3')
    timer = core.Clock()
    while timer.getTime() < duration:
        win.clearBuffer()
        for i in range(n_streamers):
            angle_rad = np.deg2rad(confetti_directions[i])
            dx = confetti_speeds[i] * np.cos(angle_rad)
            dy = confetti_speeds[i] * np.sin(angle_rad)
            for j, rect in enumerate(streamers[i]):
                lag_factor = j / streamer_length
                rect.pos = (
                    confetti_positions[i][0] + dx * lag_factor,
                    confetti_positions[i][1] + dy * lag_factor
                )
                rect.ori += np.random.uniform(-5, 5)
                rect.draw()
            confetti_positions[i] = (
                confetti_positions[i][0] + dx,
                confetti_positions[i][1] + dy
            )
        win.flip()

# Trial
def trial(coherence, correct_answer, askConfidence, giveFeedback, timePunishment_decision, timePunishment_confidence):

    # Set dotMotion parameters
    dotMotion.coherence = coherence
    if correct_answer == 'c': dotMotion.dir = 180
    elif correct_answer == 'n': dotMotion.dir = 0

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

def start_experiment():
    ########## Block 1 ##########
    instruction_1.draw()
    space.draw()
    win.flip()
    event.waitKeys(keyList=keys_instruction)
    mean_accuracy = 0
    play_sound('start_music.wav')
    while mean_accuracy < MINIMUM_ACCURACY_BLOCK1:
        mean_accuracy = 0
        for trial_number in range(N_TRIALS_BLOCK1):
            correct_answer = random.choice(['c', 'n'])
            trial_accuracy = trial(coherence=COHERENCE_EASY, correct_answer=correct_answer, giveFeedback=True, askConfidence=False, timePunishment_decision=0, timePunishment_confidence = [0, 0, 0, 0, 0, 0])
            mean_accuracy += trial_accuracy
        mean_accuracy = mean_accuracy / N_TRIALS_BLOCK1
    ########## Block 2 ##########
    instruction_2.draw()
    space.draw()
    win.flip()
    event.waitKeys(keyList=keys_instruction)
    mean_accuracy = 0
    play_sound('start_music.wav')
    while mean_accuracy < MINIMUM_ACCURACY_BLOCK2:
        mean_accuracy = 0
        for trial_number in range(N_TRIALS_BLOCK2):
            correct_answer = random.choice(['c', 'n'])
            trial_accuracy = trial(coherence=COHERENCE_DIFFICULT, correct_answer=correct_answer, giveFeedback=True, askConfidence=False, timePunishment_decision=0, timePunishment_confidence = [0, 0, 0, 0, 0, 0])
            mean_accuracy += trial_accuracy
        mean_accuracy = mean_accuracy / N_TRIALS_BLOCK2
    ########## Block 3 ##########
    instruction_3.draw()
    space.draw()
    win.flip()
    event.waitKeys(keyList=keys_instruction)
    score = 0
    timer = core.Clock()
    play_sound('start_music.wav')
    while timer.getTime() < TIME_BLOCK3:
        correct_answer = random.choice(['c', 'n'])
        trial_accuracy = trial(coherence=COHERENCE_EASY, correct_answer=correct_answer, giveFeedback=False, askConfidence=False, timePunishment_decision=1, timePunishment_confidence = [0, 0, 0, 0, 0, 0])
        score += trial_accuracy
    scoreIndicator = visual.TextStim(win, text="Score: " + str(score), color='white')
    scoreIndicator.draw()
    win.flip()
    core.wait(2)
    ########## Block 4 ##########
    instruction_4.draw()
    space.draw()
    win.flip()
    event.waitKeys(keyList=keys_instruction)
    score = 0
    timer = core.Clock()
    play_sound('start_music.wav')
    while timer.getTime() < TIME_BLOCK4:
        correct_answer = random.choice(['c', 'n'])
        trial_accuracy = trial(coherence=COHERENCE_DIFFICULT, correct_answer=correct_answer, giveFeedback=False, askConfidence=True, timePunishment_decision=1, timePunishment_confidence = [0, 0.2, 0.4, 0.6, 0.8, 1])
        score += trial_accuracy
    scoreIndicator = visual.TextStim(win, text="Score: " + str(score), color='white')
    scoreIndicator.draw()
    win.flip()
    core.wait(2)
    ########## Main Task 1 ##########
    instruction_5.draw()
    space.draw()
    win.flip()
    event.waitKeys(keyList=keys_instruction)
    score = 0
    timer = core.Clock()
    play_sound('start_music.wav')
    while timer.getTime() < TIME_MAIN:
        correct_answer = random.choice(['c', 'n'])
        trial_accuracy = trial(coherence=COHERENCE_DIFFICULT, correct_answer=correct_answer, giveFeedback=False, askConfidence=True, timePunishment_decision=2, timePunishment_confidence = [0, 0.2, 0.4, 0.6, 0.8, 1])
        score += trial_accuracy
    ########## Main Task 2 ##########
    instruction_6.draw()
    space.draw()
    win.flip()
    event.waitKeys(keyList=keys_instruction)
    score = 0
    timer = core.Clock()
    play_sound('start_music.wav')
    while timer.getTime() < TIME_MAIN:
        correct_answer = random.choice(['c', 'n'])
        trial_accuracy = trial(coherence=COHERENCE_DIFFICULT, correct_answer=correct_answer, giveFeedback=False, askConfidence=True, timePunishment_decision=1, timePunishment_confidence = [0, 0.4, 0.8, 1.2, 1.6, 2])
        score += trial_accuracy
    ########## Main Task 3 ##########
    instruction_6.draw()
    space.draw()
    win.flip()
    event.waitKeys(keyList=keys_instruction)
    score = 0
    timer = core.Clock()
    play_sound('start_music.wav')
    while timer.getTime() < TIME_MAIN:
        correct_answer = random.choice(['c', 'n'])
        trial_accuracy = trial(coherence=COHERENCE_DIFFICULT, correct_answer=correct_answer, giveFeedback=False, askConfidence=True, timePunishment_decision=2, timePunishment_confidence = [0, 0.2, 0.4, 0.6, 0.8, 1])
        score += trial_accuracy
    ########## Main Task 4 ##########
    instruction_6.draw()
    space.draw()
    win.flip()
    event.waitKeys(keyList=keys_instruction)
    score = 0
    timer = core.Clock()
    play_sound('start_music.wav')
    while timer.getTime() < TIME_MAIN:
        correct_answer = random.choice(['c', 'n'])
        trial_accuracy = trial(coherence=COHERENCE_DIFFICULT, correct_answer=correct_answer, giveFeedback=False, askConfidence=True, timePunishment_decision=1, timePunishment_confidence = [0, 0.4, 0.8, 1.2, 1.6, 2])
    score += trial_accuracy

start_experiment()                                                              # Start the experiment
confetti_streamers(win, duration=5, n_streamers=50, streamer_length=10)         # Show confetti streamers
win.close()
core.quit()