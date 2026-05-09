"""OG画像（1200x630）を作成。Twitter/Facebookシェア時に表示される。"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
NAVY = (30, 58, 95)
NAVY_DARK = (20, 41, 67)
ORANGE = (245, 166, 35)
WHITE = (255, 255, 255)
SUB = (180, 195, 215)

img = Image.new("RGB", (W, H), NAVY)
draw = ImageDraw.Draw(img)

# 背景グラデーション（簡易：上から下へnavy→navy_dark）
for y in range(H):
    t = y / H
    r = int(NAVY[0] * (1 - t) + NAVY_DARK[0] * t)
    g = int(NAVY[1] * (1 - t) + NAVY_DARK[1] * t)
    b = int(NAVY[2] * (1 - t) + NAVY_DARK[2] * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# フォント
def find_font(size):
    candidates = [
        "/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc",
        "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
        "/Library/Fonts/tokoshieIPAGothic.ttf",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
    ]
    for c in candidates:
        try:
            return ImageFont.truetype(c, size)
        except Exception:
            continue
    return ImageFont.load_default()

f_brand = find_font(36)
f_title = find_font(72)
f_sub = find_font(32)
f_meta = find_font(26)

# 左側エリア（テキスト）
LEFT_X = 60
# ロゴマーク（オレンジH）
draw.rectangle([(LEFT_X, 70), (LEFT_X + 56, 126)], fill=NAVY_DARK, outline=ORANGE, width=3)
draw.text((LEFT_X + 14, 70), "H", fill=ORANGE, font=f_brand)
draw.text((LEFT_X + 80, 80), "Hitorinku", fill=WHITE, font=f_brand)

# タイトル
draw.text((LEFT_X, 200), "現場の数字、", fill=WHITE, font=f_title)
draw.text((LEFT_X, 290), "見える化。", fill=ORANGE, font=f_title)

# サブ
draw.text((LEFT_X, 410), "工務店向け 出勤・人工管理アプリ", fill=SUB, font=f_sub)
draw.text((LEFT_X, 460), "月¥1,500 / 社員5名まで無料", fill=WHITE, font=f_sub)

# メタ
draw.text((LEFT_X, 540), "App Storeで入手  •  iPhone・iPad対応", fill=SUB, font=f_meta)

# 右側にスクショ重ね
try:
    shot = Image.open("/Users/sherlockholmes/hitorinku-lp/screenshots/hitorinku_01_matrix.png")
    # 縦長なのでHに合わせてリサイズ
    target_h = 540
    aspect = shot.width / shot.height
    target_w = int(target_h * aspect)
    shot_resized = shot.resize((target_w, target_h), Image.LANCZOS)
    # 角丸マスク
    mask = Image.new("L", (target_w, target_h), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([(0, 0), (target_w, target_h)], radius=40, fill=255)
    img.paste(shot_resized, (W - target_w - 60, 45), mask)
except Exception as e:
    print("Screenshot composite failed:", e)

img.save("/Users/sherlockholmes/hitorinku-lp/og.png", "PNG", optimize=True)
print(f"OG image saved: {W}x{H}")
