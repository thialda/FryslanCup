# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from make_friese_uitslagen import HKS_HEREN, GROU_HEREN, LEMMER_HEREN, MAKKUM_HEREN, LANGWEER_HEREN, FRIES, frisian_ranking, OUT_DIR

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

RACE_COLS = [
    ("HKS", HKS_HEREN),
    ("Grou", GROU_HEREN),
    ("IFK Lemmer", LEMMER_HEREN),
    ("Slag om Makkum", MAKKUM_HEREN),
    ("Langweer", LANGWEER_HEREN),
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

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Punten Friese herensloepen"

header = ["Sloep", "Vereniging", "Plaats"] + [n for n, _ in RACE_COLS] + ["Totaal"]
ws.append(header)

header_fill = PatternFill(start_color="DBE9F4", end_color="DBE9F4", fill_type="solid")
bold = Font(bold=True)
thin = Side(style="thin", color="AAAAAA")
border = Border(left=thin, right=thin, top=thin, bottom=thin)
center = Alignment(horizontal="center", vertical="center")

for cell in ws[1]:
    cell.font = bold
    cell.fill = header_fill
    cell.alignment = center
    cell.border = border

for sloep, vereniging, plaats, waarden, totaal in rows_out:
    row = [sloep, vereniging, plaats] + [(v if v is not None else None) for v in waarden] + [totaal]
    ws.append(row)

last_row = ws.max_row
for r in range(2, last_row + 1):
    for c in range(1, len(header) + 1):
        cell = ws.cell(row=r, column=c)
        cell.border = border
        if c >= 4:
            cell.alignment = center
            if cell.value is not None:
                cell.number_format = "0.0"
        if c == len(header):
            cell.font = bold

col_widths = [24, 34, 20, 10, 10, 12, 14, 12, 10]
for i, w in enumerate(col_widths, start=1):
    ws.column_dimensions[get_column_letter(i)].width = w

ws.freeze_panes = "A2"

note = (
    "Punten per wedstrijd op basis van de positie in het Friese klassement van die wedstrijd "
    "(1e = 0,9 punt, 2e = 2 punten, elke volgende plaats 1 punt meer). Leeg = niet gevaren in deze "
    "wedstrijd, of niet gefinisht/gestart (telt niet mee in het totaal). Sortering: minste punten "
    "(beste totaalresultaat) bovenaan, meeste punten onderaan."
)
note_row = last_row + 2
ws.cell(row=note_row, column=1, value=note).font = Font(italic=True, size=9, color="666666")
ws.merge_cells(start_row=note_row, start_column=1, end_row=note_row, end_column=len(header))
ws.row_dimensions[note_row].height = 30
ws.cell(row=note_row, column=1).alignment = Alignment(wrap_text=True, vertical="top")

out_path = os.path.join(OUT_DIR, "Punten totaal - Friese herensloepen.xlsx")
wb.save(out_path)
print("geschreven:", out_path)
