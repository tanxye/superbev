import pygame
pygame.mixer.pre_init(44100, -16, 2, 512)
from graphics import Canvas
import tkinter as _tk
import random
import time
import math
import os
import sys

# ── Graceful Shutdown Handler ────────────────────────────────────────────────
def on_closing():
    """Forces the application to stop completely when the X is clicked."""
    try:
        # Stop music and quit mixer to free up audio hardware
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    except:
        pass
    
    # 1. Destroy the UI window
    if canvas.main_window:
        canvas.main_window.destroy()
        
    # 2. Use os._exit(0) to force kill the process and all background threads
    os._exit(0)

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 600
canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT, title="SUPERBEV")
# Assign the protocol to the main window
canvas.main_window.protocol("WM_DELETE_WINDOW", on_closing)

# ── Constants and Data ───────────────────────────────────────────────────────
BG            = "#f0eae0"
BG_OVERLAY    = "#f0efee"
DARK_PURPLE   = "#460e64"
TABLE_BROWN   = "#bc8f8f"
TABLE_DARK    = "#8b4513"
WHITE         = "white"
BROWN_DARK    = "#5c2d0a"
PINK          = "#e8547a"
GREEN_LIME    = "#6db33f"
OUTLINE       = DARK_PURPLE
SUCCESS_GREEN = "#2ecc71"
FAIL_RED      = "#e74c3c"
TRUNK_GREEN   = "#2f8e2f"
VINE_GREEN    = "#2a6a3b"
FLOWER_COLOURS = ["#d98fb3", "#d9b36a", "#dcdcdc"]

TREE_BAND_PALETTES = [
    ["#ff4fd8", "#ffb3f0", "#d94dff", "#ff7ad9"],
    ["#00e5ff", "#66f2ff", "#2f6fff", "#7ad7ff"],
    ["#ffb347", "#ff884d", "#ffd36a", "#ffcc99"],
]
ALL_VARIATIONS = TREE_BAND_PALETTES[0] + TREE_BAND_PALETTES[1] + TREE_BAND_PALETTES[2]
TREE_COLOURS = [
    ("#cc44bb", "#ff44cc"),
    ("#00ccaa", "#00ffee"),
    ("#dd5500", "#ff7700"),
]

ENERGY_CURVE = [0.14]*5 + [0.20]*5 + [0.14]*5 + [0.17]*5 + [0.20]*5 + [0.14]*5 + [0.23]*5 + [0.27]*5 + [0.30]*10 + [0.33]*5 + [0.27]*5 + [0.23]*5 + [0.20]*5 + [0.40]*5 + [0.37]*5 + [0.53]*5 + [0.67]*5 + [0.77]*5 + [0.83]*5 + [0.63]*5 + [0.87]*5 + [0.60]*10 + [0.50]*5 + [0.63]*5 + [0.80]*5 + [0.63]*5 + [0.53]*5 + [0.50]*5 + [0.33]*5 + [0.43]*5 + [0.63]*5 + [0.53]*5 + [0.47]*5 + [0.50]*5 + [0.53]*5 + [0.73]*5 + [0.50]*5 + [0.57]*5 + [0.40]*5 + [0.43]*5 + [0.57]*5 + [0.33]*15 + [0.23]*5 + [0.20]*10 + [0.23]*5 + [0.30]*5 + [0.27]*10 + [0.20]*5 + [0.10]*5 + [0.17]*5 + [0.20]*5 + [0.10]*5 + [0.03]*5
BEAT_TIMES = [7.2, 8.2, 8.4, 8.9, 9.3, 9.8, 10.5, 10.8, 11.1, 11.4, 11.8, 12.2, 12.4, 12.7, 12.9, 13.4, 13.8, 14.0, 14.3, 15.7, 16.0, 16.5, 17.0, 17.5, 18.5, 19.0, 19.5, 21.0, 25.5, 26.0]

def get_energy(t):
    idx = max(0, min(int(t / 0.1), len(ENERGY_CURVE) - 1))
    return ENERGY_CURVE[idx]

def is_beat(t, last_beat, tolerance=0.12):
    if (t - last_beat) < 0.25: return False
    return any(abs(t - b) < tolerance for b in BEAT_TIMES)

def asset_path(filename):
    if getattr(sys, 'frozen', False): return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

try:
    canvas.main_window.iconbitmap(asset_path('logo.ico'))
except Exception: pass

def sleep(seconds):
    end = time.time() + seconds
    while time.time() < end:
        try:
            # Safely check if the window exists
            if not canvas.main_window.winfo_exists():
                sys.exit()
        except _tk.TclError:
            # If the window is already destroyed, the app is closing
            sys.exit()
            
        canvas.update()
        time.sleep(0.02)

# [Shape functions and Audio functions]
def rect(x1, y1, x2, y2, color="black"): return canvas.create_rectangle(int(x1), int(y1), int(x2), int(y2), color)
def oval(x1, y1, x2, y2, color="black"): return canvas.create_oval(int(x1), int(y1), int(x2), int(y2), color)
def line(x1, y1, x2, y2, color="black"): return canvas.create_line(int(x1), int(y1), int(x2), int(y2), color)
def poly(points, color="black", outline=""):
    flat = [v for p in points for v in (int(p[0]), int(p[1]))]
    return _tk.Canvas.create_polygon(canvas, *flat, fill=color, outline=outline)
def draw_text(x, y, text, size=10, color=DARK_PURPLE, anchor="center"):
    font = ("Trebuchet MS", int(size * 1.25))
    canvas.create_text(int(x), int(y), text, anchor, font, color)
def draw_button(x, y, w, h, label):
    btn = rect(x, y, x + w, y + h, WHITE)
    _tk.Canvas.create_rectangle(canvas, int(x), int(y), int(x+w), int(y+h), fill="", outline=DARK_PURPLE)
    draw_text(x + w / 2, y + h / 2, label, 10, DARK_PURPLE)
    return btn
def is_clicked(click, btn_id):
    if not click: return False
    cx, cy = (click.x, click.y) if hasattr(click, 'x') else (click[0], click[1])
    return btn_id in canvas.find_overlapping(cx - 1, cy - 1, cx + 1, cy + 1)

_mixer_ok = False
_click_sound = None
def init_audio():
    global _mixer_ok, _click_sound
    try:
        pygame.mixer.init()
        _mixer_ok = True
        if os.path.exists(asset_path("click.mp3")):
            _click_sound = pygame.mixer.Sound(asset_path("click.mp3"))
    except: _mixer_ok = False

def play_bgm():
    if _mixer_ok and os.path.exists(asset_path("bgm.mp3")):
        pygame.mixer.music.load(asset_path("bgm.mp3"))
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(loops=-1)

def play_lightshow_music():
    if _mixer_ok and os.path.exists(asset_path("Night_Blooming_Canopy.mp3")):
        pygame.mixer.music.load(asset_path("Night_Blooming_Canopy.mp3"))
        pygame.mixer.music.play()

def play_click():
    if _mixer_ok and _click_sound: _click_sound.play()

# [Game/Drawing functions follow your original logic...]
def draw_register(x, y):
    w, h = 160, 100
    rect(x, y, x + w, y + h, "#333333")
    rect(x + 20, y + 20, x + w - 20, y + 60, "#66ff66")
    draw_text(x + 80, y + 80, "REGISTER", 8, "white")

def draw_beverage(cx, cy, beverage_type):
    tw, height, fh = 48, 130, 30
    top_y = cy - height
    rect(cx - 2, top_y - 20, cx + 2, cy - 20, "#d1d1d1")
    poly([(cx-tw, top_y),(cx+tw, top_y),(cx+tw//2, top_y+fh),(cx-tw//2, top_y+fh)], color="purple", outline=OUTLINE)
    rect(cx - tw//2, top_y + fh, cx + tw//2, cy, WHITE)
    bev_color = BROWN_DARK if beverage_type == "MILO DINOSAUR" else PINK if beverage_type == "BANDUNG" else GREEN_LIME
    rect(cx - tw//2 + 2, top_y + fh + 2, cx + tw//2 - 2, cy - 2, bev_color)
    rect(cx - tw//2, cy - 50, cx + tw//2, cy - 26, "green")

def draw_price_sign(x, y):
    rect(x, y - 40, x + 200, y + 120, "#e3c49d")
    draw_text(x + 100, y - 10, "PRICE LIST", 10, DARK_PURPLE)
    for i, p in enumerate(["MILO DINO: $8", "BANDUNG: $10", "SUGARCANE: $11"]):
        draw_text(x + 20, y + 30 + i * 32, p, 9, DARK_PURPLE, anchor="w")

def draw_placard(x, y):
    pw, ph, slant, sw = 110, 80, 20, 24
    poly([(x-sw, y+ph),(x, y),(x+sw, y+ph)], color="#adab9c", outline=OUTLINE)
    poly([(x, y),(x+pw, y),(x+pw+slant, y+ph),(x+slant, y+ph)], color=WHITE, outline=OUTLINE)
    for i, word in enumerate(["Singapore's", "  Supertree", "    beverages!"]):
        draw_text(x + 60, y + 24 + i * 20, word, 8)

def bezier(x0, y0, x1, y1, x2, y2, steps=22):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = (1-t)**2*x0 + 2*(1-t)*t*x1 + t**2*x2
        y = (1-t)**2*y0 + 2*(1-t)*t*y1 + t**2*y2
        pts.append((int(x), int(y)))
    return pts

def draw_ls_background():
    for i in range(18):
        t = i / 18
        col = f"#{int(5+t*8):02x}{int(12+t*18):02x}{int(31+t*27):02x}"
        rect(0, int(i*CANVAS_HEIGHT/18), CANVAS_WIDTH, int((i+1)*CANVAS_HEIGHT/18), col)
    random.seed(77)
    for _ in range(120):
        sx, sy = random.randint(0, CANVAS_WIDTH), random.randint(0, int(CANVAS_HEIGHT*0.7))
        oval(sx, sy, sx+1, sy+1, "#cce0ff")

def draw_ls_stores():
    for xo in [50, 200, 400, 550]:
        x = xo * 2
        w, h = 44, 28
        rect(x-w, CANVAS_HEIGHT-h, x+w, CANVAS_HEIGHT, "#f5f2e3")
        poly([(x-w, CANVAS_HEIGHT-h),(x, CANVAS_HEIGHT-h-16),(x+w, CANVAS_HEIGHT-h)], color="#a54408", outline=OUTLINE)
        rect(x-24, CANVAS_HEIGHT-h+6, x+24, CANVAS_HEIGHT-8, "#a7530f")
        
def draw_signature():
    # 'e' for anchor ensures the text ends at the x, y coordinates
    # We use a very light color so it's visible but not distracting
    canvas.create_text(CANVAS_WIDTH - 10, CANVAS_HEIGHT - 10, 
                       text="tanxye", anchor="se", 
                       font=("Trebuchet MS", 8), color="#d3d3d3")

def draw_ls_supertree(cx, base_y, scale_factor, colours, band_palette):
    branch_col = colours[0]
    base_w = int(140 * 2 * scale_factor * 0.45)
    neck_w, trunk_h = int(base_w * 0.22), int(200 * 2 * scale_factor * 0.85)
    top_y = base_y - trunk_h
    branch_spread_w, num_veins = int(base_w * 1.35), 18
    
    all_led_rows = [] 
    # Draw the main trunk polygon
    poly([(cx - base_w // 2, base_y), (cx + base_w // 2, base_y), 
          (cx + neck_w, top_y), (cx - neck_w, top_y)], color=TRUNK_GREEN)
    
    # Draw the branches/veins
    for i in range(num_veins):
        vein_leds = []
        t_h = (i - (num_veins - 1) / 2) / ((num_veins - 1) / 2)
        pts = bezier(cx + int(t_h * neck_w), top_y, cx + int(t_h * branch_spread_w * 0.65), 
                     top_y - 160, cx + int(t_h * branch_spread_w), top_y - 160)
        for j in range(len(pts) - 1):
            line(pts[j][0], pts[j][1], pts[j+1][0], pts[j+1][1], branch_col)
        for di, (dx, dy) in enumerate(pts):
            if di % 2 == 0:
                led = oval(dx - 2, dy - 2, dx + 2, dy + 2, random.choice(band_palette))
                oval(dx, dy, dx + 1, dy + 1, "#e6e6e6")
                vein_leds.append(led)
        all_led_rows.append(vein_leds)
        
    # Draw the vines and flowers
    for v in range(3):
        phase = (2 * math.pi / 3) * v
        px, py = None, None
        for i in range(140):
            t = i / 140
            y, ang = base_y - int(trunk_h * t), t * 5 * 2 * math.pi + phase
            rad = (base_w // 2) * (1 - t * 0.6)
            x = cx + int(math.cos(ang) * rad)
            if px is not None: line(px, py, x, y, VINE_GREEN)
            if i % 25 == 0: # Adjusted frequency to look better
                oval(x-2, y-2, x+2, y+2, random.choice(FLOWER_COLOURS))
            px, py = x, y
            
    return all_led_rows

def run_light_show():
    """
    Fades out BGM, fades in lightshow music, runs 30s show, fades out.
    Intro order: centre tree (t2) first, then left (t1), then right (t3).
    """
    # 1. Initialize all state variables to prevent UnboundLocalError
    last_beat = -99.0
    wave_offset = 0.0
    pal_idx = [0, 1, 2]
    
    # 2. Define required constants for the animation logic
    WAKE_ORDER = [1, 0, 2]          # centre, left, right
    WAKE_TIMES = [0.0, 2.3, 4.6]    # when each wakes up
    
    # 3. Setup the UI
    play_lightshow_music()
    canvas.clear()
    draw_ls_background()
    
    # Draw order: centre first so it renders on top during the staggered intro
    t1 = draw_ls_supertree(240,  CANVAS_HEIGHT, 0.95, TREE_COLOURS[0], TREE_BAND_PALETTES[0])
    t2 = draw_ls_supertree(600,  CANVAS_HEIGHT, 1.10, TREE_COLOURS[1], TREE_BAND_PALETTES[1])
    t3 = draw_ls_supertree(960,  CANVAS_HEIGHT, 0.95, TREE_COLOURS[2], TREE_BAND_PALETTES[2])
    draw_ls_stores()
    
    all_trees = [t1, t2, t3]
    
    start = time.time()
    SHOW_DURATION = 30.0
    
    # 4. Main Animation Loop
    while True:
        # Graceful exit check
        if not canvas.main_window.winfo_exists():
            sys.exit()
            
        t_now = time.time() - start
        if t_now >= SHOW_DURATION:
            break
            
        energy = get_energy(t_now)
        beat_now = is_beat(t_now, last_beat)
        
        # ── 0–7s  quiet intro: centre first, then left, then right ───────
        if t_now < 7.0:
            awake = [ti for k, ti in enumerate(WAKE_ORDER) if t_now >= WAKE_TIMES[k]]
            for ti in awake:
                tree_rows = all_trees[ti]
                if not tree_rows: continue
                num_positions = len(tree_rows[0])
                row = int(t_now * 3) % num_positions
                for pos in range(num_positions):
                    dist = min(abs(pos - row), num_positions - abs(pos - row))
                    if dist <= 1:
                        c = random.choice(TREE_BAND_PALETTES[ti])
                        for vein in tree_rows:
                            if pos < len(vein): canvas.set_color(vein[pos], c)
                    elif random.random() < 0.25:
                        c = random.choice(TREE_BAND_PALETTES[ti])
                        for vein in tree_rows:
                            if pos < len(vein): canvas.set_color(vein[pos], c)
        
        # ── 7–14s  build: row sweep speeds up with energy ─────────────────
        elif t_now < 14.0:
            if beat_now:
                last_beat = t_now
                pal_idx = [(p + 1) % 3 for p in pal_idx]
            
            for ti, tree_rows in enumerate(all_trees):
                if not tree_rows: continue
                num_positions = len(tree_rows[0])
                pal = TREE_BAND_PALETTES[pal_idx[ti]]
                sweep_speed = 4 + energy * 8
                row = int(t_now * sweep_speed) % num_positions
                for pos in range(num_positions):
                    dist = min(abs(pos - row), num_positions - abs(pos - row))
                    if dist <= 1:
                        c = random.choice(ALL_VARIATIONS if energy > 0.6 else pal)
                        for vein in tree_rows:
                            if pos < len(vein): canvas.set_color(vein[pos], c)
                    elif random.random() < 0.08 + energy * 0.3:
                        c = random.choice(pal)
                        for vein in tree_rows:
                            if pos < len(vein): canvas.set_color(vein[pos], c)
        
        # ── 14–22s  peak: sine wave ripple row by row ─────────────────────
        elif t_now < 22.0:
            wave_offset += 0.15 + energy * 0.20
            if beat_now:
                last_beat = t_now
                pal_idx = [(p + 1) % 3 for p in pal_idx]
            
            for ti, tree_rows in enumerate(all_trees):
                num_leds = len(tree_rows[0]) if tree_rows else 1
                for vi, vein in enumerate(tree_rows):
                    for li, led in enumerate(vein):
                        row_phase = (li / num_leds) * 2 * math.pi
                        brightness = (math.sin(wave_offset + row_phase) + 1) / 2
                        if brightness > 0.55:
                            pal = ALL_VARIATIONS if energy > 0.6 else TREE_BAND_PALETTES[pal_idx[ti]]
                            c = random.choice(pal)
                        else:
                            c = TREE_BAND_PALETTES[pal_idx[ti]][0]
                        canvas.set_color(led, c)
        
        # ── 22–30s  outro: gentle fade ────────────────────────────────────
        else:
            fade_progress = (t_now - 22.0) / 8.0
            twinkle_prob = max(0.0, 0.12 - fade_progress * 0.11)
            fade_prob = fade_progress * 0.08
            for ti, tree_rows in enumerate(all_trees):
                for vein in tree_rows:
                    for led in vein:
                        if random.random() < twinkle_prob:
                            canvas.set_color(led, random.choice(TREE_BAND_PALETTES[ti]))
                        elif random.random() < fade_prob:
                            canvas.set_color(led, TRUNK_GREEN)
        
        draw_signature()
        
        canvas.update()
        frame_time = 0.06 - energy * 0.03
        time.sleep(max(0.03, frame_time))

# ── Screens ───────────────────────────────────────────────────────────────────
def show_welcome():
    canvas.clear()
    draw_ls_background()
    t1 = draw_ls_supertree(240,  CANVAS_HEIGHT, 0.95, TREE_COLOURS[0], TREE_BAND_PALETTES[0])
    t2 = draw_ls_supertree(600,  CANVAS_HEIGHT, 1.10, TREE_COLOURS[1], TREE_BAND_PALETTES[1])
    t3 = draw_ls_supertree(960,  CANVAS_HEIGHT, 0.95, TREE_COLOURS[2], TREE_BAND_PALETTES[2])
    draw_ls_stores()
    all_trees = [t1, t2, t3]

    for _ in range(5):
        for ti, tree_rows in enumerate(all_trees):
            for row_ids in tree_rows:
                for led in row_ids:
                    if random.random() > 0.6:
                        canvas.set_color(led, random.choice(TREE_BAND_PALETTES[ti]))
    sleep(0.12)

    ov_w, ov_h = 1000, 440
    oval((CANVAS_WIDTH - ov_w)//2, (CANVAS_HEIGHT - ov_h)//2,
         (CANVAS_WIDTH + ov_w)//2, (CANVAS_HEIGHT + ov_h)//2, BG_OVERLAY)
    sleep(0.1)

    logo_file = asset_path("superbev_logo.png")
    if os.path.exists(logo_file):
        canvas.create_image(int(625 - 150 - 495), int(200 - 40 - 150), logo_file)
    sleep(0.1)

    draw_text(CANVAS_WIDTH//2, 280, "Master Python basics!", 10, DARK_PURPLE)
    draw_text(CANVAS_WIDTH//2, 320, "Hit your sales targets to unlock the Supertree Light Show!", 10, DARK_PURPLE)
    sleep(0.3)

    btn_x, btn_y, btn_w, btn_h = 480, 380, 240, 90
    play_btn = draw_button(btn_x, btn_y, btn_w, btn_h, "PLAY")
    
    draw_signature()

    while True:
        for ti, tree_rows in enumerate(all_trees):
            for row_ids in tree_rows:
                if random.random() > 0.7:
                    canvas.set_color(random.choice(row_ids), random.choice(TREE_BAND_PALETTES[ti]))
        for click in canvas.get_new_mouse_clicks():
            if is_clicked(click, play_btn):
                play_click()
                return
        canvas.update()
        time.sleep(0.1)

def show_instructions():
    canvas.clear()
    rect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, BG)
    draw_text(CANVAS_WIDTH//2, 90,  "INSTRUCTIONS", 20, DARK_PURPLE)
    lines = [
        "You're in charge of selling SUPERtree BEVerages!",
        "Answer Python fundamentals questions correctly to sell drinks!",
        "Get all questions right and earn $45 or more to",
        "unlock the legendary Supertree Light Show!",
    ]
    for i, ln in enumerate(lines):
        draw_text(CANVAS_WIDTH//2, 180 + i * 70, ln, 12, DARK_PURPLE)
    sleep(1.2)
    btn_x, btn_y, btn_w, btn_h = 480, 450, 240, 90
    start_btn = draw_button(btn_x, btn_y, btn_w, btn_h, "START")
    
    draw_signature()
    
    while True:
        for click in canvas.get_new_mouse_clicks():
            if is_clicked(click, start_btn):
                play_click()
                return
        canvas.update()
        time.sleep(0.1)

def run_game():
    sales, total_earnings = 0, 0
    qs = random.sample([
        {"q": "What does 'len(list)' return?",        "a": "list length",   "b": "list string",  "correct": "a"},
        {"q": "Which is a valid list?",                "a": "(1, 2)",        "b": "[1, 2]",        "correct": "b"},
        {"q": "Result of '33' * 2?",                  "a": "'3333'",        "b": "66",            "correct": "a"},
        {"q": "Is 'A' == 'a' in Python?",             "a": "True",          "b": "False",         "correct": "b"},
        {"q": "Keyword for functions?",                "a": "def",           "b": "func",          "correct": "a"},
        {"q": "Is 7 // 2 a float?",                   "a": "Yes",           "b": "No (int)",      "correct": "b"},
        {"q": "Convert 10 to string?",                "a": "str(10)",       "b": "int(10)",       "correct": "a"},
        {"q": "for i in range(start, stop, ___)?",    "a": "step",          "b": "total",         "correct": "a"},
        {"q": "How to start a comment?",              "a": "#",             "b": "//",            "correct": "a"},
        {"q": "What's '8' == 8?",                     "a": "True",          "b": "False",         "correct": "b"},
        {"q": "Add element to end of list?",          "a": ".append()",     "b": ".add()",        "correct": "a"},
        {"q": "Is (1,) a tuple or an int?",           "a": "int",           "b": "tuple",         "correct": "b"},
        {"q": "Remainder of 10 % 3?",                 "a": "1",             "b": "3",             "correct": "a"},
        {"q": "Logical 'and' in Python?",             "a": "and",           "b": "&&",            "correct": "a"},
        {"q": "Result of 2 ** 3?",                    "a": "8",             "b": "6",             "correct": "a"},
        {"q": "Is fact = 'False' a string/boolean?",  "a": "string",        "b": "boolean",       "correct": "a"},
        {"q": "Loop through a fixed list?",           "a": "for",           "b": "while",         "correct": "a"},
        {"q": "Does input() return a str or int?",    "a": "string",        "b": "integer",       "correct": "a"},
        {"q": "Remove item from list?",               "a": ".pop()",        "b": ".delete()",     "correct": "a"},
        {"q": "Check if 5 is NOT 3?",                 "a": "5 != 3",        "b": "5 /= 3",        "correct": "a"},
        {"q": "Print 'hi' 3 times shortcut?",         "a": "print('hi'*3)", "b": "print('hi'+3)", "correct": "a"},
        {"q": "Type of None?",                        "a": "NoneType",      "b": "null",          "correct": "a"},
        {"q": "Access first item in list x?",         "a": "x[0]",          "b": "x[1]",          "correct": "a"},
        {"q": "Is 0 truthy or falsy?",                "a": "truthy",        "b": "falsy",         "correct": "b"},
        {"q": "Keyword to exit a loop early?",        "a": "break",         "b": "exit",          "correct": "a"},
        {"q": "Skip to next iteration?",              "a": "continue",      "b": "skip",          "correct": "a"},
        {"q": "What does 'not True' return?",         "a": "False",         "b": "None",          "correct": "a"},
        {"q": "Index of last item in [1,2,3]?",       "a": "2",             "b": "3",             "correct": "a"},
        {"q": "Is [] truthy or falsy?",               "a": "truthy",        "b": "falsy",         "correct": "b"},
        {"q": "Keyword to return a value?",           "a": "return",        "b": "give",          "correct": "a"},
        {"q": "Type of 3.14?",                        "a": "float",         "b": "int",           "correct": "a"},
        {"q": "Which opens a file safely?",           "a": "with open()",   "b": "file.open()",   "correct": "a"},
        {"q": "Unpack a,b = ?",                       "a": "[1, 2]",        "b": "1, 2, 3",       "correct": "a"},
        {"q": "Sort list x in place?",                "a": "x.sort()",      "b": "sort(x)",       "correct": "a"},
        {"q": "Check key in dict?",                   "a": "'k' in d",      "b": "d.has('k')",    "correct": "a"},
        {"q": "Empty dict literal?",                  "a": "{}",            "b": "[]",            "correct": "a"},
        {"q": "Concatenate two lists?",               "a": "a + b",         "b": "a & b",         "correct": "a"},
        {"q": "Get dict value safely?",               "a": "d.get('k')",    "b": "d['k']",        "correct": "a"},
        {"q": "range(5) includes 5?",                 "a": "True",          "b": "False",         "correct": "b"},
        {"q": "Make all chars lowercase?",            "a": ".lower()",      "b": ".down()",       "correct": "a"},
    ], 5)

    for i in range(5):
        canvas.clear()
        rect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, BG)
        rect(0, 480, CANVAS_WIDTH, CANVAS_HEIGHT, TABLE_BROWN)

        draw_text(1090, 40,  "GARDENS BY THE BAE", 8)
        draw_text(1112, 70,  "POP-UP STORE", 8)
        draw_text(500,  510, "MILO DINOSAUR", 8)
        draw_text(700,  510, "BANDUNG", 8)
        draw_text(900,  510, "SUGARCANE", 8)

        draw_register(80, 380)
        draw_price_sign(80, 120)
        draw_beverage(500, 470, "MILO DINOSAUR")
        draw_beverage(700, 470, "BANDUNG")
        draw_beverage(900, 470, "SUGARCANE")
        draw_placard(1040, 400)

        item  = random.choice(["MILO DINOSAUR", "BANDUNG", "SUGARCANE"])
        price = {"MILO DINOSAUR": 8, "BANDUNG": 10, "SUGARCANE": 11}[item]
        q = qs[i]

        draw_text(CANVAS_WIDTH//2, 36,  f"Customer {i+1} wants a {item}", 12)
        draw_text(CANVAS_WIDTH//2, 84,  q["q"], 13)

        bw, bh = 270, 80
        ax, ay = 320, 170
        bx, by = 630, 170
        btn_a = draw_button(ax, ay, bw, bh, "A: " + q["a"])
        btn_b = draw_button(bx, by, bw, bh, "B: " + q["b"])

        chosen = None
        canvas.get_new_mouse_clicks()

        while chosen is None:
            for click in canvas.get_new_mouse_clicks():
                if is_clicked(click, btn_a):
                    play_click()
                    chosen = "a"; break
                elif is_clicked(click, btn_b):
                    play_click()
                    chosen = "b"; break
                    
            draw_signature()
            
            canvas.update()
            time.sleep(0.02)

        if chosen == q["correct"]:
            sales += 1
            total_earnings += price
            draw_text(CANVAS_WIDTH//2, 290, f"SOLD! {item} for ${price}", 14, SUCCESS_GREEN)
        else:
            draw_text(CANVAS_WIDTH//2, 290, "Incorrect!", 15, FAIL_RED)
        sleep(0.8)

    return sales, total_earnings

def show_end_screen(sales, earnings):
    canvas.clear()
    rect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, BG)
    success = (sales == 5 and earnings >= 45)

    if success:
        draw_text(CANVAS_WIDTH//2, 160, "MISSION SUCCESS!", 22, SUCCESS_GREEN)
        draw_text(CANVAS_WIDTH//2, 240, f"Total Earnings: ${earnings}", 15)
        draw_text(CANVAS_WIDTH//2, 300, "The light show is starting soon!", 14)
        sleep(2.0)

        # BGM stops automatically when lightshow music loads
        run_light_show()

        # After lightshow ends: resume BGM for the congrats screen
        play_bgm()

        canvas.clear()
        rect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, BG)
        draw_text(CANVAS_WIDTH//2, 200, "Congrats! You won the game!", 22, DARK_PURPLE)
        btn_x, btn_y, btn_w, btn_h = 470, 360, 260, 90
        restart_btn = draw_button(btn_x, btn_y, btn_w, btn_h, "RESTART")
        
        draw_signature()
        
        while True:
            for click in canvas.get_new_mouse_clicks():
                if is_clicked(click, restart_btn):
                    play_click()
                    return True
            canvas.update()
            time.sleep(0.1)
    else:
        draw_text(CANVAS_WIDTH//2, 160, "MISSION FAILED", 22, FAIL_RED)
        draw_text(CANVAS_WIDTH//2, 240, f"Sales: {sales}/5  |  Earnings: ${earnings}", 15)
        btn_x, btn_y, btn_w, btn_h = 470, 400, 260, 90
        retry_btn = draw_button(btn_x, btn_y, btn_w, btn_h, "TRY AGAIN")
        
        draw_signature()
        
        while True:
            for click in canvas.get_new_mouse_clicks():
                if is_clicked(click, retry_btn):
                    play_click()
                    return False
            canvas.update()
            time.sleep(0.1)

def main():
    # Initialise audio once at startup, then start BGM immediately
    init_audio()
    play_bgm()

    while True:
        show_welcome()
        while True:
            show_instructions()
            s, e = run_game()
            if show_end_screen(s, e):
                break
        # Back at welcome screen: BGM is already looping (restarted after congrats)

if __name__ == "__main__":
    main()
