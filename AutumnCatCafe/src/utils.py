"""Shared drawing and formatting utilities."""
import pygame
import math
import sys
import os

# ── Font helpers ─────────────────────────────────────────────

def _find_cjk_font():
    """Return a font file path that can render Japanese, or None."""
    candidates = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/noto-cjk/NotoSansCJKjp-Regular.otf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    # Try fc-list on Linux
    try:
        import subprocess
        out = subprocess.check_output(["fc-list", ":lang=ja", "--format=%{file}\n"],
                                      stderr=subprocess.DEVNULL).decode()
        first = out.strip().split("\n")[0].strip()
        if first and os.path.exists(first):
            return first
    except Exception:
        pass
    return None

CJK_FONT_PATH = _find_cjk_font()

def make_font(size, bold=False, cjk=False):
    if cjk and CJK_FONT_PATH:
        try:
            return pygame.font.Font(CJK_FONT_PATH, size)
        except Exception:
            pass
    try:
        return pygame.font.SysFont("Arial", size, bold=bold)
    except Exception:
        return pygame.font.Font(None, size)


# ── Drawing helpers ──────────────────────────────────────────

def rounded_rect(surf, color, rect, r=12, border=None, bw=2):
    pygame.draw.rect(surf, color, rect, border_radius=r)
    if border:
        pygame.draw.rect(surf, border, rect, bw, border_radius=r)


def dashed_rect(surf, color, rect, dash=8, gap=5, w=2):
    x, y, rw, rh = rect
    for seg in [((x, y),(x+rw, y)), ((x, y+rh),(x+rw, y+rh)),
                ((x, y),(x, y+rh)), ((x+rw, y),(x+rw, y+rh))]:
        _dashed_line(surf, color, seg[0], seg[1], dash, gap, w)


def _dashed_line(surf, color, a, b, dash, gap, w):
    dx, dy = b[0]-a[0], b[1]-a[1]
    length = math.hypot(dx, dy)
    if length == 0:
        return
    ux, uy = dx/length, dy/length
    pos = 0
    drawing = True
    while pos < length:
        seg = dash if drawing else gap
        end = min(pos+seg, length)
        if drawing:
            p1 = (a[0]+ux*pos, a[1]+uy*pos)
            p2 = (a[0]+ux*end, a[1]+uy*end)
            pygame.draw.line(surf, color, p1, p2, w)
        pos = end
        drawing = not drawing


def format_yen(amount: float) -> str:
    return f"¥{int(amount):,}"


def lerp(a, b, t):
    return a + (b-a)*t


def clamp(v, lo, hi):
    return max(lo, min(hi, v))
