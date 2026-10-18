# -*- coding: utf-8 -*-
import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT

# Schrijft output naar de map die deze scripts/-map bevat (portable: werkt op elke
# computer waar deze "Friese uitslagen 2026"-map staat, bv. via pCloud-sync).
OUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------
# Friese vereniging-lookup: sloepnaam (exact zoals in uitslag) -> (vereniging, plaats)
# Bron: sloeproeien.nl / database sloeproeiverenigingen (provincie Friesland),
# gematcht op sloepnaam. Enkele toewijzingen zijn onzeker (zie voetnoot in PDF).
# ---------------------------------------------------------------
FRIES = {
    "West-Arvada": ("Terschellinger Roeivereniging", "West-Terschelling"),
    "Pulp Fiction": ("IJsselmeerminnen", "Makkum"),
    "Bartix": ("De Galliërs", "Harlingen"),
    "Sir Lancelot Skynner": ("Lancelot Ladies", "Harlingen"),
    "Vrouwe Geertruida": ("Woelwater", "Sneek"),
    "Egbert Wagenborg": ("Terschellinger Roeivereniging", "West-Terschelling"),
    "Doeke Doeksen": ("Terschellinger Roeivereniging", "West-Terschelling"),
    "Tréwes 3": ("Tréwes", "Aldeboarn"),
    "Tréwes 2": ("Tréwes", "Aldeboarn"),
    "Tréwes 1": ("Tréwes", "Aldeboarn"),
    "Argir": ("Roeiploeg Tergrêft", "Oudebildtzijl"),
    "Beluga": ("Woelwater", "Sneek"),
    "Ambiorix": ("Ambiorix", "Harlingen"),
    "Waterheks": ("rv KannietHeX&", "Nes (Heerenveen)"),
    "Wetter Wrotter": ("Grouster Roeisloepen Vereniging", "Grou"),
    "Ladykiller": ("Terschellinger Roeivereniging", "West-Terschelling"),
    "VICtorie": ("Okke Hel", "Harlingen"),
    "Karakter": ("Roeivereniging Ameland", "Nes (Ameland)"),
    "Oksewiel II": ("Den Bealch", "Terherne"),
    "Oksewiel I": ("Den Bealch", "Terherne"),
    "Skomskowster": ("Aldegeaster Skomskowers", "Oudega"),
    "Skomskower": ("Aldegeaster Skomskowers", "Oudega"),
    "Najade": ("7 Gezusters", "Franeker"),
    "Danser": ("Okke Hel", "Harlingen"),
    "Cornelis Douwes": ("Terschellinger Roeivereniging", "West-Terschelling"),
    "Benwyvis": ("Terschellinger Roeivereniging", "West-Terschelling"),
    "Toverbal": ("Norderboys", "Sexbierum"),
    "Zeeleeuw II": ("Ouwe Syl", "Oudebildtzijl"),
    "Onversaagd": ("RV Tille", "Harlingen"),
    "Gouteyck": ("Terschellinger Roeivereniging", "West-Terschelling"),
    "Twirre": ("RV Makkum", "Makkum"),
    "Schotse Vier": ("Terschellinger Roeivereniging", "West-Terschelling"),
    "Snurk": ("Okke Hel", "Harlingen"),
    "Hjoed 'n Makkie 2": ("Hjoed 'n Makkie", "Dronrijp"),
    "Grutte Bear": ("RV De Stamgasten", "Joure"),
    "Grutte Bear II": ("RV De Stamgasten", "Joure"),
    "Turftraper, De": ("De Turftrapers", "Nij Beets"),
    "Turftraper II, De": ("De Turftrapers", "Nij Beets"),
    "Wetter Fretter": ("Grouster Roeisloepen Vereniging", "Grou"),
    "Okke": ("Okke Hel", "Harlingen"),
    "Arad": ("Terschellinger Roeivereniging", "West-Terschelling"),
    "Visioen": ("Maritieme Academie Harlingen", "Harlingen"),
    "Kromme Dick": ("Okke Hel", "Harlingen"),
    "L8": ("Lemster Leeuwkes (WSV Zevenwolden)", "Lemmer"),
    "Iwan Franko": ("Woelwater", "Sneek"),
    "Rijp, De": ("Terschellinger Roeivereniging", "West-Terschelling"),
    # "Rijp" (FSN018, zonder "De") komt uit Muiden en is geen Friese sloep -- bewust niet opgenomen.
    "Zeeotter II": ("Greate Pier", "Franeker"),
    "Tobbe": ("Okke Hel", "Harlingen"),
    "Houtman": ("Terschellinger Roeivereniging", "West-Terschelling"),
    "Sterke Sietze": ("Okke Hel", "Harlingen"),
    "L.A. Buma": ("Sloeproeiteam 't Fiskerhúske", "Moddergat"),
    "Stielen Bear": ("Roeiploeg Stielen Bear", "Joure"),
    "Bruzer": ("Roeiteam Brûzer", "Workum"),
    "Mata Hari": ("Sloeproeivereniging Leeuwarden", "Leeuwarden"),
    "Elle6": ("Lemster Leeuwkes (WSV Zevenwolden)", "Lemmer"),
    "Leeuwke": ("Lemster Leeuwkes (WSV Zevenwolden)", "Lemmer"),
    "Swan, De": ("Skarrefammen", "Langweer"),
    "Skeve, De": ("Roeisloep De Skeve", "Leeuwarden"),
    "Vuurzee": ("De Vlammetjes", "Harlingen"),
    "W2": ("Grouster Roeisloepen Vereniging", "Grou"),
    "Zeeleeuw, De": ("SV Osiris", "Leeuwarden"),
    "OKA-18": ("OKA '18 (Terschellinger Roeivereniging)", "West-Terschelling"),
    "Ame Gijs": ("Hindelopen", "Hindelopen"),
    "Zeekameel": ("Een team een taak", "Ried"),
    "Bok, De": ("Roeivereniging Vlieland", "Vlieland"),
    # nieuw bij Slag om Makkum / Langweer (okt 2026), opgezocht op sloeproeien.nl/database/sloepen/<slug>
    "Fjoer Fûgel": ("Fjoer Fûgel", "Makkum"),
    "Lyts Frisia": ("Sloeproeivereniging It Heidenskip", "It Heidenskip"),
    "Dolle Heks": ("rv KannietHeX&", "Akkrum"),
    "Hjoed 'n Makkie 5,1%": ("Hjoed 'n Makkie", "Dronrijp"),
    "Freonskip": ("Túnus", "Deinum"),
    "Dolle mina": ("Drachtster Dollen", "Drachten"),
    "Wetterspetter": ("Grouster Roeisloepen Vereniging", "Grou"),
    "Onvervaard": ("RV Tille", "Harlingen"),
    "El Flamingo II": ("Frisia Roeiteam", "Harlingen"),
    "Oude Dock, 't": ("Roeiploeg Stielen Bear", "Joure"),
}

# ---------------------------------------------------------------
# Race data. Each row: (nr_orig, sloep, fsn, n, kl, tijd, snelheid, cw, vermogen, status)
# status is None for finishers; anders de tekst ("niet gefinished" / "niet gestart")
# ---------------------------------------------------------------

HKS_DAMES = [
 (1,"West-Arvada","FSN072",8,"1","02:05:52","2,26","22,83","32,73",None),
 (2,"Pulp Fiction","FSN082",8,"V","02:20:50","2,03","28,68","30,12",None),
 (3,"OKA-18","FSN041",8,"V","02:16:01","2,09","25,48","29,31",None),
 (4,"Bartix","FSN029",8,"V","02:28:43","1,90","31,29","27,27",None),
 (5,"Sir Lancelot Skynner","FSN111",8,"1","02:14:27","2,12","22,20","26,54",None),
 (6,"Vrouwe Geertruida","FSN119",8,"V","02:29:09","1,91","25,98","22,82",None),
 (7,"Mare Australis","FSN193",8,"1","02:42:47","1,73","33,87","22,15",None),
 (8,"Egbert Wagenborg","FSN071",8,"V","02:24:55","1,93","23,12","21,11",None),
 (9,"Roy Hesterman","FSN095",8,"1","02:26:20","1,94","21,09","19,31",None),
 (10,"Doeke Doeksen","FSN006",8,"1","02:47:26","1,68","31,69","19,28",None),
 (11,"GIA light","FSN080",8,"1","02:46:47","1,70","30,61","19,17",None),
 (12,"Tréwes 3","FSN136",8,"V","02:35:42","1,82","24,97","19,12",None),
 (13,"Argir","FSN229",6,"1","02:50:30","1,67","19,61","15,39",None),
 (14,"Beluga","FSN226",6,"1","02:58:58","1,58","22,72","15,24",None),
 (15,"Ambiorix","FSN017",8,"1","02:58:11","1,60","26,98","14,00",None),
 (16,"Waterheks","FSN197",8,"V","03:16:51","1,45","33,96","13,23",None),
 (17,"Wetter Wrotter","FSN238",8,"1","02:42:44","1,72","20,10","13,07",None),
 (18,"Jan van den Berg","FSN075",10,"V","02:47:05","1,70","25,85","12,84",None),
 (19,"Ladykiller","FSN059",6,"2","03:07:39","1,50","21,92","12,71",None),
 (20,"VICtorie","FSN150",8,"V","03:09:34","1,49","25,61","10,76",None),
 (21,"Karakter","FSN110",8,"V","03:01:59","1,58","20,42","10,35",None),
 (22,"Oksewiel II","FSN212",8,"2","03:31:30","1,34","27,79","8,66",None),
 (23,"Zusje","FSN147",6,"2","03:44:56","1,27","23,51","8,24",None),
 (24,"Skomskowster","FSN185",6,"-","-","-","-","-","niet gefinished"),
 (25,"Najade","FSN182",6,"-","-","-","-","-","niet gefinished"),
 (26,"Danser","FSN014",6,"-","-","-","-","-","niet gefinished"),
]

HKS_HEREN = [
 (1,"Cornelis Douwes","FSN063",8,"H","01:42:25","2,74","34,44","88,61",None),
 (2,"Benwyvis","FSN047",8,"V","01:42:46","2,73","33,80","86,18",None),
 (3,"Toverbal","FSN030",8,"V","01:50:41","2,53","35,29","71,77",None),
 (4,"Ame Gijs","FSN144",8,"V","01:56:09","2,42","34,86","62,53",None),
 (5,"Zeeleeuw II","FSN062",8,"V","01:58:56","2,38","35,65","61,02",None),
 (6,"Onversaagd","FSN046",8,"H","02:03:23","2,28","39,40","58,84",None),
 (7,"Gouteyck","FSN045",12,"1","01:46:15","2,63","38,44","58,23",None),
 (8,"Serdon","FSN100",8,"H","02:16:48","2,08","50,70","57,88",None),
 (9,"Azorean High","FSN077",10,"H","01:40:10","2,80","26,29","57,54",None),
 (10,"Twirre","FSN050",8,"H","01:49:48","2,57","27,01","57,32",None),
 (11,"Schotse Vier","FSN009",8,"V","01:59:48","2,34","34,45","55,63",None),
 (12,"Snurk","FSN084",8,"1","01:52:55","2,49","27,75","54,03",None),
 (13,"Visbyvaarder","FSN219",8,"1","01:57:48","2,39","30,31","51,99",None),
 (14,"Hjoed 'n Makkie 2","FSN133",8,"V","02:09:10","2,19","38,92","51,86",None),
 (15,"Grutte Bear","FSN142",8,"V","02:09:53","2,17","39,67","51,26",None),
 (16,"Polyester","FSN024",8,"H","02:12:12","2,12","39,04","47,34",None),
 (17,"Turftraper, De","FSN288",8,"1","02:00:55","2,33","29,14","46,70",None),
 (18,"Razende Snol","FSN211",8,"H","02:11:38","2,12","37,86","45,96",None),
 (19,"Wetter Fretter","FSN138",8,"H","02:20:50","2,01","44,61","45,96",None),
 (20,"Grutte Bear II","FSN294",8,"H","02:08:25","2,18","34,55","45,34",None),
 (21,"Okke","FSN016",10,"V","02:12:44","2,17","42,85","44,74",None),
 (22,"Skomskower","FSN172",8,"1","02:21:09","2,00","42,61","43,51",None),
 (23,"Arad","FSN055",6,"V","02:18:00","2,05","28,11","41,43",None),
 (24,"Visioen","FSN199",8,"V","02:19:52","2,03","37,72","40,43",None),
 (25,"Kromme Dick","FSN109",8,"1","01:59:13","2,36","24,26","40,42",None),
 (26,"L8","FSN277",8,"1","01:59:19","2,34","24,16","39,31",None),
 (27,"Tréwes 2","FSN123",8,"1","02:16:10","2,09","33,66","39,00",None),
 (28,"Aludux","FSN079",8,"2","02:09:05","2,18","29,22","38,26",None),
 (29,"Murk","FSN162",8,"1","02:26:09","1,97","37,13","36,07",None),
 (30,"Haakie, 't","FSN037",8,"1","02:22:51","2,00","35,09","35,63",None),
 (31,"Iwan Franko","FSN120",8,"V","02:26:01","1,94","36,24","34,13",None),
 (32,"Oksewiel I","FSN149",6,"1","02:35:13","1,83","31,68","33,23",None),
 (33,"Yellowfin","FSN094",10,"V","01:51:40","2,51","22,45","32,84",None),
 (34,"Schone Waardin","FSN039",8,"H","02:29:28","1,90","36,76","32,29",None),
 (35,"Rijp, De","FSN002",8,"2","02:36:44","1,81","40,49","31,00",None),
 (36,"Zeekameel","FSN297",8,"V","02:30:17","1,88","34,50","29,44",None),
 (37,"Schokland","FSN104",8,"2","02:38:02","1,80","39,14","29,14",None),
 (38,"Zeeotter II","FSN183",8,"1","02:28:46","1,90","32,49","28,43",None),
 (39,"Tobbe","FSN015",6,"2","02:42:28","1,73","29,67","26,57",None),
 (40,"Houtman","FSN001",8,"V","02:53:48","1,67","39,20","23,60",None),
 (41,"Sterke Sietze","FSN064",8,"2","02:59:11","1,60","42,94","22,88",None),
 (42,"L.A. Buma","FSN253",8,"2","02:37:35","1,79","28,95","21,52",None),
 (43,"Hubert Jans 2","FSN067",10,"V","02:30:12","1,86","30,81","20,39",None),
 (44,"Stad Deventer","FSN048",10,"V","02:57:29","1,64","41,65","18,95",None),
 (45,"Stokvisvaarder","FSN266",8,"2","02:37:12","1,82","23,41","18,16",None),
 (46,"Bok, De","FSN191",8,"V","02:25:42","1,95","19,07","18,15",None),
 (47,"Averij","FSN151",8,"-","-","-","-","-","niet gestart"),
 (48,"Zeeolifant","FSN005",14,"-","-","-","-","-","niet gefinished"),
]

GROU_DAMES = [
 (1,"Egbert Wagenborg","FSN071",8,"V","02:23:03","2,54","27,84","57,07",None),
 (2,"West-Arvada","FSN072",8,"1","02:21:13","2,57","25,93","55,21",None),
 (3,"Pulp Fiction","FSN082",8,"V","02:35:26","2,34","31,52","50,63",None),
 (4,"Mata Hari","FSN233",8,"V","02:26:32","2,48","26,43","50,47",None),
 (5,"Argir","FSN229",6,"1","02:35:51","2,33","22,21","47,21",None),
 (6,"Sir Lancelot Skynner","FSN111",8,"1","02:24:20","2,52","23,43","46,79",None),
 (7,"Bartix","FSN029",8,"V","02:43:44","2,22","33,56","46,28",None),
 (8,"Witte Beer, De","FSN090",8,"1","02:46:18","2,18","33,54","44,18",None),
 (9,"Waterheks","FSN197",8,"V","02:52:41","2,10","36,94","43,57",None),
 (10,"Vrouwe Geertruida","FSN119",8,"V","02:33:57","2,36","26,24","43,36",None),
 (11,"Wetter Wrotter","FSN238",8,"1","02:31:55","2,39","24,43","41,97",None),
 (12,"VICtorie","FSN150",8,"V","02:50:36","2,13","34,10","41,68",None),
 (13,"Ladykiller","FSN059",6,"2","02:57:56","2,04","27,24","39,24",None),
 (14,"Turftraper II, De","FSN241",6,"V","02:39:20","2,28","22,14","39,09",None),
 (15,"Oksewiel II","FSN212",8,"2","02:54:48","2,08","34,01","38,70",None),
 (16,"Katowice","FSN040",6,"V","03:05:06","1,96","29,94","38,39",None),
 (17,"Danser","FSN014",6,"1","03:05:36","1,96","29,48","37,51",None),
 (18,"Mare Australis","FSN193",8,"1","02:58:04","2,04","38,54","36,54",None),
 (19,"Najade","FSN182",6,"1","03:01:09","2,01","25,84","35,31",None),
 (20,"Octopus","FSN089",8,"1","02:40:33","2,26","22,79","33,28",None),
 (21,"Parel van Bru","FSN129",6,"V","03:17:21","1,84","30,78","32,70",None),
 (22,"Berend Koster","FSN101",8,"2","02:52:12","2,11","25,34","30,13",None),
 (23,"Roy Hesterman","FSN095",8,"1","02:34:36","2,35","23,70","28,68",None),
 (24,"Vuurzee","FSN068",8,"2","03:12:51","1,88","30,36","25,89",None),
 (25,"Karakter","FSN110",8,"-","-","-","-","-","niet gestart"),
]

GROU_HEREN = [
 (1,"Cornelis Douwes","FSN063",8,"H","02:04:39","2,91","36,01","111,50",None),
 (2,"Grutte Bear II","FSN294",8,"H","02:16:34","2,66","39,96","94,64",None),
 (3,"Toverbal","FSN030",8,"V","02:14:05","2,71","37,62","94,04",None),
 (4,"Ame Gijs","FSN144",8,"V","02:16:11","2,67","39,25","93,73",None),
 (5,"Schotse Vier","FSN009",8,"V","02:14:07","2,71","36,50","91,17",None),
 (6,"Anckertje, 't","FSN038",8,"H","02:35:17","2,34","53,08","86,22",None),
 (7,"Zeeleeuw II","FSN062",8,"V","02:18:46","2,62","38,05","86,00",None),
 (8,"Gouteyck","FSN045",12,"1","02:06:16","2,88","41,98","83,45",None),
 (9,"Serdon","FSN100",8,"H","02:39:29","2,28","53,49","80,34",None),
 (10,"Twirre","FSN050",8,"H","02:09:43","2,80","29,10","80,17",None),
 (11,"Onversaagd","FSN046",8,"H","02:24:45","2,51","39,98","79,81",None),
 (12,"Grutte Bear","FSN142",8,"V","02:29:42","2,43","43,73","79,10",None),
 (13,"Hjoed 'n Makkie 2","FSN133",8,"V","02:26:53","2,47","41,34","79,07",None),
 (14,"Wetter Fretter","FSN138",8,"H","02:36:21","2,32","49,50","78,80",None),
 (15,"Polyester","FSN024",8,"H","02:32:33","2,38","46,02","78,76",None),
 (16,"Skeve, De","FSN160",8,"1","02:34:57","2,34","47,88","78,26",None),
 (17,"Skomskower","FSN172",8,"1","02:30:20","2,42","43,59","77,88",None),
 (18,"Zeekameel","FSN297",8,"V","02:30:42","2,41","43,84","77,76",None),
 (19,"Evert Deddes","FSN087",8,"1","02:11:20","2,77","28,26","75,06",None),
 (20,"Turftraper, De","FSN288",8,"1","02:16:58","2,65","31,91","74,93",None),
 (21,"Oksewiel I","FSN149",8,"1","02:29:54","2,42","41,41","74,61",None),
 (22,"L8","FSN277",8,"1","02:11:06","2,77","27,73","74,05",None),
 (23,"Razende Snol","FSN211",8,"H","02:25:44","2,49","39,91","73,10",None),
 (24,"Azorean High","FSN077",8,"H","02:03:57","2,93","23,20","73,03",None),
 (25,"Okke","FSN016",10,"V","02:27:30","2,46","46,20","69,81",None),
 (26,"Murk","FSN162",8,"1","02:37:02","2,31","43,55","68,44",None),
 (27,"Schone Waardin","FSN039",8,"H","02:35:42","2,33","45,26","67,94",None),
 (28,"Tréwes 2","FSN123",8,"1","02:30:48","2,41","38,02","67,31",None),
 (29,"Minimug","FSN146",6,"2","02:45:56","2,19","37,52","66,88",None),
 (30,"Iwan Franko","FSN120",8,"V","02:35:05","2,34","39,22","63,95",None),
 (31,"Zeeotter II","FSN183",8,"1","02:26:11","2,49","32,91","63,83",None),
 (32,"Huysman, De","FSN112",8,"2","02:46:48","2,18","48,22","63,48",None),
 (33,"Noordvaarder","FSN058",8,"1","02:28:03","2,45","33,83","63,21",None),
 (34,"Rijp, De","FSN002",8,"2","02:42:35","2,23","43,46","61,68",None),
 (35,"Tobbe","FSN015",6,"2","02:51:20","2,12","37,21","60,37",None),
 (36,"Rotterdammer 2","FSN053",8,"2","02:44:27","2,21","43,66","59,92",None),
 (37,"Averij","FSN151",8,"2","02:52:40","2,10","50,13","59,63",None),
 (38,"Sterke Sietze","FSN064",8,"2","02:57:39","2,05","53,00","58,00",None),
 (39,"W2","FSN190",8,"2","02:30:14","2,42","32,40","57,99",None),
 (40,"Tréwes 1","FSN116",8,"V","02:35:28","2,34","40,98","56,33",None),
 (41,"Anthony van Hoboken","FSN088",8,"2","02:23:20","2,53","27,22","55,94",None),
 (42,"Aludux","FSN079",8,"2","02:31:02","2,41","30,81","54,30",None),
 (43,"Naruthi","FSN153",8,"2","02:43:50","2,22","38,13","52,92",None),
 (44,"L.A. Buma","FSN253",10,"2","02:34:38","2,35","39,63","52,13",None),
 (45,"Splitcase","FSN137",10,"2","02:41:26","2,25","44,02","51,04",None),
 (46,"Jan van den Berg","FSN075",10,"V","02:27:52","2,46","32,06","48,11",None),
 (47,"Stad Deventer","FSN048",10,"V","02:48:41","2,15","42,06","42,86",None),
 (48,"Stad Kampen","FSN121",12,"V","02:42:03","2,24","44,40","42,42",None),
 (49,"Hubert Jans 2","FSN067",10,"V","02:32:50","2,38","31,14","42,39",None),
 (50,"Kerwood","FSN061",12,"V","02:24:45","2,51","38,18","40,81",None),
 (51,"Van Ommeren","FSN065",8,"V","03:06:00","1,95","38,53","36,84",None),
 (52,"Zeeleeuw, De","FSN020",8,"-","-","-","-","-","niet gestart"),
]

LEMMER_HEREN = [
 (1,"Cornelis Douwes","FSN063",8,"V","02:12:05","2,88","35,65","106,11",None),
 (2,"Benwyvis","FSN047",8,"V","02:12:02","2,88","34,14","101,75",None),
 (3,"Toverbal","FSN030",8,"V","02:22:37","2,66","36,99","87,91",None),
 (4,"Ame Gijs","FSN144",8,"V","02:24:58","2,62","38,30","86,74",None),
 (5,"Zeekameel","FSN297",8,"V","02:35:19","2,45","44,76","82,80",None),
 (6,"Grutte Bear II","FSN294",8,"V","02:28:04","2,57","38,68","82,33",None),
 (7,"Zeeleeuw II","FSN062",8,"V","02:28:35","2,56","37,38","78,75",None),
 (8,"Onversaagd","FSN046",8,"V","02:33:41","2,47","39,88","76,09",None),
 (9,"Schotse Vier","FSN009",8,"V","02:28:36","2,56","35,60","74,97",None),
 (10,"Orkaan","FSN051",8,"V","02:27:20","2,58","33,28","71,88",None),
 (11,"Serdon","FSN100",8,"V","02:52:25","2,20","52,40","71,32",None),
 (12,"Twirre","FSN050",8,"V","02:20:11","2,71","28,24","70,59",None),
 (13,"Visioen","FSN199",8,"V","02:41:30","2,35","42,78","70,57",None),
 (14,"Arad","FSN055",8,"V","02:37:40","2,41","39,09","69,18",None),
 (15,"Skomskower","FSN172",8,"1","02:43:31","2,32","43,35","68,95",None),
 (16,"Razende Snol","FSN211",8,"V","02:38:38","2,40","39,32","68,35",None),
 (17,"Wetter Fretter","FSN138",8,"V","02:50:58","2,22","47,75","66,63",None),
 (18,"Grutte Bear","FSN142",8,"V","02:44:08","2,32","41,83","65,80",None),
 (19,"Sloepweesje","FSN054",8,"1","02:48:32","2,25","44,78","65,18",None),
 (20,"L8","FSN277",8,"1","02:22:11","2,67","26,76","64,15",None),
 (21,"Noordvaarder","FSN058",8,"1","02:34:43","2,46","33,85","63,33",None),
 (22,"Kromme Dick","FSN109",8,"1","02:22:07","2,67","26,33","63,22",None),
 (23,"Vrijbuiter","FSN235",8,"2","02:46:20","2,28","40,46","61,20",None),
 (24,"Rijp","FSN018",10,"V","02:38:38","2,40","43,97","61,15",None),
 (25,"Boomsluiter","FSN042",8,"1","02:57:50","2,14","48,63","60,44",None),
 (26,"Zeeotter II","FSN183",8,"1","02:36:33","2,43","32,86","59,39",None),
 (27,"Oksewiel I","FSN149",8,"1","02:47:15","2,27","39,69","59,07",None),
 (28,"Tréwes 2","FSN123",8,"1","02:44:12","2,31","36,55","57,42",None),
 (29,"Doorgáán","FSN270",8,"1","02:26:52","2,59","25,80","56,25",None),
 (30,"Doordouwer","FSN200",8,"2","02:42:36","2,34","33,78","54,62",None),
 (31,"Averij","FSN151",8,"2","03:06:03","2,04","48,85","53,18",None),
 (32,"Kromhout, 't","FSN049",10,"2","02:49:00","2,25","45,67","52,74",None),
 (33,"Tobbe","FSN015",6,"2","03:05:20","2,05","35,44","52,03",None),
 (34,"Dikkertje","FSN140",10,"2","02:55:36","2,16","50,29","51,89",None),
 (35,"Schokland","FSN104",8,"2","03:00:57","2,10","42,59","50,30",None),
 (36,"Gebr. Van Amerongen","FSN078",8,"V","02:32:40","2,49","25,24","49,10",None),
 (37,"Castor","FSN118",10,"V","02:46:17","2,29","39,49","47,82",None),
 (38,"Last of the Titanic","FSN073",8,"2","02:41:18","2,36","28,40","47,00",None),
 (39,"Doorhaler","FSN007",8,"2","03:01:19","2,10","37,27","43,77",None),
 (40,"Bacchus","FSN074",10,"V","02:39:06","2,39","31,51","43,44",None),
 (41,"Jan van den Berg","FSN075",10,"V","02:41:08","2,36","31,42","41,74",None),
 (42,"Stad Deventer","FSN048",10,"V","03:03:59","2,07","41,98","37,78",None),
 (43,"Twister","FSN070",8,"2","02:50:21","2,23","25,92","36,56",None),
 (44,"Hubert Jans 2","FSN067",10,"V","02:49:05","2,25","31,05","35,80",None),
 (45,"Splitcase","FSN137",10,"-","-","-","-","-","niet gestart"),
]

LEMMER_DAMES = [
 (1,"Swan, De","FSN216",8,"H","02:44:33","2,31","34,15","53,12",None),
 (2,"Azorean High","FSN077",8,"H","02:19:58","2,71","20,25","50,66",None),
 (3,"Egbert Wagenborg","FSN071",8,"H","02:34:52","2,45","26,97","50,12",None),
 (4,"Stielen Bear","FSN130",8,"H","02:54:24","2,18","37,61","49,31",None),
 (5,"West-Arvada","FSN072",8,"1","02:33:06","2,48","24,92","47,90",None),
 (6,"Bruzer","FSN155",6,"H","02:56:05","2,16","27,14","46,14",None),
 (7,"Pulp Fiction","FSN082",8,"H","02:46:55","2,28","30,88","46,06",None),
 (8,"Mata Hari","FSN233",8,"H","02:38:05","2,40","26,24","45,91",None),
 (9,"Vrouwe Geertruida","FSN119",8,"H","02:39:58","2,38","26,25","44,36",None),
 (10,"OKA-18","FSN041",8,"V","02:42:12","2,34","26,93","43,69",None),
 (11,"Sir Lancelot Skynner","FSN111",8,"1","02:34:43","2,46","23,22","43,28",None),
 (12,"Turftraper II, De","FSN241",6,"V","02:48:41","2,25","22,03","42,48",None),
 (13,"Bartix","FSN029",8,"V","02:56:07","2,16","33,07","42,13",None),
 (14,"Easedale","FSN281",8,"1","03:13:28","1,96","41,98","40,60",None),
 (15,"Doeke Doeksen","FSN006",8,"1","03:04:53","2,06","36,41","40,22",None),
 (16,"Argir","FSN229",6,"1","02:51:11","2,22","21,67","40,01",None),
 (17,"GIA light","FSN080",8,"1","03:03:58","2,07","34,75","38,95",None),
 (18,"Elle6","FSN276",6,"V","02:48:13","2,26","19,71","38,32",None),
 (19,"Mare Australis","FSN193",8,"1","03:11:51","1,98","37,49","37,16",None),
 (20,"Zusje","FSN147",6,"2","03:14:24","1,95","28,68","36,45",None),
 (21,"Ambiorix","FSN017",8,"1","03:07:05","2,03","32,82","35,03",None),
 (22,"Ladykiller","FSN059",6,"2","03:11:48","1,98","26,42","34,95",None),
 (23,"Oksewiel II","FSN212",8,"2","03:09:13","2,01","33,16","34,23",None),
 (24,"VICtorie","FSN150",8,"V","03:07:55","2,02","32,06","33,77",None),
 (25,"Epoxydus","FSN113",8,"V","02:44:12","2,31","20,62","32,27",None),
 (26,"Berend Koster","FSN101",8,"2","02:58:39","2,13","25,48","31,14",None),
 (27,"Najade","FSN182",6,"1","03:16:47","1,93","25,02","30,69",None),
 (28,"d'Isela","FSN117",8,"V","02:52:20","2,21","22,33","30,32",None),
 (29,"Tréwes 3","FSN136",8,"V","03:06:41","2,04","26,00","27,92",None),
 (30,"Moos","FSN125",8,"2","02:54:21","2,18","21,06","27,64",None),
 (31,"Leeuwke","FSN026",8,"V","03:32:25","1,79","33,14","24,36",None),
]

# --- Slag om Makkum 2026 (05-09-2026) en SloepRoeienLangweer 2026 (26-09-2026); bron: federatiesloeproeien.nl-PDF's ---
MAKKUM_HEREN = [
 (1,"Cornelis Douwes","FSN063",8,"H","01:14:15","2,68","33,98","82,39",None),
 (2,"Toverbal","FSN030",8,"V","01:16:34","2,60","36,17","78,13",None),
 (3,"Ame Gijs","FSN144",8,"V","01:18:33","2,54","36,70","75,43",None),
 (4,"Grutte Bear II","FSN294",8,"H","01:20:29","2,47","37,56","71,86",None),
 (5,"Anckertje, 't","FSN038",8,"H","01:30:49","2,19","51,11","68,60",None),
 (6,"Easedale","FSN281",8,"H","01:29:23","2,23","47,41","66,67",None),
 (7,"Snurk","FSN084",8,"1","01:14:43","2,67","27,91","66,43",None),
 (8,"Azorean High","FSN077",10,"H","01:08:41","2,90","27,05","65,95",None),
 (9,"Skomskower","FSN172",8,"1","01:27:10","2,28","43,26","65,49",None),
 (10,"Wetter Fretter","FSN138",8,"H","01:30:25","2,20","47,43","64,49",None),
 (11,"Serdon","FSN100",8,"H","01:33:33","2,13","51,37","63,20",None),
 (12,"Razende Snol","FSN211",8,"H","01:26:34","2,30","38,78","59,91",None),
 (13,"Zeekameel","FSN297",8,"V","01:28:10","2,26","40,42","59,18",None),
 (14,"Visioen","FSN199",8,"V","01:28:38","2,25","40,88","58,93",None),
 (15,"Mata Hari","FSN233",6,"1","01:22:36","2,41","25,22","57,62",None),
 (16,"Pulp Fiction","FSN082",6,"V","01:28:33","2,25","29,43","56,72",None),
 (17,"Zeeschuimer","FSN286",8,"2","01:19:03","2,52","27,14","54,74",None),
 (18,"Polyester","FSN024",8,"H","01:29:44","2,22","41,33","52,46",None),
 (19,"Twirre","FSN050",6,"H","01:26:01","2,32","24,61","51,66",None),
 (20,"Skeve, De","FSN160",8,"1","01:36:13","2,07","44,72","50,65",None),
 (21,"Okke","FSN016",10,"V","01:29:29","2,23","43,39","48,66",None),
 (22,"Noordvaarder","FSN058",8,"1","01:27:13","2,28","32,11","48,53",None),
 (23,"Fjoer Fûgel","FSN056",6,"2","01:29:16","2,23","24,75","46,58",None),
 (24,"Meppeler mug","FSN218",8,"2","01:22:12","2,42","27,31","46,12",None),
 (25,"Aludux","FSN079",8,"2","01:28:58","2,24","29,63","42,24",None),
 (26,"Zeeotter II","FSN183",8,"1","01:32:33","2,15","32,66","41,46",None),
 (27,"Bok, De","FSN191",8,"2","01:25:17","2,34","20,99","33,88",None),
 (28,"Stokvisvaarder","FSN266",8,"2","01:32:09","2,16","25,30","32,54",None),
 (29,"Tréwes 2","FSN123",8,"1","01:40:50","1,98","32,49","32,07",None),
 (30,"L8","FSN277",8,"-","","","","","niet gestart"),
]

MAKKUM_DAMES = [
 (1,"Bruzer","FSN155",6,"V","01:35:45","2,08","26,42","39,88",None),
 (2,"Mare Australis","FSN193",8,"1","01:40:34","1,98","37,49","36,75",None),
 (3,"Minimug","FSN146",6,"2","01:41:12","1,97","28,56","36,65",None),
 (4,"West-Arvada","FSN072",8,"1","01:26:28","2,30","23,23","35,48",None),
 (5,"Doeke Doeksen","FSN006",8,"1","01:40:14","1,99","35,36","35,00",None),
 (6,"GIA light","FSN080",8,"1","01:39:01","2,01","34,01","34,89",None),
 (7,"Danser","FSN014",6,"1","01:44:09","1,91","28,49","33,60",None),
 (8,"VICtorie","FSN150",8,"V","01:38:36","2,02","32,02","33,27",None),
 (9,"Ambiorix","FSN017",8,"1","01:41:08","1,97","31,75","30,61",None),
 (10,"Lyts Frisia","FSN265",8,"V","01:35:48","2,08","26,90","30,42",None),
 (11,"Wetter Wrotter","FSN238",8,"1","01:32:53","2,14","22,45","27,80",None),
 (12,"Skomskowster","FSN185",6,"1","01:58:13","1,68","29,39","23,89",None),
 (13,"Onvervaard","FSN091",6,"1","01:55:27","1,73","26,08","22,73",None),
 (14,"Berend Koster","FSN101",8,"2","01:47:36","1,85","23,47","18,86",None),
]

LANGWEER_HEREN = [
 (1,"Cornelis Douwes","FSN063",8,"H","01:28:57","2,84","35,30","101,00",None),
 (2,"Toverbal","FSN030",8,"V","01:32:29","2,73","37,91","96,76",None),
 (3,"Anckertje, 't","FSN038",8,"H","01:45:21","2,40","53,92","93,88",None),
 (4,"Wetter Fretter","FSN138",8,"H","01:45:10","2,40","50,98","89,20",None),
 (5,"Grutte Bear II","FSN294",8,"H","01:36:26","2,62","39,37","88,87",None),
 (6,"Easedale","FSN281",8,"H","01:46:14","2,38","49,57","84,20",None),
 (7,"Gouteyck","FSN045",12,"1","01:27:55","2,87","41,89","82,70",None),
 (8,"Twirre","FSN050",8,"H","01:29:40","2,82","29,25","81,75",None),
 (9,"Razende Snol","FSN211",8,"H","01:40:12","2,52","40,08","80,83",None),
 (10,"Turftraper, De","FSN288",8,"1","01:33:37","2,70","32,37","79,70",None),
 (11,"Oude Dock, 't","FSN141",8,"V","01:34:16","2,68","32,77","79,07",None),
 (12,"Serdon","FSN100",8,"H","01:51:38","2,26","53,24","78,19",None),
 (13,"Schone Waardin","FSN039",8,"H","01:46:36","2,37","46,22","77,72",None),
 (14,"Polyester","FSN024",8,"H","01:47:07","2,36","45,22","74,97",None),
 (15,"Haakie, 't","FSN037",8,"1","01:44:20","2,42","41,01","73,46",None),
 (16,"Skomskower","FSN172",8,"1","01:47:02","2,36","43,44","72,19",None),
 (17,"Hjoed 'n Makkie 2","FSN133",8,"V","01:45:32","2,39","40,59","70,31",None),
 (18,"Tobbe","FSN015",6,"2","01:55:22","2,19","39,16","69,62",None),
 (19,"Zeeschuimer","FSN286",8,"2","01:33:29","2,70","27,99","69,20",None),
 (20,"Snurk","FSN084",8,"1","01:33:29","2,70","27,94","69,09",None),
 (21,"Pulletje, 't","FSN003",8,"V","01:42:29","2,46","36,50","68,89",None),
 (22,"Maaike","FSN097",10,"1","01:44:03","2,43","46,91","67,76",None),
 (23,"L8","FSN277",8,"V","01:33:12","2,71","27,10","67,62",None),
 (24,"Skeve, De","FSN160",8,"1","01:52:14","2,25","46,69","67,49",None),
 (25,"Noordvaarder","FSN058",8,"1","01:41:48","2,48","34,12","65,69",None),
 (26,"Kromme Dick","FSN109",8,"1","01:33:51","2,69","26,46","64,68",None),
 (27,"Schonenvaarder","FSN205",8,"1","01:38:29","2,56","30,35","64,41",None),
 (28,"Blik op de Vecht","FSN292",8,"1","01:34:01","2,69","26,24","63,80",None),
 (29,"OKA-18","FSN041",8,"V","01:38:57","2,55","30,30","63,40",None),
 (30,"Fjoer Fûgel","FSN056",6,"2","01:44:11","2,42","26,28","63,02",None),
 (31,"Doorgáán","FSN270",10,"1","01:31:08","2,77","29,53","62,95",None),
 (32,"Rijp, De","FSN002",8,"2","01:52:17","2,25","43,58","62,91",None),
 (33,"Kromhout, 't","FSN049",10,"2","01:47:00","2,36","46,23","61,51",None),
 (34,"Freonskip","FSN264",8,"V","01:39:08","2,55","28,46","59,24",None),
 (35,"Iwan Franko","FSN120",8,"V","01:50:18","2,29","38,76","58,96",None),
 (36,"Haarlemmerhout","FSN163",8,"2","01:36:15","2,62","25,84","58,64",None),
 (37,"Zeeotter II","FSN183",8,"1","01:45:36","2,39","32,84","56,77",None),
 (38,"Aludux","FSN079",8,"2","01:43:38","2,44","31,05","56,73",None),
 (39,"Schokland","FSN104",6,"2","02:00:58","2,09","35,52","54,93",None),
 (40,"El Flamingo II","FSN086",8,"2","01:57:34","2,15","42,41","53,49",None),
 (41,"Stokvisvaarder","FSN266",8,"2","01:42:45","2,46","27,55","51,62",None),
 (42,"Tréwes 1","FSN116",8,"V","01:55:41","2,18","38,74","51,24",None),
 (43,"Houtman","FSN001",8,"V","01:59:19","2,12","41,50","50,13",None),
 (44,"L.A. Buma","FSN253",8,"2","01:52:05","2,25","34,25","49,70",None),
 (45,"Bok, De","FSN191",8,"V","01:38:48","2,56","22,47","47,23",None),
 (46,"Huysman, De","FSN112",8,"2","02:12:19","1,91","42,77","38,12",None),
 (47,"Wolter Huisman","FSN215",10,"V","01:41:58","2,48","23,99","36,77",None),
 (48,"Labora Stulti","FSN244",8,"-","","","","","niet gestart"),
 (49,"Oksewiel I","FSN149",6,"-","","","","","niet gestart"),
 (50,"Vecht, De","FSN126",8,"-","","","","","niet gestart"),
]

LANGWEER_DAMES = [
 (1,"Swan, De","FSN216",8,"H","01:43:11","2,45","35,57","65,75",None),
 (2,"Bruzer","FSN155",6,"H","01:47:56","2,34","29,13","62,90",None),
 (3,"Stielen Bear","FSN130",8,"H","01:48:47","2,32","38,90","61,57",None),
 (4,"Z.S.M.","FSN285",6,"H","01:39:28","2,54","22,42","61,54",None),
 (5,"Zeekameel","FSN297",8,"V","01:50:47","2,28","38,54","57,83",None),
 (6,"Azorean High","FSN077",8,"H","01:29:14","2,83","20,38","57,73",None),
 (7,"Pulp Fiction","FSN082",8,"H","01:45:20","2,40","32,18","56,00",None),
 (8,"Mata Hari","FSN233",6,"H","01:45:13","2,40","23,68","55,11",None),
 (9,"Altied Wad","FSN227",6,"V","01:50:58","2,28","27,05","53,85",None),
 (10,"Argir","FSN229",6,"1","01:44:40","2,41","22,65","53,53",None),
 (11,"VICtorie","FSN150",8,"V","01:52:58","2,24","36,49","51,70",None),
 (12,"Turftraper II, De","FSN241",6,"V","01:47:23","2,35","22,42","49,16",None),
 (13,"Egbert Wagenborg","FSN071",8,"H","01:43:32","2,44","26,82","49,10",None),
 (14,"West-Arvada","FSN072",8,"1","01:41:22","2,49","25,01","48,72",None),
 (15,"Doeke Doeksen","FSN006",8,"1","01:57:08","2,16","38,14","48,58",None),
 (16,"Mare Australis","FSN193",8,"1","01:59:56","2,11","39,79","47,29",None),
 (17,"Vrouwe Geertruida","FSN119",6,"V","01:50:26","2,29","23,39","47,24",None),
 (18,"Lyts Frisia","FSN265",8,"V","01:49:10","2,31","29,80","46,69",None),
 (19,"Elle6","FSN276",6,"V","01:46:09","2,38","20,54","46,59",None),
 (20,"d'Isela","FSN117",8,"1","01:40:26","2,51","22,64","45,32",None),
 (21,"Skomskowster","FSN185",6,"1","02:04:52","2,02","31,06","43,73",None),
 (22,"Minimug","FSN146",6,"2","02:04:43","2,02","29,73","42,00",None),
 (23,"Dolle mina","FSN035",6,"2","02:04:26","2,03","29,17","41,48",None),
 (24,"Danser","FSN014",6,"1","02:06:43","1,99","30,31","40,87",None),
 (25,"Dolle Heks","FSN258",6,"1","01:55:08","2,19","22,00","39,31",None),
 (26,"Visbyvaarder","FSN219",8,"2","01:51:09","2,27","25,32","37,63",None),
 (27,"Beluga","FSN226",6,"1","02:00:15","2,10","23,67","37,21",None),
 (28,"Hjoed 'n Makkie 5,1%","FSN255",6,"V","01:54:58","2,20","20,62","37,00",None),
 (29,"Voorbijganger","FSN179",8,"2","01:48:43","2,32","20,93","33,19",None),
 (30,"Onvervaard","FSN091",6,"1","02:13:16","1,89","28,42","33,05",None),
 (31,"Berend Koster","FSN101",8,"2","01:57:10","2,16","25,72","32,74",None),
 (32,"Moos","FSN125",8,"2","01:49:51","2,30","21,12","32,49",None),
 (33,"Bergenvaarder","FSN206",6,"V","02:04:56","2,02","22,94","32,24",None),
 (34,"Wetterspetter","FSN180",6,"V","02:14:53","1,87","25,98","29,15",None),
 (35,"Leeuwke","FSN026",8,"V","02:15:47","1,86","34,04","28,10",None),
 (36,"Voorganck","FSN189",8,"2","02:02:24","2,06","21,38","23,94",None),
 (37,"Oihonna","FSN220",8,"-","","","","","b.m. (buiten mededinging)"),
]

RACES = [
    ("HKS 2026", "11-04-2026", "16,7", "Dames", HKS_DAMES),
    ("HKS 2026", "11-04-2026", "16,7", "Heren", HKS_HEREN),
    ("Grouster Roeisloepenrace 2026", "25-04-2026", "21,8", "Dames", GROU_DAMES),
    ("Grouster Roeisloepenrace 2026", "25-04-2026", "21,8", "Heren", GROU_HEREN),
    ("Lemmer Iepen Frysk Kampioenskip 2026", "02-05-2026", "22,8", "Heren", LEMMER_HEREN),
    ("Lemmer Iepen Frysk Kampioenskip 2026", "02-05-2026", "22,8", "Dames", LEMMER_DAMES),
    ("Slag om Makkum 2026", "05-09-2026", "11,95", "Heren", MAKKUM_HEREN),
    ("Slag om Makkum 2026", "05-09-2026", "11,95", "Dames", MAKKUM_DAMES),
    ("SloepRoeienLangweer 2026", "26-09-2026", "15,15", "Heren", LANGWEER_HEREN),
    ("SloepRoeienLangweer 2026", "26-09-2026", "15,15", "Dames", LANGWEER_DAMES),
]

styles = getSampleStyleSheet()
title_style = ParagraphStyle("titel", parent=styles["Heading1"], fontSize=14, spaceAfter=2)
sub_style = ParagraphStyle("sub", parent=styles["Normal"], fontSize=9, spaceAfter=1)
note_style = ParagraphStyle("note", parent=styles["Normal"], fontSize=7, textColor=colors.grey, spaceBefore=8)

any_uncertain_used = False

def build_pdf(race_naam, datum, afstand, klasse, rows, filename):
    global any_uncertain_used
    frisian_rows = []
    for r in rows:
        nr_orig, sloep, fsn, n, kl, tijd, snelheid, cw, vermogen, status = r
        if sloep in FRIES:
            vereniging, plaats = FRIES[sloep]
            if "*" in vereniging:
                any_uncertain_used = True
            frisian_rows.append((sloep, vereniging, plaats, fsn, n, kl, tijd, snelheid, cw, vermogen, status))

    doc = SimpleDocTemplate(
        os.path.join(OUT_DIR, filename),
        pagesize=landscape(A4),
        leftMargin=12*mm, rightMargin=12*mm, topMargin=12*mm, bottomMargin=12*mm,
    )
    elems = []
    elems.append(Paragraph(f"{race_naam} — Friese teams — Klassement {klasse}", title_style))
    elems.append(Paragraph(f"Datum: {datum} &nbsp;&nbsp;&nbsp; Afstand: {afstand} km", sub_style))
    elems.append(Paragraph(
        f"Gefilterd op Friese teams uit de volledige uitslag ({len(frisian_rows)} van {len(rows)} sloepen). "
        f"Volgorde en meetwaarden (roeitijd, roeisnelheid, Cw, vermogen per roeier) ongewijzigd overgenomen "
        f"uit de originele uitslag; 'Om te winnen'-kolommen zijn weggelaten omdat die t.o.v. de winnaar van de "
        f"hele race berekend waren, niet t.o.v. de beste Fries. Punten zijn toegekend op basis van de positie in "
        f"dit (Friese) klassement: 1e = 0,9 punt, 2e = 2 punten, en elke volgende plaats 1 punt meer dan de vorige.",
        sub_style))
    elems.append(Spacer(1, 4*mm))

    header = ["Nr", "Sloep", "Vereniging", "Plaats", "FSN-nr", "N", "Kl.",
              "Roeitijd", "Roeisnelh.\n(m/sec)", "Cw\n(kg/m)", "Vermogen/roeier\n(Watt)", "Punten"]
    data = [header]
    for i, (sloep, vereniging, plaats, fsn, n, kl, tijd, snelheid, cw, vermogen, status) in enumerate(frisian_rows, start=1):
        punten = "" if status else ("0,9" if i == 1 else str(i))
        if status:
            data.append([str(i), sloep, vereniging, plaats, fsn, str(n), kl, status, "", "", "", punten])
        else:
            data.append([str(i), sloep, vereniging, plaats, fsn, str(n), kl, tijd, snelheid, cw, vermogen, punten])

    col_widths = [7*mm, 30*mm, 45*mm, 26*mm, 15*mm, 7*mm, 7*mm, 17*mm, 18*mm, 14*mm, 22*mm, 14*mm]
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("FONTSIZE", (0,0), (-1,-1), 7.5),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#dbe9f4")),
        ("GRID", (0,0), (-1,-1), 0.4, colors.grey),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ALIGN", (0,0), (0,-1), "CENTER"),
        ("ALIGN", (4,0), (-1,-1), "CENTER"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f4f7fa")]),
        ("TOPPADDING", (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ]))
    elems.append(t)

    elems.append(Paragraph(
        "Fries team = vereniging opgenomen onder provincie Friesland in het sloeproeiverenigingen-overzicht van "
        "sloeproeien.nl, gematcht op sloepnaam, aangevuld/gecorrigeerd met opgave van de gebruiker "
        "(o.a. Rijp/Rijp, De en Twirre). Deze selectie is met zorg samengesteld maar niet officieel geverifieerd "
        "door de organisatie.",
        note_style))

    doc.build(elems)
    print(f"geschreven: {filename}  ({len(frisian_rows)}/{len(rows)} Friese teams)")

def frisian_ranking(rows):
    """Geeft (sloep, punten_str) voor de Friese sloepen in deze uitslag, in volgorde van het Friese klassement."""
    result = []
    i = 0
    for r in rows:
        nr_orig, sloep, fsn, n, kl, tijd, snelheid, cw, vermogen, status = r
        if sloep in FRIES:
            i += 1
            punten = None if status else (0.9 if i == 1 else float(i))
            result.append((sloep, punten))
    return result

if __name__ == "__main__":
    build_pdf(*RACES[0], "HKS 2026 - Dames - Friese teams.pdf")
    build_pdf(*RACES[1], "HKS 2026 - Heren - Friese teams.pdf")
    build_pdf(*RACES[2], "Grou 2026 - Dames - Friese teams.pdf")
    build_pdf(*RACES[3], "Grou 2026 - Heren - Friese teams.pdf")
    build_pdf(*RACES[4], "IFK Lemmer 2026 - Heren - Friese teams.pdf")
    build_pdf(*RACES[5], "IFK Lemmer 2026 - Dames - Friese teams.pdf")
    build_pdf(*RACES[6], "Slag om Makkum 2026 - Heren - Friese teams.pdf")
    build_pdf(*RACES[7], "Slag om Makkum 2026 - Dames - Friese teams.pdf")
    build_pdf(*RACES[8], "SloepRoeienLangweer 2026 - Heren - Friese teams.pdf")
    build_pdf(*RACES[9], "SloepRoeienLangweer 2026 - Dames - Friese teams.pdf")

    print("Klaar. Output map:", OUT_DIR)
