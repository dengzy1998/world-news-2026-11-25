#!/usr/bin/env python3
"""Render the 25 November 2026 world-news poster (1024x1024 PNG).

52 stories from the sourced ledger stories.md: 3 illustrated leads, 12 grid
cards, 37 one-liners, a UTC timeline strip, a numbered schematic map, and a
DATE CHECK box listing older stories deliberately left out. Deterministic:
no network, no clock, no randomness. Renders entry.png beside this file.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (25, 25, 25)
MUTED = (90, 86, 76)
RED = (166, 30, 30)
BLUE = (30, 78, 138)
NAVY = (16, 42, 84)
TEAL = (15, 107, 92)
GOLD = (154, 106, 0)
LINE = (201, 194, 176)
CARD = (255, 255, 255)
MAPFILL = (216, 210, 192)
MAPLINE = (138, 132, 113)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


F_TITLE = font("DejaVuSans-Bold.ttf", 46)
F_DATE = font("DejaVuSans-Bold.ttf", 19)
F_SUB = font("DejaVuSans-Bold.ttf", 13)
F_SECTION = font("DejaVuSans-Bold.ttf", 12)
F_TAG = font("DejaVuSans-Bold.ttf", 11)
F_LEAD_HEAD = font("DejaVuSans-Bold.ttf", 16)
F_LEAD_SUM = font("DejaVuSans.ttf", 12)
F_GRID_HEAD = font("DejaVuSans-Bold.ttf", 12)
F_GRID_SUM = font("DejaVuSans.ttf", 11)
F_ONE = font("DejaVuSans.ttf", 10)
F_SMALL = font("DejaVuSans.ttf", 10)
F_SMALL_B = font("DejaVuSans-Bold.ttf", 10)
F_TINY = font("DejaVuSans.ttf", 9)
F_MAP_NUM = font("DejaVuSans-Bold.ttf", 10)

# --- story data: (number, region, headline, summary, source, accent) ---
LEADS = [
    (1, "WAR · MIDDLE EAST", "Houthis hit Riyadh's tallest tower again",
     "Second Houthi strike on the Riyadh financial-district landmark in under a week; 11 hurt.",
     "South China Morning Post", RED),
    (2, "US POLITICS", "Democrats clinch House majority of 259 seats",
     "Largest Democratic House majority since 1990, after a Tennessee race was called.",
     "Associated Press", BLUE),
    (3, "WAR · EUROPE", "Overnight strikes kill 3, injure 15",
     "Russia and Ukraine report deaths and injuries in strikes on Kyiv, Kharkiv and Samara.",
     "Yeni Safak", INK),
]

GRID = [
    (4, "WAR · GULF", "Iran says two tankers hit mines in Hormuz",
     "IRGC Navy: two tankers struck mines and caught fire in Hormuz.",
     "Reuters", RED),
    (5, "TECH · US", "Nvidia slides 7% as lawmakers question Trump",
     "Rally fades after Huang's return; Huang tells staff he is in therapy.",
     "SCMP / AP", RED),
    (6, "US POLITICS", "Trump awards Giuliani the Medal of Freedom",
     "Former New York mayor receives the highest US civilian honour.",
     "AP / SCMP", BLUE),
    (7, "MIGRATION", "Abrego Garcia leaves US voluntarily for Spain",
     "At the centre of the mistaken-deportation fight; leaves for Spain.",
     "AP", BLUE),
    (8, "TRADE · US", "US ready to slap tariffs on China, EU, 14 others",
     "Administration prepares tariffs over subsidised production, AP sources say.",
     "AP", GOLD),
    (9, "WAR · GAZA", "Israeli strike kills Hamas security chief",
     "Security chief, his wife and teenage daughters killed in Gaza City.",
     "SCMP", RED),
    (10, "EUROPE", "Merz: Europe will show Russia its limits",
     "German chancellor defends a sharp rise in defence spending.",
     "Yeni Safak", BLUE),
    (11, "MARKETS", "Nikkei -2.76% as Asian tech sells off",
     "AI-boom doubts hit tech stocks; S&P 500 -0.5%; Brent $87.49.",
     "OneTurn", TEAL),
    (12, "CRIME", "Colombia supermarket hostages freed",
     "Police storm a Cartagena supermarket; one captor killed, all hostages rescued.",
     "SCMP / AP", GOLD),
    (13, "UK · EUROPE", "Met Police still institutionally racist",
     "Britain's biggest police force has not reformed, a report finds.",
     "SCMP", INK),
    (14, "WORLD", "Landmine toll hits 5-year high: ~7,000",
     "Nearly 7,000 killed or injured in 2025; Myanmar and Syria top the list.",
     "Yeni Safak", TEAL),
    (15, "SPORT", "Senegal reinstated as AFCON champions",
     "CAS overturns CAF's award of the title to Morocco; Senegal's 1-0 win stands.",
     "MyKhel", GOLD),
]

# one-liners: (number, region, text) — kept short to fit two lines per column
ONELINERS = [
    (16, "US", "US soldier Jian Zhao admits selling military info to Chinese buyers."),
    (17, "US", "Thomas Markle indicted on child sex abuse material charges."),
    (18, "US", "Fort Hood shooter Hasan asks court to delay execution."),
    (19, "US", "Army to detonate 5-ton lead azide stockpile in Iowa."),
    (20, "US", "Trump pardons Thanksgiving turkeys Freedom and Feathers."),
    (21, "US", "Macy's Thanksgiving Day Parade marks 100th anniversary."),
    (22, "US", "Trump to meet Sen.-elect El-Sayed on universal healthcare."),
    (23, "US", "House Democrat widens probe into Trump Jr.'s investment firm."),
    (24, "US", "Appeals court gives Trump path to erase hush-money conviction."),
    (25, "US", "US loses measles-free status as cases hit decades high."),
    (26, "US", "Martha Ford, ex-Lions owner, dies at 101."),
    (27, "US", "Shein to pay $100M to settle FTC deceptive-practices claims."),
    (28, "US", "Facebook, YouTube not liable for 2022 Buffalo shooting."),
    (29, "US", "DEA let 1.4M fentanyl pills go unseized, AP finds."),
    (30, "US", "Plane crash off Mississippi coast kills 6, incl. 2 children."),
    (31, "ME", "Saudi defences intercept 4 drones over Eastern Province."),
    (32, "ME", "Gaza storm threatens 1.76M Palestinians living in tents."),
    (33, "ME", "Israeli strike kills 4 of a family in Gaza's al-Shati camp."),
    (34, "ME", "US debates targeting top Iranian leaders to end war."),
    (35, "ME", "New Israeli gates could cut off 70,000 in West Bank."),
    (36, "EU", "Ukraine and Hungary agree to deepen energy cooperation."),
    (37, "EU", "Spain heads to a snap election."),
    (38, "EU", "Gisele Pelicot blasts publisher over nude photos in promo."),
    (39, "EU", "UK's Burnham vows to end NDAs shielding abusers."),
    (40, "EU", "Russian oligarch testifies in huge UK divorce wealth fight."),
    (41, "AS", "China investigates Shanghai party chief Chen Jining."),
    (42, "AS", "Iran flogs singer 74 times over unveiled concert."),
    (43, "AS", "DR Congo military aircraft missing; rebels claim downing."),
    (44, "AS", "Rescuers search for dozens trapped in Indonesian mine."),
    (45, "AS", "Hong Kong marks a year since the Tai Po fire."),
    (46, "AS", "Gukesh draws opener vs Sindarov in chess title defence."),
    (47, "AS", "Vaibhav, 15, hits fastest List A double ton: 204 off 53."),
    (48, "AS", "Ben Stokes enters IPL 2027 auction at Rs 2 crore base."),
    (49, "AS", "East Bengal beat Al Hussein 1-0 for first ACL Two win."),
    (50, "AF", "Zambia indicts opposition leader on treason charges."),
    (51, "AF", "Drone attacks on Khartoum draw condemnation."),
    (52, "WORLD", "Oil down over 20% in November; Brent $87.49."),
]

# timeline: (hour_utc, label)
TIMELINE = [
    (0.75, "Hormuz mines"), (2.5, "Strikes kill 3"), (4.0, "Riyadh tower hit"),
    (6.5, "Nvidia -7%"), (8.0, "Democrats 259"),
    (10.0, "Giuliani honour"), (12.0, "Tariff plan"),
    (14.0, "Abrego leaves"), (16.0, "Cartagena freed"),
    (18.0, "Gaza chief killed"), (20.0, "Landmine toll"),
]

DATE_CHECK = [
    "Shenzhou 24 launches with Pakistani astronaut — 24 Nov (AP).",
    "Huawei found guilty of trade-secret theft — 24 Nov (AP).",
    "Solomon Islands names Australia top partner — 24 Nov (AP).",
    "CIA system breach first reported — 24 Nov (AP).",
    "Rep. Gomez resigns after ethics findings — 23 Nov (AP).",
]

# map dots: (story number, lon, lat, badge_dx, badge_dy)
DOTS = [(1, 46.7, 24.6, 0, -14), (2, -77, 39, -16, 12), (3, 30.5, 50.5, 0, -15),
        (4, 56.5, 26.5, 12, -12), (5, -122, 37.4, 0, 0), (6, -74, 40.7, 14, -10),
        (7, -76.7, 39, -20, -8), (8, -77, 38.9, 10, 14), (9, 34.5, 31.5, 16, 8),
        (10, 13.4, 52.5, 0, 0), (11, 139.7, 35.7, 0, 0), (12, -75.5, 10.4, 0, 0),
        (13, -0.1, 51.5, 0, -14), (14, 96, 21, 0, 0), (15, -17.4, 14.7, 0, 0)]

CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
     (-75, 62), (-60, 47), (-70, 42), (-80, 32), (-85, 25), (-97, 26),
     (-105, 20), (-110, 23), (-125, 40), (-145, 60), (-165, 60)],
    [(-80, 10), (-70, 11), (-60, 5), (-50, 0), (-40, -5), (-35, -10),
     (-40, -20), (-48, -28), (-58, -35), (-65, -40), (-70, -50), (-73, -35),
     (-75, -20), (-80, -5)],
    [(-10, 36), (-5, 43), (0, 50), (5, 58), (10, 57), (18, 56), (23, 60),
     (30, 70), (35, 68), (40, 60), (30, 50), (28, 45), (20, 40), (12, 44),
     (3, 42), (-2, 37), (-9, 38)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (40, 15), (48, 11), (51, 2), (40, -5), (35, -15), (30, -25), (20, -35),
     (15, -30), (12, -18), (9, -1), (8, 4), (-8, 5), (-15, 11)],
    [(40, 70), (50, 72), (60, 70), (70, 72), (80, 73), (90, 75), (110, 76),
     (130, 72), (150, 70), (170, 66), (178, 65), (170, 60), (160, 55),
     (155, 50), (145, 45), (140, 40), (135, 35), (130, 33), (127, 35),
     (122, 38), (120, 30), (110, 20), (108, 12), (105, 8), (100, 6),
     (97, 10), (95, 16), (90, 22), (85, 20), (80, 13), (77, 8), (72, 20),
     (66, 25), (60, 25), (55, 26), (50, 29), (48, 30), (44, 29), (40, 32),
     (38, 36), (35, 36), (30, 36), (27, 37), (23, 36), (26, 40), (28, 45),
     (30, 50), (32, 55), (35, 60), (38, 65)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32), (137, -35),
     (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (150, -22),
     (146, -19), (142, -11), (137, -12), (132, -12), (126, -14), (122, -17),
     (118, -20)],
]


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to a pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None):
    lh = leading if leading is not None else int(fnt.size * 1.25)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def draw_lead_art(draw, box, kind, accent):
    """Small programmatic illustration for a lead card."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=accent)
    if kind == "tower":
        # Riyadh financial-district tower: dark glass slab with lit windows,
        # orange burst at the crown, smoke curling up.
        cx = (x0 + x1) // 2
        base = y1 - 12
        draw.rectangle([cx - 26, y0 + 22, cx + 26, base], fill=(40, 44, 58),
                       outline=(255, 255, 255), width=1)
        for wy in range(y0 + 28, base - 4, 10):
            for wx in (cx - 18, cx - 6, cx + 6, cx + 14):
                draw.rectangle([wx, wy, wx + 4, wy + 4], fill=(255, 200, 90))
        # crown burst
        bx, by = cx, y0 + 18
        for k in range(8):
            ang = k * 45 + 15
            r = 16
            ex = bx + int(r * math.cos(math.radians(ang)))
            ey = by + int(r * math.sin(math.radians(ang)))
            draw.line([bx, by, ex, ey], fill=(255, 190, 80), width=3)
        draw.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=(255, 210, 110),
                     outline=(255, 255, 255), width=1)
        draw.text((x0 + 10, y0 + 6), "RIYADH", font=F_TAG, fill=(255, 255, 255))
        lab = "11 HURT"
        tw = draw.textlength(lab, font=F_TAG)
        draw.text((x1 - 8 - tw, y1 - 20), lab, font=F_TAG, fill=(255, 255, 255))
    elif kind == "dome":
        # US Capitol: white dome + columns, outlined in dark navy so it reads
        # as a building against the blue field.
        cx = (x0 + x1) // 2
        base = y1 - 14
        draw.ellipse([cx - 30, base - 34, cx + 30, base + 2], fill=(255, 255, 255),
                     outline=NAVY, width=2)
        draw.rectangle([cx - 34, base - 6, cx + 34, base], fill=(255, 255, 255),
                       outline=NAVY, width=2)
        draw.rectangle([cx - 5, base - 44, cx + 5, base - 34], fill=(255, 255, 255),
                       outline=NAVY, width=1)
        draw.line([cx, base - 56, cx, base - 44], fill=(255, 255, 255), width=2)
        draw.polygon([(cx, base - 56), (cx + 12, base - 53), (cx, base - 50)],
                     fill=(255, 255, 255), outline=NAVY)
        draw.rectangle([cx - 44, base - 2, cx + 44, base + 10], fill=(255, 255, 255),
                       outline=NAVY, width=2)
        for i in range(6):
            px = cx - 38 + i * 14
            draw.rectangle([px, base - 2, px + 5, base + 10], fill=NAVY)
        draw.rectangle([cx - 48, base + 10, cx + 48, base + 14], fill=(255, 255, 255),
                       outline=NAVY, width=1)
        draw.text((x0 + 10, y0 + 6), "259 SEATS", font=F_TAG, fill=(255, 255, 255))
        lab = "SINCE 1990"
        tw = draw.textlength(lab, font=F_TAG)
        draw.text((x1 - 8 - tw, y1 - 20), lab, font=F_TAG, fill=(255, 255, 255))
    else:  # "blast": orange burst over a Kyiv skyline with lit windows
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 6
        for k in range(8):
            ang = k * 45 + 10
            r = 40
            ex = cx + int(r * math.cos(math.radians(ang)))
            ey = cy + int(r * math.sin(math.radians(ang)))
            draw.line([cx, cy, ex, ey], fill=(255, 190, 80), width=3)
        draw.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(255, 210, 110),
                     outline=(255, 255, 255), width=2)
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255))
        towers = [(x0 + 14, 22), (x0 + 46, 34), (x0 + 82, 26), (x0 + 116, 40),
                  (x0 + 152, 30), (x0 + 188, 38), (x0 + 224, 24), (x0 + 258, 32)]
        for bx, bh in towers:
            draw.rectangle([bx, y1 - 12 - bh, bx + 24, y1 - 12], fill=(70, 70, 82),
                           outline=(25, 25, 25), width=1)
            for wy in range(y1 - 12 - bh + 5, y1 - 14, 9):
                for wx in (bx + 5, bx + 14):
                    draw.rectangle([wx, wy, wx + 3, wy + 3], fill=(255, 200, 90))
        draw.line([x0, y1 - 12, x1, y1 - 12], fill=(25, 25, 25), width=2)
        draw.text((x0 + 10, y0 + 6), "KYIV", font=F_TAG, fill=(255, 255, 255))
        dead = "3 DEAD"
        tw = draw.textlength(dead, font=F_TAG)
        draw.text((x1 - 8 - tw, y1 - 20), dead, font=F_TAG, fill=(255, 255, 255))


def draw_map(draw, x0, y0, x1, y1):
    def px(lon, lat):
        fx = (lon + 170.0) / 360.0
        fy = (85.0 - lat) / 145.0
        return (x0 + int(fx * (x1 - x0)), y0 + int(fy * (y1 - y0)))

    for poly in CONTINENTS:
        pts = [px(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=MAPFILL, outline=MAPLINE)
    for num, lon, lat, dx, dy in DOTS:
        cx, cy = px(lon, lat)
        bx, by = cx + dx, cy + dy
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
        if dx or dy:
            draw.line([cx, cy, bx, by], fill=RED, width=1)
        draw.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=RED,
                     outline=(255, 255, 255), width=1)
        label = str(num)
        tw = draw.textlength(label, font=F_MAP_NUM)
        draw.text((bx - tw / 2, by - 7), label, font=F_MAP_NUM, fill=(255, 255, 255))
    draw.text((x0, y1 - 12), "SCHEMATIC — NOT TO SCALE", font=F_TINY, fill=MUTED)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 6], fill=RED)
    d.text((16, 14), "THE WORLD TODAY", font=F_TITLE, fill=INK)
    date_lines = ["WEDNESDAY", "25 NOVEMBER 2026"]
    dx = W - 16
    for i, line in enumerate(date_lines):
        tw = d.textlength(line, font=F_DATE)
        d.text((dx - tw, 16 + i * 24), line, font=F_DATE, fill=RED if i == 0 else INK)
    d.text((16, 66), "52 STORIES  ·  6 REGIONS  ·  ONE PAGE  —  WEDNESDAY 25 NOVEMBER 2026",
           font=F_SUB, fill=MUTED)
    d.line([16, 88, W - 16, 88], fill=INK, width=2)

    # ---- lead cards ----
    kinds = ["tower", "dome", "blast"]
    lead_y, lead_h, lead_w, gap = 96, 184, 322, 8
    for i, (num, region, head, summ, src, accent) in enumerate(LEADS):
        x0 = 16 + i * (lead_w + gap)
        x1 = x0 + lead_w
        d.rectangle([x0, lead_y, x1, lead_y + lead_h], fill=CARD, outline=LINE, width=1)
        draw_lead_art(d, (x0 + 1, lead_y + 1, x1 - 1, lead_y + 80), kinds[i], accent)
        y = lead_y + 86
        d.text((x0 + 10, y), f"{num} · {region}", font=F_TAG, fill=accent)
        y += 16
        lines = wrap(d, head, F_LEAD_HEAD, lead_w - 20)
        y = text_block(d, x0 + 10, y, lines[:2], F_LEAD_HEAD, leading=19)
        y += 3
        lines = wrap(d, summ, F_LEAD_SUM, lead_w - 20)
        y = text_block(d, x0 + 10, y, lines[:2], F_LEAD_SUM, leading=15)
        d.text((x0 + 10, y + 2), "Source: " + src, font=F_TINY, fill=MUTED)

    # ---- grid cards (3 rows x 4) ----
    grid_y, grid_h, grid_w = 288, 96, 242
    for row in range(3):
        for col in range(4):
            item = GRID[row * 4 + col]
            num, region, head, summ, src, accent = item
            x0 = 16 + col * (grid_w + gap)
            x1 = x0 + grid_w
            y0 = grid_y + row * (grid_h + 6)
            d.rectangle([x0, y0, x1, y0 + grid_h], fill=CARD, outline=LINE, width=1)
            d.ellipse([x0 + 8, y0 + 7, x0 + 26, y0 + 25], fill=accent)
            label = str(num)
            tw = d.textlength(label, font=F_SMALL_B)
            d.text((x0 + 17 - tw / 2, y0 + 10), label, font=F_SMALL_B, fill=(255, 255, 255))
            d.text((x0 + 32, y0 + 9), region, font=F_TAG, fill=accent)
            lines = wrap(d, head, F_GRID_HEAD, grid_w - 16)
            y = text_block(d, x0 + 8, y0 + 28, lines[:2], F_GRID_HEAD, leading=13)
            lines = wrap(d, summ, F_GRID_SUM, grid_w - 16)
            text_block(d, x0 + 8, y + 2, lines[:2], F_GRID_SUM, leading=12)

    # ---- timeline strip ----
    tl_y0, tl_y1 = 596, 656
    d.rectangle([16, tl_y0, W - 16, tl_y1], fill=(255, 255, 255), outline=LINE, width=1)
    base = tl_y0 + 32
    d.line([24, base, W - 24, base], fill=INK, width=1)
    for h in range(0, 25, 4):
        x = 24 + int(h / 24.0 * (W - 48))
        d.line([x, base - 3, x, base + 3], fill=INK, width=1)
        lab = f"{h:02d}:00" + (" UTC" if h == 24 else "")
        tw = d.textlength(lab, font=F_TINY)
        lx = min(max(x - tw / 2, 24), W - 24 - tw)
        d.text((lx, base + 6), lab, font=F_TINY, fill=MUTED)
    rows = {"near": base - 13, "below": base + 18, "far": base - 25}
    order = ["near", "below", "far"]
    for i, (hour, lab) in enumerate(TIMELINE):
        x = 24 + int(hour / 24.0 * (W - 48))
        d.ellipse([x - 3, base - 3, x + 3, base + 3], fill=RED)
        tw = d.textlength(lab, font=F_TINY)
        lx = min(max(x - tw / 2, 24), W - 24 - tw)
        d.text((lx, rows[order[i % 3]]), lab, font=F_TINY, fill=INK)

    # ---- one-liners (3 columns) ----
    ol_y0 = 664
    d.text((16, ol_y0), "THE REST OF THE DAY — 37 MORE STORIES", font=F_SECTION, fill=INK)
    d.line([16, ol_y0 + 17, 690, ol_y0 + 17], fill=INK, width=1)
    col_w, col_gap = 219, 7
    cols = [ONELINERS[0:13], ONELINERS[13:25], ONELINERS[25:37]]
    for ci, col in enumerate(cols):
        cx = 16 + ci * (col_w + col_gap)
        y = ol_y0 + 24
        for num, region, text in col:
            first = f"{num}. [{region}] " + text
            lines = wrap(d, first, F_ONE, col_w)
            y = text_block(d, cx, y, lines[:2], F_ONE, leading=11)
            y += 2

    # ---- map ----
    map_x0, map_y0, map_x1, map_y1 = 698, 664, 1008, 836
    d.text((map_x0, map_y0), "WHERE IT HAPPENED — STORIES 1–15", font=F_SECTION, fill=INK)
    d.rectangle([map_x0, map_y0 + 20, map_x1, map_y1], fill=(255, 255, 255), outline=LINE, width=1)
    draw_map(d, map_x0 + 4, map_y0 + 24, map_x1 - 4, map_y1 - 4)

    # ---- date check ----
    dc_y0 = 846
    d.text((map_x0, dc_y0), "DATE CHECK — OLDER STORIES WE LEFT OUT", font=F_SECTION, fill=RED)
    d.line([map_x0, dc_y0 + 17, map_x1, dc_y0 + 17], fill=RED, width=1)
    y = dc_y0 + 24
    for item in DATE_CHECK:
        lines = wrap(d, "· " + item, F_SMALL, map_x1 - map_x0)
        y = text_block(d, map_x0, y, lines, F_SMALL, leading=12)
        y += 3
    y += 4
    lines = wrap(d, "Everything above happened, or was first reported, on 25 November 2026.",
                 F_SMALL, map_x1 - map_x0)
    text_block(d, map_x0, y, lines, F_SMALL, leading=12)

    # ---- footer ----
    d.line([16, 1008, W - 16, 1008], fill=LINE, width=1)
    d.text((16, 1012),
           "CLAIM = an unverified claim, attributed to its source.  Sources: AP · Reuters · "
           "SCMP · Yeni Safak · OneTurn · MyKhel · Arab News · ProCappers.",
           font=F_TINY, fill=MUTED)
    return img


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    render().save(out, "PNG", optimize=True)
    print("wrote", out)
