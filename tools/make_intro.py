"""Generate assets/intro.gif: the purple wizard charges his staff, fires a spell, BOOM,
the screen glitches and the java-algorithms intro decodes into place.

Same look as the profile GIFs (kkdoestech/kkdoestech tools/make_glitch.py): black space,
blue/red chromatic split, white/yellow hot accents, green terminal text, scanlines.
The avatar cutout has no arms, so the sleeve, hand and staff are drawn here.

Needs the transparent avatar cutout assets/avatars/3.png.

Usage:  python tools/make_intro.py
"""

import math
import random
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

W, H = 800, 340
BG = (8, 8, 12)
WHITE = (255, 255, 255)
BLUE = (0, 168, 255)
DEEP_BLUE = (0, 71, 255)
RED = (255, 31, 61)
GREEN = (57, 255, 20)
YELLOW = (255, 211, 0)
PURPLE = (112, 60, 170)
VIOLET_GLOW = (190, 120, 255)
GREY = (175, 175, 195)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "intro.gif"
AVATAR = ROOT / "assets" / "avatars" / "3.png"

# Timeline (frame numbers where each scene starts).
CHARGE, CAST, BOOM, GLITCH, INTRO, HOLD, FRAMES = 15, 33, 37, 47, 61, 105, 110
TYPE_START, CHIP_START, TAGLINE_START = 64, 82, 97
BLIPS = {72, 73, 89}
FRAME_MS = 60

# Wizard rig.
AV_HEIGHT, AV_X, AV_SINK = 235, 14, 4   # avatar height, left edge, px pushed below the frame
OUTLINE_PX = 4
S = 2                                    # supersampling for the hand-drawn arm and staff
GRIP_X, GRIP_LOW_Y, GRIP_HIGH_Y = 335, 292, 262
STAFF_UP, STAFF_DOWN, ORB_R = 190, 70, 15
INK = (12, 10, 16)
WOOD, WOOD_LIGHT = (112, 72, 42), (168, 116, 72)
ROBE, ROBE_DARK, CUFF = (104, 56, 156), (70, 30, 108), (205, 195, 232)
SKIN = (236, 236, 240)

# Text block.
TITLE = "java-algorithms"
SUBTITLE = "> Java OOP & algorithm study notes"
TAGLINE = "14 problems · idea → walkthrough → full solution"
CHIPS = [("OOP", BLUE), ("HashMap", RED), ("Stack", YELLOW), ("Binary Search", GREEN), ("GCD", WHITE)]
SCRAMBLE = "01{}<>[];#$%&*/=+"
TEXT_X, TITLE_Y, UNDERLINE_Y, SUB_Y, CHIP_Y, TAG_Y = 372, 92, 154, 168, 206, 246

RING_STOPS = [(0.0, WHITE), (0.18, YELLOW), (0.45, RED), (0.75, DEEP_BLUE), (1.0, (0, 30, 90))]


def load_font(names, size):
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default(size=size)


TAG_FONT = load_font(["consola.ttf", "DejaVuSansMono.ttf"], 16)
TITLE_FONT = load_font(["consolab.ttf", "DejaVuSansMono-Bold.ttf"], 46)
SUB_FONT = load_font(["consola.ttf", "DejaVuSansMono.ttf"], 18)
CHIP_FONT = load_font(["consola.ttf", "DejaVuSansMono.ttf"], 14)
TAGLINE_FONT = load_font(["consola.ttf", "DejaVuSansMono.ttf"], 15)

TITLE_ADV = TITLE_FONT.getlength("m")
TITLE_W = TITLE_ADV * len(TITLE)
TARGET = (TEXT_X + TITLE_W / 2, 178)    # where the spell lands and the text appears


# ---------- small helpers ----------

def lerp(a, b, t):
    return a + (b - a) * t


def ease_out(t):
    return 1 - (1 - t) ** 3


def mix(c0, c1, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c0, c1))


def scale(c, k):
    return tuple(int(v * max(0.0, min(1.0, k))) for v in c)


def ramp_color(t):
    for (p0, c0), (p1, c1) in zip(RING_STOPS, RING_STOPS[1:]):
        if t <= p1:
            return mix(c0, c1, (t - p0) / (p1 - p0))
    return RING_STOPS[-1][1]


def shifted(im, dx, dy):
    out = Image.new(im.mode, im.size, (0, 0, 0, 0))
    out.paste(im, (dx, dy))
    return out


def rotate_point(dx, dy, deg):
    """Where (dx, dy) lands after PIL's counter-clockwise Image.rotate(deg)."""
    t = math.radians(deg)
    return dx * math.cos(t) + dy * math.sin(t), -dx * math.sin(t) + dy * math.cos(t)


def orb_center(grip, angle):
    ox, oy = rotate_point(0, -(STAFF_UP + ORB_R - 4), angle)
    return grip[0] + ox, grip[1] + oy


# ---------- avatar + rig ----------

def load_sprite(path, height):
    """Avatar at its on-screen height, with a black border round its silhouette."""
    im = Image.open(path).convert("RGBA")
    im = im.resize((round(im.width * height / im.height), height), Image.LANCZOS)
    pad = OUTLINE_PX * 2 + 2
    canvas = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    canvas.alpha_composite(im, (pad, pad))
    alpha = canvas.getchannel("A").point(lambda a: 255 if a > 40 else 0)
    border = alpha.filter(ImageFilter.MaxFilter(OUTLINE_PX * 4 + 1)).filter(ImageFilter.GaussianBlur(1))
    out = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    out.putalpha(border)
    out.alpha_composite(canvas)
    return out, pad


def draw_rig(grip, angle):
    """Sleeve, fist and staff (with orb) on a transparent full-frame layer."""
    gx, gy = grip[0] * S, grip[1] * S
    big = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))

    # Staff and its claw on their own layer, rotated around the grip.
    staff = Image.new("RGBA", big.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(staff)
    half = 7 * S
    top, bottom = gy - STAFF_UP * S, gy + STAFF_DOWN * S
    d.rounded_rectangle((gx - half, top, gx + half, bottom), radius=half, fill=WOOD, outline=INK, width=3 * S)
    d.line((gx - 2 * S, top + 10 * S, gx - 2 * S, bottom - 10 * S), fill=WOOD_LIGHT, width=3 * S)
    for k in (0.3, 0.62):
        y = top + (bottom - top) * k
        d.line((gx - half + 3 * S, y, gx + half - 3 * S, y), fill=INK, width=2 * S)
    oy = top - (ORB_R - 4) * S
    rc = (ORB_R + 7) * S
    d.arc((gx - rc, oy - rc, gx + rc, oy + rc), start=-25, end=205, fill=INK, width=11 * S)
    rc -= 2 * S
    d.arc((gx - rc, oy - rc, gx + rc, oy + rc), start=-20, end=200, fill=WOOD, width=7 * S)
    big.alpha_composite(staff.rotate(angle, resample=Image.BICUBIC, center=(gx, gy)))

    # Sleeve: rises from below the frame to the wrist.
    d = ImageDraw.Draw(big)
    wx, wy = gx - 16 * S, gy + 12 * S
    bx, by = gx - 72 * S, (H + 50) * S
    length = math.hypot(bx - wx, by - wy)
    ux, uy = (bx - wx) / length, (by - wy) / length
    nx, ny = -uy, ux

    def at(t, w):
        return (wx + ux * length * t + nx * w, wy + uy * length * t + ny * w)

    ww, we = 23 * S, 32 * S
    d.polygon([at(0, ww), at(1, we), at(1, -we), at(0, -ww)], fill=ROBE, outline=INK, width=4 * S)
    d.polygon([at(0.25, -ww * 0.2), at(1, -we * 0.3), at(1, -we + 4 * S), at(0.25, -ww + 4 * S)], fill=ROBE_DARK)
    d.polygon([at(0, ww), at(0.16, ww * 1.05), at(0.16, -ww * 1.05), at(0, -ww)], fill=CUFF, outline=INK, width=3 * S)

    # Fist round the staff: palm, finger creases, thumb on top.
    fx, fy = gx - 2 * S, gy
    d.ellipse((fx - 21 * S, fy - 18 * S, fx + 21 * S, fy + 18 * S), fill=SKIN, outline=INK, width=3 * S)
    for k in (-9, 0, 9):
        d.line((fx + 3 * S, fy + k * S, fx + 19 * S, fy + k * S), fill=INK, width=2 * S)
    d.ellipse((fx - 22 * S, fy - 23 * S, fx + 4 * S, fy - 6 * S), fill=SKIN, outline=INK, width=3 * S)

    # Orb in the claw: dark rim, violet body, white core, specular dot.
    cx, cy = (v * S for v in orb_center(grip, angle))
    r = ORB_R * S
    d.ellipse((cx - r - 3 * S, cy - r - 3 * S, cx + r + 3 * S, cy + r + 3 * S), fill=INK)
    for k in range(10):
        t = k / 9
        rr = r * (1 - 0.8 * t)
        col = mix(PURPLE, VIOLET_GLOW, min(1, t * 1.6)) if t < 0.6 else mix(VIOLET_GLOW, WHITE, (t - 0.6) / 0.4)
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=col)
    d.ellipse((cx - r * 0.6, cy - r * 0.65, cx - r * 0.15, cy - r * 0.25), fill=WHITE)

    return big.resize((W, H), Image.LANCZOS)


def actor_layer(sprite, pad, grip_y, angle, bob):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.alpha_composite(sprite, (AV_X - pad, H + AV_SINK - AV_HEIGHT - pad + bob))
    layer.alpha_composite(draw_rig((GRIP_X, grip_y + bob), angle))
    return layer


# ---------- glitch helpers (from make_glitch.py) ----------

def tinted(sprite, color, strength=0.8):
    ghost = Image.new("RGBA", sprite.size, color + (0,))
    ghost.putalpha(sprite.getchannel("A").point(lambda a: int(a * strength)))
    return ghost


def slice_sprite(sprite, rng, count, max_shift):
    out = sprite.copy()
    for _ in range(count):
        y0 = rng.randint(0, max(0, sprite.height - 6))
        strip = sprite.crop((0, y0, sprite.width, min(sprite.height, y0 + rng.randint(4, 16))))
        out.paste((0, 0, 0, 0), (0, y0, sprite.width, y0 + strip.height))
        out.paste(strip, (rng.randint(-max_shift, max_shift), y0), strip)
    return out


def frame_slices(img, rng, count, max_shift):
    out = img.copy()
    for _ in range(count):
        y0 = rng.randint(0, H - 6)
        strip = img.crop((0, y0, W, min(H, y0 + rng.randint(3, 24))))
        out.paste(ImageChops.offset(strip, rng.randint(-max_shift, max_shift), 0), (0, y0))
    return out


def scanlines():
    overlay = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(overlay)
    for y in range(0, H, 3):
        d.line([(0, y), (W, y)], fill=(200, 200, 200))
    return overlay


SCANLINES = scanlines()


def glitch_actor_onto(canvas, act, level, rng):
    if level == 0:
        canvas.alpha_composite(act)
        return
    split = [0, 4, 8, 14][level]
    dx = rng.randint(split // 2 + 1, split)
    jx = rng.randint(-12, 12) if level >= 2 else 0
    body = slice_sprite(act, rng, 3 + level * 3, 8 * level) if level >= 2 else act
    canvas.alpha_composite(shifted(tinted(act, RED), jx + dx, rng.randint(-2, 2)))
    canvas.alpha_composite(shifted(tinted(act, BLUE), jx - dx, rng.randint(-2, 2)))
    canvas.alpha_composite(shifted(body, jx, 0))


def glitch_frame(img, level, rng):
    out = frame_slices(img, rng, [0, 2, 5, 8][level], [0, 10, 30, 60][level])
    if level >= 2:
        dx = [0, 0, 4, 8][level]
        r, g, b = out.split()
        out = Image.merge("RGB", (ImageChops.offset(r, dx, 0), g, ImageChops.offset(b, -dx, 0)))
    d = ImageDraw.Draw(out)
    for _ in range([0, 2, 5, 9][level]):
        bx, by = rng.randint(0, W - 40), rng.randint(0, H - 10)
        d.rectangle((bx, by, bx + rng.randint(6, 60), by + rng.randint(2, 8)),
                    fill=rng.choice([GREEN, YELLOW, RED, BLUE, WHITE]))
    return out


# ---------- light effects ----------

FX_RNG = random.Random(7)
CHARGE_PARTICLES = [(FX_RNG.uniform(0, 2 * math.pi), FX_RNG.uniform(50, 150), FX_RNG.uniform(0.6, 1.4),
                     FX_RNG.random(), FX_RNG.choice([VIOLET_GLOW, VIOLET_GLOW, BLUE, WHITE])) for _ in range(46)]
BOOM_SPARKS = [(FX_RNG.uniform(0, 2 * math.pi), FX_RNG.uniform(8, 30),
                FX_RNG.choice([WHITE, YELLOW, YELLOW, RED, BLUE, VIOLET_GLOW])) for _ in range(70)]


def bolt(d, x, y, ang, rng, col, segs=6):
    pts = [(x, y)]
    for _ in range(segs):
        ang += rng.uniform(-0.7, 0.7)
        step = rng.uniform(10, 18)
        x, y = x + math.cos(ang) * step, y + math.sin(ang) * step
        pts.append((x, y))
    d.line(pts, fill=col, width=2)


def orb_glow(soft, orb, power):
    ox, oy = orb
    d = ImageDraw.Draw(soft)
    r = 14 + 34 * power
    d.ellipse((ox - r, oy - r, ox + r, oy + r), fill=scale(VIOLET_GLOW, 0.3 + 0.7 * power))
    r *= 0.45
    d.ellipse((ox - r, oy - r, ox + r, oy + r), fill=scale(WHITE, 0.2 + 0.6 * power))


def charge_fx(soft, sharp, orb, i, power, rng):
    """Particles spiralling into the orb; crackling bolts once it is nearly full."""
    ox, oy = orb
    d = ImageDraw.Draw(sharp)
    clock = (i - CHARGE) / 10

    def pos(r0, ang0, u):
        r, a = r0 * (1 - u), ang0 + 3 * u
        return ox + r * math.cos(a), oy + r * math.sin(a)

    for ang0, r0, spd, ph, col in CHARGE_PARTICLES[:int(len(CHARGE_PARTICLES) * min(1, 0.3 + power))]:
        u = (clock * spd + ph) % 1
        d.line((pos(r0, ang0, max(0, u - 0.06)), pos(r0, ang0, u)), fill=scale(col, 0.4 + 0.6 * u), width=2)
    if power > 0.7:
        for _ in range(2 + int(power * 2)):
            bolt(d, ox, oy, rng.uniform(0, 2 * math.pi), rng, rng.choice([WHITE, VIOLET_GLOW, BLUE]))


def cast_fx(soft, sharp, orb, t):
    """The spell flies from the orb to the title spot."""
    (ox, oy), (tx, ty) = orb, TARGET
    bx, by = lerp(ox, tx, t), lerp(oy, ty, t)
    tail = max(0, t - 0.35)
    ImageDraw.Draw(sharp).line(((lerp(ox, tx, tail), lerp(oy, ty, tail)), (bx, by)), fill=VIOLET_GLOW, width=4)
    ImageDraw.Draw(soft).ellipse((bx - 32, by - 32, bx + 32, by + 32), fill=VIOLET_GLOW)
    ImageDraw.Draw(sharp).ellipse((bx - 10, by - 10, bx + 10, by + 10), fill=WHITE)


def boom_fx(soft, sharp, k):
    """Explosion at the title spot: hot core, two shockwave rings, flying sparks."""
    tx, ty = TARGET
    dg, ds = ImageDraw.Draw(soft), ImageDraw.Draw(sharp)
    core = max(0.0, 1 - k / 7)
    r = 40 + 10 * k
    dg.ellipse((tx - r, ty - r * 0.8, tx + r, ty + r * 0.8), fill=scale(YELLOW, core))
    dg.ellipse((tx - r / 2, ty - r * 0.4, tx + r / 2, ty + r * 0.4), fill=scale(WHITE, core))
    for delay in (0, 3):
        kk = k - delay
        if kk < 0:
            continue
        r = 16 + 30 * kk + 4 * kk * kk
        col = ramp_color(min(1, kk / 8))
        width = max(2, int(14 - 1.5 * kk))
        box = (tx - r, ty - r * 0.75, tx + r, ty + r * 0.75)
        dg.ellipse(box, outline=col, width=width + 6)
        ds.ellipse(box, outline=col, width=max(1, width // 3))
    fade = 1 - k / 10
    for ang, v, col in BOOM_SPARKS:
        dist = v * (k + 1) * (1 - 0.035 * k)
        x1, y1 = tx + math.cos(ang) * dist, ty + math.sin(ang) * dist * 0.8
        x0, y0 = tx + math.cos(ang) * (dist - v * 0.9), ty + math.sin(ang) * (dist - v * 0.9) * 0.8
        ds.line((x0, y0, x1, y1), fill=scale(col, fade), width=2)


def remnant_fx(soft, strength):
    tx, ty = TARGET
    ImageDraw.Draw(soft).ellipse((tx - 90, ty - 60, tx + 90, ty + 60), fill=scale(VIOLET_GLOW, 0.5 * strength))


# ---------- scenes ----------

@dataclass
class Shot:
    duration: int = FRAME_MS
    grip_y: float = GRIP_LOW_Y
    angle: float = -25.0           # PIL degrees: negative leans the staff top to the right
    bob: int = 0
    actor_level: int = 0
    actor_alpha: float = 1.0
    power: float = 0.25            # orb glow, 0..1
    effects: object = None         # fn(soft, sharp, orb) drawing extra light
    title: list = None             # [(char, colour), ...]
    title_split: int = 0
    underline: float = 0.0
    typed: int = 0
    cursor: bool = False
    chips: int = 0
    chip_flash: int = -1
    tagline: float = 0.0
    frame_level: int = 0
    flash: float = 0.0
    shake: tuple = (0, 0)
    fade: float = 0.0


def idle_bob(i):
    return round(1.5 + 1.5 * math.sin(2 * math.pi * (i - GLITCH) / 24))


def title_chars(i, rng):
    """Each position shows random symbols until it locks in, left to right."""
    out = []
    for j, ch in enumerate(TITLE):
        if i >= GLITCH + 2 + j * 0.6:
            out.append((ch, RED if j < 4 else WHITE))
        else:
            out.append((rng.choice(SCRAMBLE), GREEN))
    return out


def scene_arrive(i, rng):
    """0-14: the wizard glitches into existence, staff held low."""
    level = 3 if i < 3 else 2 if i < 7 else 1 if i < 11 else 0
    return Shot(actor_level=level, actor_alpha=min(1, (i + 1) / 8), power=0.2)


def scene_charge(i, rng):
    """15-36: raise the staff and charge the orb, then fire the spell at the title spot."""
    if i < CAST:
        e = ease_out(min(1, (i - CHARGE) / (CAST - 3 - CHARGE)))
        power = min(1, (i - CHARGE) / (CAST - 1 - CHARGE))
        shot = Shot(grip_y=lerp(GRIP_LOW_Y, GRIP_HIGH_Y, e), angle=lerp(-25, 4, e), power=power)
        shot.effects = lambda soft, sharp, orb: charge_fx(soft, sharp, orb, i, power, rng)
        if i >= CAST - 6:
            a = 2 + i - (CAST - 6)
            shot.shake = (rng.randint(-a, a), rng.randint(-a, a))
        return shot
    t = (i - CAST + 1) / (BOOM - CAST)
    shot = Shot(grip_y=GRIP_HIGH_Y, angle=lerp(4, -16, ease_out(min(1, t * 2))), power=0.6 * (1 - t))
    shot.effects = lambda soft, sharp, orb: cast_fx(soft, sharp, orb, t)
    return shot


def scene_boom(i, rng):
    """37-46: white flash, shockwaves and sparks; the camera shakes."""
    k = i - BOOM
    amp = [10, 9, 7, 6, 4, 3, 2, 1, 0, 0][k]
    shot = Shot(duration=50, grip_y=GRIP_HIGH_Y, angle=lerp(-16, 4, ease_out(min(1, k / 4))), power=0.3,
                flash=[0.9, 0.5, 0.2][k] if k < 3 else 0.0,
                shake=(rng.randint(-amp, amp), rng.randint(-amp, amp)),
                frame_level=1 if k >= 6 else 0)
    shot.effects = lambda soft, sharp, orb: boom_fx(soft, sharp, k)
    return shot


def scene_glitch(i, rng):
    """47-60: heavy glitch while the title decodes into place."""
    k = i - GLITCH
    level = 3 if k < 4 else 2 if k < 8 else 1 if k < 12 else 0
    shot = Shot(duration=55 if level >= 2 else FRAME_MS, grip_y=GRIP_HIGH_Y, angle=4, bob=idle_bob(i),
                power=0.35, actor_level=max(0, level - 1), frame_level=level,
                title=title_chars(i, rng), title_split=[0, 3, 6, 10][level])
    remnant = max(0.0, 1 - k / 5)
    if remnant:
        shot.effects = lambda soft, sharp, orb: remnant_fx(soft, remnant)
    return shot


def scene_intro(i, rng):
    """61-105: underline, typed subtitle, topic chips, tagline; the last frame holds."""
    k = i - INTRO
    chips = 0 if i < CHIP_START else min(len(CHIPS), (i - CHIP_START) // 3 + 1)
    popping = i < CHIP_START + 3 * len(CHIPS) and (i - CHIP_START) % 3 == 0
    shot = Shot(duration=2000 if i == HOLD else FRAME_MS, grip_y=GRIP_HIGH_Y, angle=4, bob=idle_bob(i),
                power=0.35 + 0.15 * math.sin(k / 3), title=title_chars(i, rng), title_split=2,
                underline=min(1, (k + 1) / 8), typed=max(0, 2 * (i - TYPE_START + 1)),
                cursor=(i // 4) % 2 == 0, chips=chips, chip_flash=chips - 1 if popping else -1,
                tagline=max(0.0, min(1.0, (i - TAGLINE_START + 1) / 4)))
    if i in BLIPS:
        shot.frame_level, shot.actor_level, shot.title_split = 1, 1, 6
    return shot


def scene_out(i, rng):
    """106-109: glitch out to black so the loop restarts cleanly."""
    shot = scene_intro(HOLD, rng)
    shot.duration, shot.frame_level, shot.actor_level, shot.title_split = FRAME_MS, 3, 2, 10
    shot.fade = (i - HOLD) / (FRAMES - 1 - HOLD)
    return shot


def shot_for(i, rng):
    for start, scene in ((HOLD + 1, scene_out), (INTRO, scene_intro), (GLITCH, scene_glitch),
                         (BOOM, scene_boom), (CHARGE, scene_charge), (0, scene_arrive)):
        if i >= start:
            return scene(i, rng)


# ---------- frame composition ----------

def stars(rng):
    return [(rng.randint(0, W - 1), rng.randint(0, H - 1), rng.choice([WHITE, BLUE, WHITE, YELLOW]),
             rng.randint(0, 19)) for _ in range(90)]


def background(i, starfield):
    sky = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(sky)
    for sx, sy, col, ph in starfield:
        if (i // 4 + ph) % 5 < 4:   # twinkle in 4-frame steps so most frames only redraw the wizard
            d.point((sx, sy), fill=col)
    cursor = "_" if (i // 4) % 2 == 0 else " "
    d.text((18, 14), f"> java-algorithms{cursor}", font=TAG_FONT, fill=GREEN)
    tag = "// summary.md"
    d.text((W - 18 - d.textlength(tag, font=TAG_FONT), 14), tag, font=TAG_FONT, fill=YELLOW)
    d.rectangle((W - 246, H - 18, W - 140, H - 15), fill=RED)
    d.rectangle((W - 120, H - 18, W - 14, H - 15), fill=DEEP_BLUE)
    return sky


def draw_text_block(img, shot):
    d = ImageDraw.Draw(img)
    if shot.title:
        if shot.title_split:
            for dx, col in ((shot.title_split, RED), (-shot.title_split, BLUE)):
                for j, (ch, _) in enumerate(shot.title):
                    d.text((TEXT_X + j * TITLE_ADV + dx, TITLE_Y), ch, font=TITLE_FONT, fill=col)
        for j, (ch, col) in enumerate(shot.title):
            d.text((TEXT_X + j * TITLE_ADV, TITLE_Y), ch, font=TITLE_FONT, fill=col)
    if shot.underline:
        d.rectangle((TEXT_X, UNDERLINE_Y, TEXT_X + TITLE_W * shot.underline, UNDERLINE_Y + 3), fill=BLUE)
    if shot.typed:
        text = SUBTITLE[:shot.typed]
        d.text((TEXT_X, SUB_Y), text, font=SUB_FONT, fill=GREEN)
        if shot.cursor:
            cx = TEXT_X + d.textlength(text, font=SUB_FONT) + 3
            d.rectangle((cx, SUB_Y + 3, cx + 9, SUB_Y + 20), fill=GREEN)
    x = TEXT_X
    for k, (label, col) in enumerate(CHIPS[:shot.chips]):
        w = d.textlength(label, font=CHIP_FONT) + 18
        d.rounded_rectangle((x, CHIP_Y, x + w, CHIP_Y + 24), radius=5, fill=(16, 16, 26),
                            outline=WHITE if k == shot.chip_flash else col, width=2)
        d.text((x + 9, CHIP_Y + 4), label, font=CHIP_FONT, fill=col)
        x += w + 8
    if shot.tagline:
        d.text((TEXT_X, TAG_Y), TAGLINE, font=TAGLINE_FONT, fill=mix(BG, GREY, shot.tagline))


def render(i, shot, sprite, pad, starfield, rng):
    canvas = background(i, starfield).convert("RGBA")
    act = actor_layer(sprite, pad, shot.grip_y, shot.angle, shot.bob)
    if shot.actor_alpha < 1:
        act.putalpha(act.getchannel("A").point(lambda a: int(a * shot.actor_alpha)))
    glitch_actor_onto(canvas, act, shot.actor_level, rng)
    out = canvas.convert("RGB")

    soft, sharp = Image.new("RGB", (W, H)), Image.new("RGB", (W, H))
    orb = orb_center((GRIP_X, shot.grip_y + shot.bob), shot.angle)
    orb_glow(soft, orb, shot.power * shot.actor_alpha)
    if shot.effects:
        shot.effects(soft, sharp, orb)
    out = ImageChops.screen(out, soft.filter(ImageFilter.GaussianBlur(9)))
    out = ImageChops.screen(out, sharp)

    draw_text_block(out, shot)
    if shot.flash:
        out = Image.blend(out, Image.new("RGB", (W, H), WHITE), shot.flash)
    if shot.frame_level:
        out = glitch_frame(out, shot.frame_level, rng)
    if shot.shake != (0, 0):
        moved = Image.new("RGB", (W, H), BG)
        moved.paste(out, shot.shake)
        out = moved
    out = ImageChops.multiply(out, SCANLINES)
    if shot.fade:
        out = Image.blend(out, Image.new("RGB", (W, H), BG), shot.fade)
    return out


def main():
    rng = random.Random(1337)
    sprite, pad = load_sprite(AVATAR, AV_HEIGHT)
    starfield = stars(rng)

    rendered, durations = [], []
    for i in range(FRAMES):
        shot = shot_for(i, rng)
        rendered.append(render(i, shot, sprite, pad, starfield, rng))
        durations.append(shot.duration)

    # One palette for every frame (built from a frame of each scene), so unchanged pixels keep
    # the same index and the GIF only stores the parts that move.
    samples = [12, 32, 35, 40, 44, 50, 96, HOLD]
    montage = Image.new("RGB", (W, H * len(samples)))
    for n, i in enumerate(samples):
        montage.paste(rendered[i], (0, H * n))
    palette = montage.quantize(colors=255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    frames = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in rendered]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=durations, loop=0, optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size / 1024:.0f} KB, {len(frames)} frames, {sum(durations) / 1000:.1f} s)")


if __name__ == "__main__":
    main()
