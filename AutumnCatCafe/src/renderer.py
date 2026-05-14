"""
Procedural renderer for Autumn Cat Café.
Every visual element is drawn with pygame.draw / pygame.Surface –
no external image files required.
"""
import pygame, math, random
from settings import *
from src.utils import rounded_rect, dashed_rect, format_yen, make_font


# ── Helper: draw a circle segment (arc-fill) ─────────────────
def _filled_arc(surf, color, cx, cy, r, a_start, a_end, steps=32):
    pts = [(cx, cy)]
    for i in range(steps+1):
        a = math.radians(a_start + (a_end-a_start)*i/steps)
        pts.append((cx + math.cos(a)*r, cy + math.sin(a)*r))
    pygame.draw.polygon(surf, color, pts)


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self._init_fonts()
        self._build_static_surfaces()

    # ── Font init ─────────────────────────────────────────────
    def _init_fonts(self):
        self.f_title   = make_font(46, bold=True)
        self.f_sub     = make_font(20, bold=True)
        self.f_upg_hdr = make_font(28, bold=True)
        self.f_upg_name= make_font(22, bold=True)
        self.f_upg_lv  = make_font(13, bold=False)
        self.f_cost    = make_font(21, bold=True)
        self.f_yen     = make_font(54, bold=True)
        self.f_yen_lbl = make_font(18, bold=False)
        self.f_rate    = make_font(16, bold=False)
        self.f_cjk     = make_font(26, bold=True, cjk=True)
        self.f_cjk_sm  = make_font(18, bold=False, cjk=True)
        self.f_notif   = make_font(20, bold=True)
        self.f_float   = make_font(22, bold=True)

    # ── Pre-build the static café background card ─────────────
    def _build_static_surfaces(self):
        # We re-draw each frame (animated), so nothing truly static yet.
        pass

    # ══════════════════════════════════════════════════════════
    #  MAIN ENTRY
    # ══════════════════════════════════════════════════════════
    def draw_all(self, surface, game):
        t = game.cat_anim.t

        # 1) Base background
        surface.fill(LIGHT_CREAM)
        self._draw_bg_texture(surface)

        # 2) Left panel
        self._draw_left_panel(surface, game)

        # 3) Café card (right)
        self._draw_cafe_card(surface, t, game.cat_anim)

        # 4) Customers (in front of café, behind leaves)
        game.customers.draw(surface)

        # 5) Particle leaves (on top of everything)
        game.leaves.draw(surface)

        # 6) Floating text
        game.float_text.draw(surface)

        # 7) Currency bar bottom-left
        self._draw_currency_bar(surface, game)

    # ── Background texture ────────────────────────────────────
    def _draw_bg_texture(self, surface):
        # Subtle leaf silhouettes in background
        for i in range(0, WIDTH, 160):
            for j in range(0, HEIGHT, 140):
                alpha_s = pygame.Surface((50, 50), pygame.SRCALPHA)
                pygame.draw.ellipse(alpha_s, (230,215,190,35),
                                    (0, 8, 50, 30))
                surface.blit(alpha_s, (i + (j % 40), j))

    # ══════════════════════════════════════════════════════════
    #  LEFT PANEL
    # ══════════════════════════════════════════════════════════
    def _draw_left_panel(self, surface, game):
        pw = LEFT_PANEL_W

        # ── Title area ───────────────────────────────────────
        # "AUTUMN CAT CAFÉ" bold text
        t1 = self.f_title.render("AUTUMN", True, DARK_BROWN)
        t2 = self.f_title.render("CAT CAFÉ", True, DARK_BROWN)
        surface.blit(t1, (32, 24))
        surface.blit(t2, (32, 68))

        # Red Japanese sign box (top-right of title)
        sign_x, sign_y = 268, 18
        rounded_rect(surface, RED_ACCENT, (sign_x, sign_y, 80, 108), r=6)
        # White border
        pygame.draw.rect(surface, WHITE, (sign_x, sign_y, 80, 108), 3, border_radius=6)
        # Draw 秋のカフェ vertically
        kanji = ["秋", "の", "カ", "フ", "ェ"]
        for ki, ch in enumerate(kanji):
            ks = self.f_cjk_sm.render(ch, True, WHITE)
            surface.blit(ks, (sign_x + 40 - ks.get_width()//2,
                              sign_y + 8 + ki * 19))

        # Horizontal divider
        pygame.draw.line(surface, DASHED_COLOR, (20, 138), (pw-20, 138), 2)

        # ── Upgrade panel ─────────────────────────────────────
        panel_rect = (18, 148, pw-36, HEIGHT-220)
        rounded_rect(surface, PANEL_CREAM, panel_rect, r=14)
        dashed_rect(surface, DASHED_COLOR, panel_rect, dash=9, gap=6, w=2)

        hdr = self.f_upg_hdr.render("Upgrades", True, DARK_BROWN)
        surface.blit(hdr, (panel_rect[0]+18, panel_rect[1]+14))

        # Upgrade buttons
        for btn in game.upgrade_buttons:
            self._draw_upgrade_button(surface, btn, game.yen)

        # ── Income rate display ───────────────────────────────
        rate_txt = self.f_rate.render(
            f"Income: {format_yen(game.income_per_second)}/sec", True, WARM_BROWN)
        surface.blit(rate_txt, (32, HEIGHT-168))

    # ── Single upgrade button ─────────────────────────────────
    def _draw_upgrade_button(self, surface, btn, yen):
        x, y, w, h = btn.rect
        upgrade     = btn.upgrade
        can         = upgrade.can_afford(yen)
        hovered     = btn.hovered

        # Button container background
        bg = BUTTON_HOVER if (hovered and can) else OFF_WHITE
        if not can:
            bg = (220, 212, 200)
        rounded_rect(surface, bg, (x, y, w, h), r=10,
                     border=DASHED_COLOR, bw=1)

        # Level badge (top-left, tiny)
        if upgrade.level > 0:
            lv_txt = self.f_upg_lv.render(f"LEVEL {upgrade.level}", True, WARM_BROWN)
            surface.blit(lv_txt, (x+12, y+6))

        # Icon (left side)
        self._draw_upgrade_icon(surface, upgrade.icon_key,
                                x+14, y + h//2, can)

        # Name text
        name_col = DARK_BROWN if can else (150, 130, 110)
        name_surf = self.f_upg_name.render(upgrade.name, True, name_col)
        surface.blit(name_surf, (x+52, y + h//2 - name_surf.get_height()//2))

        # Cost pill (right side)
        cost_str = format_yen(upgrade.current_cost)
        pill_col = BUTTON_DARK if can else (120, 100, 85)
        if hovered and can:
            pill_col = (55, 30, 14)
        pw2 = max(90, self.f_cost.size(cost_str)[0] + 24)
        pill_x = x + w - pw2 - 8
        pill_y = y + (h - 36)//2
        rounded_rect(surface, pill_col, (pill_x, pill_y, pw2, 36), r=8)
        cs = self.f_cost.render(cost_str, True, GOLDEN if can else (180,160,130))
        surface.blit(cs, (pill_x + pw2//2 - cs.get_width()//2,
                          pill_y + 18 - cs.get_height()//2))

    # ── Upgrade icons (drawn procedurally) ───────────────────
    def _draw_upgrade_icon(self, surface, key, cx, cy, active):
        col_main  = GOLDEN if active else (160, 140, 110)
        col_dark  = WARM_BROWN if active else (130, 110, 85)
        col_red   = RED_ACCENT if active else (140, 110, 100)

        if key == "lantern":
            # Mini chochin lantern
            pygame.draw.ellipse(surface, col_red, (cx-9, cy-13, 18, 26))
            pygame.draw.line(surface, col_dark, (cx, cy-13), (cx, cy-18), 2)
            pygame.draw.line(surface, col_dark, (cx, cy+13), (cx, cy+18), 2)
            for dy in [-4, 0, 4]:
                pygame.draw.line(surface, col_dark, (cx-9, cy+dy),
                                 (cx+9, cy+dy), 1)

        elif key == "coffee":
            # Espresso machine
            rounded_rect(surface, col_dark, (cx-11, cy-14, 22, 22), r=3)
            rounded_rect(surface, col_main, (cx-8, cy-11, 16, 10), r=2)
            pygame.draw.rect(surface, col_dark, (cx-5, cy+8, 10, 6))
            # Steam
            for sx in [-3, 3]:
                for sy_off in range(3):
                    pygame.draw.circle(surface, (220,210,200),
                                       (cx+sx, cy-16-sy_off*4), 2)

        elif key == "seat":
            # Stool icon
            pygame.draw.circle(surface, col_main, (cx, cy-8), 9)
            pygame.draw.line(surface, col_dark, (cx, cy+1), (cx, cy+16), 3)
            pygame.draw.line(surface, col_dark, (cx-8, cy+16),
                             (cx+8, cy+16), 3)

        elif key == "beans":
            # Coffee bean
            pygame.draw.ellipse(surface, col_dark, (cx-9, cy-6, 18, 12))
            pygame.draw.arc(surface, col_main,
                            (cx-7, cy-5, 14, 10), 0, math.pi, 2)

        elif key == "cat":
            # Mini lucky cat
            pygame.draw.circle(surface, col_main, (cx, cy-4), 10)
            # Ears
            pygame.draw.polygon(surface, col_main,
                                [(cx-10, cy-12), (cx-5, cy-18), (cx-2, cy-12)])
            pygame.draw.polygon(surface, col_main,
                                [(cx+10, cy-12), (cx+5, cy-18), (cx+2, cy-12)])
            # Eyes
            pygame.draw.circle(surface, col_dark, (cx-4, cy-5), 2)
            pygame.draw.circle(surface, col_dark, (cx+4, cy-5), 2)
            # Paw raised
            pygame.draw.circle(surface, col_main, (cx+12, cy-8), 6)

    # ══════════════════════════════════════════════════════════
    #  RIGHT CAFÉ CARD
    # ══════════════════════════════════════════════════════════
    def _draw_cafe_card(self, surface, t, cat_anim):
        cx = RIGHT_PANEL_X
        cy = RIGHT_PANEL_Y
        cw = RIGHT_PANEL_W
        ch = RIGHT_PANEL_H

        # Card shadow
        shad = pygame.Surface((cw+10, ch+10), pygame.SRCALPHA)
        pygame.draw.rect(shad, (0,0,0,55), (6, 6, cw, ch), border_radius=22)
        surface.blit(shad, (cx-3, cy-3))

        # Card border (cream)
        rounded_rect(surface, CREAM, (cx-6, cy-6, cw+12, ch+12), r=22)
        # Card background (dark maroon)
        rounded_rect(surface, BG_MAROON, (cx, cy, cw, ch), r=18)

        # ── Cloudy top decoration ─────────────────────────────
        self._draw_cloud_top(surface, cx, cy, cw)

        # ── Awning / tarp ─────────────────────────────────────
        self._draw_awning(surface, cx + cw//2, cy + 48, 380, 70)

        # ── Back wall of café building ────────────────────────
        bld_x = cx + cw//2 - 190
        bld_y = cy + 130
        bld_w = 380
        bld_h = 340
        rounded_rect(surface, DARK_BROWN, (bld_x, bld_y, bld_w, bld_h), r=6)

        # ── Inner window / opening ────────────────────────────
        win_x = bld_x + 20
        win_y = bld_y + 10
        win_w = bld_w - 40
        win_h = bld_h - 80
        rounded_rect(surface, BG_DARK_MAROON, (win_x, win_y, win_w, win_h), r=4)

        # ── カフェ banner signs ───────────────────────────────
        self._draw_banner_signs(surface, cx + cw//2, bld_y + 20)

        # ── Right vertical banner ─────────────────────────────
        self._draw_vertical_banner(surface, bld_x + bld_w + 10, bld_y + 30)

        # ── Left lantern ─────────────────────────────────────
        self._draw_lantern(surface, bld_x - 30, bld_y + 80, t)

        # ── Counter / bar ─────────────────────────────────────
        bar_x  = bld_x + 18
        bar_y  = bld_y + bld_h - 140
        bar_w  = bld_w - 36
        bar_h  = 30
        rounded_rect(surface, GOLDEN, (bar_x, bar_y, bar_w, bar_h), r=5)
        rounded_rect(surface, GOLDEN_DARK, (bar_x, bar_y, bar_w, 6), r=5)

        # ── Shelf behind counter ──────────────────────────────
        shelf_y = bar_y - 60
        pygame.draw.rect(surface, WARM_BROWN,
                         (bar_x + 10, shelf_y, bar_w - 20, 10))
        # Cups on shelf
        for ci in range(4):
            sx = bar_x + 30 + ci * 50
            self._draw_cup(surface, sx, shelf_y - 16, small=True)

        # ── Stools ────────────────────────────────────────────
        for i in range(3):
            sx = bld_x + 60 + i * 110
            self._draw_stool(surface, sx, bld_y + bld_h - 60)

        # ── Coffee cup on counter ─────────────────────────────
        self._draw_cup(surface, bar_x + 30, bar_y - 20)
        self._draw_steam(surface, bar_x + 30, bar_y - 35, t)
        self._draw_cup(surface, bar_x + bar_w - 55, bar_y - 20)
        self._draw_steam(surface, bar_x + bar_w - 55, bar_y - 35, t + 1.0)

        # ── Animated cat ─────────────────────────────────────
        cat_cx = cx + cw//2 + 10
        cat_cy = int(bar_y - 8 + cat_anim.bob)
        self._draw_cat(surface, cat_cx, cat_cy, cat_anim)

        # ── Scattered interior leaves ─────────────────────────
        self._draw_interior_leaves(surface, cx, cy, cw, ch, t)

        # ── Card border overlay (top scallop awning) ──────────
        self._draw_top_awning_scallop(surface, cx, cy, cw)

    # ── Cloud top decoration ──────────────────────────────────
    def _draw_cloud_top(self, surface, cx, cy, cw):
        cloud_col = (92, 42, 22)
        radii = [55, 48, 60, 52, 45, 58, 50, 46]
        xs    = [cx+40, cx+110, cx+185, cx+265, cx+345, cx+435, cx+540, cx+620]
        for x, r in zip(xs, radii):
            pygame.draw.circle(surface, cloud_col, (x, cy+r-10), r)

    # ── Top awning scallop (golden) ───────────────────────────
    def _draw_top_awning_scallop(self, surface, cx, cy, cw):
        scallop_col  = GOLDEN
        scallop_col2 = GOLDEN_DARK
        y0 = cy + 20
        r  = 44
        for i in range(9):
            sx = cx + 18 + i * (cw - 36) // 8
            pygame.draw.circle(surface, scallop_col, (sx, y0), r)
            # Darker strip along bottom of each scallop
            pygame.draw.arc(surface, scallop_col2,
                            (sx-r, y0, r*2, r*2), math.pi, 2*math.pi, 6)

    # ── Striped awning over building ──────────────────────────
    def _draw_awning(self, surface, mx, top_y, w, h):
        # Base golden rect
        pygame.draw.rect(surface, GOLDEN, (mx-w//2, top_y, w, h))
        # Diagonal stripes
        stripe_w = 28
        for i in range(-2, w // stripe_w + 3):
            x0 = mx - w//2 + i * stripe_w
            pts = [(x0, top_y), (x0+stripe_w//2, top_y),
                   (x0+stripe_w//2 + h, top_y+h), (x0+h, top_y+h)]
            pygame.draw.polygon(surface, GOLDEN_DARK, pts)
        # Bottom fringe
        fringe_h = 14
        for fi in range(w // 16 + 1):
            fx = mx - w//2 + fi * 16
            pygame.draw.ellipse(surface, GOLDEN,
                                (fx, top_y+h-4, 16, fringe_h))

    # ── Banner signs カフェ ────────────────────────────────────
    def _draw_banner_signs(self, surface, center_x, top_y):
        chars  = ["カ", "フ", "ェ"]
        sq     = 58
        gap    = 8
        total  = len(chars) * sq + (len(chars)-1) * gap
        sx     = center_x - total//2
        for i, ch in enumerate(chars):
            bx = sx + i * (sq + gap)
            rounded_rect(surface, RED_ACCENT, (bx, top_y, sq, sq), r=5)
            pygame.draw.rect(surface, DARK_RED, (bx, top_y, sq, sq), 2, border_radius=5)
            ts = self.f_cjk.render(ch, True, WHITE)
            surface.blit(ts, (bx + sq//2 - ts.get_width()//2,
                               top_y + sq//2 - ts.get_height()//2))

    # ── Vertical banner ───────────────────────────────────────
    def _draw_vertical_banner(self, surface, x, y):
        bw, bh = 44, 180
        rounded_rect(surface, RED_ACCENT, (x, y, bw, bh), r=6)
        pygame.draw.rect(surface, DARK_RED, (x, y, bw, bh), 2, border_radius=6)
        # Small cup icon at top
        pygame.draw.ellipse(surface, WHITE, (x+10, y+8, 24, 16))
        # 秋のカフェ vertically
        chars = ["秋", "の", "カ", "フ", "ェ"]
        for ki, ch in enumerate(chars):
            ts = self.f_cjk_sm.render(ch, True, WHITE)
            surface.blit(ts, (x + bw//2 - ts.get_width()//2,
                               y + 32 + ki * 27))
        # Hanging cords
        pygame.draw.line(surface, DARK_BROWN, (x, y), (x-8, y-20), 2)
        pygame.draw.line(surface, DARK_BROWN, (x+bw, y), (x+bw+8, y-20), 2)

    # ── Japanese lantern ──────────────────────────────────────
    def _draw_lantern(self, surface, x, y, t):
        # Glow
        glow = pygame.Surface((90, 90), pygame.SRCALPHA)
        glow_r = int(38 + math.sin(t*1.8)*4)
        pygame.draw.circle(glow, (255,160,60,45), (45,45), glow_r)
        surface.blit(glow, (x-45, y-45))

        # Hanging cord
        pygame.draw.line(surface, DARK_BROWN, (x, y-40), (x, y-22), 2)

        # Lantern body
        body_col = RED_ACCENT
        pygame.draw.ellipse(surface, body_col, (x-18, y-22, 36, 44))
        # Ribs
        for ri in range(5):
            ry = y - 22 + ri * 10
            rw = int(36 * math.sin(math.pi * ri / 4)) if ri > 0 and ri < 4 else 2
            pygame.draw.ellipse(surface, DARK_RED,
                                (x - rw//2 - 1, ry, max(2, rw+2), 4))
        # Top and bottom caps
        pygame.draw.rect(surface, GOLDEN_DARK, (x-8, y-25, 16, 6))
        pygame.draw.rect(surface, GOLDEN_DARK, (x-8, y+19, 16, 6))
        # Inner glow colour
        inner = pygame.Surface((26, 34), pygame.SRCALPHA)
        inner.fill((255,160,60, int(80 + math.sin(t*2)*25)))
        surface.blit(inner, (x-13, y-17))

        # Tassel
        for ti in range(5):
            tx = x - 8 + ti*4
            pygame.draw.line(surface, GOLDEN, (tx, y+25), (tx, y+38), 1)

    # ── Counter stool ─────────────────────────────────────────
    def _draw_stool(self, surface, x, y):
        # Seat
        pygame.draw.ellipse(surface, WARM_BROWN, (x-20, y-10, 40, 18))
        pygame.draw.ellipse(surface, GOLDEN_DARK, (x-20, y-10, 40, 8))
        # Leg
        pygame.draw.rect(surface, DARK_BROWN, (x-3, y+8, 6, 30))
        # Foot bar
        pygame.draw.ellipse(surface, DARK_BROWN, (x-16, y+34, 32, 8))

    # ── Coffee cup ────────────────────────────────────────────
    def _draw_cup(self, surface, x, y, small=False):
        s = 0.55 if small else 1.0
        w, h = int(22*s), int(18*s)
        # Saucer
        pygame.draw.ellipse(surface, GOLDEN_DARK, (x-int(14*s), y+h-2, int(28*s), int(8*s)))
        # Cup body
        pygame.draw.rect(surface, OFF_WHITE, (x-w//2, y, w, h), border_radius=3)
        # Handle
        pygame.draw.arc(surface, GOLDEN_DARK,
                        (x+w//2-4, y+2, int(10*s), int(10*s)),
                        math.radians(270), math.radians(90), 2)
        # Coffee inside
        pygame.draw.ellipse(surface, WARM_BROWN,
                            (x-w//2+2, y+2, w-4, int(8*s)))

    # ── Steam wisps ───────────────────────────────────────────
    def _draw_steam(self, surface, x, y, t):
        for si in range(3):
            phase = t * 2 + si * 0.9
            sx = x + math.sin(phase) * 5 + (si-1)*6
            sy = y - si * 9
            alpha = max(0, int(130 - si*40 - math.sin(phase)*20))
            steam_s = pygame.Surface((8,8), pygame.SRCALPHA)
            pygame.draw.circle(steam_s, (220, 215, 210, alpha), (4,4), 4)
            surface.blit(steam_s, (int(sx)-4, int(sy)-4))

    # ── The Black Cat ─────────────────────────────────────────
    def _draw_cat(self, surface, cx, cy, anim):
        bob = int(anim.bob)
        tail = anim.tail_rad
        blinking = anim.blinking

        # Body (black oval)
        body_w, body_h = 78, 58
        pygame.draw.ellipse(surface, (22, 14, 8),
                            (cx - body_w//2, cy - body_h//2, body_w, body_h))

        # Head
        head_r = 30
        hx, hy = cx, cy - body_h//2 - head_r + 8
        pygame.draw.circle(surface, (22, 14, 8), (hx, hy), head_r)

        # Ears
        ear_pts_l = [(hx-24, hy-8), (hx-12, hy-32), (hx-4, hy-12)]
        ear_pts_r = [(hx+24, hy-8), (hx+12, hy-32), (hx+4, hy-12)]
        pygame.draw.polygon(surface, (22, 14, 8), ear_pts_l)
        pygame.draw.polygon(surface, (22, 14, 8), ear_pts_r)
        # Inner ear pink
        inner_l = [(hx-20, hy-10), (hx-13, hy-26), (hx-7, hy-13)]
        inner_r = [(hx+20, hy-10), (hx+13, hy-26), (hx+7, hy-13)]
        pygame.draw.polygon(surface, (160, 90, 90), inner_l)
        pygame.draw.polygon(surface, (160, 90, 90), inner_r)

        # Eyes  – blink closes them
        eye_y = hy - 4
        if blinking:
            # Closed line
            pygame.draw.line(surface, (220, 210, 200),
                             (hx-14, eye_y), (hx-4, eye_y), 3)
            pygame.draw.line(surface, (220, 210, 200),
                             (hx+4, eye_y), (hx+14, eye_y), 3)
        else:
            # White sclera
            pygame.draw.circle(surface, (235, 230, 218), (hx-10, eye_y), 9)
            pygame.draw.circle(surface, (235, 230, 218), (hx+10, eye_y), 9)
            # Pupils
            pygame.draw.circle(surface, (22, 14, 8), (hx-10, eye_y), 6)
            pygame.draw.circle(surface, (22, 14, 8), (hx+10, eye_y), 6)
            # Shine dots
            pygame.draw.circle(surface, WHITE, (hx-8, eye_y-3), 2)
            pygame.draw.circle(surface, WHITE, (hx+12, eye_y-3), 2)

        # ">O.O<" text face style (mouth/whiskers)
        # Nose
        pygame.draw.polygon(surface, (200, 130, 130),
                            [(hx, hy+5), (hx-3, hy+2), (hx+3, hy+2)])
        # Whiskers
        for side in [-1, 1]:
            for wi in range(3):
                wx1 = hx + side * 4
                wy  = hy + 4 + wi * 4
                wx2 = hx + side * 26
                wy2 = hy + 2 + wi * 4
                pygame.draw.line(surface, (180,170,160), (wx1, wy), (wx2, wy2), 1)

        # Mouth
        pygame.draw.arc(surface, (180,160,150),
                        (hx-8, hy+5, 16, 8), math.pi, 2*math.pi, 2)

        # Tail (animated)
        tail_base_x = cx + body_w//2 - 8
        tail_base_y = cy + body_h//2 - 6
        tail_len = 55
        tc_x = tail_base_x + math.cos(tail) * tail_len
        tc_y = tail_base_y + math.sin(tail) * tail_len * 0.7 - 10
        # Draw arc tail as thick line
        points = []
        for ti in range(12):
            frac = ti / 11.0
            angle = tail * frac
            lx = tail_base_x + math.cos(angle) * tail_len * frac
            ly = tail_base_y + math.sin(angle) * tail_len * frac * 0.7 - 10 * frac
            points.append((int(lx), int(ly)))
        if len(points) > 1:
            pygame.draw.lines(surface, (22, 14, 8), False, points, 8)
        # Tail tip (lighter)
        if points:
            pygame.draw.circle(surface, (55, 40, 30), points[-1], 7)

        # Barista apron hint
        apron_pts = [(cx-22, cy-5), (cx+22, cy-5),
                     (cx+18, cy+body_h//2+2), (cx-18, cy+body_h//2+2)]
        apron_s = pygame.Surface((60, 40), pygame.SRCALPHA)
        pygame.draw.polygon(apron_s, (220, 180, 140, 90),
                            [(20, 0),(40,0),(36,38),(14,38)])
        surface.blit(apron_s, (cx-30, cy-8))

        # Small bow-tie / ribbon
        bow_y = cy - body_h//2 + 6
        pygame.draw.polygon(surface, RED_ACCENT,
                            [(cx-10, bow_y), (cx, bow_y+6), (cx-10, bow_y+12)])
        pygame.draw.polygon(surface, RED_ACCENT,
                            [(cx+10, bow_y), (cx, bow_y+6), (cx+10, bow_y+12)])
        pygame.draw.circle(surface, GOLDEN, (cx, bow_y+6), 4)

    # ── Scattered interior leaves ─────────────────────────────
    def _draw_interior_leaves(self, surface, cx, cy, cw, ch, t):
        random.seed(42)          # deterministic positions
        for i in range(10):
            lx = cx + random.randint(60, cw-60)
            ly = cy + random.randint(100, ch-60)
            angle = random.uniform(0, 360) + t * random.uniform(5, 15)
            lc = random.choice(LEAF_COLORS)
            ls = random.randint(12, 22)
            leaf_s = pygame.Surface((ls*2+4, ls*2+4), pygame.SRCALPHA)
            pygame.draw.ellipse(leaf_s, (*lc, 90),
                                (0, ls//2, ls*2, ls*2//3 + ls//2))
            rot = pygame.transform.rotate(leaf_s, angle)
            r = rot.get_rect(center=(int(lx), int(ly)))
            surface.blit(rot, r)
        random.seed()            # restore randomness

    # ══════════════════════════════════════════════════════════
    #  CURRENCY BAR (bottom-left)
    # ══════════════════════════════════════════════════════════
    def _draw_currency_bar(self, surface, game):
        bar_h = 78
        bar_y = HEIGHT - bar_h
        bar_w = LEFT_PANEL_W

        # Dark background
        rounded_rect(surface, DARK_PANEL,
                     (12, bar_y + 10, bar_w - 24, bar_h - 14), r=12)

        # Yen text
        yen_str = format_yen(game.yen)
        ys = self.f_yen.render(yen_str, True, GOLDEN)
        surface.blit(ys, (30, bar_y + 14))

        # Small "/sec" label
        rts = self.f_yen_lbl.render(
            f"+{format_yen(game.income_per_second)}/sec", True, (160,140,100))
        surface.blit(rts, (bar_w - rts.get_width() - 24, bar_y + 42))
