#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Карточкаи дутарафаи «Шаҳоб» — версияи 3
Тарафи пушт: бе ҷойҳои сафед, бо суратҳои рангоранги маҳсулот
"""

from reportlab.lib.pagesizes import A6
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, Color
import math

pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuBold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

GREEN_DARK  = HexColor('#0E4D2B')
GREEN_MAIN  = HexColor('#1B7A4E')
GREEN_MID   = HexColor('#27AE60')
GREEN_LIGHT = HexColor('#E8F8F5')
GREEN_PALE  = HexColor('#D4EFDF')
ORANGE      = HexColor('#D35400')
ORANGE_SOFT = HexColor('#FDEBD0')
CREAM       = HexColor('#FEF9E7')
DARK        = HexColor('#1C2833')
GRAY        = HexColor('#5D6D7E')
WHITE       = HexColor('#FFFFFF')
SOFT_BG     = HexColor('#F0F3F4')

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

def draw_oil(c, cx, cy, s=1.0):
    c.saveState()
    c.setFillColor(HexColor('#F7DC6F'))
    c.roundRect(cx-5*s, cy-11*s, 10*s, 18*s, 2*s, fill=1, stroke=0)
    c.setFillColor(HexColor('#F4D03F'))
    c.roundRect(cx-4*s, cy-9*s, 8*s, 12*s, 1.5*s, fill=1, stroke=0)
    c.setFillColor(HexColor('#7D6608'))
    c.roundRect(cx-3*s, cy+7*s, 6*s, 4*s, 1*s, fill=1, stroke=0)
    c.setFillColor(HexColor('#9A7D0A'))
    c.circle(cx, cy+12*s, 2.2*s, fill=1, stroke=0)
    c.setFillColor(HexColor('#F9E79F'))
    c.setFont('DejaVu', 3.5*s)
    c.drawCentredString(cx, cy-2*s, "oil")
    c.restoreState()

def draw_rice(c, cx, cy, s=1.0):
    c.saveState()
    c.setFillColor(HexColor('#F5EEF8'))
    path = c.beginPath()
    path.moveTo(cx-8*s, cy-10*s)
    path.lineTo(cx-9*s, cy+5*s)
    path.lineTo(cx+9*s, cy+5*s)
    path.lineTo(cx+8*s, cy-10*s)
    path.close()
    c.drawPath(path, fill=1, stroke=0)
    c.setFillColor(HexColor('#8E44AD'))
    c.rect(cx-9*s, cy+2*s, 18*s, 5*s, fill=1, stroke=0)
    c.setFillColor(HexColor('#D2B4DE'))
    for dx, dy in [(-3, -2), (0, -4), (3, -1), (-2, -6), (2, -7)]:
        c.ellipse(cx+dx*s-1.5*s, cy+dy*s-1*s, cx+dx*s+1.5*s, cy+dy*s+1*s, fill=1, stroke=0)
    c.restoreState()

def draw_sugar(c, cx, cy, s=1.0):
    c.saveState()
    c.setFillColor(HexColor('#FDFEFE'))
    c.roundRect(cx-7*s, cy-9*s, 14*s, 16*s, 1.5*s, fill=1, stroke=0)
    c.setStrokeColor(HexColor('#BDC3C7'))
    c.setLineWidth(0.7)
    c.roundRect(cx-7*s, cy-9*s, 14*s, 16*s, 1.5*s, fill=0, stroke=1)
    c.setFillColor(HexColor('#E74C3C'))
    c.rect(cx-7*s, cy+1*s, 14*s, 5*s, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('DejaVuBold', 4.5*s)
    c.drawCentredString(cx, cy+2.8*s, "SUGAR")
    c.setFillColor(HexColor('#F5B7B1'))
    c.circle(cx, cy-4*s, 3*s, fill=1, stroke=0)
    c.restoreState()

def draw_pasta(c, cx, cy, s=1.0):
    c.saveState()
    colors = [HexColor('#F9E79F'), HexColor('#F4D03F'), HexColor('#F7DC6F'), HexColor('#F5B041')]
    for i, col in enumerate(colors):
        c.setFillColor(col)
        ox = (i - 1.5) * 3.2 * s
        c.roundRect(cx+ox-1.3*s, cy-11*s, 2.6*s, 18*s, 1*s, fill=1, stroke=0)
    c.setFillColor(HexColor('#D4AC0D'))
    c.circle(cx, cy+9*s, 3.5*s, fill=1, stroke=0)
    c.setFillColor(HexColor('#7D6608'))
    c.setFont('DejaVuBold', 3*s)
    c.drawCentredString(cx, cy+8*s, "P")
    c.restoreState()

def draw_cookies(c, cx, cy, s=1.0):
    c.saveState()
    for i, (dx, dy, r, col) in enumerate([
        (-4, 3, 5.5, '#D35400'),
        (4, 0, 6, '#E67E22'),
        (0, 5, 4.5, '#F5B041')
    ]):
        c.setFillColor(HexColor(col))
        c.circle(cx+dx*s, cy+dy*s, r*s, fill=1, stroke=0)
        c.setFillColor(HexColor('#4A235A'))
        for ox, oy in [(-1.5, 1), (1.2, -0.8), (0, 1.5)]:
            c.circle(cx+dx*s+ox*s, cy+dy*s+oy*s, 0.8*s, fill=1, stroke=0)
    c.restoreState()

def draw_chocolate(c, cx, cy, s=1.0):
    c.saveState()
    c.setFillColor(HexColor('#5D4037'))
    c.roundRect(cx-9*s, cy-6*s, 18*s, 12*s, 2*s, fill=1, stroke=0)
    c.setFillColor(HexColor('#8D6E63'))
    c.rect(cx-8*s, cy-1*s, 16*s, 3.5*s, fill=1, stroke=0)
    c.setStrokeColor(HexColor('#3E2723'))
    c.setLineWidth(0.6)
    for i in range(1, 4):
        c.line(cx-9*s + i*4.5*s, cy-5*s, cx-9*s + i*4.5*s, cy+5*s)
    c.restoreState()

def draw_drink(c, cx, cy, s=1.0):
    c.saveState()
    c.setFillColor(HexColor('#2980B9'))
    c.roundRect(cx-4.5*s, cy-11*s, 9*s, 18*s, 2.5*s, fill=1, stroke=0)
    c.setFillColor(HexColor('#5DADE2'))
    c.roundRect(cx-3.5*s, cy-9*s, 7*s, 11*s, 1.5*s, fill=1, stroke=0)
    c.setFillColor(HexColor('#1A5276'))
    c.circle(cx, cy+9*s, 2.5*s, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('DejaVuBold', 3.5*s)
    c.drawCentredString(cx, cy-1*s, "•")
    c.restoreState()

def draw_apple(c, cx, cy, s=1.0):
    c.saveState()
    c.setFillColor(HexColor('#E74C3C'))
    c.circle(cx, cy, 7*s, fill=1, stroke=0)
    c.setFillColor(HexColor('#C0392B'))
    c.circle(cx+2*s, cy+1*s, 5*s, fill=1, stroke=0)
    c.setFillColor(HexColor('#27AE60'))
    path = c.beginPath()
    path.moveTo(cx, cy+6*s)
    path.curveTo(cx+4*s, cy+10*s, cx+6*s, cy+8*s, cx+3*s, cy+5*s)
    path.close()
    c.drawPath(path, fill=1, stroke=0)
    c.setStrokeColor(HexColor('#6E2C00'))
    c.setLineWidth(1.2)
    c.line(cx, cy+6*s, cx, cy+9*s)
    c.restoreState()

def draw_front(c, w, h):
    c.setFillColor(WHITE)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    c.setFillColor(GREEN_DARK)
    c.rect(0, h-16*mm, w, 16*mm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('DejaVuBold', 17)
    c.drawCentredString(w/2, h-7*mm, "ШАҲОБ")
    c.setFont('DejaVu', 6)
    c.drawCentredString(w/2, h-12.5*mm, "мағозаи хӯрокворӣ")
    y = h - 23*mm
    c.setFillColor(GREEN_MAIN)
    c.setFont('DejaVuBold', 11)
    c.drawCentredString(w/2, y, "★  6 ХАРИД — 1 ТӮҲФА!  ★")
    y -= 8.5*mm
    rounded_rect(c, 5*mm, y-1.5*mm, w-10*mm, 8*mm, 2.5*mm,
                 fill=ORANGE_SOFT, stroke=ORANGE, sw=1.8)
    c.setFillColor(ORANGE)
    c.setFont('DejaVuBold', 7.2)
    c.drawCentredString(w/2, y+1.8*mm, "ҲАР ХАРИД АЗ 260 СОМОНӢ БОЛО = 1 ХОНАЧА")
    y -= 8.5*mm
    c.setFillColor(DARK)
    c.setFont('DejaVuBold', 7.5)
    c.drawCentredString(w/2, y, "ХОНАЧАҲОИ ХАРИД")
    bw, bh = 26*mm, 18.5*mm
    gx, gy = 3.5*mm, 2.6*mm
    sx = (w - (3*bw + 2*gx)) / 2
    sy = y - 3.2*mm - bh
    for i in range(6):
        row, col = divmod(i, 3)
        x = sx + col*(bw+gx)
        by = sy - row*(bh+gy)
        rounded_rect(c, x, by, bw, bh, 2.5*mm, fill=GREEN_LIGHT, stroke=GREEN_MID, sw=1.5)
        c.setFillColor(GREEN_DARK)
        c.setFont('DejaVuBold', 14)
        c.drawCentredString(x+bw/2, by+bh-6.8*mm, str(i+1))
        c.setFillColor(GRAY)
        c.setFont('DejaVu', 5)
        c.drawCentredString(x+bw/2, by+3*mm, "муҳр / стикер")
        c.setStrokeColor(HexColor('#A9DFBF'))
        c.setDash(1, 1.2)
        c.setLineWidth(0.7)
        c.line(x+2.5*mm, by+5.8*mm, x+bw-2.5*mm, by+5.8*mm)
        c.setDash()
    gy = 23*mm
    rounded_rect(c, 5*mm, gy, w-10*mm, 18.5*mm, 3*mm, fill=CREAM, stroke=ORANGE, sw=2)
    c.setFillColor(ORANGE)
    c.setFont('DejaVuBold', 7.5)
    c.drawCentredString(w/2, gy+13.5*mm, "★  ТӮҲФАИ ШУМО  ★")
    c.setFillColor(DARK)
    c.setFont('DejaVuBold', 8)
    c.drawCentredString(w/2, gy+8*mm, "САБАДИ МАҲСУЛОТИ ХӮРОКВОРӢ")
    c.setFillColor(ORANGE)
    c.setFont('DejaVuBold', 13)
    c.drawCentredString(w/2, gy+2.8*mm, "100 СОМОНӢ")
    c.setFillColor(GRAY)
    c.setFont('DejaVu', 4.7)
    c.drawCentredString(w/2, 6*mm, "1. Харид ≥ 260 с. → 1 хонача    2. 6 хонача → тӯҳфа")
    c.drawCentredString(w/2, 3.2*mm, "3. Карточкаро ба корманд нишон диҳед    4. Як карточка = 1 тӯҳфа")
    c.setFillColor(GREEN_DARK)
    c.rect(0, 0, w, 2*mm, fill=1, stroke=0)

def draw_back(c, w, h):
    c.setFillColor(HexColor('#E8F6F3'))
    c.rect(0, 0, w, h, fill=1, stroke=0)
    c.setFillColor(GREEN_DARK)
    c.rect(0, h-13*mm, w, 13*mm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('DejaVuBold', 13)
    c.drawCentredString(w/2, h-5.5*mm, "ШАҲОБ")
    c.setFont('DejaVu', 5.5)
    c.drawCentredString(w/2, h-10*mm, "маҳсулоти тару тоза • ҳар рӯз")
    y = h - 20*mm
    c.setFillColor(GREEN_MAIN)
    c.setFont('DejaVuBold', 8.5)
    c.drawCentredString(w/2, y, "МАҲСУЛОТИ МАҒОЗАИ МО")
    items = [
        (draw_oil, "Равған", HexColor('#FEF9E7')),
        (draw_rice, "Биринҷ", HexColor('#F5EEF8')),
        (draw_sugar, "Шакар", HexColor('#FDEDEC')),
        (draw_pasta, "Макарон", HexColor('#FEF5E7')),
        (draw_cookies, "Печенье", HexColor('#FDF2E9')),
        (draw_chocolate, "Шоколад", HexColor('#F5EEF8')),
        (draw_drink, "Нӯшокӣ", HexColor('#EBF5FB')),
        (draw_apple, "Мева", HexColor('#E8F8F5')),
    ]
    size = 19*mm
    gap = 2.5*mm
    cols = 4
    total = cols*size + (cols-1)*gap
    sx = (w - total)/2
    sy = y - 7*mm - size
    for i, (fn, label, bg) in enumerate(items):
        row, col = divmod(i, 4)
        x = sx + col*(size+gap)
        iy = sy - row*(size + 9*mm)
        rounded_rect(c, x, iy, size, size, 3*mm, fill=bg, stroke=GREEN_PALE, sw=1.2)
        fn(c, x+size/2, iy+size/2+0.5*mm, s=1.05)
        c.setFillColor(DARK)
        c.setFont('DejaVu', 5.2)
        c.drawCentredString(x+size/2, iy-4.2*mm, label)
    by = 16*mm
    rounded_rect(c, 5*mm, by, w-10*mm, 13*mm, 2.5*mm,
                 fill=GREEN_LIGHT, stroke=GREEN_MAIN, sw=1.5)
    c.setFillColor(GREEN_DARK)
    c.setFont('DejaVuBold', 8)
    c.drawCentredString(w/2, by+8*mm, "6 ХАРИД = 1 ТӮҲФА")
    c.setFont('DejaVu', 6)
    c.drawCentredString(w/2, by+3*mm, "Аз 260 сомонӣ харид кун ва сабад бигир!")
    c.setFillColor(GREEN_DARK)
    c.rect(0, 0, w, 2*mm, fill=1, stroke=0)
    c.setFillColor(HexColor('#D5F5E3'))
    c.setFont('DejaVu', 5)
    c.drawCentredString(w/2, 4.5*mm, "Мағозаи «Шаҳоб» • сифат ва эътимод")

def create():
    c = canvas.Canvas("shahob_card_v3.pdf", pagesize=A6)
    w, h = A6
    draw_front(c, w, h)
    c.showPage()
    draw_back(c, w, h)
    c.save()
    print("✅ Карточкаи v3 омода шуд: shahob_card_v3.pdf")

if __name__ == "__main__":
    create()
