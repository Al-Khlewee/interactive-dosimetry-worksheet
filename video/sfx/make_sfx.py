"""Synthesize the video's sound effects and the full soundtrack.

Every sound is generated here from sine tones and filtered noise, so there
is nothing to license. Cue times match the animation timeline in
../dosimetry-video.html (scene starts, counters, the baseline marker).

Usage: python3 make_sfx.py            -> writes the SFX WAVs and soundtrack.wav
"""
import wave
from pathlib import Path

import numpy as np

SR = 44100
DURATION = 85.0
OUT = Path(__file__).parent
rng = np.random.default_rng(7)


def t_axis(sec):
    return np.arange(int(SR * sec)) / SR


def envelope(n, attack, release_curve=4.0):
    """Fast linear attack, exponential-ish release over the rest."""
    a = max(1, int(SR * attack))
    env = np.ones(n)
    env[:a] = np.linspace(0, 1, a)
    env[a:] = np.exp(-release_curve * np.linspace(0, 1, n - a))
    return env


def lowpass_sweep(x, cutoffs):
    """One-pole low-pass with a per-sample cutoff (Hz)."""
    y = np.zeros_like(x)
    alpha = 1 - np.exp(-2 * np.pi * cutoffs / SR)
    acc = 0.0
    for i in range(len(x)):
        acc += alpha[i] * (x[i] - acc)
        y[i] = acc
    return y


def whoosh(sec=0.9, lo=300, hi=3200, level=0.5):
    n = int(SR * sec)
    noise = rng.standard_normal(n)
    shape = np.sin(np.pi * np.linspace(0, 1, n)) ** 1.6          # swell in and out
    cut = lo + (hi - lo) * shape
    band = lowpass_sweep(noise, cut) - lowpass_sweep(noise, cut * 0.35)
    out = band * shape
    return level * out / (np.abs(out).max() + 1e-9)


def tick(freq=1900, level=0.22):
    t = t_axis(0.05)
    tone = np.sin(2 * np.pi * freq * t) * np.exp(-t * 90)
    click = rng.standard_normal(len(t)) * np.exp(-t * 400) * 0.25
    return level * (tone + click)


def blip(level=0.28):
    t = t_axis(0.16)
    f = np.where(t < 0.06, 880, 1320)
    phase = 2 * np.pi * np.cumsum(f) / SR
    return level * np.sin(phase) * envelope(len(t), 0.004, 5)


def bell(freq, sec=1.4, level=0.3):
    t = t_axis(sec)
    partials = [(1.0, 1.0), (2.0, 0.35), (2.76, 0.22), (5.4, 0.08)]   # soft, slightly inharmonic
    s = sum(a * np.sin(2 * np.pi * freq * m * t) * np.exp(-t * (3 + 2.5 * m)) for m, a in partials)
    return level * s * envelope(len(t), 0.003, 0.0) / 1.65


def chime():
    return bell(1046.5, level=0.3)                                       # C6


def chime_positive():
    a, b = bell(1046.5, level=0.26), bell(1318.5, level=0.26)            # C6 then E6
    out = np.zeros(len(a) + int(SR * 0.12))
    out[:len(a)] += a
    out[int(SR * 0.12):] += b
    return out


def closing():
    t = t_axis(2.2)
    notes = [523.25, 659.25, 783.99, 1046.5]                             # C major, soft pad
    pad = sum(np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t) for f in notes)
    env = np.minimum(t / 0.25, 1) * np.exp(-t * 1.6)
    return 0.12 * pad * env


def write(path, x):
    x = np.clip(x, -1, 1)
    pcm = (x * 32767).astype('<i2')
    stereo = np.repeat(pcm[:, None], 2, axis=1)
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(stereo.tobytes())


sounds = {
    'whoosh': whoosh(),
    'transition': whoosh(sec=0.6, lo=180, hi=1400, level=0.12),
    'tick': tick(),
    'blip': blip(),
    'chime': chime(),
    'chime_positive': chime_positive(),
    'closing': closing(),
}

# Key moments only; every other step stays silent.
cues = [
    (0.2, 'whoosh'),                                                     # emblem appears
    *[(t, 'tick') for t in (2.9, 3.3, 3.7, 4.1)],                        # equation terms light up
    *[(t, 'transition') for t in (6, 14, 21, 29, 37, 45, 55, 63, 72, 78)],  # scene changes, very quiet
    (12.4, 'blip'),                                                      # electrometer reaches 1.950 nC
    (60.6, 'chime'),                                                     # final dose 0.1028 Gy
    (67.0, 'chime_positive'),                                            # marker lands in "Normal"
    (82.3, 'closing'),                                                   # closing card
]

if __name__ == '__main__':
    for name, x in sounds.items():
        write(OUT / f'{name}.wav', x)
    track = np.zeros(int(SR * DURATION))
    for at, name in cues:
        x = sounds[name]
        i = int(SR * at)
        j = min(len(track), i + len(x))
        track[i:j] += x[:j - i]
    track *= 0.5 / np.abs(track).max()                                   # peak about -6 dBFS
    write(OUT / 'soundtrack.wav', track)
    print('wrote', len(sounds), 'sounds and soundtrack.wav')
