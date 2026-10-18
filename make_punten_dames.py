# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from make_friese_uitslagen import HKS_DAMES, GROU_DAMES, LEMMER_DAMES, MAKKUM_DAMES, LANGWEER_DAMES, FRIES, frisian_ranking, OUT_DIR

RACE_COLS = [
    ("HKS", HKS_DAMES),
    ("Grou", GROU_DAMES),
    ("IFK Lemmer", LEMMER_DAMES),
    ("Slag om Makkum", MAKKUM_DAMES),
    ("Langweer", LANGWEER_DAMES),
]

punten_per_sloep = {}
for racenaam, rows in RACE_COLS:
    for sloep, punten in frisian_ranking(rows):
        punten_per_sloep.setdefault(sloep, {})[racenaam] = punten

rows_out = []
for sloep, per_race in punten_per_sloep.items():
    vereniging, plaats = FRIES[sloep]
    waarden = [per_race.get(naam) for naam, _ in RACE_COLS]
    behaalde = [v for v in waarden if v is not None]
    totaal = sum(behaalde) if behaalde else None
    rows_out.append((sloep, vereniging, plaats, waarden, totaal))

rows_out.sort(key=lambda x: (x[4] is None, x[4] if x[4] is not None else 0))

for sloep, vereniging, plaats, waarden, totaal in rows_out:
    print(sloep, waarden, totaal)

# ---------------------------------------------------------------
# PDF
# ---------------------------------------------------------------
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

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
    os.path.join(OUT_DIR, "Punten totaal - Friese damessloepen.pdf"),
    pagesize=landscape(A4),
    leftMargin=15*mm, rightMargin=15*mm, topMargin=15*mm, bottomMargin=15*mm,
)
elems = []
elems.append(Paragraph("Puntentotaal Friese damessloepen 2026", title_style))
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
    "Roeisloepenrace 2026, Lemmer Iepen Frysk Kampioenskip 2026, Slag om Makkum 2026, SloepRoeienLangweer 2026), klasse Dames.",
    note_style))

doc.build(elems)
print("geschreven: Punten totaal - Friese damessloepen.pdf")

# ---------------------------------------------------------------
# ODS (LibreOffice Calc)
# ---------------------------------------------------------------
from odf.opendocument import OpenDocumentSpreadsheet
from odf.style import (Style, TableColumnProperties, TableCellProperties,
                        TextProperties, ParagraphProperties)
from odf.table import Table as OdfTable, TableColumn, TableRow, TableCell
from odf.text import P

ods = OpenDocumentSpreadsheet()

header_style = Style(name="HeaderCell", family="table-cell")
header_style.addElement(TableCellProperties(backgroundcolor="#DBE9F4", border="0.5pt solid #AAAAAA"))
header_style.addElement(TextProperties(fontweight="bold"))
ods.automaticstyles.addElement(header_style)

cell_style = Style(name="DataCell", family="table-cell")
cell_style.addElement(TableCellProperties(border="0.5pt solid #AAAAAA"))
ods.automaticstyles.addElement(cell_style)

num_style = Style(name="NumCell", family="table-cell")
num_style.addElement(TableCellProperties(border="0.5pt solid #AAAAAA"))
num_style.addElement(ParagraphProperties(textalign="center"))
ods.automaticstyles.addElement(num_style)

total_style = Style(name="TotalCell", family="table-cell")
total_style.addElement(TableCellProperties(border="0.5pt solid #AAAAAA"))
total_style.addElement(TextProperties(fontweight="bold"))
total_style.addElement(ParagraphProperties(textalign="center"))
ods.automaticstyles.addElement(total_style)

col_widths_ods = ["2.6cm", "5cm", "3cm", "1.6cm", "1.6cm", "2.2cm", "2.6cm", "2cm", "1.6cm"]
col_styles = []
for i, w in enumerate(col_widths_ods):
    cs = Style(name=f"Col{i}", family="table-column")
    cs.addElement(TableColumnProperties(columnwidth=w))
    ods.automaticstyles.addElement(cs)
    col_styles.append(cs)

table = OdfTable(name="Punten Friese damessloepen")
for cs in col_styles:
    table.addElement(TableColumn(stylename=cs))

def make_cell(value, style, is_text=True):
    if value is None:
        cell = TableCell(stylename=style)
        cell.addElement(P(text=""))
        return cell
    if is_text:
        cell = TableCell(stylename=style, valuetype="string")
        cell.addElement(P(text=str(value)))
    else:
        cell = TableCell(stylename=style, valuetype="float", value=value)
        display = str(value).replace(".", ",")
        cell.addElement(P(text=display))
    return cell

header_row = TableRow()
for h in header:
    header_row.addElement(make_cell(h, header_style, is_text=True))
table.addElement(header_row)

for sloep, vereniging, plaats, waarden, totaal in rows_out:
    row = TableRow()
    row.addElement(make_cell(sloep, cell_style, is_text=True))
    row.addElement(make_cell(vereniging, cell_style, is_text=True))
    row.addElement(make_cell(plaats, cell_style, is_text=True))
    for v in waarden:
        row.addElement(make_cell(v, num_style, is_text=False))
    row.addElement(make_cell(totaal, total_style, is_text=False))
    table.addElement(row)

# lege rij + toelichting
empty_row = TableRow()
table.addElement(empty_row)
note_row = TableRow()
note_cell = TableCell(stylename=cell_style, numbercolumnsspanned=len(header))
note_cell.addElement(P(text=(
    "Punten per wedstrijd op basis van de positie in het Friese klassement van die wedstrijd "
    "(1e = 0,9 punt, 2e = 2 punten, elke volgende plaats 1 punt meer). Leeg = niet gevaren in deze "
    "wedstrijd, of niet gefinisht/gestart (telt niet mee in het totaal). Sortering: minste punten "
    "(beste totaalresultaat) bovenaan, meeste punten onderaan."
)))
note_row.addElement(note_cell)
for _ in range(len(header) - 1):
    note_row.addElement(TableCell())
table.addElement(note_row)

ods.spreadsheet.addElement(table)

ods_path = os.path.join(OUT_DIR, "Punten totaal - Friese damessloepen.ods")
ods.save(ods_path)
print("geschreven:", ods_path)
