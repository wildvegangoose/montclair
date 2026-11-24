"""Merge Montclair directory listings (<= 1950) into per-street JSON files.

archive/data/street_index.json   {slug: {name, houses, first, last}}
archive/data/streets/<slug>.json {name, houses: {number: {cards:[...], listings:[...], news:[...]}}}
Only directory years <= CUTOFF (1950) are included (names after 1950 are omitted by design).
"""
import os, re, json, glob, collections, difflib, urllib.parse
from common import OUT, slug, SLUG, TOWN, canon_street, normalize_raw_street, _split_street, _edit_dist, SUFFIX

CUTOFF = TOWN["directories"]["name_cutoff_year"]
VIEWER = "https://www.digifind-it.com/IDIViewer/web/viewer.html?file="
CONF = json.load(open(os.path.join(OUT, "data", "streets.json")))
houses = collections.defaultdict(lambda: collections.defaultdict(lambda: {"cards": [], "listings": [], "news": []}))


def norm_num(n):
    n = (n or "").strip().upper()
    m = re.match(r"^(\d+)", n)
    return m.group(1) if m else n


GIVEN = set("""Albert Alfred Alice Ann Anna Anne Arthur Barbara Benjamin Bertha Betty Carl Carrie Catherine Charles Clara Daniel David Donald
Dorothy Edith Edna Edward Edwin Eleanor Elizabeth Ella Ellen Emily Emma Ernest Esther Ethel Eugene Evelyn Florence Frances Francis Frank
Fred Frederick George Gertrude Grace Harold Harriet Harry Helen Henry Herbert Howard Ida Irene Isabel Jacob James Jane Jean Jennie John
Joseph Josephine Julia Katherine Kenneth Laura Lawrence Leo Leonard Lillian Louis Louise Lucy Mabel Margaret Marie Marion Martha Mary
Mildred Minnie Nellie Norman Patrick Paul Peter Philip Ralph Raymond Richard Robert Rose Ruth Samuel Sarah Stanley Theodore Thomas Victor
Viola Walter William Willard""".split())

OCC_STOP = set("""wid elk clk mgr eng ins emp tchr slsman pres sec acct mech elec arch atty lwyr carp pntr mach rest tel real est oil gas
auto bank asst supv foreman driver dentist lawyer writer student nurse artist tailor butcher grocer baker barber janitor fireman policeman
broker printer chemist doctor author editor painter plumber mason cook maid widow in of at and for h r res bds rms""".split())

DITTO_RE = re.compile(r"^(?:[•■▪◦*.,'’‘`]+\s*)?(?:[—\-–_~]{1,3}|[“\"”]{1,2})\s*")

HEADINGS = {
    "Montclair", "Upper", "Bloomfield", "Glen", "Ridge", "Verona", "Caldwell", "Essex", "Fells", "Cedar",
    "Oranges", "Orange", "Directory", "Co", "Inc", "The", "Eo", "So", "Wo", "Newark", "Irvington", "Arlington",
    "Street", "Avenue", "Road", "Place", "Terrace", "Mrs", "Miss", "Rev", "Dr", "Price", "Lee", "Baldwin",
    "Th", "Name", "Motor", "Sum", "Su", "Sm", "In", "Ck", "Low", "Her", "Al", "St", "La",
}


def format_surname(raw_tok):
    s = raw_tok.strip(" ,.;:'’‘\"“”`")
    s = re.sub(r"^O['’‘]([A-Za-z])", lambda m: "O’" + m.group(1).upper(), s)
    if re.match(r"^(?:Mac|Mc|De|Di|Du|La|Le|Vander|Van|Von|St|O['’])[A-Z]", s):
        return s
    return s.title()


def _split_echoed_surname(surname, given, direct, text):
    if direct or DITTO_RE.match((text or "").strip()):
        return surname, given, direct
    m_v = re.match(r"^(Vander|Van|Von|De|Di|Du|La|Le)\s+([A-Z][a-z]{2,})\s+([A-Z][a-z]{2,}.*)$", given or "")
    if m_v:
        return m_v.group(1) + m_v.group(2), m_v.group(3), True
    gtoks = (given or "").split()
    if len(gtoks) >= 2 and surname:
        w0 = gtoks[0].rstrip(".,")
        w1 = gtoks[1].rstrip(".,")
        if (
            len(w0) >= 4
            and re.match(r"^[A-Z][a-z]+$", w0)
            and w0 not in GIVEN
            and len(w1) >= 3
            and re.match(r"^[A-Z][a-z]+$", w1)
            and w1 not in {"Mrs", "Miss", "Inc", "Corp"}
            and w0.lower() != surname.lower()
            and (
                difflib.SequenceMatcher(None, w0.lower(), surname.lower()).ratio() >= 0.62
                or (len(surname) >= 4 and w0[:4].lower() == surname[:4].lower())
            )
        ):
            return format_surname(w0), " ".join(gtoks[1:]), True
    return surname, given, direct


dir_files = sorted(glob.glob(os.path.join(OUT, "data", "dir_*.json")))
for f in dir_files:
    y = int(re.search(r"dir_(\d+)", f).group(1))
    if y > CUTOFF:
        continue
    for r in json.load(open(f)):
        raw_st = r.get("raw_street") or ""
        st = canon_street(raw_st, CONF) if raw_st else r.get("street")
        if not st or st.startswith("~"):
            continue
        surname = (r.get("surname") or "").strip(" ,.;:'’‘\"“”`")
        given = re.sub(r"^([A-Z][a-z]+)\s+0(?=\s|$)", r"\1 O", r.get("given") or "")
        given = re.sub(r"\b([A-Z])\s+([a-z]{2,})", r"\1\2", given)
        given = re.sub(r"\b0\b", "O", given)
        given = re.sub(r"\b1\b", "I", given)
        spouse = r.get("spouse")
        if spouse:
            spouse = re.sub(r"\b([A-Z])\s+([a-z]{2,})", r"\1\2", spouse)
            spouse = re.sub(r"\b0\b", "O", spouse)
            spouse = re.sub(r"\b1\b", "I", spouse)
        occ = r.get("occ") or ""
        direct = bool(r.get("direct"))
        old_sur = surname
        m_caps = re.match(
            r"^([A-Z]{3,})\s+([A-Z]{2,}(?:\s+[A-Z]\.?)*)\s+(?:\(([A-Za-z .'’]+)\)\s+)?([a-z].*)$",
            (r.get("text") or "").strip(),
        )
        if m_caps and m_caps.group(1).title() not in HEADINGS:
            surname = format_surname(m_caps.group(1).title())
            given = " ".join(w.title() for w in m_caps.group(2).split())
            if m_caps.group(3) and not spouse:
                spouse = m_caps.group(3).strip()
            occ = re.split(r"\s(?:r|h|bds|res)\s+(?:\([0-9A-Za-z]+\)\s+)?\d", m_caps.group(4))[0].strip(" ,;")[:80]
            direct = True
        else:
            surname, given, direct = _split_echoed_surname(surname, given, direct, r.get("text"))
        src_quoted = urllib.parse.quote(r["src"], safe="/")
        entry = {
            "year": r["year"],
            "surname": surname,
            "given": given,
            "spouse": spouse,
            "occ": occ,
            "tenure": r["tenure"],
            "town": r.get("town") or "Montclair",
            "crop": r.get("crop"),
            "src": f"{VIEWER}{src_quoted}#page={r['page']}",
            "text": r["text"],
            "_direct": direct,
        }
        if old_sur and surname != old_sur:
            entry["surname_ocr"] = old_sur
        houses[st][norm_num(r["number"])]["listings"].append(entry)


def _mid_initial(given):
    parts = [p.rstrip(".") for p in (given or "").split() if p.rstrip(".") not in {"Jr", "Sr", "Mrs", "Miss", "Rev", "Dr"}]
    return parts[1][0].upper() if len(parts) >= 2 and parts[1] else ""


def _spouse_first(spouse):
    parts = (spouse or "").split()
    return parts[0].rstrip(".").lower() if parts else ""


def _wid_husband(occ):
    m = re.search(r"\bwid\s+([A-Z][a-z]+)", occ or "")
    return m.group(1).lower() if m else ""


def harmonize(ls):
    direct_counts = collections.Counter(l["surname"] for l in ls if l.get("_direct") and l["surname"] not in HEADINGS and len(l["surname"]) >= 3)
    house_surnames = collections.Counter(l["surname"] for l in ls if l["surname"] not in HEADINGS and len(l["surname"]) >= 3)

    groups = collections.defaultdict(list)
    for l in ls:
        g = (l["given"] or "").split()
        if g and len(g[0].rstrip(".")) > 1:
            groups[g[0].rstrip(".")].append(l)

    for first_name, g in groups.items():
        if len(g) < 2:
            continue
        votes = collections.Counter()
        for l in g:
            s = l["surname"]
            if not s or s in HEADINGS or len(s) <= 2:
                continue
            if not l.get("_direct") and s in GIVEN:
                continue
            votes[s] += 1
        if not votes:
            continue

        for l in g:
            cur = l["surname"]
            candidates = [(s, cnt) for s, cnt in votes.most_common() if s != cur]
            if not candidates:
                continue
            cur_mid = _mid_initial(l["given"])
            cur_sp = _spouse_first(l["spouse"])
            cur_wid = _wid_husband(l["occ"])

            chosen = None
            for top, n in candidates:
                top_rows = [x for x in g if x["surname"] == top]
                if not top_rows:
                    continue
                top_mids = {_mid_initial(x["given"]) for x in top_rows if _mid_initial(x["given"])}
                top_sps = {_spouse_first(x["spouse"]) for x in top_rows if _spouse_first(x["spouse"])}
                top_wids = {_wid_husband(x["occ"]) for x in top_rows if _wid_husband(x["occ"])}
                if (cur_mid and top_mids and cur_mid not in top_mids) or (cur_sp and top_sps and cur_sp not in top_sps) or (cur_wid and top_wids and cur_wid not in top_wids):
                    continue
                ratio = difflib.SequenceMatcher(None, cur.lower(), top.lower()).ratio()
                ed = _edit_dist(cur.lower(), top.lower())
                same_sp = bool(cur_sp and cur_sp in top_sps)
                same_wid = bool(cur_wid and cur_wid in top_wids)
                same_mid = bool(cur_mid and cur_mid in top_mids)

                if l.get("_direct"):
                    if (cur in HEADINGS or len(cur) <= 2) and (n >= 2 or same_sp or same_wid):
                        chosen = top; break
                    if (ed <= 2 and ratio >= 0.72) and (n >= 2 or direct_counts[top] >= 2) and direct_counts[cur] <= 1:
                        chosen = top; break
                    if same_sp and ratio >= 0.55 and (n >= 2 or direct_counts[top] >= 2) and direct_counts[cur] <= 1:
                        chosen = top; break
                else:
                    cur_is_confirmed = direct_counts[cur] >= 1 or (
                        house_surnames[cur] >= 2 and cur not in GIVEN and cur not in HEADINGS
                        and not ((direct_counts[top] >= 1 or house_surnames[top] >= 3) and (same_sp or same_wid or same_mid))
                    )
                    if cur_is_confirmed:
                        if ed <= 2 and ratio >= 0.72 and house_surnames[top] > house_surnames[cur]:
                            chosen = top; break
                        continue
                    if cur in HEADINGS or len(cur) <= 3 or cur in GIVEN:
                        if n >= 2 or direct_counts[top] >= 1 or same_sp or same_wid:
                            chosen = top; break
                    if ratio >= 0.62 and (n >= 2 or direct_counts[top] >= 1):
                        chosen = top; break
                    min_ygap = min(abs(l["year"] - x["year"]) for x in top_rows)
                    if (same_sp or same_wid) and min_ygap <= 10 and (ratio >= 0.45 or (n >= 1 and house_surnames[top] >= 2 and house_surnames[cur] <= 1)):
                        chosen = top; break
                    if same_mid and min_ygap <= 4 and n >= 2 and ratio >= 0.55:
                        chosen = top; break
            if chosen:
                l["surname_ocr"] = cur
                l["surname"] = chosen

    for l in ls:
        if l["surname"] in HEADINGS:
            l["surname_ocr"] = l["surname"]
            l["surname"] = ""
        l.pop("_direct", None)


streets_dir = os.path.join(OUT, "data", "streets")
os.makedirs(streets_dir, exist_ok=True)
for old_f in glob.glob(os.path.join(streets_dir, "*.json")):
    os.remove(old_f)

index = {}
for street, hs in houses.items():
    clean = street.lstrip("~")
    s = slug(clean)
    for h in hs.values():
        harmonize(h["listings"])
        h["listings"].sort(key=lambda l: (l["year"], l["tenure"] != "householder", l["surname"]))
        seen = set()
        h["listings"] = [
            l for l in h["listings"]
            if not ((k := (l["year"], l["surname"], l["given"])) in seen or seen.add(k))
        ]
    years = [l["year"] for h in hs.values() for l in h["listings"]]
    data = {"name": clean, "confirmed": True, "houses": hs}
    json.dump(data, open(os.path.join(streets_dir, s + ".json"), "w"))
    index[s] = {"name": clean, "houses": len(data["houses"]), "first": min(years) if years else None, "last": max(years) if years else None}

json.dump(index, open(os.path.join(OUT, "data", "street_index.json"), "w"))
print(
    f"{len(index)} streets, {sum(v['houses'] for v in index.values())} addresses, "
    f"{sum(len(h['listings']) for hs in houses.values() for h in hs.values())} listings"
)
