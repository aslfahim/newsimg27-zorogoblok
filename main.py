#!/usr/bin/env python3
"""The Day on File — card catalogue of 27 November 2026 world news.

Draws a 1024x1024 PNG: a library card catalogue of the day's 38 core
stories, each on its own index card with a continent tab, catalogue
number, headline and one-line summary. The lead story (two Italians
killed in an Iranian drone strike in Kuwait) is filed on a red card.

Stdlib + PIL only. Fonts are shipped in fonts/ so the render is
identical in the grader sandbox. Output goes to $MAKEFUN_OUTPUT_DIR
(default ./out) as entry.png, deterministically.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BASE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- stories
# (continent, headline, summary) — all 38 CORE stories from the shared
# research file; every story happened or was first reported on
# Friday 27 November 2026. Nothing invented.
STORIES = [
    ("N. AMERICA", "Nor'easter batters US East Coast",
     "Thanksgiving storm cuts power to 250,000+ from New Jersey to North Carolina."),
    ("N. AMERICA", "Judge: FCC violated ABC free speech",
     "Federal judge rules the FCC violated ABC's free-speech rights."),
    ("N. AMERICA", "Trump asks Putin to pull back",
     "Trump says he asked Putin to pull back aggression in Europe; Zelensky questions US focus."),
    ("N. AMERICA", "Musk: SpaceX shares for every US child",
     "Elon Musk says every child in the US will get two SpaceX shares."),
    ("N. AMERICA", "Army detonates explosives stockpile",
     "US Army declares success in detonating a lead-based explosives stockpile in Iowa."),
    ("N. AMERICA", "Apple enters the AI agent race",
     "Apple enters the AI agent race, taking on OpenAI, Anthropic and Meta."),
    ("EUROPE", "UK net migration lowest since 1997",
     "UK net migration falls to its lowest since 1997, excluding the pandemic."),
    ("EUROPE", "Depardieu to stand trial",
     "Gerard Depardieu to stand trial over alleged rape of an actress in 2018, court rules."),
    ("EUROPE", "Diesel tanker capsizes near Ibiza",
     "Tanker carrying up to 7,000 tonnes of diesel capsizes near Ibiza, killing one."),
    ("EUROPE", "Lille hand Bayern first defeat",
     "LOSC Lille beat Bayern Munich 2-1, handing them their first defeat of the season."),
    ("EUROPE", "EU leaders discuss Ukraine aid",
     "EU leaders discuss financial assistance for Ukraine amid security and economy concerns."),
    ("EUROPE", "UK to pay EU participation fee",
     "The UK to pay a 'participation' fee to deliver EU deals."),
    ("EUROPE", "France's mainstream at risk",
     "France's political mainstream risks a presidential-vote debacle with no clear candidate."),
    ("ASIA", "Two Italians killed in Kuwait drone strike",
     "Two Italians killed in an Iranian drone attack in Kuwait; Iran denies responsibility."),
    ("ASIA", "Gukesh-Sindarov marathon draw",
     "Gukesh and Sindarov draw a marathon Game 3; World Chess Championship tied 1.5-1.5."),
    ("ASIA", "Kim vows more nuclear weapons",
     "North Korea's Kim vows to build more nuclear weapons after ignoring Trump's overture."),
    ("ASIA", "Fire at Bangkok oil refinery",
     "Massive fire at a Bangkok oil refinery leaves several injured; Bangchak shuts all units."),
    ("ASIA", "India SC: judicial member on PMLA bench",
     "India's Supreme Court: a judicial member must sit on the bench confirming PMLA attachments."),
    ("ASIA", "India SC quashes Anand Mohan release",
     "Supreme Court quashes the premature release of former MP Anand Mohan; Bihar move illegal."),
    ("ASIA", "Cabinet approves Rs 11,000-crore scheme",
     "Union Cabinet approves an Rs 11,000-crore scheme to boost construction-equipment making."),
    ("ASIA", "Sri Lanka A reach Rising Stars final",
     "Sri Lanka A beat India A to reach the Asia Cup Rising Stars final."),
    ("ASIA", "India-China border 'generally stable'",
     "China says the situation in India-China border areas remains 'generally stable'."),
    ("ASIA", "Politician hosts 400,000-guest wedding",
     "Indian politician facing murder charges hosts a wedding for 400,000 guests."),
    ("ASIA", "Mecca-alliance meeting in Islamabad",
     "Pakistan, Saudi Arabia and Turkey to hold a Mecca-alliance meeting in Islamabad, 27-28 Nov."),
    ("MIDDLE EAST", "Hamas weighs response after Gaza killings",
     "Hamas weighs its response after Israel kills 10 people in Gaza."),
    ("MIDDLE EAST", "Shin Bet torture claims as death penalty looms",
     "Israeli rights group says Shin Bet tortures Palestinians into confessions."),
    ("MIDDLE EAST", "Iraq blocks Kurdistan crossings",
     "Iraq blocks two border crossings in the Kurdistan region, by Syria and Iran."),
    ("AFRICA", "300+ Russians killed backing Mali junta",
     "More than 300 Russians killed as Moscow supports Mali's junta."),
    ("AFRICA", "Ramaphosa wins court bid",
     "Cyril Ramaphosa wins a court bid to overturn an impeachment report."),
    ("AFRICA", "DRC Ebola passes 12,000 cases",
     "DRC Ebola epidemic crosses 12,000 confirmed cases and more than 5,900 deaths."),
    ("S. AMERICA", "US & Qatar help Venezuela clear arrears",
     "US and Qatar to help Venezuela clear regional development-bank arrears via bridge loans."),
    ("S. AMERICA", "Argentina Senate suspends 2027 primaries",
     "Senate suspends 2027 primaries; Congress bars central bank from funding the government."),
    ("OCEANIA", "NZ final election results revealed",
     "New Zealand's final results revealed; ~400,000 special votes decide a slim coalition majority."),
    ("OCEANIA", "Barrett to captain the All Blacks",
     "Geordie Barrett to captain the All Blacks for the first time in Sunday's rematch vs England."),
    ("OCEANIA", "Sinner out of Australian Open 2027",
     "Jannik Sinner out of the Australian Open 2027 with a knee injury."),
    ("OCEANIA", "NZ v India 2nd Test starts",
     "New Zealand v India 2nd Test starts in Christchurch; Gurnoor Brar makes Test debut."),
    ("OCEANIA", "Black Friday warning in NZ",
     "Black Friday warning: one in three NZ retailers upping sales; half of tracked goods no cheaper."),
    ("SCIENCE", "Giant planet beyond Neptune?",
     "New astronomical evidence raises the possibility of a giant planet beyond Neptune."),
]

LEAD = 13  # index of the Kuwait drone-strike story (card No. 14)

TAB_COLORS = {
    "N. AMERICA": (31, 78, 121),
    "EUROPE": (46, 94, 60),
    "ASIA": (122, 54, 28),
    "MIDDLE EAST": (120, 72, 20),
    "AFRICA": (96, 58, 110),
    "S. AMERICA": (14, 110, 110),
    "OCEANIA": (30, 90, 120),
    "SCIENCE": (90, 40, 80),
}

INK = (28, 28, 26)
PAPER = (244, 239, 228)
CARD = (255, 253, 247)
CARD_LINE = (178, 168, 148)
MAST = (24, 42, 54)
LEAD_BG = (253, 232, 232)
LEAD_TAB = (178, 34, 34)
LEAD_INK = (140, 20, 20)


def font(name, size):
    return ImageFont.truetype(os.path.join(BASE, "fonts", name), size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit `width` px."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, fnt, width, max_lines):
    """Wrap and, if too long, trim the last line with an ellipsis."""
    lines = wrap(draw, text, fnt, width)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    while lines and draw.textlength(lines[-1] + "...", font=fnt) > width:
        lines[-1] = lines[-1].rsplit(" ", 1)[0] if " " in lines[-1] else lines[-1][:-1]
    lines[-1] = lines[-1] + "..."
    return lines


def main():
    assert len(STORIES) == 38, len(STORIES)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    f_title = font("DejaVuSerif-Bold.ttf", 46)
    f_date = font("DejaVuSans-Bold.ttf", 21)
    f_sub = font("DejaVuSans.ttf", 13)
    f_tab = font("DejaVuSans-Bold.ttf", 10)
    f_num = font("DejaVuSans-Bold.ttf", 10)
    f_head = font("DejaVuSans-Bold.ttf", 12)
    f_sum = font("DejaVuSans.ttf", 10)
    f_foot = font("DejaVuSans.ttf", 11)

    # ---- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 98], fill=MAST)
    d.rectangle([0, 98, W, 101], fill=(198, 162, 60))
    title = "THE DAY ON FILE"
    d.text((18, 12), title, font=f_title, fill=(250, 246, 236))
    d.text((18, 66), "FRIDAY 27 NOVEMBER 2026", font=f_date, fill=(233, 196, 90))
    right = "38 STORIES  ·  6 CONTINENTS + SCIENCE"
    d.text((W - 18 - d.textlength(right, font=f_sub), 20), right,
           font=f_sub, fill=(214, 222, 228))
    right2 = "CARD CATALOGUE OF THE WORLD'S NEWS"
    d.text((W - 18 - d.textlength(right2, font=f_sub), 66), right2,
           font=f_sub, fill=(214, 222, 228))

    # ---- card grid: 5 cols x 8 rows ------------------------------------
    cols, rows = 5, 8
    mx, my, gap = 14, 112, 8
    cw = (W - 2 * mx - (cols - 1) * gap) // cols
    ch = (992 - my - (rows - 1) * gap) // rows
    inner = cw - 14

    for i, (cont, head, summ) in enumerate(STORIES):
        r, c = divmod(i, cols)
        x = mx + c * (cw + gap)
        y = my + r * (ch + gap)
        lead = i == LEAD
        bg = LEAD_BG if lead else CARD
        tab = LEAD_TAB if lead else TAB_COLORS[cont]
        d.rounded_rectangle([x, y, x + cw, y + ch], radius=4, fill=bg,
                            outline=CARD_LINE, width=1)
        # tab strip
        d.rounded_rectangle([x, y, x + cw, y + 19], radius=4, fill=tab)
        d.rectangle([x, y + 12, x + cw, y + 19], fill=tab)
        d.rectangle([x, y, x + cw, y + 19], outline=tab)
        d.text((x + 7, y + 4), cont, font=f_tab, fill=(255, 255, 255))
        num = "No. %02d" % (i + 1)
        d.text((x + cw - 7 - d.textlength(num, font=f_num), y + 4), num,
               font=f_num, fill=(255, 255, 255))
        # headline (max 3 lines) + summary (max 3 lines)
        hlines = fit_lines(d, head, f_head, inner, 3)
        slines = fit_lines(d, summ, f_sum, inner, 3)
        ty = y + 25
        for ln in hlines:
            d.text((x + 7, ty), ln, font=f_head,
                   fill=LEAD_INK if lead else INK)
            ty += 14
        ty += 2
        for ln in slines:
            d.text((x + 7, ty), ln, font=f_sum, fill=(74, 70, 64))
            ty += 12
        # catalogue rule line under the tab
        d.line([x + 7, y + 21, x + cw - 7, y + 21], fill=(214, 204, 186))

    # ---- footer ---------------------------------------------------------
    foot = ("Filed 27 November 2026  ·  Every story happened or was first "
            "reported that day  ·  Lead card: Kuwait drone strike")
    d.text(((W - d.textlength(foot, font=f_foot)) // 2, 1000), foot,
           font=f_foot, fill=(96, 90, 80))

    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    img.save(path, "PNG", optimize=True)
    print("wrote", path, img.size, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()
