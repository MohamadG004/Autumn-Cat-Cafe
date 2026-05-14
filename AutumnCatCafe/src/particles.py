"""Particle systems: falling leaves and floating money text."""
import pygame, math, random
from settings import LEAF_COLORS, WIDTH, HEIGHT, GOLDEN, RED_ACCENT


# ── Single Leaf ──────────────────────────────────────────────

class Leaf:
    def __init__(self, x=None, y=None):
        self.x     = x if x is not None else random.randint(0, WIDTH)
        self.y     = y if y is not None else random.randint(-60, -5)
        self.size  = random.randint(8, 20)
        self.color = random.choice(LEAF_COLORS)
        self.vy    = random.uniform(38, 85)
        self.vx    = random.uniform(-25, 25)
        self.rot   = random.uniform(0, 360)
        self.rspe  = random.uniform(-90, 90)
        self.wob   = random.uniform(0, math.pi*2)
        self.wspe  = random.uniform(1.5, 3.5)
        self.alpha = random.randint(170, 235)
        self.alive = True
        # pre-build surface
        self._surf = None
        self._build()

    def _build(self):
        d = self.size * 2 + 4
        s = pygame.Surface((d, d), pygame.SRCALPHA)
        # Oval leaf
        pygame.draw.ellipse(s, (*self.color, self.alpha),
                            (2, d//2 - self.size//3, self.size*2, self.size*2//3 + self.size//2))
        # Stem
        pygame.draw.line(s, (*self.color, self.alpha),
                         (d//2, d//2), (d//2 + self.size//2, d//2 + self.size//3), 1)
        self._base = s

    def update(self, dt):
        self.wob += self.wspe * dt
        self.x   += (self.vx + math.sin(self.wob) * 18) * dt
        self.y   += self.vy * dt
        self.rot += self.rspe * dt
        if self.y > HEIGHT + 30:
            self.alive = False

    def draw(self, surface):
        rotated = pygame.transform.rotate(self._base, self.rot)
        r = rotated.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated, r)


# ── Leaf System ──────────────────────────────────────────────

class LeafSystem:
    def __init__(self):
        self.leaves      = []
        self.spawn_t     = 0.0
        self.spawn_int   = 0.35
        # seed some leaves already on screen
        for _ in range(18):
            lf = Leaf(y=random.randint(0, HEIGHT))
            self.leaves.append(lf)

    def update(self, dt):
        self.spawn_t += dt
        if self.spawn_t >= self.spawn_int:
            self.spawn_t = 0
            self.leaves.append(Leaf())
        for lf in self.leaves:
            lf.update(dt)
        self.leaves = [lf for lf in self.leaves if lf.alive]

    def draw(self, surface):
        for lf in self.leaves:
            lf.draw(surface)


# ── Floating Text ────────────────────────────────────────────

class FloatingText:
    def __init__(self, x, y, text, color, font):
        self.x     = float(x)
        self.y     = float(y)
        self.text  = text
        self.color = color
        self.font  = font
        self.alpha = 255.0
        self.vy    = -62.0
        self.alive = True

    def update(self, dt):
        self.y    += self.vy * dt
        self.vy   += 28 * dt   # decelerate
        self.alpha -= 220 * dt
        if self.alpha <= 0:
            self.alive = False

    def draw(self, surface):
        if not self.font:
            return
        surf = self.font.render(self.text, True, self.color)
        surf.set_alpha(max(0, int(self.alpha)))
        r = surf.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(surf, r)


class FloatTextSystem:
    def __init__(self):
        self.texts = []

    def add(self, x, y, text, color=GOLDEN, font=None):
        self.texts.append(FloatingText(x, y, text, color, font))

    def update(self, dt):
        for t in self.texts:
            t.update(dt)
        self.texts = [t for t in self.texts if t.alive]

    def draw(self, surface):
        for t in self.texts:
            t.draw(surface)
