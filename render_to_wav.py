# src/render_to_wav.py

import subprocess
from pathlib import Path
from select_path import load_config

root = load_config()
midi_dir = root / "midi"
wav_dir = root / "clean"
wav_dir.mkdir(parents=True, exist_ok=True)

project_root = Path(__file__).resolve().parent.parent
soundfont_dir = project_root / "soundfonts"

# Find any .sf2 or .sf3 soundfont files
sf2_files = list(soundfont_dir.glob("*.sf2")) + list(soundfont_dir.glob("*.sf3"))
if not sf2_files:
    raise FileNotFoundError(f"No soundfont found in {soundfont_dir}")

soundfont = str(sf2_files[0])
print(f"Using soundfont: {soundfont}")

def render_one(midi_path: Path, wav_path: Path):
    """Render a single MIDI file to WAV using FluidSynth."""
    fluidsynth_path = r"D:\fluidsynth\bin\fluidsynth.exe"
    cmd = [
        fluidsynth_path,
        "-ni",
        "-o", "audio.driver=null",  # silent, offline render
        "-r", "44100",              # sample rate
        "-T", "wav",                # output file type
        "-F", str(wav_path),        # output path
        soundfont,                  # soundfont
        str(midi_path),             # midi file
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"\n FluidSynth failed for {midi_path.name}")
        print("Command:", " ".join(cmd))
        print("STDERR:\n", result.stderr)
    else:
        print(f" Rendered {midi_path.name} -> {wav_path.name}")

# Gather all valid MIDI files (skip macOS ._ files)
midis = [m for m in midi_dir.glob("*.mid") if not m.name.startswith("._")]

if not midis:
    print(f"No valid MIDI files found in {midi_dir}. Run generate_midi.py first.")
else:
    for midi_file in midis:
        wav_file = wav_dir / (midi_file.stem + ".wav")
        try:
            render_one(midi_file, wav_file)
        except Exception as e:
            print(f" Skipping {midi_file.name} due to error: {e}")

print(f"\nFast WAV rendering complete ->  {wav_dir}")
