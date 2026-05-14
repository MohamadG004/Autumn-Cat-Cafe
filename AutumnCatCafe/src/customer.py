"""Tiny chibi customers that walk into the café."""
import pygame, math, random
from settings import WIDTH, HEIGHT, CUSTOMER_INTERVAL, CUSTOMER_BONUS

_SKIN  = [(180,130,90),(220,185,148),(100,68,48),(200,160,110),(240,205,168)]
_SHIRT = [(160,80,80),(80,110,160),(100,140,100),(180,140,80),(130,80,165),(200,130,60)]
_HAIR  = [(40,28,18),(80,55,30),(200,160,100),(55,40,30),(160,120,70)]

SERVE_X = 760   # x where they stop


class Customer:
    def __init__(self):
        self.x        = float(WIDTH + 40)
        self.y        = float(HEIGHT - 168)
        self.speed    = random.uniform(65, 110)
        self.skin     = random.choice(_SKIN)
        self.shirt    = random.choice(_SHIRT)
        self.hair     = random.choice(_HAIR)
        self.scale    = random.uniform(0.72, 0.95)
        self.state    = "walking"        # walking → ordering → leaving
        self.order_t  = random.uniform(2.2, 3.8)
        self.alpha    = 255.0
        self.alive    = True
        self.bob_t    = random.uniform(0, math.pi*2)
        self.bob_spd  = random.uniform(5, 8)
        self.served   = False            # callback fired yet?

    def update(self, dt):
        self.bob_t += self.bob_spd * dt

        if self.state == "walking":
            self.x -= self.speed * dt
            if self.x <= SERVE_X:
                self.x     = SERVE_X
                self.state = "ordering"

        elif self.state == "ordering":
            self.order_t -= dt
            if self.order_t <= 0:
                self.state = "leaving"

        elif self.state == "leaving":
            self.x     -= self.speed * 0.85 * dt
            self.alpha -= 160 * dt
            if self.alpha <= 0:
                self.alive = False

    def draw(self, surface):
        bob = math.sin(self.bob_t) * 2 if self.state == "walking" else 0
        cx  = int(self.x)
        cy  = int(self.y + bob)
        s   = self.scale
        a   = max(0, int(self.alpha))

        # Build chibi on a small surface
        W, H = 56, 90
        buf  = pygame.Surface((W, H), pygame.SRCALPHA)

        # Legs
        leg_col = (*self.shirt, a)
        pygame.draw.rect(buf, leg_col, (W//2-13, 58, 11, 24))
        pygame.draw.rect(buf, leg_col, (W//2+2,  58, 11, 24))
        # Shoes
        shoe = (38, 28, 18, a)
        pygame.draw.ellipse(buf, shoe, (W//2-16, 77, 16, 9))
        pygame.draw.ellipse(buf, shoe, (W//2+0,  77, 16, 9))
        # Body
        pygame.draw.ellipse(buf, (*self.shirt, a), (W//2-16, 36, 32, 28))
        # Head
        pygame.draw.circle(buf, (*self.skin, a), (W//2, 22), 17)
        # Hair
        pygame.draw.ellipse(buf, (*self.hair, a), (W//2-17, 6, 34, 20))
        # Eyes
        pygame.draw.circle(buf, (30, 20, 12, a), (W//2-6, 22), 3)
        pygame.draw.circle(buf, (30, 20, 12, a), (W//2+6, 22), 3)
        # Shine
        pygame.draw.circle(buf, (255,255,255, a), (W//2-5, 20), 1)
        pygame.draw.circle(buf, (255,255,255, a), (W//2+7, 20), 1)

        scaled = pygame.transform.scale(buf, (int(W*s), int(H*s)))
        r = scaled.get_rect(midbottom=(cx, cy))
        surface.blit(scaled, r)

        # Speech bubble when ordering
        if self.state == "ordering":
            bx, by = cx + 18, cy - int(90*s) - 4
            pygame.draw.ellipse(surface, (252,248,240),
                                (bx-18, by-14, 36, 22))
            pygame.draw.ellipse(surface, (200,180,155),
                                (bx-18, by-14, 36, 22), 1)
            # coffee cup dots
            pygame.draw.circle(surface, (100,65,35), (bx-4, by-3), 3)
            pygame.draw.circle(surface, (224,164,42), (bx+4, by-3), 3)


class CustomerSystem:
    def __init__(self):
        self.customers   = []
        self.spawn_t     = 0.0
        self.spawn_int   = CUSTOMER_INTERVAL
        self.on_served   = None   # callback(x, y)

    def update(self, dt):
        self.spawn_t += dt
        if self.spawn_t >= self.spawn_int:
            self.spawn_t    = 0
            self.spawn_int  = random.uniform(CUSTOMER_INTERVAL*0.7,
                                             CUSTOMER_INTERVAL*1.4)
            self.customers.append(Customer())

        for c in self.customers:
            was_ordering = (c.state == "ordering")
            c.update(dt)
            # Fire served callback once
            if was_ordering and c.state == "leaving" and not c.served:
                c.served = True
                if self.on_served:
                    self.on_served(c.x, c.y)

        self.customers = [c for c in self.customers if c.alive]

    def draw(self, surface):
        for c in self.customers:
            c.draw(surface)
