#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Карточкаи лоялӣ барои мағозаи «Шаҳоб»
«6 ХАРИД — 1 ТӮҲФА!»
Шарт: ҳар харид ≥ 260 сомонӣ = 1 хонача
Тӯҳфа: сабади маҳсулот ба маблағи 100 сомонӣ
Андоза: A6 (105 × 148 мм)
"""

from reportlab.lib.pagesizes import A6, A5
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuBold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

# Рангҳои премиум барои «Шаҳоб»
GREEN_DARK   = HexColor('#1B5E20')
GREEN_MAIN   = HexColor('#2E7D32')
GREEN_LIGHT  = HexColor('#E8F5E9')
GREEN_BORDER = HexColor('#43A047')
ORANGE       = HexColor('#E65100')
ORANGE_LIGHT = HexColor('#FFF3E0')
GOLD         = HexColor('#F9A825')
DARK         = HexColor('#212121')
GRAY         = HexColor('#616161')
WHITE        = HexColor('#FFFFFF')
CREAM        = HexColor('#FFFDE7')

def draw_rounded_rect(c, x, y, w, h, radius, fill_color=None, stroke_color=None, stroke_width=1.5):
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

def create_card(filename="shahob_loyalty_card.pdf"):
    c = canvas.Canvas(filename, pagesize=A6)
    width, height = A6

    # Заминаи тоза
    c.setFillColor(WHITE)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # === БАРНОМАИ БОЛО (сабзи тира) ===
    c.setFillColor(GREEN_DARK)
    c.rect(0, height - 18*mm, width, 18*mm, fill=1, stroke=0)

    # Номи бренд ШАҲОБ
    c.setFillColor(WHITE)
    c.setFont('DejaVuBold', 16)
    c.drawCentredString(width/2, height - 8*mm, "ШАҲОБ")

    # Ҷойи логотип
    c.setFont('DejaVu', 6)
    c.drawCentredString(width/2, height - 13.5*mm, "[ҶОЙИ ЛОГОТИП]")

    # === САРЛАВҲАИ БОЗӢ ===
    y = height - 26*mm
    c.setFillColor(GREEN_MAIN)
    c.setFont('DejaVuBold', 12)
    c.drawCentredString(width/2, y, "★  6 ХАРИД — 1 ТӮҲФА!  ★")

    # === ШАРТИ АСОСӢ (хеле равшан) ===
    y -= 8*mm
    draw_rounded_rect(c, 6*mm, y - 2*mm, width - 12*mm, 9*mm, 2.5*mm,
                      fill_color=ORANGE_LIGHT, stroke_color=ORANGE, stroke_width=1.8)
    c.setFillColor(ORANGE)
    c.setFont('DejaVuBold', 8)
    c.drawCentredString(width/2, y + 1.5*mm, "ҲАР ХАРИД АЗ 260 СОМОНӢ БОЛО = 1 ХОНАЧА")

    # === 6 ХОНАЧА ===
    y -= 10*mm
    c.setFillColor(DARK)
    c.setFont('DejaVuBold', 8)
    c.drawCentredString(width/2, y, "ХОНАЧАҲОИ ХАРИД")

    box_w = 27*mm
    box_h = 20*mm
    gap_x = 3.5*mm
    gap_y = 3*mm
    start_x = (width - (3*box_w + 2*gap_x)) / 2
    start_y = y - 4*mm - box_h

    numbers = ["1", "2", "3", "4", "5", "6"]

    for i in range(6):
        row = i // 3
        col = i % 3
        x = start_x + col * (box_w + gap_x)
        by = start_y - row * (box_h + gap_y)

        draw_rounded_rect(c, x, by, box_w, box_h, 2.8*mm,
                          fill_color=GREEN_LIGHT,
                          stroke_color=GREEN_BORDER,
                          stroke_width=1.6)

        # Рақам
        c.setFillColor(GREEN_DARK)
        c.setFont('DejaVuBold', 15)
        c.drawCentredString(x + box_w/2, by + box_h - 7.5*mm, numbers[i])

        # Ҷойи муҳр
        c.setFillColor(GRAY)
        c.setFont('DejaVu', 5.5)
        c.drawCentredString(x + box_w/2, by + 3.5*mm, "муҳр / стикер")

        # Хатти нуқтадор
        c.setStrokeColor(HexColor('#A5D6A7'))
        c.setDash(1, 1.5)
        c.setLineWidth(0.8)
        c.line(x + 2.5*mm, by + 6.5*mm, x + box_w - 2.5*mm, by + 6.5*mm)
        c.setDash()

    # === БЛОКИ ТӮҲФА ===
    gift_y = 26*mm
    gift_h = 20*mm
    draw_rounded_rect(c, 5*mm, gift_y, width - 10*mm, gift_h, 3*mm,
                      fill_color=CREAM,
                      stroke_color=ORANGE,
                      stroke_width=2)

    c.setFillColor(ORANGE)
    c.setFont('DejaVuBold', 8)
    c.drawCentredString(width/2, gift_y + gift_h - 5.5*mm, "★  ТӮҲФАИ ШУМО  ★")

    c.setFillColor(DARK)
    c.setFont('DejaVuBold', 9)
    c.drawCentredString(width/2, gift_y + gift_h - 11*mm, "САБАДИ МАҲСУЛОТИ ХӮРОКВОРӢ")

    c.setFillColor(ORANGE)
    c.setFont('DejaVuBold', 12)
    c.drawCentredString(width/2, gift_y + 4*mm, "100 СОМОНӢ")

    # === ҚОИДАҲОИ КӮТОҲ ===
    rules_y = 4.5*mm
    c.setFillColor(GRAY)
    c.setFont('DejaVu', 5)
    rules = [
        "1. Харид ≥ 260 с. → 1 хонача   2. 6 хонача → тӯҳфа",
        "3. Карточкаро ба корманд нишон диҳед   4. Як карточка = 1 тӯҳфа"
    ]
    for i, line in enumerate(rules):
        c.drawCentredString(width/2, rules_y + (1 - i)*3*mm, line)

    # Рамзи поёнӣ
    c.setFillColor(GREEN_DARK)
    c.rect(0, 0, width, 2.5*mm, fill=1, stroke=0)

    c.save()
    print(f"✅ Карточкаи Шаҳоб омода шуд: {filename}")

def create_staff_guide(filename="shahob_staff_guide.pdf"):
    c = canvas.Canvas(filename, pagesize=A5)
    width, height = A5

    # Барномаи боло
    c.setFillColor(GREEN_DARK)
    c.rect(0, height - 16*mm, width, 16*mm, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont('DejaVuBold', 13)
    c.drawCentredString(width/2, height - 7*mm, "РОҲНАМОИ КОРМАНД — ШАҲОБ")
    c.setFont('DejaVu', 8)
    c.drawCentredString(width/2, height - 12*mm, "«6 ХАРИД — 1 ТӮҲФА!»")

    y = height - 26*mm
    c.setFillColor(DARK)

    # 1
    c.setFont('DejaVuBold', 10)
    c.drawString(12*mm, y, "1. Кай хонача пур карда мешавад?")
    y -= 6*mm
    c.setFont('DejaVu', 9)
    c.drawString(14*mm, y, "• Харид ≥ 260 сомонӣ → 1 хонача пур кунед")
    y -= 5*mm
    c.drawString(14*mm, y, "• Харид < 260 сомонӣ → хонача ПУР НАКУНЕД")
    y -= 5*mm
    c.drawString(14*mm, y, "• Танҳо 1 хонача барои 1 хариди мувофиқ")

    y -= 8*mm
    c.setFont('DejaVuBold', 10)
    c.drawString(12*mm, y, "2. Кай карточка пурра мешавад?")
    y -= 6*mm
    c.setFont('DejaVu', 9)
    c.drawString(14*mm, y, "Вақте ки ҳамаи 6 хонача пур шуданд.")
    y -= 5*mm
    c.drawString(14*mm, y, "Ба мизоҷ бигӯед: «Табрик! Тӯҳфаи шумо омода аст!»")

    y -= 8*mm
    c.setFont('DejaVuBold', 10)
    c.drawString(12*mm, y, "3. Кай тӯҳфа дода мешавад?")
    y -= 6*mm
    c.setFont('DejaVu', 9)
    c.drawString(14*mm, y, "• Карточкаро гиред ва тафтиш кунед")
    y -= 5*mm
    c.drawString(14*mm, y, "• Сабади маҳсулотро (≈ 100 сомонӣ) омода кунед")
    y -= 5*mm
    c.drawString(14*mm, y, "• Карточкаро қайд кунед: «ТӮҲФА ДОДА ШУД»")
    y -= 5*mm
    c.drawString(14*mm, y, "• Карточкаи истифодашударо нигоҳ доред")

    y -= 8*mm
    c.setFont('DejaVuBold', 10)
    c.drawString(12*mm, y, "4. Муҳим!")
    y -= 6*mm
    c.setFont('DejaVu', 9)
    c.drawString(14*mm, y, "• Як карточка = танҳо як тӯҳфа")
    y -= 5*mm
    c.drawString(14*mm, y, "• Карточкаи қалбакӣ ё такрорӣ қабул накунед")
    y -= 5*mm
    c.drawString(14*mm, y, "• Агар шарти иловагӣ лозим бошад — аз мудир пурсед")

    # Ҷадвали хулоса
    y -= 12*mm
    c.setFillColor(GREEN_LIGHT)
    c.roundRect(10*mm, y - 22*mm, width - 20*mm, 28*mm, 3*mm, fill=1, stroke=0)

    c.setFillColor(GREEN_DARK)
    c.setFont('DejaVuBold', 9)
    c.drawCentredString(width/2, y, "ХУЛОСАИ ЗУД")

    c.setFont('DejaVu', 8)
    c.setFillColor(DARK)
    c.drawString(14*mm, y - 7*mm, "Харид ≥ 260 с.  →  1 хонача")
    c.drawString(14*mm, y - 12*mm, "6 хонача пур  →  тӯҳфа (сабад 100 с.)")
    c.drawString(14*mm, y - 17*mm, "Пас аз тӯҳфа  →  карточкаро қайд кунед")

    # Поён
    c.setFillColor(GREEN_DARK)
    c.rect(0, 0, width, 8*mm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('DejaVu', 7)
    c.drawCentredString(width/2, 3*mm, "Мағозаи хӯроквории «Шаҳоб»  •  6 харид = 1 тӯҳфа")

    c.save()
    print(f"✅ Роҳнамои корманд омода шуд: {filename}")

def create_poster_text(filename="shahob_kassa_poster.txt"):
    text = """═══════════════════════════════════════
        МАҒОЗАИ «ШАҲОБ»
═══════════════════════════════════════

   ★  6 ХАРИД — 1 ТӮҲФА!  ★

   АЗ 260 СОМОНӢ ХАРИД КУН!
   1 ХОНАЧА ПУР КУН!
   6 ХОНАЧА = ТӮҲФАИ 100 СОМОНӢ!

═══════════════════════════════════════
  Карточкаро гир → хоначаҳоро пур кун
         → тӯҳфа бигир!
═══════════════════════════════════════
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"✅ Матни реклама барои касса омода шуд: {filename}")

if __name__ == "__main__":
    create_card()
    create_staff_guide()
    create_poster_text()
