"""Ve Hinh 1.1 (quy trinh giai trinh + diem dut gay kiem chung) ra PNG cho ban Word.

Chay:  python app/tools/gen_hinh_1_1.py
Output: thesis/figures/hinh_1_1.png (2x scale cho net khi in)
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "thesis" / "figures" / "hinh_1_1.png"

# Palette theo design.md
NAVY = (8, 26, 54)
GRAY7 = (75, 75, 75)
GRAY4 = (174, 180, 194)
RED = (236, 93, 105)
RED1 = (253, 236, 238)
WHITE = (255, 255, 255)

S = 2  # scale 2x
W, H = 1180 * S, 330 * S
img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)

FONT_DIR = Path("C:/Windows/Fonts")
f_body = ImageFont.truetype(str(FONT_DIR / "times.ttf"), 15 * S)
f_bold = ImageFont.truetype(str(FONT_DIR / "timesbd.ttf"), 15 * S)
f_small = ImageFont.truetype(str(FONT_DIR / "times.ttf"), 13 * S)


def box(x, y, w, h, lines, fill, color, font, border):
    d.rounded_rectangle([x, y, x + w, y + h], radius=6 * S, fill=fill, outline=border, width=2 * S)
    total = sum(font.getbbox(t)[3] - font.getbbox(t)[1] + 4 * S for t in lines) - 4 * S
    cy = y + (h - total) / 2
    for t in lines:
        bb = font.getbbox(t)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        d.text((x + (w - tw) / 2, cy), t, fill=color, font=font)
        cy += th + 4 * S


def arrow(x1, y, x2):
    d.line([x1, y, x2 - 8 * S, y], fill=GRAY7, width=2 * S)
    d.polygon([(x2, y), (x2 - 10 * S, y - 5 * S), (x2 - 10 * S, y + 5 * S)], fill=GRAY7)


BY, BH, BW_, GAP = 200 * S, 86 * S, 196 * S, 40 * S
steps = [
    (["Chốt sổ", "kế toán"], False),
    (["Dữ liệu tháng", "(sổ cái, ngân sách,", "rent roll)"], False),
    (["Công đoạn AI", "soạn giải trình", "≈ 1 giờ"], True),
    (["Giải trình", "chênh lệch"], False),
    (["Báo cáo", "quản trị"], False),
]
x = 20 * S
centers = []
for lines, dark in steps:
    box(x, BY, BW_, BH, lines,
        NAVY if dark else WHITE, WHITE if dark else GRAY7,
        f_bold if dark else f_body, NAVY if dark else GRAY4)
    centers.append(x + BW_ / 2)
    x += BW_ + GAP
for i in range(4):
    arrow(centers[i] + BW_ / 2, BY + BH / 2, centers[i + 1] - BW_ / 2)

# Callout diem dut gay (tren hop AI)
cw, ch = 430 * S, 108 * S
cx = centers[2] - cw / 2
cy0 = 36 * S
d.rounded_rectangle([cx, cy0, cx + cw, cy0 + ch], radius=6 * S, fill=RED1, outline=RED, width=2 * S)
call = [
    ("ĐIỂM ĐỨT GÃY KIỂM CHỨNG", f_bold, RED),
    ("Số lấy từ nguồn nào? Nhận định dựa trên căn cứ nào?", f_small, GRAY7),
    ("Dấu vết kiểm toán dừng tại đây", f_small, GRAY7),
]
yy = cy0 + 12 * S
for t, f, c in call:
    bb = f.getbbox(t)
    d.text((cx + (cw - (bb[2] - bb[0])) / 2, yy), t, fill=c, font=f)
    yy += (bb[3] - bb[1]) + 8 * S
# duong dut noi callout -> hop AI
mx = centers[2]
yline = cy0 + ch
while yline < BY - 10 * S:
    d.line([mx, yline, mx, min(yline + 6 * S, BY - 10 * S)], fill=RED, width=2 * S)
    yline += 12 * S
d.polygon([(mx, BY - 2 * S), (mx - 6 * S, BY - 12 * S), (mx + 6 * S, BY - 12 * S)], fill=RED)

OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT)
print("Saved", OUT, img.size)
