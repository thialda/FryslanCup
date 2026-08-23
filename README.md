# Friese uitslagen 2026 — hoe dit werkt

Deze map bevat de gefilterde ("alleen Friese teams") uitslagen van drie sloeproeiwedstrijden
in 2026 (HKS, Grouster Roeisloepenrace, IFK Lemmer), plus twee puntentabellen (heren en dames)
die de resultaten van die drie wedstrijden combineren tot een puntenklassement
(1e = 0,9 punt, 2e = 2 punten, elke volgende plaats 1 punt meer, minste punten bovenaan).

## Bestanden in deze map

- `HKS 2026 - Dames/Heren - Friese teams.pdf`
- `Grou 2026 - Dames/Heren - Friese teams.pdf`
- `IFK Lemmer 2026 - Dames/Heren - Friese teams.pdf`
- `Punten totaal - Friese herensloepen.pdf` + `.xlsx`
- `Punten totaal - Friese damessloepen.pdf` + `.xlsx` + `.ods`
- `scripts/` — de Python-scripts die al het bovenstaande genereren

## Hoe een nieuwe uitslag verwerken

1. Open de nieuwe uitslag-PDF (zelfde formaat als HKS/Grou/IFK Lemmer: kolommen Nr, Sloep,
   FSN-nr, N, G, Kl., roeitijd, snelheid, Cw, vermogen per roeier, straf, om te winnen).
2. Typ de rijen over als een Python-lijst van tuples in `scripts/make_friese_uitslagen.py`
   (zie de bestaande `HKS_DAMES`, `HKS_HEREN`, enz. als voorbeeld — elke tuple is
   `(nr, sloep, fsn, n, kl, tijd, snelheid, cw, vermogen, status)`, met `status=None`
   voor finishers en de tekst ("niet gefinished"/"niet gestart") voor uitvallers).
3. Als er een nieuwe sloep bij zit die Fries is maar nog niet in de `FRIES`-dictionary staat:
   zoek de vereniging/plaats op (bijv. via sloeproeien.nl/database/sloepen/<sloepnaam-slug>,
   of via de officiële startlijst van de wedstrijd — vaak een PDF op de site van de
   organiserende vereniging, met kolommen Thuishaven/Team) en voeg toe aan `FRIES`.
4. Voeg de nieuwe race toe aan de `RACES`-lijst onderaan `make_friese_uitslagen.py`, en aan de
   `RACE_COLS`-lijst in `make_punten_tabel.py` / `make_punten_dames.py` / de bijbehorende
   Excel-scripts.
5. Draai de scripts (in deze volgorde, vanuit de `scripts/`-map):
   ```
   python3 make_friese_uitslagen.py
   python3 make_punten_tabel.py
   python3 make_punten_excel.py
   python3 make_punten_dames.py
   python3 make_punten_excel_dames.py
   ```
   Benodigde Python-pakketten: `reportlab`, `openpyxl`, `odfpy`
   (`pip3 install --user reportlab openpyxl odfpy`).

De output-map wordt automatisch bepaald als de bovenliggende map van `scripts/`, dus dit werkt
op elke computer waar deze hele map (inclusief `scripts/`) terechtkomt — bijvoorbeeld via
pCloud-sync op een andere pc, of nadat deze map opnieuw gedownload is.

## Belangrijk: dit is geen officiële bron

De Friese-team-classificatie is met zorg samengesteld (gecombineerd uit de sloeproeien.nl
verenigingen-/sloependatabase, officiële startlijsten, en correcties van Roland), maar niet
officieel geverifieerd door de wedstrijdorganisatie(s).
