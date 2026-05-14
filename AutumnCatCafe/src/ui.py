"""UI component classes – buttons with hover/click states."""
import pygame
from settings import *


class Button:
    def __init__(self, x, y, w, h, label, font=None):
        self.rect    = (x, y, w, h)
        self.label   = label
        self.font    = font
        self.hovered = False
        self._pressed= False

    def handle_event(self, event):
        mx, my = pygame.mouse.get_pos()
        x, y, w, h = self.rect
        self.hovered = (x <= mx <= x+w and y <= my <= y+h)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered:
                self._pressed = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self._pressed and self.hovered:
                self._pressed = False
                return True          # clicked
            self._pressed = False
        return False


class UpgradeButton(Button):
    """Upgrade button that also carries the Upgrade object."""
    def __init__(self, x, y, w, h, upgrade):
        super().__init__(x, y, w, h, upgrade.name)
        self.upgrade = upgrade
        self.can_buy = False

    def handle_event(self, event):
        return super().handle_event(event)
