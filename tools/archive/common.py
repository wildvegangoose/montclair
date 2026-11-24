"""Shared helpers for the Montclair library-archive pipeline.

Source: Montclair History Online (Montclair Public Library & Montclair History Center),
hosted by Digifind-IT (configured in tools/town.json).
"""
import os, re, time, urllib.request, urllib.parse, difflib, json

BASE = "https://www.digifind-it.com"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "archive")
TOWN = json.load(open(os.path.join(ROOT, "tools", "town.json")))
UA = TOWN["user_agent"]
SLUG = TOWN["digifind"]["slug"]
DIG = TOWN["digifind"]


def fetch(url, dest=None, tries=4, pause=0.4, timeout=180):
    url = urllib.parse.quote(url, safe=":/?&=%#")
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = r.read()
            time.sleep(pause)
            if dest:
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with open(dest, "wb") as f:
                    f.write(data)
                return dest
            return data
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 * (i + 1))


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


# --- street names -------------------------------------------------------
SUFFIX = {
    "av": "Avenue", "ave": "Avenue", "avenue": "Avenue", "ay": "Avenue",
    "rd": "Road", "road": "Road",
    "pl": "Place", "pi": "Place", "place": "Place",
    "ter": "Terrace", "terr": "Terrace", "terrace": "Terrace",
    "dr": "Drive", "drive": "Drive",
    "ct": "Court", "court": "Court",
    "la": "Lane", "ln": "Lane", "lane": "Lane",
    "pky": "Parkway", "pkv": "Parkway", "pkwy": "Parkway", "parkway": "Parkway",
    "st": "Street", "street": "Street",
    "blvd": "Boulevard", "boulevard": "Boulevard",
    "way": "Way", "cir": "Circle", "circle": "Circle",
    "cres": "Crescent", "crescent": "Crescent",
    "pk": "Park", "park": "Park",
    "plz": "Plaza", "plaza": "Plaza",
    "sq": "Square", "square": "Square",
    "hgts": "Heights", "crest": "Crest",
}

DIRS = {
    "N": "NORTH", "S": "SOUTH", "E": "EAST", "W": "WEST",
    "NORTH": "NORTH", "SOUTH": "SOUTH", "EAST": "EAST", "WEST": "WEST",
}

ORDINALS = {
    "1ST": "First", "2D": "Second", "2ND": "Second", "3D": "Third",
    "3RD": "Third", "4TH": "Fourth", "5TH": "Fifth",
}

# Known Montclair historic spelling/spacing variants -> canonical street names
STREET_ALIASES = {
    "GLEN RIDGE AVENUE": "GLENRIDGE AVENUE",
    "GLEN RIDGE PARKWAY": "GLENRIDGE PARKWAY",
    "CLAIRMONT AVENUE": "CLAREMONT AVENUE",
    "CLAIRMONT PLACE": "CLAREMONT PLACE",
    "CLAIRWILL AVENUE": "CLAREWILL AVENUE",
    "BELLEVIEW AVENUE": "BELLEVUE AVENUE",
    "BELLEVIEW PLAZA": "BELLEVUE PLAZA",
    "GORDON HURST AVENUE": "GORDONHURST AVENUE",
    "WAY SIDE PLACE": "WAYSIDE PLACE",
    "SAINT LUKES PLACE": "ST LUKES PLACE",
    "ST LUKE S PLACE": "ST LUKES PLACE",
    "ST LUKE PLACE": "ST LUKES PLACE",
    "MT HEBRON ROAD": "MOUNT HEBRON ROAD",
    "MT VIEW PLACE": "MOUNT VIEW PLACE",
    "MOUNTAIN VIEW PLACE": "MOUNT VIEW PLACE",
    "MT VERNON ROAD": "MOUNT VERNON ROAD",
    "BELLAIR DRIVE": "BELLAIRE DRIVE",
    "LA SALLE ROAD": "LASALLE ROAD",
    "ORANGE AVENUE": "ORANGE ROAD",
    "CRESCENT STREET": "THE CRESCENT",
    "CRESCENT": "THE CRESCENT",
    "THE CRESCENT STREET": "THE CRESCENT",
    "UPPER MOUNTAIN": "UPPER MOUNTAIN AVENUE",
    "NORTH MOUNTAIN": "NORTH MOUNTAIN AVENUE",
    "SOUTH MOUNTAIN": "SOUTH MOUNTAIN AVENUE",
    "NORTH FULLERTON": "NORTH FULLERTON AVENUE",
    "SOUTH FULLERTON": "SOUTH FULLERTON AVENUE",
    "FULLERTON AVENUE": "SOUTH FULLERTON AVENUE",
    "BLOOMFIELD": "BLOOMFIELD AVENUE",
    "VALLEY": "VALLEY ROAD",
    "MIDLAND": "MIDLAND AVENUE",
    "CLAREMONT": "CLAREMONT AVENUE",
    "WATCHUNG": "WATCHUNG AVENUE",
    "BELLEVUE": "BELLEVUE AVENUE",
    "HIGHLAND": "HIGHLAND AVENUE",
    "LORRAINE": "LORRAINE AVENUE",
    "WILDWOOD": "WILDWOOD AVENUE",
    "INWOOD": "INWOOD AVENUE",
    "FERNWOOD": "FERNWOOD AVENUE",
    "GREENWOOD": "GREENWOOD AVENUE",
    "WILLOWDALE": "WILLOWDALE AVENUE",
    "CLUB STREET": "CLUB ROAD",
    "DRAPER STREET": "DRAPER TERRACE",
    "WALNUT CRES": "WALNUT CRESCENT",
    "MC DONOUGH STREET": "MCDONOUGH STREET",
    "VAN VLECK": "VAN VLECK STREET",
    "VAN GIESON GAP": "VAN GIESON GAP ROAD",
}

BASE_ALIASES = {
    "GLEN RIDGE": "GLENRIDGE",
    "CLAIRMONT": "CLAREMONT",
    "CLAIRWILL": "CLAREWILL",
    "BELLEVIEW": "BELLEVUE",
    "GORDON HURST": "GORDONHURST",
    "WAY SIDE": "WAYSIDE",
    "SAINT LUKES": "ST LUKES",
    "ST LUKE S": "ST LUKES",
    "ST LUKE": "ST LUKES",
    "MT HEBRON": "MOUNT HEBRON",
    "MT VIEW": "MOUNT VIEW",
    "MT VERNON": "MOUNT VERNON",
    "BELLAIR": "BELLAIRE",
    "LA SALLE": "LASALLE",
    "MC DONOUGH": "MCDONOUGH",
    "BLOOMFLELD": "BLOOMFIELD",
    "BLOOMFLEID": "BLOOMFIELD",
    "BLOOMFIEL": "BLOOMFIELD",
    "CLAREINONT": "CLAREMONT",
    "FULLERTONN": "FULLERTON",
    "MOUNTAJN": "MOUNTAIN",
    "VALIEV": "VALLEY",
    "IN WOOD": "INWOOD",
    "FERN WOOD": "FERNWOOD",
    "GREEN WOOD": "GREENWOOD",
    "WILD WOOD": "WILDWOOD",
    "WILLOW DALE": "WILLOWDALE",
    "NORTH VIEW": "NORTHVIEW",
    "ELM WOOD": "ELMWOOD",
    "OAK WOOD": "OAKWOOD",
    "GLEN WOOD": "GLENWOOD",
    "EDGE MONT": "EDGEMONT",
    "EDGE WOOD": "EDGEWOOD",
    "EDGE CLIFF": "EDGECLIFF",
    "UNDER CLIFF": "UNDERCLIFF",
    "ROCK LEDGE": "ROCKLEDGE",
    "AFTER GLOW": "AFTERGLOW",
    "WATER BURY": "WATERBURY",
    "FAIR FIELD": "FAIRFIELD",
    "PARK HURST": "PARKHURST",
    "MONT CLAIR": "MONTCLAIR",
    "HAW THORNE": "HAWTHORNE",
    "EAGLE ROCK": "EAGLE ROCK",
    "LLEW ELLYN": "LLEWELLYN",
}


def load_streets():
    p = os.path.join(OUT, "data", "streets.json")
    return json.load(open(p)) if os.path.exists(p) else []


def _edit_dist(a, b):
    if a == b:
        return 0
    if abs(len(a) - len(b)) > 2:
        return 99
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb))
        prev = cur
    return prev[-1]


def normalize_raw_street(raw):
    """Pre-clean OCR'd street text: fix fused suffixes, split 'p i', ordinals, and single-letter OCR splits."""
    s = re.sub(r"[^A-Za-z0-9 ]", " ", raw or "").strip()
    if not s:
        return ""
    s = re.sub(r"\b([1-5])\s+(st|nd|rd|th|d)\b", r"\1\2", s, flags=re.I)
    s = re.sub(r"\bpk\s*y\s*([NSEW])\b", r"pkwy \1", s, flags=re.I)
    s = re.sub(r"\b(pkwy|pky|pkv)([NSEW])\b", r"pkwy \2", s, flags=re.I)
    s = re.sub(r"\b(rd|av|ave|st|pl|dr|la|ter|ct)I?([NSEW])\b", r"\1 \2", s)
    s = re.sub(r"\b([A-Za-z]{4,})(av|rd|pl|st|dr|ter)\b", r"\1 \2", s)
    s = re.sub(r"\bp\s+[il]\s*$", "pl", s, flags=re.I)
    # Fix OCR-exploded single-word street names like "V a lle y"
    if (
        re.match(r"^[A-Z](?:\s+[A-Za-z]{1,3}){2,}$", s)
        and s.split()[-1].lower() not in SUFFIX
        and s.split()[-1].upper() not in DIRS
    ):
        s = s.replace(" ", "")
    # Rejoin OCR single-letter split at start of capitalized word ("V alley", "G lenridge")
    s = re.sub(r"\b([A-Z])\s+([a-z]{2,})\b", r"\1\2", s)
    s = re.sub(
        r"\b([A-Z][a-z]+)\s+([a-z]{1,3})\b",
        lambda m: m.group(0) if m.group(2).lower() in SUFFIX else m.group(1) + m.group(2),
        s,
    )
    # Expand leading single-letter direction ("N Fullerton av" -> "NORTH Fullerton av", "S Mountain av" -> "SOUTH Mountain av")
    s = re.sub(r"^([NSEW])\s+(?=[A-Za-z0-9]{2,})", lambda m: DIRS[m.group(1).upper()] + " ", s)
    # Pull trailing direction ("Fullerton av N" -> "NORTH Fullerton av")
    d = re.match(r"^(.*\S)\s+([NSEW]|North|South|East|West)$", s, flags=re.I)
    if d:
        s = DIRS[d.group(2).upper()] + " " + d.group(1)
    # Normalize "Up Mountain" / "U Mountain" -> "Upper Mountain"
    s = re.sub(r"^(?:Up|Upp|U)\s+Mountain\b", "Upper Mountain", s, flags=re.I)
    toks = [ORDINALS.get(tok.upper(), tok) for tok in s.split()]
    return " ".join(toks).strip()


def _split_street(name):
    """Split canonical uppercase street into (dir_prefix, base_name, suffix).
    Preserves 'UPPER MOUNTAIN' as distinct base from 'NORTH/SOUTH MOUNTAIN'."""
    w = name.upper().split()
    if not w:
        return "", "", ""
    suf = ""
    if len(w) >= 2 and w[-1].lower() in SUFFIX:
        suf = SUFFIX[w[-1].lower()].upper()
        w = w[:-1]
    dir_p = ""
    if len(w) >= 2 and w[0] in ("NORTH", "SOUTH", "EAST", "WEST"):
        dir_p = w[0]
        w = w[1:]
    base = " ".join(w)
    base = BASE_ALIASES.get(base, base)
    return dir_p, base, suf


def canon_street(raw, streets):
    """Map an OCR'd Montclair street ('N Fullerton av', 'Glen Ridge av', 'Park') to a canonical name in streets.json.
    Never crosses directional prefixes (NORTH vs SOUTH vs UPPER) or unrelated street suffixes."""
    if not raw or not streets:
        return None
    s = normalize_raw_street(raw)
    if not s:
        return None
    w = s.split()
    if w[-1].lower() in SUFFIX:
        w[-1] = SUFFIX[w[-1].lower()]
    elif len(w) == 1 or (len(w) == 2 and w[0].upper() in ("NORTH", "SOUTH", "EAST", "WEST")):
        # Check aliases first before assuming Street (e.g. "Bloomfield" -> "BLOOMFIELD AVENUE", "N Fullerton" -> "NORTH FULLERTON AVENUE")
        bare_cand = " ".join(w).upper()
        if bare_cand in STREET_ALIASES:
            cand = STREET_ALIASES[bare_cand]
            if cand in streets:
                return cand
        w.append("Street")
    cand = " ".join(w).upper()
    cand = STREET_ALIASES.get(cand, cand)
    if cand in streets:
        return cand

    c_dir, c_base, c_suf = _split_street(cand)
    rebuilt = " ".join(x for x in (c_dir, c_base, c_suf) if x)
    rebuilt = STREET_ALIASES.get(rebuilt, rebuilt)
    if rebuilt in streets:
        return rebuilt
    c_dir, c_base, c_suf = _split_street(rebuilt)
    c_ns = c_base.replace(" ", "")

    suffixed = [st for st in streets if _split_street(st)[2]]
    parsed = [(st, *_split_street(st)) for st in suffixed]

    # Exact space-collapsed match within same (dir, suffix)
    for st, s_dir, s_base, s_suf in parsed:
        if s_dir == c_dir and s_suf == c_suf and s_base.replace(" ", "") == c_ns:
            return st

    # If suffix was defaulted to STREET for a single-word street that uniquely exists with another suffix (e.g. "Midland" -> MIDLAND AVENUE)
    raw_toks = normalize_raw_street(raw).split()
    if raw_toks and raw_toks[-1].lower() not in SUFFIX:
        hits = [st for st, s_dir, s_base, _ in parsed if s_dir == c_dir and s_base.replace(" ", "") == c_ns]
        if len(hits) == 1:
            return hits[0]

    # Fuzzy OCR match on BASE NAME ONLY within same (dir, suffix)
    if len(c_ns) >= 5:
        max_d = 1 if len(c_ns) <= 7 else 2
        best, best_score = None, (99, 0.0)
        for st, s_dir, s_base, s_suf in parsed:
            if s_dir != c_dir or s_suf != c_suf:
                continue
            s_ns = s_base.replace(" ", "")
            d = _edit_dist(c_ns, s_ns)
            if d <= max_d:
                ratio = difflib.SequenceMatcher(None, c_ns, s_ns).ratio()
                if ratio >= 0.78 and (d, -ratio) < best_score:
                    best, best_score = st, (d, -ratio)
        if best:
            return best

    return None
