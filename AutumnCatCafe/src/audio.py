"""Generate simple tones with numpy/pygame for UI feedback."""
import pygame

_ENABLED = False
_SOUNDS  = {}

def _init():
    global _ENABLED
    try:
        import numpy as np
        rate = 44100

        def tone(freq, dur, vol=0.28, kind="sine"):
            n = int(rate * dur)
            t = np.linspace(0, dur, n, endpoint=False)
            if kind == "sine":
                w = np.sin(2 * np.pi * freq * t)
            else:
                w = np.sign(np.sin(2 * np.pi * freq * t)) * 0.6
            # envelope
            atk = min(int(0.01*rate), n)
            rel = min(int(0.08*rate), n)
            env = np.ones(n)
            env[:atk]  = np.linspace(0, 1, atk)
            env[-rel:] = np.linspace(1, 0, rel)
            w = (w * env * vol * 32767).astype(np.int16)
            stereo = np.column_stack([w, w])
            return pygame.sndarray.make_sound(stereo)

        _SOUNDS["click"]   = tone(440,  0.07, 0.20)
        _SOUNDS["coin"]    = tone(880,  0.14, 0.22)
        _SOUNDS["upgrade"] = tone(660,  0.28, 0.28)
        _SOUNDS["error"]   = tone(200,  0.10, 0.18)
        # upgrade chord: layer two tones (play sequentially)
        _SOUNDS["upgrade2"]= tone(990,  0.20, 0.20)
        _ENABLED = True
    except Exception:
        _ENABLED = False


def init_audio():
    if pygame.mixer.get_init():
        _init()


def play(name: str):
    if _ENABLED and name in _SOUNDS:
        try:
            _SOUNDS[name].play()
            if name == "upgrade" and "upgrade2" in _SOUNDS:
                pygame.time.set_timer(pygame.USEREVENT + 99, 160, 1)
        except Exception:
            pass
