"""Build js/sanborn-data.js: address -> Sanborn fire-insurance map sheet, from the hand-transcribed street indexes
of the two Library of Congress volumes covering Montclair (public domain, "free to use and reuse"):
  1885: https://www.loc.gov/item/sanborn05557_001/  (index_1885.txt; 4 sheets, downtown core)
  1907: https://www.loc.gov/item/sanborn05475_003/  (index_1907.txt; Essex County Vol. 3, sheets 1-68)
loc_image_ids.json lists each volume's IIIF image ids in viewer order (from the item's ?fo=json record)."""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
IDS = json.load(open(os.path.join(HERE, "loc_image_ids.json")))
VOLS = {
    "1885": {
        "label": "1885 (downtown core)",
        "item": "https://www.loc.gov/item/sanborn05557_001/",
        "res": "g3814mm.g3814mm_g055571885",
        "prefix": "g3814mm",
        "svc": "g3814mm_g055571885",
    },
    "1907": {
        "label": "1907 (Essex County Vol. 3)",
        "item": "https://www.loc.gov/item/sanborn05475_003/",
        "res": "g3814em.g3814em_g05475190703",
        "prefix": "g3814em",
        "svc": "g3814em_g05475190703",
    },
}

out = {}
for y, v in VOLS.items():
    rows = []
    for line in open(os.path.join(HERE, f"index_{y}.txt"), encoding="utf-8"):
        if not line.strip() or line.startswith("#"):
            continue
        st, rng, sheets, note = (line.rstrip("\n").split("|") + [""])[:4]
        lo, hi = (map(int, rng.split("-")) if rng else (None, None))
        rows.append([st, lo, hi, [int(s) for s in sheets.split(",")], note])
    # sheet number -> position in the LOC viewer (sp) and IIIF id
    sheets = {}
    for i, iid in enumerate(IDS[y], 1):
        m = re.search(r"-(\d{4})$", iid)
        if m:
            snum = int(m.group(1))
            if snum > 0:  # skip 0000 key map when mapping numbered sheets
                sheets[snum] = [i, iid]
    out[y] = dict(v, rows=rows, sheets=sheets)

os.makedirs(os.path.join(ROOT, "js"), exist_ok=True)
js = (
    "/* Sanborn fire-insurance maps of Montclair, NJ (Library of Congress, public domain). Built by tools/sanborn/build.py. */\n"
    "var MW = window.MW = window.MW || {};\n"
    'MW.sanbornCredit = "Sanborn Map Company, <i>Montclair</i> (1885) and <i>Essex County, Vol. 3: Montclair</i> (1907)";\n'
    "MW.sanborn = " + json.dumps(out, separators=(",", ":")) + ";\n"
)
open(os.path.join(ROOT, "js", "sanborn-data.js"), "w", encoding="utf-8").write(js)
print({y: (len(o["rows"]), len(o["sheets"])) for y, o in out.items()})
