"""Core Game class – ties together all subsystems."""
import pygame
from settings import *
from src.renderer  import Renderer
from src.ui        import UpgradeButton
from src.upgrades  import make_upgrades
from src.customer  import CustomerSystem
from src.particles import LeafSystem, FloatTextSystem
from src.animations import CatAnimator, ShakeEffect
from src.utils     import format_yen, make_font
import src.audio   as audio


class Game:
    def __init__(self, screen):
        self.screen = screen

        # ── Core state ────────────────────────────────────────
        self.yen              = float(STARTING_YEN)
        self.income_per_second= AUTO_INCOME_BASE
        self._income_acc      = 0.0
        self.upgrades         = make_upgrades()

        # ── Subsystems ────────────────────────────────────────
        self.renderer     = Renderer(screen)
        self.customers    = CustomerSystem()
        self.leaves       = LeafSystem()
        self.float_text   = FloatTextSystem()
        self.cat_anim     = CatAnimator()
        self.shake        = ShakeEffect()

        # Font for floating text
        self._float_font = make_font(22, bold=True)

        # ── Callbacks ─────────────────────────────────────────
        self.customers.on_served = self._on_customer_served

        # ── UI buttons (generated from upgrades list) ─────────
        self.upgrade_buttons = self._make_upgrade_buttons()

    # ── Button factory ────────────────────────────────────────
    def _make_upgrade_buttons(self):
        buttons = []
        start_y = 222
        row_h   = 79
        for i, upg in enumerate(self.upgrades):
            btn = UpgradeButton(
                x=28, y=start_y + i * row_h,
                w=LEFT_PANEL_W - 56, h=68,
                upgrade=upg
            )
            buttons.append(btn)
        return buttons

    # ── Customer served callback ──────────────────────────────
    def _on_customer_served(self, x, y):
        self.yen += CUSTOMER_BONUS
        self.float_text.add(x, y, f"+¥{CUSTOMER_BONUS}",
                            color=GOLDEN, font=self._float_font)
        audio.play("coin")

    # ── Calculate total income / sec ─────────────────────────
    def _recalc_income(self):
        self.income_per_second = AUTO_INCOME_BASE + sum(
            upg.total_income for upg in self.upgrades)

    # ══════════════════════════════════════════════════════════
    #  EVENT HANDLING
    # ══════════════════════════════════════════════════════════
    def handle_event(self, event):
        # Upgrade button clicks
        for i, btn in enumerate(self.upgrade_buttons):
            if btn.handle_event(event):
                self._try_purchase(i)

        # Mouse-move updates hover state (handled in handle_event above)

    def _try_purchase(self, idx: int):
        upg = self.upgrades[idx]
        if self.yen >= upg.current_cost:
            self.yen -= upg.current_cost
            upg.purchase()
            self._recalc_income()
            self.shake.trigger(5)
            audio.play("upgrade")
            self.float_text.add(
                LEFT_PANEL_W // 2, HEIGHT - 220,
                f"✦ {upg.name} lv.{upg.level}!",
                color=RED_ACCENT, font=self._float_font
            )
        else:
            audio.play("error")

    # ══════════════════════════════════════════════════════════
    #  UPDATE
    # ══════════════════════════════════════════════════════════
    def update(self, dt: float):
        # Passive income tick
        self._income_acc += self.income_per_second * dt
        if self._income_acc >= 1.0:
            gained = int(self._income_acc)
            self.yen += gained
            self._income_acc -= gained

        # Update hover state for buttons
        for btn in self.upgrade_buttons:
            btn.can_buy = btn.upgrade.can_afford(self.yen)

        # Systems
        self.customers.update(dt)
        self.leaves.update(dt)
        self.float_text.update(dt)
        self.cat_anim.update(dt)
        self.shake.update(dt)

    # ══════════════════════════════════════════════════════════
    #  DRAW
    # ══════════════════════════════════════════════════════════
    def draw(self):
        ox, oy = self.shake.offset()
        if ox or oy:
            tmp = pygame.Surface((WIDTH, HEIGHT))
            self.renderer.draw_all(tmp, self)
            self.screen.blit(tmp, (ox, oy))
        else:
            self.renderer.draw_all(self.screen, self)
