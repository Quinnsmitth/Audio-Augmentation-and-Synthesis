from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo
from pathlib import Path
import random

# Path to save generated MIDI files
root = Path("/Users/quinnsmith/Desktop/guitar_synth")
midi_dir = root / "midi"
midi_dir.mkdir(parents=True, exist_ok=True)

print(f"Writing clean guitar riffs to: {midi_dir}")

# Electric guitar program number (General MIDI 28)
CLEAN_GUITAR_PROGRAM = 27

# Realistic electric guitar note range (E2–E6)
GUITAR_RANGE = range(40, 89)

# Common guitar scales (intervals from root note)
SCALES = {
    "C_major":      [0, 2, 4, 5, 7, 9, 11, 12],
    "A_minor":      [0, 2, 3, 5, 7, 8, 10, 12],
    "E_minor_pent": [0, 3, 5, 7, 10, 12],
    "A_blues":      [0, 3, 5, 6, 7, 10, 12],
    "G_major":      [0, 2, 4, 5, 7, 9, 11, 12],
    "D_mixolydian": [0, 2, 4, 5, 7, 9, 10, 12],
    "G_mixolydian": [0, 2, 4, 5, 7, 9, 10, 12],
    "C_mixolydian": [0, 2, 4, 5, 7, 9, 10, 12],
    "major_pent":   [0, 2, 4, 7, 9, 12],
}

def create_clean_guitar_riff(filepath, tempo_bpm=120, num_bars=2):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    # Set tempo and program
    track.append(MetaMessage('set_tempo', tempo=bpm2tempo(tempo_bpm), time=0))
    track.append(Message('program_change', program=CLEAN_GUITAR_PROGRAM, time=0))

    scale = random.choice(list(SCALES.values()))
    print(f"Using scale: {scale}")

    root_note = random.choice([47, 50, 52, 55, 57])
    ticks = mid.ticks_per_beat
    total_length = num_bars * 4 * ticks
    time = 0
    last_note = None

    while time < total_length:
        interval = random.choice(scale)
        note = max(min(root_note + interval, max(GUITAR_RANGE)), min(GUITAR_RANGE))
        velocity = random.randint(80, 120)
        duration = random.choice([ticks//2, ticks, ticks*3//2])
        overlap = random.randint(15, 45)
        pick_delay = random.choice([0, 3, 7, -4])

        # Hammer on / Pull off
        if last_note and random.random() < 0.25:
            note = last_note + random.choice([-2, -1, 1, 2])

        # Slide (pitch bends)
        if random.random() < 0.15:
            track.append(Message('pitchwheel', pitch=random.choice([-1600, 1600]), time=30))
            track.append(Message('pitchwheel', pitch=0, time=30))

        # Note on
        track.append(Message('note_on', note=note, velocity=velocity, time=max(0, pick_delay)))

        # Vibrato for notes longer than 1/4 note
        if duration > ticks:
            vib = random.randint(100, 600)
            track.append(Message('pitchwheel', pitch=vib, time=duration//3))
            track.append(Message('pitchwheel', pitch=-vib, time=duration//3))
            track.append(Message('pitchwheel', pitch=0, time=duration//3))

        # Ensure note off
        track.append(Message('note_off', note=note, velocity=velocity, time=max(0, duration - overlap)))

        last_note = note
        time += duration

    mid.save(filepath)


def create_grateful_dead_riff(filepath, tempo_bpm=110, num_bars=4):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    track.append(MetaMessage('set_tempo', tempo=bpm2tempo(tempo_bpm), time=0))
    track.append(Message('program_change', program=CLEAN_GUITAR_PROGRAM, time=0))

    scale = random.choice([
        SCALES["D_mixolydian"],
        SCALES["G_mixolydian"],
        SCALES["C_mixolydian"],
        SCALES["major_pent"]
    ])
    root_note = random.choice([50, 52, 55, 57])

    ticks = mid.ticks_per_beat
    total_ticks = num_bars * 4 * ticks
    time = 0
    last_note = None

    while time < total_ticks:
        interval = random.choice(scale)
        note = root_note + interval
        velocity = random.randint(70, 105)
        duration = random.choice([ticks//2, ticks//2 + ticks//8])

        # Hammer on / Pull off
        if last_note and random.random() < 0.30:
            note = last_note + random.choice([-2, -1, 1, 2])

        # Octave slide
        if random.random() < 0.10:
            slide_target = note + 12
            track.append(Message("note_on", note=note, velocity=velocity, time=0))
            track.append(Message("pitchwheel", pitch=3000, time=60))
            track.append(Message("note_off", note=note, velocity=velocity, time=10))
            note = slide_target

        track.append(Message("note_on", note=note, velocity=velocity, time=max(0, random.randint(-5, 10))))

        # Vibrato for sustained notes
        if duration > ticks//2 and random.random() < 0.40:
            vib_amt = random.randint(200, 900)
            track.append(Message("pitchwheel", pitch=vib_amt, time=duration//3))
            track.append(Message("pitchwheel", pitch=-vib_amt, time=duration//3))
            track.append(Message("pitchwheel", pitch=0, time=duration//3))

        # Ensure note off
        track.append(Message("note_off", note=note, velocity=velocity, time=0))
        last_note = note
        time += duration

    mid.save(filepath)


def create_clean_chord_progression(filepath, tempo_bpm=120, num_bars=4):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    track.append(MetaMessage('set_tempo', tempo=bpm2tempo(tempo_bpm), time=0))
    track.append(Message('program_change', program=CLEAN_GUITAR_PROGRAM, time=0))

    # chords = [C, G, Am, F, Dm, Em, Bdim]
    chords = [
        [60, 64, 67], [67, 71, 74], [57, 60, 64], [65, 69, 72],
        [62, 65, 69], [64, 67, 71], [59, 62, 65]
    ]

    progression = random.choices(chords, k=num_bars)
    ticks = mid.ticks_per_beat
    chord_dur = 4 * ticks

    for chord in progression:
        # Strum downward pick
        for i, note in enumerate(chord):
            track.append(Message('note_on', note=note, velocity=90 - i*8, time=i*25))

        # Light vibrato
        track.append(Message('pitchwheel', pitch=400, time=chord_dur//3))
        track.append(Message('pitchwheel', pitch=-400, time=chord_dur//3))
        track.append(Message('pitchwheel', pitch=0, time=chord_dur//3))

        # Note off
        for note in chord:
            track.append(Message('note_off', note=note, velocity=64, time=3))
    mid.save(filepath)
    
# Generate files
for i in range(1):
    tempo = random.choice(range(90, 161, 10))
    bars = random.choice([1, 2, 4])
    fpath = midi_dir / f"clean_riff_{i:03d}.mid"
    create_clean_guitar_riff(fpath, tempo_bpm=tempo, num_bars=bars)

for i in range(1):
    tempo = random.choice(range(90, 140, 5))
    bars = random.choice([2, 4, 8])
    fpath = midi_dir / f"dead_riff_{i:03d}.mid"
    create_grateful_dead_riff(fpath, tempo_bpm=tempo, num_bars=bars)

for i in range(1):
    tempo = random.choice(range(90, 161, 10))
    bars = random.choice([1, 2, 4])
    fpath = midi_dir / f"clean_chord_{i:03d}.mid"
    create_clean_chord_progression(fpath, tempo_bpm=tempo, num_bars=bars)

print(f"Generated 30 MIDI files in {midi_dir}")
