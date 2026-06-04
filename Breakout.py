import sys
import math
import random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QFrame, QComboBox, QSizePolicy, QGridLayout
)
from PyQt6.QtCore import Qt, QTimer, QRectF, QPointF, QSizeF, pyqtSignal
from PyQt6.QtGui import (
    QPainter, QColor, QFont, QPen, QBrush, QLinearGradient,
    QRadialGradient, QPainterPath, QFontMetrics
)

# ─────────────────────────────────────────────────────────────────────────────
# TRANSLATIONS
# ─────────────────────────────────────────────────────────────────────────────
TR = {
    "en": {
        "title": "Breakout",
        "score": "Score", "best": "Best", "level": "Level",
        "lives": "Lives", "start": "▶  Start", "restart": "↺  Restart",
        "pause": "⏸  Pause", "resume": "▶  Resume",
        "theme": "Theme", "language": "Language",
        "dark": "Dark", "light": "Light",
        "controls": "Mouse or ←→ keys\nto move paddle.\nDon't let ball drop!",
        "game_over": "GAME OVER", "win": "YOU WIN!",
        "tap_start": "Click START to play",
        "level_up": "LEVEL UP!", "new_best": "NEW BEST!",
        "combo": "COMBO x", "ready": "READY",
        "bricks": "Bricks",
    },
    "zh": {
        "title": "打砖块",
        "score": "分数", "best": "最高分", "level": "关卡",
        "lives": "生命", "start": "▶  开始", "restart": "↺  重来",
        "pause": "⏸  暂停", "resume": "▶  继续",
        "theme": "主题", "language": "语言",
        "dark": "深色", "light": "浅色",
        "controls": "鼠标或←→键\n移动挡板。\n不要让球掉落！",
        "game_over": "游戏结束", "win": "你赢了！",
        "tap_start": "点击开始按钮",
        "level_up": "升级！", "new_best": "新纪录！",
        "combo": "连击 x", "ready": "准备",
        "bricks": "砖块",
    },
    "fa": {
        "title": "برک‌اوت",
        "score": "امتیاز", "best": "بهترین", "level": "سطح",
        "lives": "جان", "start": "▶  شروع", "restart": "↺  مجدد",
        "pause": "⏸  مکث", "resume": "▶  ادامه",
        "theme": "تم", "language": "زبان",
        "dark": "تاریک", "light": "روشن",
        "controls": "موس یا کلیدهای ←→\nبرای حرکت راکت.\nتوپ را نگه دارید!",
        "game_over": "بازی تمام شد", "win": "بردی!",
        "tap_start": "برای شروع کلیک کنید",
        "level_up": "ارتقا سطح!", "new_best": "رکورد جدید!",
        "combo": "زنجیره x", "ready": "آماده",
        "bricks": "آجر",
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# THEMES
# ─────────────────────────────────────────────────────────────────────────────
THEMES = {
    "dark": {
        "win_bg1": "#0d0d1a", "win_bg2": "#1a1a35",
        "panel_bg": "#12122a", "panel_border": "#2a2a5a",
        "field_bg1": "#080818", "field_bg2": "#111130",
        "field_border": "#2a2a6a",
        "text": "#e0e0ff", "text2": "#7788bb", "text_dim": "#445588",
        "accent": "#e94560", "accent2": "#00d4ff",
        "btn_bg": "#e94560", "btn_h": "#ff6b6b",
        "btn2_bg": "#533483", "btn2_h": "#7b52ab",
        "btn3_bg": "#0f3460", "btn3_h": "#1e5f9e",
        "btn_txt": "#ffffff",
        "cmb_bg": "#0f1535", "cmb_border": "#2a3a7a",
        "paddle_c1": "#00d4ff", "paddle_c2": "#0088cc",
        "paddle_rim": "#88eeff",
        "ball_c1": "#ffffff", "ball_c2": "#aaccff",
        "ball_glow": "#00d4ff",
        "particle_clrs": ["#ff4757", "#ffa502", "#2ed573",
                          "#1e90ff", "#a855f7", "#ff6b9d"],
        "sep": "#2a2a5a",
        "stat_val": "#00d4ff", "score_clr": "#ffd700",
        "hp_clr": "#ff4757",
    },
    "light": {
        "win_bg1": "#e8eeff", "win_bg2": "#d0d8ff",
        "panel_bg": "#f4f6ff", "panel_border": "#c0cce8",
        "field_bg1": "#dde4ff", "field_bg2": "#c8d4ff",
        "field_border": "#9aaad8",
        "text": "#1a1a3e", "text2": "#445588", "text_dim": "#9aaad8",
        "accent": "#e94560", "accent2": "#1e90ff",
        "btn_bg": "#e94560", "btn_h": "#ff6b6b",
        "btn2_bg": "#7c4dff", "btn2_h": "#9c6dff",
        "btn3_bg": "#3d5afe", "btn3_h": "#5d7aff",
        "btn_txt": "#ffffff",
        "cmb_bg": "#dde4ff", "cmb_border": "#9aaad8",
        "paddle_c1": "#1e90ff", "paddle_c2": "#1464b4",
        "paddle_rim": "#74b9ff",
        "ball_c1": "#ffffff", "ball_c2": "#ddeeff",
        "ball_glow": "#1e90ff",
        "particle_clrs": ["#e94560", "#ff8800", "#00b050",
                          "#1e90ff", "#9c27b0", "#e91e8c"],
        "sep": "#c0cce8",
        "stat_val": "#1e90ff", "score_clr": "#ff6600",
        "hp_clr": "#e94560",
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# BRICK PALETTE  (row_index → color scheme)
# ─────────────────────────────────────────────────────────────────────────────
BRICK_PALETTES = [
    {"bg": "#ff4757", "rim": "#ff6b81", "shadow": "#c0392b", "pts": 70},
    {"bg": "#ff6348", "rim": "#ff8a75", "shadow": "#c0462a", "pts": 60},
    {"bg": "#ffa502", "rim": "#ffd32a", "shadow": "#e67e00", "pts": 50},
    {"bg": "#eccc68", "rim": "#f9de8a", "shadow": "#b5982f", "pts": 40},
    {"bg": "#2ed573", "rim": "#7bed9f", "shadow": "#1e8449", "pts": 30},
    {"bg": "#1e90ff", "rim": "#74b9ff", "shadow": "#1464b4", "pts": 25},
    {"bg": "#a855f7", "rim": "#c084fc", "shadow": "#7e22ce", "pts": 20},
    {"bg": "#ff6b9d", "rim": "#ffa8c8", "shadow": "#c2185b", "pts": 15},
]

BRICK_ROWS    = 6
BRICK_COLS    = 12
BRICK_GAP     = 3
BRICK_TOP_PAD = 0.08   # fraction of field height
BALL_SPEED_BASE = 380  # px/s at level 1
PADDLE_SPEED    = 600
MAX_LIVES       = 3


# ─────────────────────────────────────────────────────────────────────────────
# PARTICLE
# ─────────────────────────────────────────────────────────────────────────────
class Particle:
    def __init__(self, x, y, color, speed_scale=1.0):
        self.x, self.y = x, y
        self.color = QColor(color)
        a = random.uniform(0, 2 * math.pi)
        s = random.uniform(80, 220) * speed_scale
        self.vx = math.cos(a) * s
        self.vy = math.sin(a) * s
        self.life = random.uniform(0.5, 1.0)
        self.max_life = self.life
        self.r = random.uniform(3, 8)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 220 * dt
        self.life -= dt * 1.8
        return self.life > 0

    def draw(self, p: QPainter):
        a = max(0.0, self.life / self.max_life)
        r = self.r * a
        c = QColor(self.color); c.setAlphaF(a)
        grad = QRadialGradient(self.x, self.y, r)
        grad.setColorAt(0, QColor(255, 255, 255, int(200 * a)))
        grad.setColorAt(0.4, c)
        c2 = QColor(self.color); c2.setAlphaF(0)
        grad.setColorAt(1, c2)
        p.setBrush(QBrush(grad))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(QPointF(self.x, self.y), r, r)


# ─────────────────────────────────────────────────────────────────────────────
# BRICK
# ─────────────────────────────────────────────────────────────────────────────
class Brick:
    def __init__(self, row, col, hp, palette):
        self.row, self.col = row, col
        self.hp = hp
        self.max_hp = hp
        self.palette = palette
        self.alive = True
        self.hit_flash = 0.0
        self.rect = QRectF()

    def hit(self):
        self.hp -= 1
        self.hit_flash = 0.25
        if self.hp <= 0:
            self.alive = False

    def update(self, dt):
        self.hit_flash = max(0.0, self.hit_flash - dt * 4)

    def draw(self, p: QPainter, theme_key: str):
        if not self.alive:
            return
        pal = self.palette
        r = self.rect
        hp_ratio = self.hp / self.max_hp

        # Shadow
        sh = QColor(pal["shadow"]); sh.setAlpha(80)
        p.setBrush(QBrush(sh)); p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(r.adjusted(3, 3, 3, 3), 5, 5)

        # Body gradient
        g = QLinearGradient(r.left(), r.top(), r.left(), r.bottom())
        top_c = QColor(pal["rim"])
        bot_c = QColor(pal["bg"])
        if self.hit_flash > 0:
            f = self.hit_flash / 0.25
            top_c = _blend(QColor("#ffffff"), top_c, f)
            bot_c  = _blend(QColor("#ffffff"), bot_c,  f)
        g.setColorAt(0, top_c)
        g.setColorAt(1, bot_c)
        p.setBrush(QBrush(g))
        pen = QPen(QColor(pal["shadow"]), 1)
        p.setPen(pen)
        p.drawRoundedRect(r, 5, 5)

        # HP bar for multi-hit bricks
        if self.max_hp > 1:
            bh = max(3, r.height() * 0.12)
            bw = (r.width() - 6) * hp_ratio
            bar_r = QRectF(r.left() + 3, r.bottom() - bh - 2, bw, bh)
            hp_c = QColor("#ff4757") if hp_ratio < 0.5 else QColor("#2ed573")
            p.setBrush(QBrush(hp_c)); p.setPen(Qt.PenStyle.NoPen)
            p.drawRoundedRect(bar_r, 2, 2)

        # Shine
        shine_r = QRectF(r.left() + 4, r.top() + 3,
                         r.width() * 0.55, r.height() * 0.35)
        shine_g = QLinearGradient(shine_r.topLeft(), shine_r.bottomLeft())
        shine_g.setColorAt(0, QColor(255, 255, 255, 100))
        shine_g.setColorAt(1, QColor(255, 255, 255, 0))
        p.setBrush(QBrush(shine_g)); p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(shine_r, 3, 3)


def _blend(c1: QColor, c2: QColor, t: float) -> QColor:
    t = max(0.0, min(1.0, t))
    return QColor(
        int(c1.red()   * t + c2.red()   * (1 - t)),
        int(c1.green() * t + c2.green() * (1 - t)),
        int(c1.blue()  * t + c2.blue()  * (1 - t)),
    )


# ─────────────────────────────────────────────────────────────────────────────
# GAME FIELD WIDGET
# ─────────────────────────────────────────────────────────────────────────────
class FieldWidget(QWidget):
    sig_score   = pyqtSignal(int)
    sig_best    = pyqtSignal(int)
    sig_level   = pyqtSignal(int)
    sig_lives   = pyqtSignal(int)
    sig_bricks  = pyqtSignal(int)
    sig_state   = pyqtSignal(str)

    def __init__(self, theme, lang, parent=None):
        super().__init__(parent)
        self.theme_key = theme
        self.t  = THEMES[theme]
        self.lang = lang
        self.setMinimumSize(280, 320)
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # game state
        self.state   = "idle"
        self.score   = 0
        self.best    = 0
        self.level   = 1
        self.lives   = MAX_LIVES
        self.bricks  : list[Brick] = []
        self.particles: list[Particle] = []
        self.combo   = 0
        self.flash_text = ""
        self.flash_t    = 0.0

        # paddle
        self.pad_x   = 0.0   # center x
        self.pad_y   = 0.0
        self.pad_w   = 0.0
        self.pad_h   = 0.0
        self.pad_target_x = 0.0
        self.key_left = False
        self.key_right= False

        # ball
        self.ball_x  = 0.0
        self.ball_y  = 0.0
        self.ball_r  = 0.0
        self.ball_vx = 0.0
        self.ball_vy = 0.0
        self.ball_on_pad = True
        self.trail: list[tuple[float, float, float]] = []  # x,y,alpha

        import time
        self._last_ts = time.perf_counter()
        self.timer = QTimer(self)
        self.timer.setInterval(14)
        self.timer.timeout.connect(self._tick)

    # ── public ────────────────────────────────────────────────────────────
    def set_theme(self, tk):
        self.theme_key = tk
        self.t = THEMES[tk]
        self.update()

    def set_lang(self, lang):
        self.lang = lang
        self.update()

    def start(self):
        self.score  = 0
        self.level  = 1
        self.lives  = MAX_LIVES
        self.combo  = 0
        self.particles.clear()
        self._init_geometry()
        self._build_level()
        self.state = "ready"
        self.timer.start()
        self._emit_all()
        self.sig_state.emit(self.state)
        self.update()

    def restart(self):
        self.start()

    def pause_toggle(self):
        if self.state == "playing":
            self.state = "paused"
            self.timer.stop()
        elif self.state == "paused":
            self.state = "playing"
            import time; self._last_ts = time.perf_counter()
            self.timer.start()
        self.sig_state.emit(self.state)
        self.update()

    # ── setup ─────────────────────────────────────────────────────────────
    def _init_geometry(self):
        W, H = self.width(), self.height()
        self.ball_r = max(7, min(W, H) * 0.022)
        self.pad_h  = max(10, H * 0.025)
        self.pad_w  = max(60, W * 0.18)
        self.pad_y  = H * 0.91
        self.pad_x  = W / 2
        self.pad_target_x = W / 2
        self._reset_ball()

    def _reset_ball(self):
        self.ball_x = self.pad_x
        self.ball_y = self.pad_y - self.pad_h / 2 - self.ball_r - 1
        speed = BALL_SPEED_BASE + (self.level - 1) * 30
        angle = math.radians(random.uniform(-30, 30) - 90)
        self.ball_vx = speed * math.cos(angle)
        self.ball_vy = speed * math.sin(angle)
        self.ball_on_pad = True
        self.trail.clear()

    def _build_level(self):
        self.bricks.clear()
        W, H = self.width(), self.height()
        field_x0 = W * 0.02
        field_x1 = W * 0.98
        field_y0 = H * BRICK_TOP_PAD
        field_h  = H * 0.48

        bw = (field_x1 - field_x0 - BRICK_GAP * (BRICK_COLS + 1)) / BRICK_COLS
        bh = min(max(14, (field_h - BRICK_GAP * (BRICK_ROWS + 1)) / BRICK_ROWS), 36)

        for row in range(BRICK_ROWS):
            pal = BRICK_PALETTES[row % len(BRICK_PALETTES)]
            hp = 1 if self.level < 3 else (2 if row < 2 else 1)
            for col in range(BRICK_COLS):
                b = Brick(row, col, hp, pal)
                bx = field_x0 + BRICK_GAP + col * (bw + BRICK_GAP)
                by = field_y0 + BRICK_GAP + row * (bh + BRICK_GAP)
                b.rect = QRectF(bx, by, bw, bh)
                self.bricks.append(b)
        self.sig_bricks.emit(self._alive_count())

    # ── main loop ─────────────────────────────────────────────────────────
    def _tick(self):
        import time
        now = time.perf_counter()
        dt  = min(now - self._last_ts, 0.05)
        self._last_ts = now

        self.flash_t = max(0.0, self.flash_t - dt)
        self.particles = [p for p in self.particles if p.update(dt)]

        for b in self.bricks:
            b.update(dt)

        if self.state == "playing":
            self._update_paddle(dt)
            self._update_ball(dt)

        self.update()

    def _update_paddle(self, dt):
        W = self.width()
        spd = PADDLE_SPEED
        if self.key_left:
            self.pad_target_x -= spd * dt
        if self.key_right:
            self.pad_target_x += spd * dt
        half = self.pad_w / 2
        self.pad_target_x = max(half, min(W - half, self.pad_target_x))
        self.pad_x += (self.pad_target_x - self.pad_x) * min(1.0, 20 * dt)

        if self.ball_on_pad:
            self.ball_x = self.pad_x

    def _update_ball(self, dt):
        if self.ball_on_pad:
            return
        W, H = self.width(), self.height()
        steps = 4
        sub = dt / steps
        for _ in range(steps):
            self.ball_x += self.ball_vx * sub
            self.ball_y += self.ball_vy * sub

            # trail
            self.trail.append((self.ball_x, self.ball_y, 1.0))
            if len(self.trail) > 18:
                self.trail.pop(0)

            # walls
            if self.ball_x - self.ball_r < 0:
                self.ball_x = self.ball_r
                self.ball_vx = abs(self.ball_vx)
                self._spawn_wall_particles(self.ball_x, self.ball_y)
            if self.ball_x + self.ball_r > W:
                self.ball_x = W - self.ball_r
                self.ball_vx = -abs(self.ball_vx)
                self._spawn_wall_particles(self.ball_x, self.ball_y)
            if self.ball_y - self.ball_r < 0:
                self.ball_y = self.ball_r
                self.ball_vy = abs(self.ball_vy)
                self._spawn_wall_particles(self.ball_x, self.ball_y)

            # paddle
            pad_rect = QRectF(self.pad_x - self.pad_w / 2,
                              self.pad_y - self.pad_h / 2,
                              self.pad_w, self.pad_h)
            if (self.ball_vy > 0 and
                    pad_rect.left() - self.ball_r < self.ball_x < pad_rect.right() + self.ball_r and
                    pad_rect.top() - self.ball_r < self.ball_y < pad_rect.bottom()):
                self.ball_y = pad_rect.top() - self.ball_r
                rel = (self.ball_x - self.pad_x) / (self.pad_w / 2)
                rel = max(-0.85, min(0.85, rel))
                speed = math.hypot(self.ball_vx, self.ball_vy)
                angle = math.radians(-90 + rel * 60)
                self.ball_vx = speed * math.cos(angle)
                self.ball_vy = speed * math.sin(angle)
                self.combo = 0
                self._spawn_paddle_particles()

            # bricks
            self._check_brick_collisions()

            # fell below
            if self.ball_y - self.ball_r > H:
                self._lose_life()
                return

        # fade trail
        self.trail = [(x, y, a * 0.82) for x, y, a in self.trail]

    def _check_brick_collisions(self):
        br = self.ball_r
        bx, by = self.ball_x, self.ball_y

        for brick in self.bricks:
            if not brick.alive:
                continue
            r = brick.rect
            # closest point on rect to ball
            cx = max(r.left(), min(bx, r.right()))
            cy = max(r.top(),  min(by, r.bottom()))
            dx = bx - cx
            dy = by - cy
            dist2 = dx * dx + dy * dy
            if dist2 >= br * br:
                continue

            dist = math.sqrt(dist2) if dist2 > 0 else 0.001
            nx, ny = dx / dist, dy / dist

            # reflect
            dot = self.ball_vx * nx + self.ball_vy * ny
            self.ball_vx -= 2 * dot * nx
            self.ball_vy -= 2 * dot * ny

            # push out
            overlap = br - dist
            self.ball_x += nx * overlap
            self.ball_y += ny * overlap

            # damage brick
            pal = brick.palette
            brick.hit()
            if not brick.alive:
                self.combo += 1
                pts = pal["pts"] * self.combo
                self.score += pts
                if self.score > self.best:
                    self.best = self.score
                    self.sig_best.emit(self.best)
                self.sig_score.emit(self.score)
                self.sig_bricks.emit(self._alive_count())
                for _ in range(14):
                    self.particles.append(
                        Particle(r.center().x(), r.center().y(), pal["bg"])
                    )
                if self.combo > 2:
                    self.flash_text = TR[self.lang]["combo"] + str(self.combo)
                    self.flash_t = 0.8
            else:
                for _ in range(6):
                    self.particles.append(
                        Particle(cx, cy, pal["rim"], 0.5)
                    )

            # check win
            if self._alive_count() == 0:
                self._next_level()
            break  # one collision per sub-step

    def _alive_count(self):
        return sum(1 for b in self.bricks if b.alive)

    def _lose_life(self):
        self.lives -= 1
        self.sig_lives.emit(self.lives)
        self.combo = 0
        if self.lives <= 0:
            self.state = "gameover"
            self.timer.stop()
            self.sig_state.emit(self.state)
        else:
            self.state = "ready"
            self._reset_ball()
            self.sig_state.emit(self.state)
        self.update()

    def _next_level(self):
        self.level += 1
        self.sig_level.emit(self.level)
        self.flash_text = TR[self.lang]["level_up"]
        self.flash_t = 1.4
        self._build_level()
        self._reset_ball()
        self.state = "ready"
        self.sig_state.emit(self.state)

    # ── particles helpers ─────────────────────────────────────────────────
    def _spawn_wall_particles(self, x, y):
        clr = random.choice(self.t["particle_clrs"])
        for _ in range(4):
            self.particles.append(Particle(x, y, clr, 0.4))

    def _spawn_paddle_particles(self):
        for _ in range(8):
            self.particles.append(
                Particle(self.ball_x, self.ball_y,
                         self.t["paddle_rim"], 0.6)
            )

    def _emit_all(self):
        self.sig_score.emit(self.score)
        self.sig_best.emit(self.best)
        self.sig_level.emit(self.level)
        self.sig_lives.emit(self.lives)
        self.sig_bricks.emit(self._alive_count())

    # ── input ─────────────────────────────────────────────────────────────
    def mouseMoveEvent(self, e):
        self.pad_target_x = e.position().x()
        if self.state in ("playing", "ready"):
            if self.ball_on_pad:
                self.ball_x = self.pad_x
            self.update()

    def mousePressEvent(self, e):
        self.setFocus()
        if self.state == "ready":
            self.ball_on_pad = False
            self.state = "playing"
            self.sig_state.emit(self.state)

    def keyPressEvent(self, e):
        k = e.key()
        if k in (Qt.Key.Key_Left, Qt.Key.Key_A):
            self.key_left = True
        elif k in (Qt.Key.Key_Right, Qt.Key.Key_D):
            self.key_right = True
        elif k == Qt.Key.Key_Space:
            if self.state == "ready":
                self.ball_on_pad = False
                self.state = "playing"
                self.sig_state.emit(self.state)
            elif self.state in ("playing", "paused"):
                self.pause_toggle()

    def keyReleaseEvent(self, e):
        k = e.key()
        if k in (Qt.Key.Key_Left, Qt.Key.Key_A):
            self.key_left = False
        elif k in (Qt.Key.Key_Right, Qt.Key.Key_D):
            self.key_right = False

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if self.state != "idle":
            self._init_geometry()
            self._build_level()

    # ── PAINT ─────────────────────────────────────────────────────────────
    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        W, H = self.width(), self.height()
        t = self.t

        # background
        grad = QLinearGradient(0, 0, 0, H)
        grad.setColorAt(0, QColor(t["field_bg1"]))
        grad.setColorAt(1, QColor(t["field_bg2"]))
        p.fillRect(0, 0, W, H, grad)

        # border glow
        pen = QPen(QColor(t["field_border"]), 2)
        p.setPen(pen)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRect(1, 1, W - 2, H - 2)

        if self.state == "idle":
            self._draw_idle(p, W, H)
            return

        # bricks
        for b in self.bricks:
            b.draw(p, self.theme_key)

        # particles
        for part in self.particles:
            part.draw(p)

        # trail
        for i, (tx, ty, ta) in enumerate(self.trail):
            r = self.ball_r * 0.55 * ta
            if r < 1:
                continue
            c = QColor(t["ball_glow"])
            c.setAlphaF(ta * 0.45)
            p.setBrush(QBrush(c))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(QPointF(tx, ty), r, r)

        # ball
        self._draw_ball(p)

        # paddle
        self._draw_paddle(p)

        # flash
        if self.flash_t > 0:
            self._draw_flash(p, W, H)

        # overlay
        if self.state in ("paused", "gameover", "ready"):
            self._draw_overlay(p, W, H)

    def _draw_idle(self, p, W, H):
        t = self.t
        fs = max(20, min(W, H) // 10)
        p.setFont(QFont("Arial", fs, QFont.Weight.Bold))
        p.setPen(QPen(QColor(t["accent"])))
        p.drawText(QRectF(0, H * 0.38, W, fs * 1.5),
                   Qt.AlignmentFlag.AlignCenter, TR[self.lang]["title"])
        ss = max(10, fs // 2)
        p.setFont(QFont("Arial", ss))
        p.setPen(QPen(QColor(t["text2"])))
        p.drawText(QRectF(0, H * 0.56, W, ss * 2),
                   Qt.AlignmentFlag.AlignCenter, TR[self.lang]["tap_start"])

    def _draw_ball(self, p):
        t = self.t
        bx, by, br = self.ball_x, self.ball_y, self.ball_r

        # glow
        glow = QRadialGradient(bx, by, br * 2.8)
        gc = QColor(t["ball_glow"]); gc.setAlpha(60)
        glow.setColorAt(0, gc)
        glow.setColorAt(1, QColor(0, 0, 0, 0))
        p.setBrush(QBrush(glow)); p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(QPointF(bx, by), br * 2.8, br * 2.8)

        # body
        grad = QRadialGradient(bx - br * 0.3, by - br * 0.3, br * 1.6)
        grad.setColorAt(0, QColor(t["ball_c1"]))
        grad.setColorAt(0.5, QColor(t["ball_c2"]))
        grad.setColorAt(1, QColor(t["ball_glow"]))
        p.setBrush(QBrush(grad))
        pen = QPen(QColor(t["ball_glow"]), 1.2)
        p.setPen(pen)
        p.drawEllipse(QPointF(bx, by), br, br)

        # shine
        sg = QRadialGradient(bx - br * 0.28, by - br * 0.32, br * 0.7)
        sg.setColorAt(0, QColor(255, 255, 255, 200))
        sg.setColorAt(1, QColor(255, 255, 255, 0))
        p.setBrush(QBrush(sg)); p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(QPointF(bx - br * 0.15, by - br * 0.18),
                      br * 0.55, br * 0.45)

    def _draw_paddle(self, p):
        t  = self.t
        pw = self.pad_w
        ph = self.pad_h
        px = self.pad_x - pw / 2
        py = self.pad_y - ph / 2
        r  = ph / 2

        # glow
        glow = QRadialGradient(self.pad_x, self.pad_y, pw * 0.7)
        gc = QColor(t["paddle_c1"]); gc.setAlpha(40)
        glow.setColorAt(0, gc)
        glow.setColorAt(1, QColor(0, 0, 0, 0))
        p.setBrush(QBrush(glow)); p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(QPointF(self.pad_x, self.pad_y), pw * 0.7, ph * 2.5)

        # body
        grad = QLinearGradient(px, py, px, py + ph)
        grad.setColorAt(0, QColor(t["paddle_rim"]))
        grad.setColorAt(0.5, QColor(t["paddle_c1"]))
        grad.setColorAt(1, QColor(t["paddle_c2"]))
        p.setBrush(QBrush(grad))
        p.setPen(QPen(QColor(t["paddle_rim"]), 1.5))
        p.drawRoundedRect(QRectF(px, py, pw, ph), r, r)

        # shine
        sr = QRectF(px + 4, py + 2, pw * 0.6, ph * 0.4)
        sg = QLinearGradient(sr.topLeft(), sr.bottomLeft())
        sg.setColorAt(0, QColor(255, 255, 255, 160))
        sg.setColorAt(1, QColor(255, 255, 255, 0))
        p.setBrush(QBrush(sg)); p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(sr, r * 0.4, r * 0.4)

    def _draw_flash(self, p, W, H):
        a = min(1.0, self.flash_t / 0.35)
        fs = max(16, min(W, H) // 14)
        p.setFont(QFont("Arial", fs, QFont.Weight.Bold))
        tc = QColor(self.t["accent"]); tc.setAlphaF(a)
        sc = QColor(0, 0, 0, int(140 * a))
        p.setPen(QPen(sc))
        p.drawText(QRectF(3, H * 0.42 + 3, W, fs * 2),
                   Qt.AlignmentFlag.AlignCenter, self.flash_text)
        p.setPen(QPen(tc))
        p.drawText(QRectF(0, H * 0.42, W, fs * 2),
                   Qt.AlignmentFlag.AlignCenter, self.flash_text)

    def _draw_overlay(self, p, W, H):
        t = self.t
        ov = QColor(0, 0, 0, 150)
        p.fillRect(0, 0, W, H, ov)
        fs = max(18, min(W, H) // 12)

        if self.state == "ready":
            txt = TR[self.lang]["ready"]
            clr = t["accent2"]
            sub = "▶  Click / Space"
        elif self.state == "paused":
            txt = TR[self.lang]["pause"]
            clr = t["accent"]
            sub = ""
        else:
            txt = TR[self.lang]["game_over"]
            clr = "#ff4757"
            sub = f"{TR[self.lang]['score']}: {self.score}"

        p.setFont(QFont("Arial", fs, QFont.Weight.Bold))
        p.setPen(QPen(QColor(clr)))
        p.drawText(QRectF(0, H * 0.36, W, fs * 1.6),
                   Qt.AlignmentFlag.AlignCenter, txt)

        if sub:
            ss = max(10, fs // 2)
            p.setFont(QFont("Arial", ss))
            p.setPen(QPen(QColor(t["text2"])))
            p.drawText(QRectF(0, H * 0.36 + fs * 2, W, ss * 2),
                       Qt.AlignmentFlag.AlignCenter, sub)

        if self.state == "gameover" and self.score >= self.best > 0:
            ns = max(10, fs // 2)
            p.setFont(QFont("Arial", ns, QFont.Weight.Bold))
            p.setPen(QPen(QColor("#ffd700")))
            p.drawText(QRectF(0, H * 0.36 + fs * 4, W, ns * 2),
                       Qt.AlignmentFlag.AlignCenter,
                       TR[self.lang]["new_best"])


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def make_btn(text, bg, hover, fg="#ffffff"):
    b = QPushButton(text)
    b.setCursor(Qt.CursorShape.PointingHandCursor)
    b.setMinimumHeight(36)
    b.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    b.setStyleSheet(f"""
        QPushButton{{background:{bg};color:{fg};border:none;
            border-radius:7px;font-size:12px;font-weight:bold;padding:5px 8px;}}
        QPushButton:hover{{background:{hover};}}
    """)
    return b


# ─────────────────────────────────────────────────────────────────────────────
# MAIN WINDOW
# ─────────────────────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lang = "en"
        self.theme_key = "dark"
        self.t = THEMES[self.theme_key]
        self.setWindowTitle(TR[self.lang]["title"])
        self.setMinimumSize(540, 440)
        self.resize(980, 660)
        self._build_ui()
        self._apply_theme()

    # ── BUILD ─────────────────────────────────────────────────────────────
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # FIELD
        self.field = FieldWidget(self.theme_key, self.lang)
        self.field.sig_score.connect(lambda v: self.v_score.setText(str(v)))
        self.field.sig_best.connect(lambda v:  self.v_best.setText(str(v)))
        self.field.sig_level.connect(lambda v: self.v_level.setText(str(v)))
        self.field.sig_lives.connect(self._update_lives)
        self.field.sig_bricks.connect(lambda v: self.v_bricks.setText(str(v)))
        self.field.sig_state.connect(self._on_state)
        root.addWidget(self.field, stretch=1)

        # PANEL
        self.panel = QFrame()
        self.panel.setFixedWidth(196)
        self.panel.setSizePolicy(QSizePolicy.Policy.Fixed,
                                 QSizePolicy.Policy.Expanding)
        pv = QVBoxLayout(self.panel)
        pv.setContentsMargins(12, 14, 12, 14)
        pv.setSpacing(7)
        root.addWidget(self.panel)

        tr = TR[self.lang]

        # title
        self.lbl_title = QLabel(tr["title"])
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_title.setFont(QFont("Arial", 17, QFont.Weight.Bold))
        pv.addWidget(self.lbl_title)

        pv.addSpacing(4)

        # stats
        stats_frame = QFrame()
        sg = QGridLayout(stats_frame)
        sg.setContentsMargins(6, 6, 6, 6)
        sg.setSpacing(4)

        def mkrow(key, val="0"):
            k = QLabel(tr[key])
            k.setFont(QFont("Arial", 9))
            v = QLabel(val)
            v.setFont(QFont("Arial", 13, QFont.Weight.Bold))
            v.setAlignment(Qt.AlignmentFlag.AlignRight |
                           Qt.AlignmentFlag.AlignVCenter)
            return k, v

        self.k_score,  self.v_score  = mkrow("score")
        self.k_best,   self.v_best   = mkrow("best")
        self.k_level,  self.v_level  = mkrow("level",  "1")
        self.k_lives,  self.v_lives  = mkrow("lives")
        self.k_bricks, self.v_bricks = mkrow("bricks")

        rows = [(self.k_score,  self.v_score),
                (self.k_best,   self.v_best),
                (self.k_level,  self.v_level),
                (self.k_lives,  self.v_lives),
                (self.k_bricks, self.v_bricks)]
        for i, (k, v) in enumerate(rows):
            sg.addWidget(k, i, 0)
            sg.addWidget(v, i, 1)

        pv.addWidget(stats_frame)

        # hearts row
        self.hearts_lbl = QLabel("♥ ♥ ♥")
        self.hearts_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hearts_lbl.setFont(QFont("Arial", 14))
        pv.addWidget(self.hearts_lbl)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        pv.addWidget(sep)

        # buttons
        self.btn_start   = make_btn(tr["start"],   self.t["btn_bg"],  self.t["btn_h"])
        self.btn_pause   = make_btn(tr["pause"],   self.t["btn2_bg"], self.t["btn2_h"])
        self.btn_restart = make_btn(tr["restart"], self.t["btn3_bg"], self.t["btn3_h"])
        self.btn_pause.hide()
        self.btn_restart.hide()

        self.btn_start.clicked.connect(self._on_start)
        self.btn_pause.clicked.connect(self._on_pause)
        self.btn_restart.clicked.connect(self._on_restart)

        pv.addWidget(self.btn_start)
        pv.addWidget(self.btn_pause)
        pv.addWidget(self.btn_restart)

        sep2 = QFrame(); sep2.setFrameShape(QFrame.Shape.HLine)
        pv.addWidget(sep2)

        # theme
        trow = QHBoxLayout()
        self.k_theme = QLabel(tr["theme"])
        self.k_theme.setFont(QFont("Arial", 9))
        self.cmb_theme = QComboBox()
        self.cmb_theme.addItems([tr["dark"], tr["light"]])
        self.cmb_theme.currentIndexChanged.connect(self._on_theme)
        trow.addWidget(self.k_theme); trow.addWidget(self.cmb_theme)
        pv.addLayout(trow)

        # language
        lrow = QHBoxLayout()
        self.k_lang = QLabel(tr["language"])
        self.k_lang.setFont(QFont("Arial", 9))
        self.cmb_lang = QComboBox()
        self.cmb_lang.addItems(["English", "中文", "فارسی"])
        self.cmb_lang.currentIndexChanged.connect(self._on_lang)
        lrow.addWidget(self.k_lang); lrow.addWidget(self.cmb_lang)
        pv.addLayout(lrow)

        sep3 = QFrame(); sep3.setFrameShape(QFrame.Shape.HLine)
        pv.addWidget(sep3)

        # controls hint
        self.lbl_ctrl = QLabel(tr["controls"])
        self.lbl_ctrl.setWordWrap(True)
        self.lbl_ctrl.setFont(QFont("Arial", 8))
        self.lbl_ctrl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pv.addWidget(self.lbl_ctrl)

        pv.addStretch()

        # store translatable label pairs
        self._stat_rows = [
            (self.k_score,  "score"),
            (self.k_best,   "best"),
            (self.k_level,  "level"),
            (self.k_lives,  "lives"),
            (self.k_bricks, "bricks"),
        ]

    # ── SLOTS ─────────────────────────────────────────────────────────────
    def _on_start(self):
        self.field.start()
        self.field.setFocus()
        self.btn_start.hide()
        self.btn_pause.show()
        self.btn_restart.show()

    def _on_pause(self):
        self.field.pause_toggle()

    def _on_restart(self):
        self.field.restart()
        self.field.setFocus()
        tr = TR[self.lang]
        self.btn_pause.setText(tr["pause"])
        self.btn_start.hide()
        self.btn_pause.show()
        self.btn_restart.show()

    def _on_state(self, state):
        tr = TR[self.lang]
        if state == "paused":
            self.btn_pause.setText(tr["resume"])
        elif state in ("playing", "ready"):
            self.btn_pause.setText(tr["pause"])
        elif state == "gameover":
            self.btn_pause.hide()
            self.btn_restart.show()
        elif state == "idle":
            self.btn_start.show()
            self.btn_pause.hide()
            self.btn_restart.hide()

    def _on_theme(self, idx):
        self.theme_key = "dark" if idx == 0 else "light"
        self.t = THEMES[self.theme_key]
        self.field.set_theme(self.theme_key)
        self._apply_theme()

    def _on_lang(self, idx):
        self.lang = ["en", "zh", "fa"][idx]
        self.field.set_lang(self.lang)
        self._retranslate()
        self._apply_theme()

    def _update_lives(self, v):
        self.v_lives.setText(str(v))
        hearts = "♥ " * v + "♡ " * (MAX_LIVES - v)
        self.hearts_lbl.setText(hearts.strip())
        clr = "#ff4757" if v > 0 else "#555"
        self.hearts_lbl.setStyleSheet(f"color:{clr};background:transparent;border:none;")

    # ── THEME ─────────────────────────────────────────────────────────────
    def _apply_theme(self):
        t = self.t
        self.setStyleSheet(
            f"QMainWindow{{background:{t['win_bg1']};}}"
        )
        self.panel.setStyleSheet(f"""
            QFrame{{background:{t['panel_bg']};
                    border-left:2px solid {t['panel_border']};}}
            QLabel{{color:{t['text']};background:transparent;border:none;}}
            QFrame[frameShape="4"]{{background:{t['sep']};
                                    border:none;max-height:1px;}}
        """)
        cmb = f"""
            QComboBox{{background:{t['cmb_bg']};color:{t['text']};
                border:1px solid {t['cmb_border']};border-radius:5px;
                padding:2px 5px;font-size:10px;}}
            QComboBox::drop-down{{border:none;width:14px;}}
            QComboBox QAbstractItemView{{background:{t['cmb_bg']};
                color:{t['text']};
                selection-background-color:{t['btn_h']};
                border:1px solid {t['cmb_border']};}}
        """
        self.cmb_theme.setStyleSheet(cmb)
        self.cmb_lang.setStyleSheet(cmb)

        self.lbl_title.setStyleSheet(
            f"color:{t['accent']};background:transparent;border:none;")
        self.v_score.setStyleSheet(
            f"color:{t['score_clr']};font-weight:bold;background:transparent;border:none;")
        self.v_best.setStyleSheet(
            f"color:{t['score_clr']};font-weight:bold;background:transparent;border:none;")
        self.v_level.setStyleSheet(
            f"color:{t['stat_val']};font-weight:bold;background:transparent;border:none;")
        self.v_bricks.setStyleSheet(
            f"color:{t['accent2']};font-weight:bold;background:transparent;border:none;")
        self.lbl_ctrl.setStyleSheet(
            f"color:{t['text2']};background:transparent;border:none;")

        self._style_btn(self.btn_start,   t["btn_bg"],  t["btn_h"])
        self._style_btn(self.btn_pause,   t["btn2_bg"], t["btn2_h"])
        self._style_btn(self.btn_restart, t["btn3_bg"], t["btn3_h"])

    def _style_btn(self, btn, bg, hv):
        btn.setStyleSheet(f"""
            QPushButton{{background:{bg};color:{self.t['btn_txt']};
                border:none;border-radius:7px;
                font-size:12px;font-weight:bold;padding:6px 8px;}}
            QPushButton:hover{{background:{hv};}}
        """)

    # ── RETRANSLATE ───────────────────────────────────────────────────────
    def _retranslate(self):
        tr = TR[self.lang]
        self.setWindowTitle(tr["title"])
        self.lbl_title.setText(tr["title"])
        self.lbl_ctrl.setText(tr["controls"])
        self.k_theme.setText(tr["theme"])
        self.k_lang.setText(tr["language"])
        for lbl, key in self._stat_rows:
            lbl.setText(tr[key])
        self.btn_start.setText(tr["start"])
        self.btn_restart.setText(tr["restart"])
        st = self.field.state
        self.btn_pause.setText(
            tr["resume"] if st == "paused" else tr["pause"])
        self.cmb_theme.blockSignals(True)
        self.cmb_theme.setItemText(0, tr["dark"])
        self.cmb_theme.setItemText(1, tr["light"])
        self.cmb_theme.blockSignals(False)

        is_rtl = self.lang == "fa"
        self.panel.setLayoutDirection(
            Qt.LayoutDirection.RightToLeft if is_rtl
            else Qt.LayoutDirection.LeftToRight
        )


# ─────────────────────────────────────────────────────────────────────────────
# APP
# ─────────────────────────────────────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Breakout")

    win = MainWindow()
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
