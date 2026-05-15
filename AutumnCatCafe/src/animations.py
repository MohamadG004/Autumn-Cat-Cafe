"""Animation helpers: cat idle, screen shake."""
import math, random


class CatAnimator:
    def __init__(self):
        self.t          = 0.0
        self.blink_t    = 0.0
        self.blink_int  = 3.5   # seconds between blinks
        self.blinking   = False
        self.blink_dur  = 0.14
        self.tail_angle = 0.0
        self.tail_dir   = 1
        self.tail_speed = 48    # degrees / sec
        self._click_bounce = 0.0   # extra vertical bounce on click

    def trigger_click(self):
        """Make the cat hop upward when the brew button is pressed."""
        self._click_bounce = 1.0

    def update(self, dt):
        self.t += dt

        # Click bounce decay
        if self._click_bounce > 0:
            self._click_bounce = max(0.0, self._click_bounce - dt * 7)

        # Tail wag
        self.tail_angle += self.tail_speed * self.tail_dir * dt
        if abs(self.tail_angle) > 28:
            self.tail_dir *= -1

        # Blinking
        self.blink_t += dt
        if not self.blinking and self.blink_t >= self.blink_int:
            self.blinking = True
            self.blink_t  = 0.0
        if self.blinking and self.blink_t >= self.blink_dur:
            self.blinking = False
            self.blink_t  = 0.0
            self.blink_int = random.uniform(2.5, 5.0)

    @property
    def bob(self):
        """Vertical bob offset in pixels (includes click hop)."""
        hop = -math.sin(self._click_bounce * math.pi) * 14
        return math.sin(self.t * 1.4) * 2.5 + hop

    @property
    def tail_rad(self):
        return math.radians(self.tail_angle)


class ShakeEffect:
    def __init__(self):
        self.intensity = 0
        self.timer     = 0.0
        self.duration  = 0.28

    def trigger(self, intensity=5):
        self.intensity = intensity
        self.timer     = self.duration

    def update(self, dt):
        if self.timer > 0:
            self.timer = max(0.0, self.timer - dt)

    def offset(self):
        if self.timer <= 0:
            return (0, 0)
        t = self.timer / self.duration
        i = max(1, int(self.intensity * t))
        return (random.randint(-i, i), random.randint(-i, i))