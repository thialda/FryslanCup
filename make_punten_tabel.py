# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from make_friese_uitslagen import HKS_HEREN, GROU_HEREN, LEMMER_HEREN, MAKKUM_HEREN, LANGWEER_HEREN, FRIES, frisian_ranking, OUT_DIR

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

RACE_COLS = [
    ("HKS", HKS_HEREN),
    ("Grou", GROU_HEREN),
    ("IFK Lemmer", LEMMER_HEREN),
    ("Slag om Makkum", MAKKUM_HEREN),
    ("Langweer", LANGWEER_HEREN),
]

# sloep -> {racenaam: punten (float) of None (deelgenomen maar niet gefinisht/gestart)}
punten_per_sloep = {}
for racenaam, rows in RACE_COLS:
    for sloep, punten in frisian_ranking(rows):
        punten_per_sloep.setdefault(sloep, {})[racenaam] = punten

# Totaal = som van behaalde punten (alleen races met een resultaat); DNS/DNF races tellen niet mee.
rows_out = []
for sloep, per_race in punten_per_sloep.items():
    vereniging, plaats = FRIES[sloep]
    waarden = [per_race.get(naam) for naam, _ in RACE_COLS]
    behaalde = [v for v in waarden if v is not None]
    totaal = sum(behaalde) if behaalde else None
    rows_out.append((sloep, vereniging, plaats, waarden, totaal))

# Sorteer: minste punten (beste) bovenaan, meeste (slechtste) onderaan.
# Sloepen zonder enig resultaat (totaal None) helemaal onderaan.
rows_out.sort(key=lambda x: (x[4] is None, x[4] if x[4] is not None else 0))

def fmt(v):
    if v is None:
        return "-"
    if v == int(v):
        return f"{int(v)}" if v != 0.9 else "0,9"
    return f"{v:.1f}".replace(".", ",")

styles = getSampleStyleSheet()
title_style = ParagraphStyle("titel", parent=styles["Heading1"], fontSize=14, spaceAfter=2)
sub_style = ParagraphStyle("sub", parent=styles["Normal"], fontSize=9, spaceAfter=1)
note_style = ParagraphStyle("note", parent=styles["Normal"], fontSize=7, textColor=colors.grey, spaceBefore=8)

doc = SimpleDocTemplate(
    os.path.join(OUT_DIR, "Punten totaal - Friese herensloepen.pdf"),
    pagesize=landscape(A4),
    leftMargin=15*mm, rightMargin=15*mm, topMargin=15*mm, bottomMargin=15*mm,
)
elems = []
elems.append(Paragraph("Puntentotaal Friese herensloepen 2026", title_style))
elems.append(Paragraph(
    "Punten per wedstrijd op basis van de positie in het Friese klassement van die wedstrijd "
    "(1e = 0,9 punt, 2e = 2 punten, elke volgende plaats 1 punt meer). '-' = niet gevaren in deze "
    "wedstrijd, of niet gefinisht/gestart (telt niet mee in het totaal). Sortering: minste punten "
    "(beste totaalresultaat) bovenaan, meeste punten onderaan.",
    sub_style))
elems.append(Spacer(1, 4*mm))

header = ["Sloep", "Vereniging", "Plaats"] + [n for n, _ in RACE_COLS] + ["Totaal"]
data = [header]
for sloep, vereniging, plaats, waarden, totaal in rows_out:
    data.append([sloep, vereniging, plaats] + [fmt(v) for v in waarden] + [fmt(totaal)])

col_widths = [34*mm, 55*mm, 30*mm, 20*mm, 20*mm, 26*mm, 28*mm, 22*mm, 20*mm]
t = Table(data, colWidths=col_widths, repeatRows=1)
t.setStyle(TableStyle([
    ("FONTSIZE", (0,0), (-1,-1), 8),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME", (-1,1), (-1,-1), "Helvetica-Bold"),
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#dbe9f4")),
    ("GRID", (0,0), (-1,-1), 0.4, colors.grey),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("ALIGN", (3,0), (-1,-1), "CENTER"),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f4f7fa")]),
    ("TOPPADDING", (0,0), (-1,-1), 3),
    ("BOTTOMPADDING", (0,0), (-1,-1), 3),
]))
elems.append(t)

elems.append(Paragraph(
    "Zelfde Friese-teamselectie als in de afzonderlijke uitslagen per wedstrijd (HKS 2026, Grouster "
    "Roeisloepenrace 2026, Lemmer Iepen Frysk Kampioenskip 2026, Slag om Makkum 2026, SloepRoeienLangweer 2026), klasse Heren.",
    note_style))

doc.build(elems)
print("geschreven: Punten totaal - Friese herensloepen.pdf")
for sloep, vereniging, plaats, waarden, totaal in rows_out:
    print(sloep, waarden, totaal)
