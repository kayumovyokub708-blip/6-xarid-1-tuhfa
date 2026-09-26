#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Карточкаи дутарафаи лоялӣ барои мағозаи «Шаҳоб»
Тарафи пеш  — бозӣ
Тарафи пушт — суратҳои маҳсулот + бренд
Андоза: A6
"""

from reportlab.lib.pagesizes import A6
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.utils import ImageReader
import math

pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuBold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

# Рангҳо
GREEN_DARK   = HexColor('#145A32')
GREEN_MAIN   = HexColor('#1E8449')
GREEN_MID    = HexColor('#27AE60')
GREEN_LIGHT  = HexColor('#E8F8F5')
GREEN_PALE   = HexColor('#D5F5E3')
ORANGE       = HexColor('#D35400')
ORANGE_SOFT  = HexColor('#FDEBD0')
CREAM        = HexColor('#FEF9E7')
GOLD         = HexColor('#F39C12')
DARK         = HexColor('#1C2833')
GRAY         = HexColor('#5D6D7E')
WHITE        = HexColor('#FFFFFF')
SOFT_BG      = HexColor('#F4F6F7')

def rounded_rect(c, x, y, w, h, r, fill=None, stroke=None, sw=1.5):
    c.saveState()
    if fill: c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(sw)
    p = c.beginPath()
    p.moveTo(x + r, y)
    p.lineTo(x + w - r, y)
    p.arcTo(x + w - 2*r, y, x + w, y + 2*r, -90, 90)
    p.lineTo(x + w, y + h - r)
    p.arcTo(x + w - 2*r, y + h - 2*r, x + w, y + h, 0, 90)
    p.lineTo(x + r, y + h)
    p.arcTo(x, y + h - 2*r, x + 2*r, y + h, 90, 90)
    p.lineTo(x, y + r)
    p.arcTo(x, y, x + 2*r, y + 2*r, 180, 90)
    p.close()
    if fill and stroke:
        c.drawPath(p, fill=1, stroke=1)
    elif fill:
        c.drawPath(p, fill=1, stroke=0)
    else:
        c.drawPath(p, fill=0, stroke=1)
    c.restoreState()

# ==================== ИКОНКАҲОИ МАҲСУЛОТ ====================

def draw_oil_bottle(c, cx, cy, scale=1.0):
    s = scale
    c.saveState()
    c.setFillColor(HexColor('#F5CBA7'))
    c.roundRect(cx - 4*s, cy - 10*s, 8*s, 16*s, 1.5*s, fill=1, stroke=0)
    c.setFillColor(HexColor('#D4A017'))
    c.rect(cx - 2.5*s, cy + 6*s, 5*s, 4*s, fill=1, stroke=0)
    c.setFillColor(HexColor('#7D6608'))
    c.circle(cx, cy + 11*s, 2*s, fill=1, stroke=0)
    c.setFillColor(HexColor('#F9E79F'))
    c.rect(cx - 3*s, cy - 2*s, 6*s, 5*s, fill=1, stroke=0)
    c.restoreState()

def draw_rice_bag(c, cx, cy, scale=1.0):
    s = scale
    c.saveState()
    c.setFillColor(HexColor('#F5EEF8'))
    path = c.beginPath()
    path.moveTo(cx - 7*s, cy - 9*s)
    path.lineTo(cx - 8*s, cy + 6*s)
    path.lineTo(cx + 8*s, cy + 6*s)
    path.lineTo(cx + 7*s, cy - 9*s)
    path.close()
    c.drawPath(path, fill=1, stroke=0)
    c.setFillColor(HexColor('#8E44AD'))
    c.rect(cx - 8*s, cy + 4*s, 16*s, 4*s, fill=1, stroke=0)
    c.setFillColor(HexColor('#D2B4DE'))
    c.circle(cx, cy - 1*s, 3*s, fill=1, stroke=0)
    c.restoreState()

def draw_sugar(c, cx, cy, scale=1.0):
    s = scale
    c.saveState()
    c.setFillColor(HexColor('#FDFEFE'))
    c.roundRect(cx - 6*s, cy - 8*s, 12*s, 14*s, 1*s, fill=1, stroke=0)
    c.setStrokeColor(HexColor('#BDC3C7'))
    c.setLineWidth(0.6)
    c.roundRect(cx - 6*s, cy - 8*s, 12*s, 14*s, 1*s, fill=0, stroke=1)
    c.setFillColor(HexColor('#E74C3C'))
    c.rect(cx - 6*s, cy + 2*s, 12*s, 4*s, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('DejaVuBold', 4*s)
    c.drawCentredString(cx, cy + 3.2*s, "SUGAR")
    c.restoreState()

def draw_pasta(c, cx, cy, scale=1.0):
    s = scale
    c.saveState()
    c.setFillColor(HexColor('#F9E79F'))
    for i, offset in enumerate([-4, -1.5, 1, 3.5]):
        c.roundRect(cx + offset*s - 1.2*s, cy - 9*s, 2.4*s, 16*s, 0.8*s, fill=1, stroke=0)
    c.setFillColor(HexColor('#D4AC0D'))
    c.circle(cx, cy + 9*s, 3*s, fill=1, stroke=0)
    c.restoreState()

def draw_cookies(c, cx, cy, scale=1.0):
    s = scale
    c.saveState()
    c.setFillColor(HexColor('#D35400'))
    c.circle(cx - 3*s, cy + 2*s, 5*s, fill=1, stroke=0)
    c.setFillColor(HexColor('#E67E22'))
    c.circle(cx + 3*s, cy - 1*s, 5.5*s, fill=1, stroke=0)
    c.setFillColor(HexColor('#F5B041'))
    c.circle(cx, cy + 4*s, 4*s, fill=1, stroke=0)
    c.setFillColor(HexColor('#6E2C00'))
    for dx, dy in [(-1, 1), (1.5, 0), (0, -1.5)]:
        c.circle(cx + dx*s, cy + 4*s + dy*s, 0.7*s, fill=1, stroke=0)
    c.restoreState()

def draw_chocolate(c, cx, cy, scale=1.0):
    s = scale
    c.saveState()
    c.setFillColor(HexColor('#6E2C00'))
    c.roundRect(cx - 8*s, cy - 5*s, 16*s, 10*s, 1.5*s, fill=1, stroke=0)
    c.setFillColor(HexColor('#935116'))
    c.rect(cx - 7*s, cy - 1*s, 14*s, 3*s, fill=1, stroke=0)
    c.setStrokeColor(HexColor('#4A235A'))
    c.setLineWidth(0.5)
    for i in range(3):
        c.line(cx - 5*s + i*5*s, cy - 4*s, cx - 5*s + i*5*s, cy + 4*s)
    c.restoreState()

def draw_drink(c, cx, cy, scale=1.0):
    s = scale
    c.saveState()
    c.setFillColor(HexColor('#3498DB'))
    c.roundRect(cx - 4*s, cy - 9*s, 8*s, 16*s, 2*s, fill=1, stroke=0)
    c.setFillColor(HexColor('#85C1E9'))
    c.rect(cx - 3*s, cy + 2*s, 6*s, 4*s, fill=1, stroke=0)
    c.setFillColor(HexColor('#1A5276'))
    c.circle(cx, cy + 9*s, 2.2*s, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('DejaVu', 3.5*s)
    c.drawCentredString(cx, cy - 2*s, "•")
    c.restoreState()

def draw_cart(c, cx, cy, scale=1.0):
    s = scale
    c.saveState()
    c.setStrokeColor(GREEN_DARK)
    c.setFillColor(GREEN_MAIN)
    c.setLineWidth(1.2*s)
    path = c.beginPath()
    path.moveTo(cx - 8*s, cy + 2*s)
    path.lineTo(cx - 6*s, cy - 6*s)
    path.lineTo(cx + 6*s, cy - 6*s)
    path.lineTo(cx + 8*s, cy + 2*s)
    path.close()
    c.drawPath(path, fill=1, stroke=1)
    c.setFillColor(DARK)
    c.circle(cx - 4*s, cy - 8*s, 2*s, fill=1, stroke=0)
    c.circle(cx + 4*s, cy - 8*s, 2*s, fill=1, stroke=0)
    c.setStrokeColor(GREEN_DARK)
    c.setLineWidth(1.5*s)
    c.line(cx + 8*s, cy + 2*s, cx + 10*s, cy + 8*s)
    c.line(cx + 10*s, cy + 8*s, cx + 7*s, cy + 8*s)
    c.restoreState()

def draw_front(c, width, height):
    c.setFillColor(WHITE)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    c.setFillColor(GREEN_DARK)
    c.rect(0, height - 17*mm, width, 17*mm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('DejaVuBold', 18)
    c.drawCentredString(width/2, height - 7.5*mm, "ШАҲОБ")
    c.setFont('DejaVu', 6)
    c.drawCentredString(width/2, height - 13*mm, "мағозаи хӯрокворӣ")
    y = height - 24*mm
    c.setFillColor(GREEN_MAIN)
    c.setFont('DejaVuBold', 11)
    c.drawCentredString(width/2, y, "★  6 ХАРИД — 1 ТӮҲФА!  ★")
    y -= 9*mm
    rounded_rect(c, 5*mm, y - 1.5*mm, width - 10*mm, 8.5*mm, 2.5*mm,
                 fill=ORANGE_SOFT, stroke=ORANGE, sw=1.8)
    c.setFillColor(ORANGE)
    c.setFont('DejaVuBold', 7.5)
    c.drawCentredString(width/2, y + 2*mm, "ҲАР ХАРИД АЗ 260 СОМОНӢ БОЛО = 1 ХОНАЧА")
    y -= 9*mm
    c.setFillColor(DARK)
    c.setFont('DejaVuBold', 7.5)
    c.drawCentredString(width/2, y, "ХОНАЧАҲОИ ХАРИД")
    box_w, box_h = 26.5*mm, 19*mm
    gap_x, gap_y = 3.5*mm, 2.8*mm
    start_x = (width - (3*box_w + 2*gap_x)) / 2
    start_y = y - 3.5*mm - box_h
    for i in range(6):
        row, col = i // 3, i % 3
        x = start_x + col * (box_w + gap_x)
        by = start_y - row * (box_h + gap_y)
        rounded_rect(c, x, by, box_w, box_h, 2.5*mm,
                     fill=GREEN_LIGHT, stroke=GREEN_MID, sw=1.5)
        c.setFillColor(GREEN_DARK)
        c.setFont('DejaVuBold', 14)
        c.drawCentredString(x + box_w/2, by + box_h - 7*mm, str(i+1))
        c.setFillColor(GRAY)
        c.setFont('DejaVu', 5)
        c.drawCentredString(x + box_w/2, by + 3.2*mm, "муҳр / стикер")
        c.setStrokeColor(HexColor('#A9DFBF'))
        c.setDash(1, 1.2)
        c.setLineWidth(0.7)
        c.line(x + 2.5*mm, by + 6*mm, x + box_w - 2.5*mm, by + 6*mm)
        c.setDash()
    gift_y = 24*mm
    rounded_rect(c, 5*mm, gift_y, width - 10*mm, 19*mm, 3*mm,
                 fill=CREAM, stroke=ORANGE, sw=2)
    c.setFillColor(ORANGE)
    c.setFont('DejaVuBold', 7.5)
    c.drawCentredString(width/2, gift_y + 14*mm, "★  ТӮҲФАИ ШУМО  ★")
    c.setFillColor(DARK)
    c.setFont('DejaVuBold', 8)
    c.drawCentredString(width/2, gift_y + 8.5*mm, "САБАДИ МАҲСУЛОТИ ХӮРОКВОРӢ")
    c.setFillColor(ORANGE)
    c.setFont('DejaVuBold', 13)
    c.drawCentredString(width/2, gift_y + 3*mm, "100 СОМОНӢ")
    c.setFillColor(GRAY)
    c.setFont('DejaVu', 4.8)
    c.drawCentredString(width/2, 6.5*mm, "1. Харид ≥ 260 с. → 1 хонача    2. 6 хонача → тӯҳфа")
    c.drawCentredString(width/2, 3.5*mm, "3. Карточкаро ба корманд нишон диҳед    4. Як карточка = 1 тӯҳфа")
    c.setFillColor(GREEN_DARK)
    c.rect(0, 0, width, 2*mm, fill=1, stroke=0)

def draw_back(c, width, height):
    c.setFillColor(SOFT_BG)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    c.setFillColor(GREEN_DARK)
    c.rect(0, height - 14*mm, width, 14*mm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('DejaVuBold', 14)
    c.drawCentredString(width/2, height - 6*mm, "ШАҲОБ")
    c.setFont('DejaVu', 6)
    c.drawCentredString(width/2, height - 11*mm, "маҳсулоти тару тоза • ҳар рӯз")
    y = height - 22*mm
    c.setFillColor(GREEN_MAIN)
    c.setFont('DejaVuBold', 9)
    c.drawCentredString(width/2, y, "МАҲСУЛОТИ МАҒОЗАИ МО")
    icons = [
        (draw_oil_bottle, "Равған"),
        (draw_rice_bag, "Биринҷ"),
        (draw_sugar, "Шакар"),
        (draw_pasta, "Макарон"),
        (draw_cookies, "Печенье"),
        (draw_chocolate, "Шоколад"),
        (draw_drink, "Нӯшокӣ"),
        (draw_cart, "Аробача"),
    ]
    icon_size = 18*mm
    gap = 3*mm
    cols = 4
    total_w = cols * icon_size + (cols-1) * gap
    start_x = (width - total_w) / 2
    start_y = y - 8*mm - icon_size
    for idx, (draw_fn, label) in enumerate(icons):
        row = idx // cols
        col = idx % cols
        x = start_x + col * (icon_size + gap)
        iy = start_y - row * (icon_size + 8*mm)
        rounded_rect(c, x, iy, icon_size, icon_size, 2.5*mm,
                     fill=WHITE, stroke=GREEN_PALE, sw=1)
        draw_fn(c, x + icon_size/2, iy + icon_size/2 + 1*mm, scale=1.15)
        c.setFillColor(DARK)
        c.setFont('DejaVu', 5)
        c.drawCentredString(x + icon_size/2, iy - 4*mm, label)
    bottom_y = 18*mm
    rounded_rect(c, 6*mm, bottom_y, width - 12*mm, 14*mm, 2.5*mm,
                 fill=GREEN_LIGHT, stroke=GREEN_MAIN, sw=1.5)
    c.setFillColor(GREEN_DARK)
    c.setFont('DejaVuBold', 8)
    c.drawCentredString(width/2, bottom_y + 8.5*mm, "6 ХАРИД = 1 ТӮҲФА")
    c.setFont('DejaVu', 6.5)
    c.drawCentredString(width/2, bottom_y + 3.5*mm, "Аз 260 сомонӣ харид кун ва сабад бигир!")
    c.setFillColor(GREEN_DARK)
    c.rect(0, 0, width, 2*mm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('DejaVu', 5)
    c.drawCentredString(width/2, 5*mm, "Мағозаи «Шаҳоб» • сифат ва эътимод")

def create_double_sided(filename="shahob_card_double.pdf"):
    c = canvas.Canvas(filename, pagesize=A6)
    width, height = A6
    draw_front(c, width, height)
    c.showPage()
    draw_back(c, width, height)
    c.save()
    print(f"✅ Карточкаи дутарафа омода шуд: {filename}")

if __name__ == "__main__":
    create_double_sided()
