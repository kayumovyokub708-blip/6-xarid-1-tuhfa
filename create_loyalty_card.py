#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Карточкаи лоялӣ: «6 ХАРИД — 1 ТӮҲФА!»
Барои мағозаи хурди хӯрокворӣ
Андоза: A6 (105 × 148 мм)
"""

from reportlab.lib.pagesizes import A6
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import Color, HexColor

# Шрифтҳо
pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuBold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

# Рангҳо (зинда, аммо касбӣ)
GREEN_MAIN = HexColor('#2E7D32')      # сабзи асосии мағоза
GREEN_LIGHT = HexColor('#E8F5E9')     # заминаи сабук
ORANGE = HexColor('#FF6F00')          # тӯҳфа / ҳаракат
ORANGE_LIGHT = HexColor('#FFF3E0')
DARK = HexColor('#1B1B1B')
WHITE = HexColor('#FFFFFF')
GRAY = HexColor('#616161')
BOX_BORDER = HexColor('#43A047')
GIFT_BG = HexColor('#FFF8E1')
GIFT_BORDER = HexColor('#FF8F00')

def draw_rounded_rect(c, x, y, w, h, radius, fill_color=None, stroke_color=None, stroke_width=1):
    c.saveState()
    if fill_color:
        c.setFillColor(fill_color)
    if stroke_color:
        c.setStrokeColor(stroke_color)
        c.setLineWidth(stroke_width)
    p = c.beginPath()
    p.moveTo(x + radius, y)
    p.lineTo(x + w - radius, y)
    p.arcTo(x + w - 2*radius, y, x + w, y + 2*radius, -90, 90)
    p.lineTo(x + w, y + h - radius)
    p.arcTo(x + w - 2*radius, y + h - 2*radius, x + w, y + h, 0, 90)
    p.lineTo(x + radius, y + h)
    p.arcTo(x, y + h - 2*radius, x + 2*radius, y + h, 90, 90)
    p.lineTo(x, y + radius)
    p.arcTo(x, y, x + 2*radius, y + 2*radius, 180, 90)
    p.close()
    if fill_color and stroke_color:
        c.drawPath(p, fill=1, stroke=1)
    elif fill_color:
        c.drawPath(p, fill=1, stroke=0)
    else:
        c.drawPath(p, fill=0, stroke=1)
    c.restoreState()

def create_card(filename="loyalty_card_6_xarid.pdf"):
    c = canvas.Canvas(filename, pagesize=A6)
    width, height = A6  # 105mm x 148mm

    # === ЗАМИНАИ УМУМӢ ===
    c.setFillColor(WHITE)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # Рамзи болоӣ (сабз)
    c.setFillColor(GREEN_MAIN)
    c.rect(0, height - 8*mm, width, 8*mm, fill=1, stroke=0)

    # === ҶОЙИ ЛОГОТИП / НОМИ МАҒОЗА ===
    c.setFillColor(WHITE)
    c.setFont('DejaVu', 7)
    c.drawCentredString(width/2, height - 5.5*mm, "[НОМИ МАҒОЗА / ЛОГОТИП]")

    # === САРЛАВҲА ===
    y = height - 18*mm
    c.setFillColor(GREEN_MAIN)
    c.setFont('DejaVuBold', 13)
    c.drawCentredString(width/2, y, "★  6 ХАРИД — 1 ТӮҲФА!  ★")

    # === ШУОР ===
    y -= 7*mm
    c.setFillColor(DARK)
    c.setFont('DejaVu', 8)
    c.drawCentredString(width/2, y, "6 бор аз мо харид кун — тӯҳфаи худро бигир!")

    # === ХАТТИ ТАҚСИМКУНАНДА ===
    y -= 4*mm
    c.setStrokeColor(GREEN_LIGHT)
    c.setLineWidth(1.5)
    c.line(8*mm, y, width - 8*mm, y)

    # === 6 ХОНАЧА ===
    y -= 6*mm
    c.setFillColor(DARK)
    c.setFont('DejaVuBold', 9)
    c.drawCentredString(width/2, y, "ХОНАЧАҲОИ ХАРИД")

    # Андозаи хоначаҳо
    box_w = 28*mm
    box_h = 22*mm
    gap_x = 4*mm
    gap_y = 3.5*mm
    start_x = (width - (3*box_w + 2*gap_x)) / 2
    start_y = y - 5*mm - box_h

    numbers = ["1", "2", "3", "4", "5", "6"]

    for i in range(6):
        row = i // 3
        col = i % 3
        x = start_x + col * (box_w + gap_x)
        by = start_y - row * (box_h + gap_y)

        # Қуттии хонача
        draw_rounded_rect(c, x, by, box_w, box_h, 3*mm,
                          fill_color=GREEN_LIGHT,
                          stroke_color=BOX_BORDER,
                          stroke_width=1.8)

        # Рақам
        c.setFillColor(GREEN_MAIN)
        c.setFont('DejaVuBold', 16)
        c.drawCentredString(x + box_w/2, by + box_h - 8*mm, numbers[i])

        # Ҷойи муҳр / стикер
        c.setFillColor(GRAY)
        c.setFont('DejaVu', 6)
        c.drawCentredString(x + box_w/2, by + 4*mm, "муҳр / стикер")

        # Хатти нуқтадор барои ҷойи имзо
        c.setStrokeColor(HexColor('#A5D6A7'))
        c.setDash(1, 2)
        c.line(x + 3*mm, by + 7*mm, x + box_w - 3*mm, by + 7*mm)
        c.setDash()

    # === БЛОКИ ТӮҲФА ===
    gift_y = 28*mm
    gift_h = 22*mm
    draw_rounded_rect(c, 6*mm, gift_y, width - 12*mm, gift_h, 3.5*mm,
                      fill_color=GIFT_BG,
                      stroke_color=GIFT_BORDER,
                      stroke_width=2)

    c.setFillColor(ORANGE)
    c.setFont('DejaVuBold', 9)
    c.drawCentredString(width/2, gift_y + gift_h - 6*mm, "★  ТӮҲФАИ ШУМО  ★")

    c.setFillColor(DARK)
    c.setFont('DejaVuBold', 10)
    c.drawCentredString(width/2, gift_y + gift_h - 12*mm, "САБАДИ МАҲСУЛОТ")

    c.setFillColor(ORANGE)
    c.setFont('DejaVuBold', 11)
    c.drawCentredString(width/2, gift_y + 5*mm, "БА АРЗИШИ 80 СОМОНӢ")

    # === ҚОИДАҲОИ КӮТОҲ ===
    rules_y = 5*mm
    c.setFillColor(GRAY)
    c.setFont('DejaVu', 5.5)
    rules = [
        "1. Бо ҳар харид 1 хонача пур карда мешавад.",
        "2. Пас аз 6 хонача → тӯҳфа гиред.",
        "3. Карточкаро ба корманд нишон диҳед.",
        "4. Як карточка = як тӯҳфа."
    ]
    for i, line in enumerate(rules):
        c.drawString(7*mm, rules_y + (3 - i)*3.2*mm, line)

    # Рамзи поёнӣ
    c.setFillColor(GREEN_MAIN)
    c.rect(0, 0, width, 3*mm, fill=1, stroke=0)

    c.save()
    print(f"✅ Карточка омода шуд: {filename}")

def create_staff_guide(filename="staff_guide.pdf"):
    """Роҳнамои кӯтоҳ барои кормандон (A5)"""
    from reportlab.lib.pagesizes import A5
    c = canvas.Canvas(filename, pagesize=A5)
    width, height = A5

    c.setFillColor(GREEN_MAIN)
    c.rect(0, height - 15*mm, width, 15*mm, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont('DejaVuBold', 14)
    c.drawCentredString(width/2, height - 10*mm, "РОҲНАМОИ КОРМАНД")
    c.setFont('DejaVu', 9)
    c.drawCentredString(width/2, height - 13.5*mm, "«6 ХАРИД — 1 ТӮҲФА!»")

    y = height - 25*mm
    c.setFillColor(DARK)
    c.setFont('DejaVuBold', 11)
    c.drawString(12*mm, y, "Чӣ гуна хонача пур карда мешавад?")

    y -= 7*mm
    c.setFont('DejaVu', 9)
    lines = [
        "• Пас аз ҳар хариди воқеӣ (ҳар қадар маблағ) —",
        "  1 хоначаро бо муҳр, стикер ё имзо пур кунед.",
        "• Танҳо 1 хонача барои 1 харид.",
        "• Карточкаи мизоҷро гиред ва хоначаро пур кунед.",
    ]
    for line in lines:
        c.drawString(14*mm, y, line)
        y -= 5*mm

    y -= 4*mm
    c.setFont('DejaVuBold', 11)
    c.drawString(12*mm, y, "Кай карточка пурра мешавад?")
    y -= 6*mm
    c.setFont('DejaVu', 9)
    c.drawString(14*mm, y, "Вақте ки ҳамаи 6 хонача пур шуданд.")
    y -= 5*mm
    c.drawString(14*mm, y, "Ба мизоҷ бигӯед: «Тӯҳфаи шумо омода аст!»")

    y -= 8*mm
    c.setFont('DejaVuBold', 11)
    c.drawString(12*mm, y, "Кай тӯҳфа дода мешавад?")
    y -= 6*mm
    c.setFont('DejaVu', 9)
    c.drawString(14*mm, y, "• Карточкаро гиред ва тафтиш кунед.")
    y -= 5*mm
    c.drawString(14*mm, y, "• Сабади маҳсулотро (≈ 80 сомонӣ) омода кунед.")
    y -= 5*mm
    c.drawString(14*mm, y, "• Карточкаро қайд кунед (масалан, бо қалам")
    y -= 5*mm
    c.drawString(14*mm, y, "  «ТӮҲФА ДОДА ШУД» нависед ё буред).")
    y -= 5*mm
    c.drawString(14*mm, y, "• Карточкаи истифодашударо нигоҳ доред.")

    y -= 8*mm
    c.setFont('DejaVuBold', 11)
    c.drawString(12*mm, y, "Муҳим!")
    y -= 6*mm
    c.setFont('DejaVu', 9)
    c.drawString(14*mm, y, "• Як карточка = танҳо як тӯҳфа.")
    y -= 5*mm
    c.drawString(14*mm, y, "• Карточкаи қалбакӣ ё такрорӣ қабул накунед.")
    y -= 5*mm
    c.drawString(14*mm, y, "• Агар шарти иловагӣ лозим бошад —")
    y -= 5*mm
    c.drawString(14*mm, y, "  аз мудир пурсед.")

    # Поён
    c.setFillColor(GREEN_MAIN)
    c.rect(0, 0, width, 8*mm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('DejaVu', 7)
    c.drawCentredString(width/2, 3*mm, "Сабад: равған, шакар, биринҷ, макарон, печенье, шоколад, нӯшокӣ...")

    c.save()
    print(f"✅ Роҳнамои корманд омода шуд: {filename}")

if __name__ == "__main__":
    create_card()
    create_staff_guide()
