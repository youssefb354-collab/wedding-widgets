#!/usr/bin/env python3
"""Generate Canva-import HTML (13 website sections, 1366x768 each) for 6 wedding designs,
plus art-placement JSON used to drop the watercolor art in after import."""
import json, html, os
from urllib.parse import quote

BASE = "https://youssefb354-collab.github.io/wedding-widgets"
W, H = 1366, 768
OUT = os.path.dirname(os.path.abspath(__file__))

T = {
  "sage":       dict(bg="#F7F4EE", alt="#ECEFE5", card="#FFFFFF", ink="#2C3729", soft="#5B6756", line="#D8DDCD", acc="#7D8F6E", acc2="#B39566", btn="#56694A", btnInk="#FFFFFF",
                     disp="Cormorant Garamond", script="Pinyon Script", body="Montserrat", ital="Cormorant Garamond", names="script", layout="classic", hero="hero.jpg", dark=False, caps=False),
  "oldmoney":   dict(bg="#F3EDE2", alt="#E9E0CF", card="#FBF7F0", ink="#2E2A1F", soft="#5F5645", line="#D8CBB3", acc="#5D6B3B", acc2="#7A2434", btn="#6B1F2E", btnInk="#FBF7F0",
                     disp="Prata", script="Pinyon Script", body="EB Garamond", ital="Cormorant Garamond", names="disp", layout="classic", hero="hero-oldmoney.jpg", dark=False, caps=False, polaroid=True),
  "bordeaux":   dict(bg="#F6EFE6", alt="#EEE1D3", card="#FFFBF6", ink="#351820", soft="#6B4A4F", line="#E0CDBD", acc="#7A2434", acc2="#B08A57", btn="#6B1F2E", btnInk="#FFF8F0",
                     disp="Playfair Display", script="Pinyon Script", body="EB Garamond", ital="Playfair Display", names="disp", layout="editorial", hero="hero-bordeaux.jpg", dark=False, caps=False, polaroid=True),
  "terracotta": dict(bg="#F6EEE3", alt="#EFDFCB", card="#FFF9F1", ink="#3A2A20", soft="#6B5646", line="#E4CFB8", acc="#B5583A", acc2="#6F7442", btn="#A04B30", btnInk="#FFF9F1",
                     disp="DM Serif Display", script="Alex Brush", body="Lato", ital="Cormorant Garamond", names="disp", layout="arch", hero="hero-terracotta.jpg", dark=False, caps=True),
  "midnight":   dict(bg="#121927", alt="#19223A", card="#1F2A44", ink="#F2ECE0", soft="#BDB7AB", line="#34405C", acc="#C9A96E", acc2="#8FA3C7", btn="#C9A96E", btnInk="#121927",
                     disp="Cinzel", script="Great Vibes", body="Montserrat", ital="Cormorant Garamond", names="disp", layout="split", hero="hero-midnight.jpg", dark=True, caps=True),
  "dustyblue":  dict(bg="#F3F5F7", alt="#E4EBF1", card="#FFFFFF", ink="#22303D", soft="#536477", line="#D2DCE6", acc="#6F8FAF", acc2="#BC9C74", btn="#4C6C8C", btnInk="#FFFFFF",
                     disp="Cormorant Garamond", script="Parisienne", body="Lato", ital="Cormorant Garamond", names="script", layout="arch", hero="hero-dustyblue.jpg", dark=False, caps=False, archLeft=True),
}
NAMES = ("Amelia", "James")
DATE_LONG = "Saturday, 12 June 2027"
CITY = "Provence, France"
MONO = "A & J"

def esc(s): return html.escape(s, quote=True)

class Page:
    def __init__(self, label, bg):
        self.label, self.bg, self.items, self.art = label, bg, [], []
    def add(self, s): self.items.append(s)
    def text(self, txt, x, y, w, font, size, color, align="center", weight=400, italic=False, spacing=0, upper=False, lh=1.25, href=None):
        st = (f"left:{x}px;top:{y}px;width:{w}px;font-family:'{font}';font-size:{size}px;color:{color};text-align:{align};"
              f"font-weight:{weight};line-height:{lh};letter-spacing:{spacing}px;" + ("font-style:italic;" if italic else "") + ("text-transform:uppercase;" if upper else ""))
        body = esc(txt).replace("\n", "<br>")
        if href: body = f'<a href="{esc(href)}" style="color:{color};text-decoration:none">{body}</a>'
        self.add(f'<p class="a" style="{st}">{body}</p>')
    def rect(self, x, y, w, h, fill="transparent", radius=0, border=None, opacity=1, rot=0):
        b = f"border:{border};" if border else ""
        self.add(f'<div class="a" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{fill};border-radius:{radius};{b}opacity:{opacity};transform:rotate({rot}deg)"></div>')
    def img(self, src, x, y, w, h, radius="0", rot=0, alt="Photo"):
        self.add(f'<img class="a" src="{BASE}/photos/{src}" alt="{esc(alt)}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;object-fit:cover;border-radius:{radius};transform:rotate({rot}deg)">')
    def button(self, label, href, x, y, w, t, ghost=False, h=52, font=None, square=False, light=False):
        fill = "transparent" if ghost else t["btn"]
        col = (("#FFFFFF" if light else t["ink"]) if ghost else t["btnInk"])
        border = f"1px solid {'#FFFFFF' if light else t['soft']}" if ghost else "0"
        r = "0" if square else f"{h//2}px"
        self.add(f'<a class="a" href="{esc(href)}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;line-height:{h}px;background:{fill};border:{border};border-radius:{r};'
                 f'color:{col};text-align:center;text-decoration:none;font-family:\'{font or t["body"]}\';font-size:13px;letter-spacing:3px;font-weight:600;text-transform:uppercase">{esc(label)}</a>')
    def place(self, kind, x, y, w, rot=0, h=None):
        self.art.append(dict(kind=kind, left=x, top=y, width=w, height=h, rotation=rot))
    def html(self):
        return (f'<section data-document-role="page" data-label="{esc(self.label)}" style="position:relative;width:{W}px;height:{H}px;overflow:hidden;background:{self.bg}">'
                + "".join(self.items) + "</section>")

def title(p, t, txt, y=70, color=None, sub=None, swag=None):
    p.text(txt, 0, y, W, t["script"], 92, color or t["acc"], lh=1.1)
    if sub: p.text(sub, 0, y + 112, W, t["body"], 14, t["soft"], spacing=4, upper=True)
    if swag is not None: p.place("swag", 533, swag, 300)

def build(key):
    t = T[key]; pages = []; dark = t["dark"]
    on_photo = "#FFFFFF"
    rsvp = f"{BASE}/rsvp.html?theme={key}&meals=Lamb|Sea%20bass|Vegetarian&max=6&shuttle=1&song=1&deadline=2027-04-01&tz=Europe/Paris"
    cal = f"{BASE}/calendar.html?theme={key}&start=2027-06-12T16:00&tz=Europe/Paris&title={quote('Amelia & James — Wedding')}&loc={quote('Domaine des Oliviers, Aix-en-Provence')}"
    maps = "https://www.google.com/maps/search/?api=1&query=" + quote("Domaine des Oliviers, Aix-en-Provence, France")
    namefont = t["script"] if t["names"] == "script" else t["disp"]
    names_upper = t["caps"] and t["names"] == "disp"

    # 1 COVER — envelope
    p = Page("Welcome", t["alt"])
    p.place("corner", -20, -20, 430); p.place("corner", 956, 358, 430, rot=180)
    p.text("You are invited", 0, 92, W, t["body"], 14, t["soft"], spacing=6, upper=True)
    p.text(f"{NAMES[0]} & {NAMES[1]}", 0, 124, W, t["script"], 72, t["acc"] if not dark else t["acc"], lh=1.1)
    p.place("envelope", 443, 228, 480)
    p.text(DATE_LONG, 0, 600, W, t["body"], 15, t["soft"], spacing=5, upper=True)
    p.button("Tap to open", "#Our%20Day", 573, 640, 220, t, ghost=True)
    pages.append(p)

    # 2 HERO
    p = Page("Our Day", t["bg"])
    L = t["layout"]
    if L == "classic":
        p.img(t["hero"], 0, 0, W, H, alt="The couple")
        p.rect(0, 0, W, H, fill="#14100A", opacity=.48)
        p.text("Together with their families", 0, 150, W, t["body"], 14, on_photo, spacing=6, upper=True)
        if t["names"] == "script":
            p.text(f"{NAMES[0]} & {NAMES[1]}", 0, 196, W, t["script"], 132, on_photo, lh=1.05)
            y = 362
        else:
            p.text(NAMES[0], 0, 186, W, t["disp"], 104, on_photo, lh=1)
            p.text("&", 0, 296, W, t["ital"], 46, on_photo, italic=True, lh=1)
            p.text(NAMES[1], 0, 346, W, t["disp"], 104, on_photo, lh=1)
            y = 470
        p.text("invite you to celebrate their wedding", 0, y, W, t["ital"], 28, on_photo, italic=True)
        p.text(f"{DATE_LONG}  ·  {CITY}", 0, y + 52, W, t["body"], 15, on_photo, spacing=5, upper=True)
        p.button("RSVP", rsvp, 513, y + 104, 150, t)
        p.button("Save the date", cal, 683, y + 104, 190, t, ghost=True, light=True)
    elif L == "editorial":
        p.img(t["hero"], 716, 64, 590, 640, alt="The couple")
        p.rect(732, 80, 558, 608, border="1px solid #FFFFFF", opacity=.7)
        p.text("Together with their families", 90, 150, 560, t["body"], 13, t["soft"], align="start", spacing=5, upper=True)
        p.text(NAMES[0], 86, 190, 600, t["disp"], 118, t["ink"], align="start", lh=1)
        p.text("&", 220, 304, 200, t["script"], 92, t["acc2"], align="start", lh=1)
        p.text(NAMES[1], 86, 380, 600, t["disp"], 118, t["ink"], align="start", lh=1)
        p.text("invite you to celebrate their wedding", 90, 520, 560, t["ital"], 26, t["ink"], align="start", italic=True)
        p.text(f"{DATE_LONG}  ·  {CITY}", 90, 566, 600, t["body"], 13, t["soft"], align="start", spacing=4, upper=True)
        p.button("RSVP", rsvp, 90, 612, 150, t, square=True)
        p.button("Save the date", cal, 256, 612, 200, t, ghost=True, square=True)
    elif L == "arch":
        left = t.get("archLeft", False)
        ax = 150 if left else 806
        tx = 620 if left else 60
        p.place("corner", (W - 300) if left else -30, -30 if left else 498, 300, rot=(90 if left else 270))
        p.rect(ax - 14, 66, 438, 650, radius="219px 219px 18px 18px", border=f"1px solid {t['line']}")
        p.img(t["hero"], ax, 80, 410, 622, radius="205px 205px 12px 12px", alt="The couple")
        p.text("Together with their families", tx, 180, 690, t["body"], 13, t["soft"], spacing=5, upper=True)
        if t["names"] == "script":
            p.text(f"{NAMES[0]} & {NAMES[1]}", tx, 236, 690, t["script"], 80, t["ink"], lh=1.1)
            y = 350
        else:
            p.text(f"{NAMES[0]}", tx, 220, 690, t["disp"], 88, t["ink"], upper=names_upper, spacing=4, lh=1)
            p.text("&", tx, 312, 690, t["script"], 80, t["acc"], lh=1)
            p.text(f"{NAMES[1]}", tx, 390, 690, t["disp"], 88, t["ink"], upper=names_upper, spacing=4, lh=1)
            y = 500
        p.text("invite you to celebrate their wedding", tx, y, 690, t["ital"], 26, t["ink"], italic=True)
        p.text(f"{DATE_LONG}  ·  {CITY}", tx, y + 48, 690, t["body"], 13, t["soft"], spacing=4, upper=True)
        p.button("RSVP", rsvp, tx + 175, y + 96, 150, t)
        p.button("Save the date", cal, tx + 341, y + 96, 190, t, ghost=True)
    elif L == "split":
        p.img(t["hero"], 0, 0, 600, H, alt="The couple")
        p.rect(0, 0, 600, H, fill="#080C16", opacity=.25)
        p.place("corner", 1096, -20, 290, rot=90)
        p.text("Together with their families", 600, 170, 766, t["body"], 13, t["soft"], spacing=6, upper=True)
        p.text(NAMES[0], 600, 214, 766, t["disp"], 82, t["ink"], spacing=10, upper=True, lh=1)
        p.text("&", 600, 300, 766, t["script"], 78, t["acc"], lh=1)
        p.text(NAMES[1], 600, 376, 766, t["disp"], 82, t["ink"], spacing=10, upper=True, lh=1)
        p.text("invite you to celebrate their wedding", 600, 490, 766, t["ital"], 26, t["ink"], italic=True)
        p.text(f"{DATE_LONG}  ·  {CITY}", 600, 536, 766, t["body"], 13, t["soft"], spacing=5, upper=True)
        p.button("RSVP", rsvp, 818, 586, 150, t)
        p.button("Save the date", cal, 984, 586, 190, t, ghost=True)
    pages.append(p)

    # 3 SAVE THE DATE + COUNTDOWN
    p = Page("Save the Date", t["alt"])
    title(p, t, "Save the Date", y=56, swag=140)
    p.text("12 · 06 · 2027", 0, 240, W, t["disp"], 96, t["ink"], spacing=6, lh=1)
    p.text("Ceremony at 4:00 pm  ·  Domaine des Oliviers", 0, 370, W, t["body"], 15, t["soft"], spacing=4, upper=True)
    for i, (n, lab) in enumerate([("240", "Days"), ("22", "Hours"), ("41", "Minutes"), ("55", "Seconds")]):
        x = 343 + i * 176
        rad = "80px 80px 12px 12px" if L == "arch" else ("0" if L == "editorial" else "14px")
        p.rect(x, 430, 152, 150, fill=t["card"], radius=rad, border=f"1px solid {t['line']}")
        p.text(n, x, 462, 152, t["disp"], 54, t["acc"], lh=1)
        p.text(lab, x, 536, 152, t["body"], 12, t["soft"], spacing=3, upper=True)
    p.button("Add to calendar", cal, 563, 624, 240, t, square=(L == "editorial"))
    pages.append(p)

    # 4 OUR STORY
    p = Page("Our Story", t["bg"])
    title(p, t, "Our Story", y=40)
    story = [("story-1.jpg", "2019", "First hello", "A rainy afternoon, one shared umbrella and a coffee that turned into a four-hour conversation."),
             ("story-2.jpg", "2022", "Our first home", "Two cities, too many boxes and one very spoiled cat named Olive."),
             ("story-3.jpg", "2026", "The question", "At sunset on the beach, James asked — and Amelia said yes before he finished.")]
    for i, (ph, yr, ttl, txt) in enumerate(story):
        x = 133 + i * 390
        if t.get("polaroid"):
            rot = [-2.5, 2, -1.5][i]
            p.rect(x, 200, 320, 330, fill="#FFFDF8", rot=rot)
            p.img(ph, x + 14, 214, 292, 250, rot=rot, alt=ttl)
            p.rect(x + 112, 188, 96, 26, fill=t["line"], opacity=.85, rot=rot - 3)
            p.text(yr, x, 474, 320, t["script"], 34, "#3A3530")
        else:
            rad = "160px 160px 12px 12px" if L == "arch" else ("0" if L == "editorial" else "14px")
            p.img(ph, x + 10, 200, 300, 320, radius=rad, alt=ttl)
            p.text(yr, x, 536, 320, t["body"], 13, t["acc"], spacing=5, upper=True)
        p.text(ttl, x, 560, 320, t["ital"], 32, t["ink"], italic=True)
        p.text(txt, x + 10, 608, 300, t["body"], 15, t["soft"], lh=1.6)
    pages.append(p)

    # 5 THE DAY
    p = Page("The Day", t["alt"])
    title(p, t, "The Day", y=40, sub=DATE_LONG, swag=168)
    sched = [("15:30", "Guests arrive", "Welcome drinks in the olive grove"), ("16:00", "Ceremony", "Garden terrace"), ("17:00", "Cocktail hour", "Canapés & live strings"),
             ("19:00", "Dinner & speeches", "Under the plane trees"), ("21:30", "Cake cutting", "With a toast"), ("22:00", "Dancing", "Until the last song")]
    for i, (tm, ttl, note) in enumerate(sched):
        col, row = i % 3, i // 3
        x, y = 163 + col * 360, 290 + row * 220
        p.rect(x + 130, y, 80, 80, fill=t["card"], radius="40px", border=f"1px solid {t['line']}")
        p.text(tm, x + 130, y + 24, 80, t["disp"], 22, t["acc"], lh=1.2)
        p.text(ttl, x, y + 96, 340, t["disp"], 26, t["ink"])
        p.text(note, x, y + 136, 340, t["body"], 15, t["soft"])
    pages.append(p)

    # 6 VENUE
    p = Page("The Venue", t["bg"])
    title(p, t, "The Venue", y=40)
    rad = "220px 220px 14px 14px" if L == "arch" else ("0" if L == "editorial" else "16px")
    p.img("venue.jpg", 130, 200, 560, 470 if L != "arch" else 500, radius=rad, alt="Venue")
    p.text("Domaine des Oliviers", 760, 230, 500, t["disp"], 40, t["ink"], align="start", upper=names_upper)
    p.text("Chemin des Oliviers, 13100\nAix-en-Provence, France", 760, 300, 480, t["body"], 17, t["soft"], align="start", lh=1.6)
    p.text("Free parking on site. The ceremony is outdoors on grass — block heels recommended.", 760, 384, 470, t["body"], 16, t["soft"], align="start", lh=1.6)
    p.button("Google Maps", maps, 760, 490, 200, t, square=(L == "editorial"))
    p.button("Apple Maps", "https://maps.apple.com/?q=" + quote("Domaine des Oliviers, Aix-en-Provence"), 976, 490, 190, t, ghost=True, square=(L == "editorial"))
    p.text("Tip: add a live map with Apps › Embed › Google Maps", 760, 572, 470, t["body"], 13, t["soft"], align="start", italic=True)
    pages.append(p)

    # 7 TRAVEL & STAY
    p = Page("Travel & Stay", t["alt"])
    title(p, t, "Travel & Stay", y=40)
    p.text("Marseille airport (MRS) is 35 minutes away. A shuttle runs from the hotels below at 15:00 and back at midnight.", 283, 200, 800, t["body"], 17, t["soft"], lh=1.6)
    hotels = [("8 min drive", "Hôtel Le Pigonnet", "10% off until 1 March", "AMELIAJAMES27"), ("12 min drive", "Villa Gallici", "Room block of 15 rooms", "WEDDING-AJ"), ("Nearby villages", "Airbnb & gîtes", "Search Puyricard or Éguilles", "")]
    for i, (dist, name, note, code) in enumerate(hotels):
        x = 133 + i * 390
        rad = "150px 150px 14px 14px" if L == "arch" else ("0" if L == "editorial" else "16px")
        p.rect(x, 300, 320, 380, fill=t["card"], radius=rad, border=f"1px solid {t['line']}")
        p.text(dist, x, 370 if L == "arch" else 340, 320, t["body"], 12, t["acc"], spacing=4, upper=True)
        p.text(name, x, 404 if L == "arch" else 374, 320, t["disp"], 28, t["ink"], upper=names_upper)
        p.text(note, x + 20, 454 if L == "arch" else 424, 280, t["body"], 15, t["soft"])
        if code:
            p.rect(x + 50, 504 if L == "arch" else 480, 220, 44, radius="8px", border=f"1px dashed {t['acc']}")
            p.text(f"Code: {code}", x + 50, 516 if L == "arch" else 492, 220, t["body"], 14, t["ink"], weight=600)
        p.button("Book", "https://www.booking.com", x + 100, 596, 120, t, ghost=True, h=46, square=(L == "editorial"))
    pages.append(p)

    # 8 DRESS CODE
    p = Page("Dress Code", t["bg"])
    p.place("corner", -20, -20, 380); p.place("corner", 1006, 408, 380, rot=180)
    title(p, t, "Dress Code", y=60, swag=150)
    p.text("Garden formal", 0, 250, W, t["ital"], 44, t["ink"], italic=True)
    p.text("Think flowing fabrics and soft tones. Please avoid white and ivory.\nEvenings get cool — bring a layer.", 283, 330, 800, t["body"], 18, t["soft"], lh=1.7)
    pal = {"sage": ["#8A9A7B", "#C9B8A3", "#E8DCCB", "#B89B6A", "#6E7F6A"], "oldmoney": ["#5D6B3B", "#7A2434", "#C9B48E", "#E9E0CF", "#2E2A1F"],
           "bordeaux": ["#6B1F2E", "#A8475A", "#D9B8B0", "#B08A57", "#F1E4D6"], "terracotta": ["#B5583A", "#D99A6C", "#E8CBA8", "#6F7442", "#F3E6D3"],
           "midnight": ["#1D2433", "#34405C", "#C9A96E", "#E9E0CF", "#8FA3C7"], "dustyblue": ["#6F8FAF", "#A9BFD3", "#E4EBF1", "#BC9C74", "#45627F"]}[key]
    for i, c in enumerate(pal):
        p.rect(458 + i * 94, 470, 70, 70, fill=c, radius="35px", border=f"3px solid {t['card']}")
    pages.append(p)

    # 9 GALLERY
    p = Page("Moments", t["alt"])
    title(p, t, "Moments", y=30)
    g = [("gallery-1.jpg", 133, 180, 520, 520), ("gallery-2.jpg", 673, 180, 270, 250), ("gallery-3.jpg", 963, 180, 270, 250),
         ("gallery-4.jpg", 673, 450, 270, 250), ("gallery-5.jpg", 963, 450, 270, 250)]
    for (ph, x, y, w, h) in g:
        rad = "140px 140px 10px 10px" if L == "arch" else ("0" if L == "editorial" else "12px")
        p.img(ph, x, y, w, h, radius=rad, alt="Moment")
    pages.append(p)

    # 10 GIFTS / LIVE / PHOTOS
    p = Page("Gifts", t["bg"])
    title(p, t, "With Love", y=40)
    cards = [("Gifts", "Your presence is our greatest gift. If you wish, contribute to our honeymoon in Japan.", "Honeymoon fund", "https://www.paypal.com"),
             ("Watch Live", "Can’t be with us? Join the ceremony live — the link opens 15 minutes before.", "Watch live", "https://www.youtube.com"),
             ("Share Photos", "Upload your photos to our shared album and use #AmeliaAndJamesSayIDo", "Open album", "https://photos.google.com")]
    for i, (ttl, txt, lab, url) in enumerate(cards):
        x = 133 + i * 390
        rad = "150px 150px 14px 14px" if L == "arch" else ("0" if L == "editorial" else "16px")
        p.rect(x, 210, 320, 440, fill=t["card"], radius=rad, border=f"1px solid {t['line']}")
        p.text(ttl, x, 290, 320, t["disp"], 32, t["ink"], upper=names_upper)
        p.text(txt, x + 30, 352, 260, t["body"], 16, t["soft"], lh=1.6)
        p.button(lab, url, x + 50, 560, 220, t, h=48, square=(L == "editorial"))
    pages.append(p)

    # 11 FAQ
    p = Page("Questions", t["alt"])
    title(p, t, "Questions", y=30)
    faq = [("Can I bring a plus-one?", "Everyone invited is named in your RSVP. If your invitation says “and guest”, you’ll see a space for their name."),
           ("Are children invited?", "We love your little ones, but our celebration is adults-only (babies in arms welcome)."),
           ("When is the RSVP deadline?", "Please reply by 1 April 2027 so we can confirm numbers with the caterer."),
           ("Will the ceremony be unplugged?", "Yes — please keep phones away during the ceremony. Our photographer has it covered!"),
           ("Is there parking?", "Yes, free on-site parking. Taxis can be booked through the venue for the ride home."),
           ("What should I wear?", "Garden formal — see the Dress Code section for our palette.")]
    for i, (q, a) in enumerate(faq):
        col, row = i % 2, i // 2
        x, y = 153 + col * 560, 190 + row * 180
        p.text(q, x, y, 500, t["disp"], 24, t["ink"], align="start")
        p.text(a, x, y + 46, 500, t["body"], 16, t["soft"], align="start", lh=1.6)
        p.rect(x, y + 150, 500, 1, fill=t["line"])
    pages.append(p)

    # 12 RSVP
    p = Page("RSVP", t["bg"])
    p.place("corner", -20, -20, 400); p.place("corner", 986, 388, 400, rot=180)
    rad = "300px 300px 24px 24px" if L == "arch" else ("0" if L == "editorial" else "24px")
    p.rect(333, 120, 700, 540, fill=t["card"], radius=rad, border=f"1px solid {t['line']}")
    p.text("RSVP", 333, 190 if L == "arch" else 170, 700, t["script"], 104, t["acc"], lh=1.1)
    p.text("Kindly reply by 1 April 2027", 333, 320, 700, t["ital"], 26, t["soft"], italic=True)
    p.text("One reply for your whole household — names, meals and dietary needs.\nIt takes one minute.", 393, 372, 580, t["body"], 16, t["soft"], lh=1.7)
    p.button("Reply now", rsvp, 563, 470, 240, t, h=58, square=(L == "editorial"))
    p.button("Add to calendar", cal, 583, 548, 200, t, ghost=True, h=46, square=(L == "editorial"))
    pages.append(p)

    # 13 THANK YOU
    p = Page("Thank You", t["alt"])
    p.place("swag", 433, 50, 500)
    p.text(MONO, 0, 250, W, t["script"], 120, t["acc"], lh=1.1)
    p.text(f"{DATE_LONG}  ·  {CITY}", 0, 420, W, t["body"], 15, t["soft"], spacing=5, upper=True)
    p.text("Questions? hello@ameliaandjames.com", 0, 470, W, t["body"], 16, t["soft"], href="mailto:hello@ameliaandjames.com")
    p.text("#AmeliaAndJamesSayIDo", 0, 510, W, t["ital"], 26, t["ink"], italic=True)
    p.place("swag", 433, 540, 500)
    pages.append(p)

    fonts = "family=" + "&family=".join(sorted({f.replace(" ", "+") + (":ital,wght@0,400;0,600;1,400" if f in ("EB Garamond", "Cormorant Garamond", "Playfair Display") else "") for f in (t["disp"], t["script"], t["body"], t["ital"])}))
    doc = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{esc(key.title())} Wedding Website — Canva template</title>'
           f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fonts}&display=swap">'
           '<style>body{margin:0;background:#888}section{margin:0 auto 24px}.a{position:absolute;margin:0;box-sizing:border-box}p.a{white-space:normal}</style></head><body>'
           + "\n".join(pg.html() for pg in pages) + "</body></html>")
    open(os.path.join(OUT, f"{key}.html"), "w").write(doc)
    json.dump([{"page": i + 1, "label": pg.label, "art": pg.art} for i, pg in enumerate(pages)], open(os.path.join(OUT, f"{key}-art.json"), "w"), indent=1)
    return len(pages), sum(len(pg.art) for pg in pages)

if __name__ == "__main__":
    for k in T: print(k, build(k))
