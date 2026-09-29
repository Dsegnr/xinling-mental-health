# -*- coding: utf-8 -*-
"""生成『心聆』项目 LOGO（主图 + 透明底版本 + SVG 源文件）。"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
LOGO_DIR = os.path.join(ROOT, "LOGO")
os.makedirs(LOGO_DIR, exist_ok=True)

SIZE = 1024
TOP = (18, 74, 168)      # 深蓝
BOTTOM = (14, 168, 158)  # 青绿
TEAL = (14, 168, 158)
NAVY = (18, 74, 168)
WHITE = (255, 255, 255)


def font(size, bold=True):
    candidates = [
        r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\simsun.ttc",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def vertical_gradient(size, top, bottom):
    import numpy as np
    h, w = size
    t = np.array(top, dtype=float)
    b = np.array(bottom, dtype=float)
    rows = np.linspace(0.0, 1.0, h)[:, None, None]
    arr = (t * (1.0 - rows) + b * rows).astype(np.uint8)
    arr = np.repeat(arr, w, axis=1)
    return Image.fromarray(arr, "RGB")


def rounded_mask(size, radius):
    mask = Image.new("L", size, 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=255)
    return mask


def draw_mark(d, cx, cy, scale=1.0, color=WHITE, width=18):
    """心电波形 + 心形 + 聆听声波。cx,cy 为画布中心，scale 缩放。"""
    w = width

    # 1) 心电基线（左进右出，中央为心形）
    pts_left = [
        (cx - 330 * scale, cy),
        (cx - 130 * scale, cy),
        (cx - 95 * scale, cy + 22 * scale),
        (cx - 60 * scale, cy - 14 * scale),
    ]
    d.line(pts_left, fill=color, width=w, joint="curve")

    # 心形（R 峰）：两条贝塞尔近似弧线 + 底部尖角
    r = 78 * scale
    heart_cx = cx
    heart_cy = cy - 8 * scale
    d.ellipse(
        [heart_cx - r, heart_cy - r, heart_cx, heart_cy],
        outline=color,
        width=w,
    )
    d.ellipse(
        [heart_cx, heart_cy - r, heart_cx + r, heart_cy],
        outline=color,
        width=w,
    )
    d.line(
        [
            (heart_cx - r + 2, heart_cy - 6 * scale),
            (heart_cx, heart_cy + 1.25 * r),
            (heart_cx + r - 2, heart_cy - 6 * scale),
        ],
        fill=color,
        width=w,
        joint="curve",
    )

    pts_right = [
        (cx + 95 * scale, cy - 14 * scale),
        (cx + 130 * scale, cy + 22 * scale),
        (cx + 165 * scale, cy),
        (cx + 330 * scale, cy),
    ]
    d.line(pts_right, fill=color, width=w, joint="curve")

    # 2) 聆听声波（右侧三条同心弧）
    arc_cx = cx + 235 * scale
    arc_cy = cy - 180 * scale
    for k, rr in enumerate([88, 128, 168]):
        rr = rr * scale
        bbox = [arc_cx - rr, arc_cy - rr, arc_cx + rr, arc_cy + rr]
        d.arc(bbox, start=-75, end=75, fill=color, width=int(w * 0.85))

    # 3) 顶部一瓣“脑回”弧线，呼应脑科学（左侧小弧）
    bbox2 = [cx - 300 * scale, cy - 205 * scale, cx - 120 * scale, cy - 25 * scale]
    d.arc(bbox2, start=160, end=350, fill=color, width=int(w * 0.75))
    bbox3 = [cx - 260 * scale, cy - 170 * scale, cx - 150 * scale, cy - 55 * scale]
    d.arc(bbox3, start=180, end=330, fill=color, width=int(w * 0.6))


def make_main_logo():
    img = vertical_gradient((SIZE, SIZE), TOP, BOTTOM)
    mask = rounded_mask((SIZE, SIZE), 200)
    out = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)

    d = ImageDraw.Draw(out)
    draw_mark(d, cx=460, cy=380, scale=1.0)

    f_name = font(148, bold=True)
    text = "心聆"
    tw = d.textlength(text, font=f_name)
    d.text(((SIZE - tw) / 2, 640), text, font=f_name, fill=WHITE)

    f_tag = font(44, bold=False)
    tag = "听见心的声音"
    tw = d.textlength(tag, font=f_tag)
    d.text(((SIZE - tw) / 2, 830), tag, font=f_tag, fill=(230, 250, 248, 235))
    out.save(os.path.join(LOGO_DIR, "心聆LOGO.png"))


def make_transparent_logo():
    out = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    draw_mark(d, cx=460, cy=360, scale=0.95)
    f_name = font(148, bold=True)
    text = "心聆"
    tw = d.textlength(text, font=f_name)
    d.text(((SIZE - tw) / 2, 610), text, font=f_name, fill=WHITE)
    f_tag = font(44, bold=False)
    tag = "听见心的声音"
    tw = d.textlength(tag, font=f_tag)
    d.text(((SIZE - tw) / 2, 820), tag, font=f_tag, fill=(215, 245, 243, 235))
    out.save(os.path.join(LOGO_DIR, "心聆LOGO_透明底.png"))

    # 浅色背景版本：青色图形 + 深蓝文字
    out2 = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(out2)
    draw_mark(d2, cx=460, cy=360, scale=0.95, color=TEAL)
    tw = d2.textlength(text, font=f_name)
    d2.text(((SIZE - tw) / 2, 610), text, font=f_name, fill=NAVY)
    tw = d2.textlength(tag, font=f_tag)
    d2.text(((SIZE - tw) / 2, 820), tag, font=f_tag, fill=(40, 120, 130, 235))
    out2.save(os.path.join(LOGO_DIR, "心聆LOGO_透明底_浅色版.png"))


def make_svg():
    svg = r'''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#124AA8"/>
      <stop offset="1" stop-color="#0EA89E"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="1024" height="1024" rx="200" fill="url(#bg)"/>
  <g stroke="#FFFFFF" stroke-width="18" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M130 380 L330 380 L365 402 L400 366"/>
    <path d="M520 366 L555 402 L590 380 L790 380"/>
    <circle cx="382" cy="380" r="78" stroke-width="18"/>
    <circle cx="538" cy="380" r="78" stroke-width="18"/>
    <path d="M405 386 L460 482 L515 386"/>
    <path d="M160 175 L340 355" />
    <path d="M200 210 L300 310" />
    <path d="M695 200 A88 88 0 0 1 871 200" />
    <path d="M655 165 A128 128 0 0 1 911 165" />
    <path d="M615 130 A168 168 0 0 1 951 130" />
  </g>
  <text x="512" y="772" font-family="Microsoft YaHei, SimHei, sans-serif" font-size="150" font-weight="bold" fill="#FFFFFF" text-anchor="middle">心聆</text>
  <text x="512" y="878" font-family="Microsoft YaHei, SimHei, sans-serif" font-size="44" fill="#E6FAF8" text-anchor="middle">听见心的声音</text>
</svg>'''
    with open(os.path.join(LOGO_DIR, "心聆LOGO.svg"), "w", encoding="utf-8") as f:
        f.write(svg)


if __name__ == "__main__":
    make_main_logo()
    make_transparent_logo()
    make_svg()
    print("LOGO generated at:", LOGO_DIR)
