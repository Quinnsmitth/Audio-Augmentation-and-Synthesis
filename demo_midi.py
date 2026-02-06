from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo
from pathlib import Path
import random
import os

# Get path to the user's Downloads folder
downloads_dir = Path.home() / "Downloads"

# Create the MIDI file path
midi_path = downloads_dir / "simple_guitar_riff.mid"

# Create a new MIDI file and track
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

# Parameters
bpm = 180
preset = 27
length = 8

# Meta information
track.append(MetaMessage('set_tempo', tempo=bpm2tempo(bpm)))  # 100 BPM
track.append(MetaMessage('track_name', name='Simple Guitar Riff'))

# General MIDI program number for clean electric guitar (program 27)
track.append(Message('program_change', program=preset, time=0))

# Define a simple C major riff (MIDI note numbers for E2–A5 range)
notes = [48, 52, 55, 60, 64, 67]  # C major chord tones

# Generate 8 random strums
for i in range(length):
    note = random.choice(notes)
    velocity = random.randint(70, 110)
    duration = random.choice([240, 480])  # quarter or half note

    # Note on / note off events
    track.append(Message('note_on', note=note, velocity=velocity, time=0))
    track.append(Message('note_off', note=note, velocity=0, time=duration))

# Save the file
mid.save(midi_path)
print(f"Saved MIDI file to: {midi_path}")
