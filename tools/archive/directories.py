"""Extract Montclair residents from Montclair History Online digitized city directories (pre-1951).

For each Price & Lee Montclair volume (1910-1949):
  1. Download the PDF from Digifind-IT (or reuse local sample if present).
  2. Automatically detect the exact contiguous [start_page, end_page] of the Montclair Alphabetical
     Directory section (excluding Bloomfield, Glen Ridge, Verona, Caldwell, Street Guides, Buyers' Guides,
     and any misbound years in the microfilm scan).
  3. Extract word bounding boxes via `pdftotext -bbox-layout -f START -l END`, filter rotated side-margin
     ads, segment 1-column or 2-column layouts with skew-aware local margins, build a global monotonic
     alphabetical surname spine (weighted LNDS) so dropped dittos/OCR noise never poison active surnames,
     and match Montclair residential addresses against the 392 confirmed Montclair streets in streets.json.
  4. For selected milestone crop years, render and crop each householder's scanned line (with surname
     header strip stitched above ditto entries).
"""
import os, re, sys, json, html, bisect, subprocess, collections, urllib.parse
from common import BASE, OUT, fetch, slug, load_streets, canon_street, normalize_raw_street, SUFFIX, SLUG, DIG, TOWN

CROP_YEARS = set(TOWN["directories"]["crop_years"])
CUTOFF = TOWN["directories"]["name_cutoff_year"]
TMP = os.path.join(OUT, "_tmp")
os.makedirs(TMP, exist_ok=True)
STREETS = load_streets()

PAGE_RE = re.compile(r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', re.S)
LINE_RE = re.compile(r'<line xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</line>', re.S)
WORD_RE = re.compile(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', re.S)

DITTO_CORE = r"(?:[—\-–_~]{1,3}|[“\"”]{1,2})"
DITTO_START = re.compile(rf"^(?:[•■▪◦*.,'’‘`^]+\s*)?(?:{DITTO_CORE}|\^\s+|[Il1|!]{{1,2}}[-—–])\s*(.*)$")
EARLY_QUOTE_DITTO = re.compile(r"^(?:[uUwtvfIl1*“\"]|cc|\(\s*t|\*{1,2}|44|1“)\s+([A-Z][a-z].*)$")
PURE_NOISE = re.compile(r"^[\s•■▪◦*.,'’‘`—\-–_~“\"”»«<>^|=+:;/\\()0-9]{1,4}$")

TEN_RE = r"(h|r|bds|rms|res|bd)"
APT_RE = r"(?:\([0-9A-Za-z]{1,4}\)\s+)?"
NUM_RE = r"(\d{1,4}[A-Za-z]?(?:-\d+)?)"
STR_RE = r"([A-Z0-9][A-Za-z0-9.'’]*(?:\s[A-Za-z0-9.'’]+){0,4}?)"
OPT_MC = r"(?:\s+(?:U\s*M|M))?"

# Montclair entries in Montclair's own directory section have NO trailing town code (or optional M / UM)
ADDR_STD = re.compile(rf"\b{TEN_RE}\.?\s+{APT_RE}['’‘]?{NUM_RE}\s+{STR_RE}{OPT_MC}\.?$")
ADDR_DO = re.compile(rf"\b{NUM_RE}\s+{STR_RE}{OPT_MC}\s+{TEN_RE}\.?\s+do\.?$")

OTHER_TOWN_END = re.compile(
    r"\b(?:h|r|bds|rms|res|bd)\.?\s+(?:at\s+)?(?:"
    r"Newark|Bloomfield|Glen\s*Ridge|Verona|Caldwell|North\s*Caldwell|West\s*Caldwell|"
    r"Essex\s*Fells|Cedar\s*Grove|Orange|East\s*Orange|West\s*Orange|South\s*Orange|"
    r"E\s*Orange|W\s*Orange|S\s*Orange|Maplewood|Nutley|Belleville|Passaic|Paterson|"
    r"Clifton|Little\s*Falls|New\s*York|Brooklyn|Jersey\s*City|Hoboken|Elizabeth|Irvington|"
    r"B|GR|G\s*R|V|C|EF|CG|O|EO|WO|SO|NY|NJ)\.?$",
    re.I,
)

# Any completed entry ending so subsequent lines never glue onto a finished entry
COMPLETE_END = re.compile(
    r"(?:\b(?:h|r|bds|rms|res|bd)\.?\s+(?:at\s+[A-Z][A-Za-z .]+|do\.?|"
    r"(?:\([0-9A-Za-z]+\)\s+)?\d+[A-Za-z-]*\s+[A-Za-z0-9.'’ ]{3,})"
    r"|\brem\s+to\s+[A-Z][A-Za-z .]+"
    r"|\bdied\s+[A-Z][a-z]+\s+\d+.*)"
    r"(?:\s*[—\-–]+\s*See\b.*)?$",
    re.I,
)
SEE_TAIL_RE = re.compile(r"\s*[—\-–]+\s*See\b.*$", re.I)
CONT_TAIL_RE = re.compile(r"\s*(?:[—\-–]+\s*|\(\s*)Continued\)?.*$", re.I)

ABBR_PAIRS = {"UM", "WO", "EO", "SO", "NY", "NJ", "US", "PA", "GR"}
DITTO_CHARS = set("—-–_~“\"”•■▪◦*")

OCC_STOP = set("""wid elk clk mgr eng ins emp tchr slsman pres sec treas acct mech elec arch archt atty lwyr carp pntr mach rest tel real est
oil gas auto bank asst supv foreman driver dentist lawyer writer student nurse artist tailor butcher grocer baker barber janitor fireman
policeman broker printer chemist doctor author editor painter plumber mason cook maid widow housekpr bkkpr steno chauf lab drsmkr seamstress
rem died see inc co corp bros sons and in of at for h r res bds rms bd do""".split())

HEADING_WORDS = {
    "Montclair", "Bloomfield", "Glen", "Ridge", "Verona", "Caldwell", "Essex", "Fells", "Cedar", "Grove",
    "Oranges", "Orange", "Directory", "Price", "Lee", "Baldwin", "Newark", "Irvington", "Upper",
    "Sales", "Service", "Parts", "Phone", "Tel", "Telephone", "Co", "Inc", "Corp", "Ltd", "See", "Continued",
}

TEN = {"h": "householder", "r": "resident", "res": "resident", "bds": "boarder", "bd": "boarder", "rms": "rooms"}

OCR_FIRST = {
    "a": set("lra"), "b": set("rjpehb"), "c": set("ogqdce"), "d": set("oqd"),
    "g": set("cqog"), "h": set("nbh"), "m": set("nm"), "n": set("mnu"),
    "r": set("pbkr"), "s": set("fs"), "w": set("vw"),
}


def pdf_url_for(y):
    return f"/{SLUG}/data/City Directories/{y}.pdf"


def alpha_key(sur):
    if not sur:
        return ""
    s = re.sub(r"^St([A-Z])", r"Saint\1", sur.strip())
    return re.sub(r"[^a-z]", "", s.lower())


def find_montclair_alpha_range(pdf, target_year):
    """Scan all pages via fast pdftotext and return (start_pno, end_pno) of the full A-Z Montclair Alphabetical Directory."""
    raw = subprocess.run(["pdftotext", pdf, "-"], capture_output=True, text=True, errors="ignore").stdout
    pages = raw.split("\x0c")
    if pages and not pages[-1].strip():
        pages.pop()
    n = len(pages)
    if n == 0:
        return 1, 0

    town_tag = [None] * n  # "MC" or "OTHER"
    yr_tag = [None] * n
    is_alpha = [False] * n
    is_street_guide = [False] * n
    alpha_counts = [0] * n

    res_re = re.compile(r"\b(?:h|r|bds|res)\s+(?:\([A-Za-z0-9]+\)\s+)?(?:\d+\s+[A-Z]|do\b)")
    # Genuine Price & Lee street/numerical guide cues (avoid matching display ads with stray numbers)
    sg_re = re.compile(
        r"(?:\bfr\s+\d+[\d/]*\s+[A-Za-z]+|\b[A-Z][A-Za-z ]+(?:Av|St|Rd|Pl|Ter|Dr)\s*[—\-–]+\s*continued\b"
        r"|\b(?:Av|St|Rd|Pl|Ter|Dr)\s+(?:begins|crosses|ends|intersects)\b"
        r"|^\d+[A-Za-z]?\s+[©O®@ΔA]\s*[A-Z][a-z]+)",
        re.M | re.I,
    )

    other_town_dir_re = re.compile(
        r"(?:BLOOMFIELD|GLENRIDGE|VERONA|CALDWELL|CEDARGROVE|ESSEXFELLS|BELLEVILLE|NUTLEY)"
        r"(?:\(?\d{4}\)?)?(?:NUMERICAL|BUSINESS|HOUSE|STREET)?DIR(?:ECTORY|ECTO|EC)?\b"
    )
    mc_dir_re = re.compile(
        r"MONTCLAIR(?:\(?\d{4}\)?)?(?:DIR(?:ECTORY|ECTO|EC)?|DIEECTO|DIKECTO)"
    )
    mc_non_alpha_re = re.compile(
        r"MONTCLAIR(?:\(?\d{4}\)?)?(?:BUSINESSDIR|CLASSIFIED|BUYERSGUIDE|HOUSEDIR|STREETGUIDE|NUMERICAL)"
        r"|CLASSIFIEDBUSINESS|CLASSIFIEDDIR|BUYERSGUIDE|NUMERICALDIRECTORY|STREETANDAVENUEGUIDE"
    )
    combined_hdr_re = re.compile(r"MONTCLAIRBLOOMFIELD(?:\(?\d{4}\)?)?DIR")

    for i, txt in enumerate(pages):
        head = re.sub(r"\s+", " ", txt[:2200].upper())
        # Fully strip spaces/punctuation for OCR-split running headers like "M O N TCLA IR (1914) D IR E C T O R Y"
        head_flat = re.sub(r"[^A-Z0-9()]", "", head)

        if combined_hdr_re.search(head_flat) or mc_non_alpha_re.search(head_flat):
            town_tag[i] = "OTHER"
        elif mc_dir_re.search(head_flat):
            town_tag[i] = "MC"
        elif other_town_dir_re.search(head_flat):
            town_tag[i] = "OTHER"

        my = re.search(
            r"(18\d\d|19\d\d)THEPR?[IE]CE|MONTCLAIR\((18\d\d|19\d\d)\)|DIRECTORY(18\d\d|19\d\d)",
            head_flat,
        )
        if my:
            yr_tag[i] = int(next(g for g in my.groups() if g))

        ac = len(res_re.findall(txt))
        sg = len(sg_re.findall(txt))
        alpha_counts[i] = ac
        if sg >= 3 and ac < 10:
            is_street_guide[i] = True
        elif ac >= 4 and sg <= max(4, ac * 0.45):
            is_alpha[i] = True

    # Identify hard barriers:
    # - another town's directory or classified/street-guide header (not flanked by MC on both sides within ±12 pages)
    # - genuine street-guide runs (>=5 consecutive non-alpha street-guide pages)
    # - genuine wrong-year runs (>=3 wrong-year pages in a ±4 window, ignoring single OCR digit glitches like 1914->1911)
    sg_run = [0] * n
    run = 0
    for i in range(n):
        if is_street_guide[i] or (not is_alpha[i] and run > 0 and i + 1 < n and is_street_guide[i + 1]):
            run += 1
        else:
            run = 0
        sg_run[i] = run
    in_sg_block = [False] * n
    i = n - 1
    while i >= 0:
        if sg_run[i] >= 5:
            for k in range(i - sg_run[i] + 1, i + 1):
                in_sg_block[k] = True
            i -= sg_run[i]
        else:
            i -= 1

    barrier = [False] * n
    for i in range(n):
        if town_tag[i] == "OTHER":
            left_mc = any(town_tag[k] == "MC" for k in range(max(0, i - 12), i))
            right_mc = any(town_tag[k] == "MC" for k in range(i + 1, min(n, i + 13)))
            if not (left_mc and right_mc):
                barrier[i] = True
        elif in_sg_block[i]:
            barrier[i] = True
        elif yr_tag[i] is not None and abs(yr_tag[i] - target_year) > 2:
            wrong_near = sum(
                1 for k in range(max(0, i - 4), min(n, i + 5))
                if yr_tag[k] is not None and abs(yr_tag[k] - target_year) > 2
            )
            if wrong_near >= 3:
                barrier[i] = True

    # Partition non-barrier pages into segments; allow short ad-insert gaps (up to 12 pages) inside an A-Z run
    best = None  # (score, start, end)
    i = 0
    while i < n:
        if barrier[i] or not is_alpha[i]:
            i += 1
            continue
        s = i
        e = i
        mc_hits = 1 if town_tag[i] == "MC" else 0
        alpha_pages = 1
        yr_votes = collections.Counter()
        if yr_tag[i] is not None:
            yr_votes[yr_tag[i]] += 1
        j = i + 1
        gap = 0
        while j < n and not barrier[j]:
            if is_alpha[j]:
                e = j
                alpha_pages += 1
                gap = 0
            else:
                gap += 1
                if gap > 12:
                    break
            if town_tag[j] == "MC":
                mc_hits += 1
            if yr_tag[j] is not None:
                yr_votes[yr_tag[j]] += 1
            j += 1
        # Must be explicitly Montclair-tagged (at least 3 MC headers) and substantial
        if mc_hits >= 3 and alpha_pages >= 20:
            maj_yr = yr_votes.most_common(1)[0][0] if yr_votes else target_year
            if abs(maj_yr - target_year) <= 2:
                cand = (alpha_pages, s, e)
                if best is None or cand[0] > best[0]:
                    best = cand
        i = j

    if not best:
        return 1, 0
    _, s, e = best
    while e > s and not is_alpha[e]:
        e -= 1
    while s < e and not is_alpha[s]:
        s += 1
    return s + 1, e + 1


def join_words(words):
    """Join word boxes on a single visual baseline, fusing intra-word OCR kerning splits while keeping real spaces."""
    if not words:
        return None
    words = sorted(words, key=lambda w: w[0])
    x0 = words[0][0]
    y0 = min(w[1] for w in words)
    x1 = max(w[2] for w in words)
    y1 = max(w[3] for w in words)
    out = words[0][4]
    prev_x0, prev_x1, prev_txt = words[0][0], words[0][2], words[0][4]
    for wx0, wy0, wx1, wy1, txt in words[1:]:
        if wx1 <= prev_x1 + 0.5 and txt == prev_txt:
            continue
        gap = wx0 - prev_x1
        fuse = False
        if (-6.0 <= gap <= 2.2 and wx0 > prev_x0 + 1.5) or (-1.5 <= gap <= 2.2):
            if prev_txt and prev_txt[-1].isalpha() and txt and (txt[0].islower() or txt[0] in "\xad-"):
                fuse = True
            elif prev_txt.isdigit() and txt.isdigit() and gap >= -1.5:
                fuse = True
            elif txt in (")", ",", "."):
                fuse = True
            elif prev_txt == "(":
                fuse = True
            elif -1.5 <= gap <= 1.6 and len(prev_txt) == 1 and len(txt) == 1 and (prev_txt + txt) in ABBR_PAIRS:
                fuse = True
            elif all(c in DITTO_CHARS for c in prev_txt) and all(c in DITTO_CHARS for c in txt):
                fuse = True
        elif -6.0 <= gap <= 2.7 and len(prev_txt) == 1 and prev_txt.isupper() and txt and txt[0].islower() and txt not in ("h", "r"):
            fuse = True

        out += txt if fuse else (" " + txt)
        prev_x0, prev_x1, prev_txt = wx0, max(prev_x1, wx1), txt

    out = re.sub(rf"^((?:[•■▪◦*.,'’‘`^]+\s*)?{DITTO_CORE})([A-Za-z(])", r"\1 \2", out)
    return [out.strip(), x0, y0, x1, y1]


def raw_pages(bbox_html):
    """Yield (pw, ph, raw_lines) filtering out rotated vertical margin-ad glyphs."""
    for pw_s, ph_s, body in PAGE_RE.findall(bbox_html):
        pw, ph = float(pw_s), float(ph_s)
        raw_lines = []
        for lx0, ly0, lx1, ly1, inner in LINE_RE.findall(body):
            ws = []
            for wx0, wy0, wx1, wy1, wtxt in WORD_RE.findall(inner):
                t = html.unescape(wtxt).strip()
                if not t:
                    continue
                fx0, fy0, fx1, fy1 = float(wx0), float(wy0), float(wx1), float(wy1)
                wh = fy1 - fy0
                # Skip huge display-ad headlines while keeping normal body text on tall scans (ph ~ 1080)
                if wh > max(32.0, ph * 0.038):
                    continue
                ws.append((fx0, fy0, fx1, fy1, t))
            if ws:
                ws.sort(key=lambda w: w[0])
                raw_lines.append(ws)
        yield pw, ph, raw_lines


def detect_columns(pw, ph, raw_lines, y_vol=1949):
    """Detect 1-column or 2-column left-edge x coordinates on a Montclair directory page."""
    header_y = 0.0
    for ws in raw_lines:
        y0 = min(w[1] for w in ws)
        if y0 < ph * 0.24:
            line_txt = " ".join(w[4].replace(" ", "") for w in ws)
            if re.search(r"D\s*I\s*R\s*E\s*C\s*T\s*O\s*R\s*Y|P\s*R\s*I\s*C\s*E\s*&\s*L\s*E\s*E", line_txt, re.I):
                header_y = max(header_y, max(w[3] for w in ws))

    x_votes = collections.Counter()
    for ws in raw_lines:
        y0 = min(w[1] for w in ws)
        if y0 <= header_y + 1 or y0 > ph * 0.94:
            continue
        for idx, (wx0, wy0, wx1, wy1, wt) in enumerate(ws[:4]):
            if idx > 0 and wx0 - ws[idx - 1][2] < 10:
                continue
            if DITTO_START.match(wt) or wt in ("“", "\"", "—", "-", "_"):
                x_votes[round(wx0 / 2) * 2] += 2
                break
            if re.match(r"^[A-Z][a-z]{1,}$", wt) and len(ws) - idx >= 2:
                x_votes[round(wx0 / 2) * 2] += 1
                break

    if not x_votes:
        return [], header_y

    cluster_gap = 18 if y_vol <= 1926 else 14
    clusters = []
    for x in sorted(x_votes):
        if clusters and x - clusters[-1][-1][0] <= cluster_gap:
            clusters[-1].append((x, x_votes[x]))
        else:
            clusters.append([(x, x_votes[x])])

    cols = []
    for cl in clusters:
        total = sum(v for _, v in cl)
        if total < 10:
            continue
        peak = max(v for _, v in cl)
        thresh = min(peak, max(2, peak * 0.22))
        left_edge = float(min(x for x, v in cl if v >= thresh))
        if left_edge > pw - 115:
            continue
        if cols and left_edge - cols[-1] < 115:
            continue
        cols.append(left_edge)

    return cols, header_y


def column_entries(pw, ph, raw_lines, y_vol):
    cols, header_y = detect_columns(pw, ph, raw_lines, y_vol)
    if not cols:
        return

    if len(cols) >= 2:
        col_w = min(cols[i + 1] - cols[i] for i in range(len(cols) - 1))
        max_col_w = col_w + 10
    else:
        # 1-column page (1910-1925): exclude right-side rotated ads by capping column width
        max_col_w = min(pw - cols[0] - 8, max(260.0, pw * 0.68))

    per_col_words = [[] for _ in cols]
    for ws in raw_lines:
        ly0 = min(w[1] for w in ws)
        if ly0 <= header_y + 1 or ly0 > ph * 0.95:
            continue
        for ci, edge in enumerate(cols):
            right_lim = (cols[ci + 1] - 8) if ci + 1 < len(cols) else min(pw, edge + max_col_w)
            cws = [w for w in ws if edge - 12 <= w[0] < right_lim and w[2] <= right_lim + 12]
            if cws:
                ymid = sum((w[1] + w[3]) * 0.5 for w in cws) / len(cws)
                per_col_words[ci].append((ymid, cws))

    if y_vol <= 1924:
        start_max, cont_max = 19.5, 56.0
    else:
        start_max, cont_max = 13.8, 54.0

    for ci, edge in enumerate(cols):
        groups = sorted(per_col_words[ci], key=lambda g: (g[0], g[1][0][0]))
        merged_lines = []
        for ymid, cws in groups:
            if merged_lines and abs(ymid - merged_lines[-1][0]) <= 2.6:
                _, prev_ws = merged_lines[-1]
                comb = prev_ws + cws
                new_ymid = sum((w[1] + w[3]) * 0.5 for w in comb) / len(comb)
                merged_lines[-1] = (new_ymid, comb)
            else:
                merged_lines.append((ymid, list(cws)))

        clines = []
        for _, cws in merged_lines:
            joined = join_words(cws)
            if not joined:
                continue
            t, x0, y0, x1, y1 = joined
            if PURE_NOISE.match(t) and not re.match(r"^\d+$", t):
                continue
            clines.append((t, x0, y0, x1, y1))

        if not clines:
            continue

        near_lim = edge + 14.0
        local_edges = []
        for i in range(len(clines)):
            near = [clines[j][1] for j in range(max(0, i - 12), min(len(clines), i + 13)) if clines[j][1] < near_lim]
            if len(near) >= 2:
                near_s = sorted(near)
                local_edges.append(near_s[max(0, len(near_s) // 6)])
            else:
                local_edges.append(edge)

        cur = None
        for (t, x0, y0, x1, y1), loc_edge in zip(clines, local_edges):
            d = x0 - loc_edge
            explicit_ditto = bool(DITTO_START.match(t)) and not re.match(r"^[—\-–]+\s*Continued\b", t, re.I)
            if explicit_ditto and -10 <= d <= 14:
                kind = "start"
            elif -10 <= d <= start_max:
                kind = "start"
            elif start_max < d <= cont_max:
                kind = "cont"
            else:
                continue

            prev_hyph = bool(cur and cur[0].endswith(("-", "\xad")) and not explicit_ditto and 0 <= (y0 - cur[4]) <= 10)
            prev_complete = bool(cur and not prev_hyph and COMPLETE_END.search(cur[0]))
            is_see_line = bool(re.match(r"^[—\-–]+\s*See\b", t, re.I))

            is_new = (
                cur is None
                or (kind == "start" and not prev_hyph and not is_see_line)
                or (prev_complete and not is_see_line)
                or y0 < cur[2] - 5
                or (y0 - cur[4]) > 18
            )
            if is_new:
                if cur:
                    yield ci, cur[6], cur[7], cur[0], cur[1], cur[2], cur[3], cur[4], cur[5]
                cur = [t, x0, y0, x1, y1, [x0, y0, x1, y1], loc_edge, d]
            else:
                if cur[0].endswith(("-", "\xad")):
                    stem = cur[0][:-1]
                    if stem and stem[-1].islower() and re.match(r"^Hn\b", t):
                        t = "lin" + t[2:]
                    cur[0] = stem + t
                else:
                    cur[0] = cur[0] + " " + t
                cur[1] = min(cur[1], x0)
                cur[2] = min(cur[2], y0)
                cur[3] = max(cur[3], x1)
                cur[4] = max(cur[4], y1)
        if cur:
            yield ci, cur[6], cur[7], cur[0], cur[1], cur[2], cur[3], cur[4], cur[5]


def format_surname(raw_tok):
    s = raw_tok.strip(" ,.;:'’‘\"“”`")
    s = re.sub(r"^O['’‘]([A-Za-z])", lambda m: "O’" + m.group(1).upper(), s)
    if re.match(r"^(?:Mac|Mc|De|Di|Du|La|Le|Vander|Van|Von|St|O’)[A-Z]", s):
        return s
    return s.title()


def extract_header_surname(t):
    t_nc = CONT_TAIL_RE.sub("", t).strip()
    s = re.sub(r"^[\s•■▪◦*.,'’‘“”`^\[\]]+", "", t_nc)
    if not s:
        return None, ""
    toks = s.split()
    if len(toks) >= 2 and all(w.isupper() and len(w) >= 2 for w in toks[:2]):
        m_caps = re.match(r"^([A-Z][A-Z'’\-]{2,})\s+([A-Z]{2,}(?:\s+[A-Z]\.?)*)(\s+(?:\([A-Za-z .'’]+\)\s+)?[a-z].*)$", s)
        if m_caps and m_caps.group(1).title() not in HEADING_WORDS:
            s = m_caps.group(1).title() + " " + " ".join(w.title() for w in m_caps.group(2).split()) + m_caps.group(3)
        else:
            return None, ""

    s = re.sub(r"^O\s*['’‘]\s*([A-Z][A-Za-z-]+)", lambda m: "O’" + m.group(1).replace("-", ""), s)
    s = re.sub(r"^(Mc|Mac)\s+([A-Z][a-z]{2,})", r"\1\2", s)
    m_pfx = re.match(r"^(Vander|Van|Von|De|Di|Du|La|Le|St)\.?[\s]+([A-Z][a-z]{1,})\b(.*)$", s)
    if m_pfx:
        rem = m_pfx.group(3).strip()
        if not rem or re.match(r"^(?:[A-Z]|\(|wid\b|rem\b|died\b|see\b)", rem):
            s = m_pfx.group(1) + m_pfx.group(2) + m_pfx.group(3)

    parts = s.split()
    if not parts or not re.match(r"^[A-Z][A-Za-z'’‘-]*,?$", parts[0]):
        return None, ""
    sur = parts[0].rstrip(",").replace("-", "")
    idx = 1
    while idx < len(parts) and not parts[0].endswith(","):
        nxt = parts[idx].rstrip(",")
        if re.match(r"^[a-z'’]{1,8}$", nxt) and nxt.lower() not in OCC_STOP:
            if len(sur) >= 4 and len(nxt) > 3:
                break
            sur += nxt
            idx += 1
            if parts[idx - 1].endswith(","):
                break
        else:
            break

    if len(sur) < 2 or sur.title() in HEADING_WORDS:
        return None, ""
    rest = " ".join(parts[idx:])
    return format_surname(sur), rest


def _rejoin_spaced_given(s):
    toks = s.split()
    if len(toks) < 2 or not re.match(r"^[A-Z][a-z]{0,4}$", toks[0]):
        return s
    stop = OCC_STOP - {"r", "h"}
    word = toks[0]
    i = 1
    while i < len(toks):
        t = toks[i]
        if not re.match(r"^[a-z]{1,10}$", t) or t in stop:
            break
        if len(word) >= 4 and len(t) > 2:
            break
        if len(word) == 1 and len(t) == 1:
            if not (i + 1 < len(toks) and re.match(r"^[a-z]{1,5}$", toks[i + 1]) and toks[i + 1] not in stop):
                break
        word += t
        i += 1
    return " ".join([word] + toks[i:])


def clean_person_fields(pre):
    spouse_m = re.search(r"\(([A-Za-z .'’‘]+)\)", pre)
    spouse = None
    if spouse_m:
        sp = re.sub(r"\s+", " ", spouse_m.group(1)).strip(" '’‘")
        sp = _rejoin_spaced_given(sp)
        sp = re.sub(r"\b([A-Z])\s+([a-z]{2,})", r"\1\2", sp)
        sp = re.sub(r"^([A-Z][a-z]+)\s+0$", r"\1 O", sp)
        spouse = sp or None
    pre_ns = re.sub(r"\([^)]*\)", " ", pre)
    pre_ns = re.sub(r"^[\s'’‘“”`\"^.,:;!*~_\-–—•■\[\]]+", "", pre_ns)
    pre_ns = _rejoin_spaced_given(pre_ns)
    pre_ns = re.sub(r"^([A-Z][a-z]+)\s+0(?=\s|$)", r"\1 O", pre_ns)
    g = re.match(r"^((?:[A-Z][a-z]+\.?|[A-Z]\.?)(?:\s(?:[A-Z][a-z]+\.?|[A-Z]\.?|Jr|Sr|Mrs|Miss|Rev|Dr))*)", pre_ns)
    given = g.group(1).strip() if g else ""
    occ = re.split(r"\s(?:r|h|bds|res)\s\d", pre_ns[len(given):])[0].strip(" ,;")
    return given, spouse, occ[:80]


def build_alphabetical_spine(items, y_vol):
    """Global monotonic alphabetical surname spine (weighted LNDS via Fenwick tree)."""
    cands = []
    for idx, it in enumerate(items):
        t, d = it["t"], it["d"]
        t_clean = re.sub(r"^[A-Z0-9]{1,2}\s+(?=[—\-–_~“\"”])", "", t)
        m_dit = DITTO_START.match(t_clean)
        if m_dit and not re.match(r"^[—\-–]+\s*Continued\b", t_clean, re.I):
            it["ditto"] = (True, m_dit.group(1))
            continue
        if y_vol <= 1924 and 2.5 <= d <= 14.0:
            m_eq = EARLY_QUOTE_DITTO.match(t_clean)
            if m_eq:
                it["ditto"] = (True, m_eq.group(1))
                continue
        it["ditto"] = (False, "")

        t_nocont = CONT_TAIL_RE.sub("", t).strip()
        is_guide = (it["idx_in_col"] <= 2 and len(t_nocont.split()) == 1 and d <= 6.5)
        sur, rest = extract_header_surname(t)
        if not sur:
            continue

        raw_first = re.sub(r"^[\s•■▪◦*.,'’‘“”`^\[\]]+", "", t_nocont).split()[0].rstrip(",")
        if re.match(r"^[A-Z]{2}[a-z]{2,}", raw_first) and not re.match(r"^(?:Mc|Mac|De|Di|Du|La|Le|Van|Von|St|Fitz)", raw_first):
            continue

        key = alpha_key(sur)
        if len(key) < 2:
            continue
        it["cand"] = (sur, rest, key, is_guide)

        max_sur_d = 5.5
        if d > max_sur_d:
            continue
        if is_guide:
            if idx + 1 < len(items):
                nxt_t = items[idx + 1]["t"]
                if DITTO_START.match(nxt_t) or items[idx + 1]["d"] >= 3.0:
                    cands.append((idx, key, sur, rest, 8, True))
            continue
        if not rest:
            continue
        if not (re.match(r"^[A-Z]", rest) or rest.startswith("see ")):
            continue
        if re.search(r"\b(?:Tel\.?|Phone|MOntclair|BLoomfield|ORange|Inc\.|Co\.,)\b", t):
            w = 1
        elif re.search(
            r"\b(?:h|r|bds|rms|res|bd)\.?\s+(?:\([0-9A-Za-z]+\)\s+)?\d+\s+[A-Z0-9]"
            r"|\bh\.?\s+do\b|\br\.?\s+do\b|\bbds\.?\s+do\b|\bdied\b|\brem\s+to\b|\bmarried\b|\bwid\b|^see\s+[A-Z]",
            rest,
        ):
            w = 10
        else:
            w = 3
        cands.append((idx, key, sur, rest, w, False))

    if not cands:
        return set(), {}

    uniq_keys = sorted(set(c[1] for c in cands))
    key_rank = {k: i + 1 for i, k in enumerate(uniq_keys)}
    n_rk = len(uniq_keys)
    bit_val = [0] * (n_rk + 1)
    bit_idx = [-1] * (n_rk + 1)
    parent = [-1] * len(cands)
    best_end = (0, -1)

    for ci_pos, (_, key, _, _, w, _) in enumerate(cands):
        rk = key_rank[key]
        bv, bi = 0, -1
        x = rk
        while x > 0:
            if bit_val[x] > bv:
                bv, bi = bit_val[x], bit_idx[x]
            x -= x & -x
        tot = bv + w
        parent[ci_pos] = bi
        if tot > best_end[0]:
            best_end = (tot, ci_pos)
        x = rk
        while x <= n_rk:
            if tot >= bit_val[x]:
                bit_val[x], bit_idx[x] = tot, ci_pos
            x += x & -x

    spine_pos = []
    cur_p = best_end[1]
    while cur_p != -1:
        spine_pos.append(cur_p)
        cur_p = parent[cur_p]
    spine_pos.reverse()

    while len(spine_pos) >= 4 and ord(cands[spine_pos[2]][1][0]) - ord(cands[spine_pos[0]][1][0]) > 2:
        spine_pos.pop(0)
    while len(spine_pos) >= 4 and ord(cands[spine_pos[-1]][1][0]) - ord(cands[spine_pos[-3]][1][0]) > 2:
        spine_pos.pop()

    accepted = {cands[p][0] for p in spine_pos}
    repaired = {}
    spine_items = [(cands[p][0], cands[p][1], cands[p][2]) for p in spine_pos]
    spine_indices = [s[0] for s in spine_items]

    for idx, it in enumerate(items):
        if idx in accepted or "cand" not in it:
            continue
        sur, rest, key, is_guide = it["cand"]
        if it["d"] > 5.5:
            continue
        pos = bisect.bisect_left(spine_indices, idx)
        prev_k = spine_items[pos - 1][1] if pos > 0 else None
        next_k = spine_items[pos][1] if pos < len(spine_items) else None
        if not (prev_k and next_k):
            continue
        has_full_given = bool(re.match(r"^[A-Z][a-z]{2,}\b", rest)) and rest.split()[0] not in ("Mrs", "Miss", "Inc", "Corp")
        nxt_explicit_ditto = idx + 1 < len(items) and bool(DITTO_START.match(items[idx + 1]["t"]))
        if not (has_full_given or nxt_explicit_ditto or is_guide):
            continue
        if prev_k <= key <= next_k:
            accepted.add(idx)
            continue
        if prev_k[0] == next_k[0]:
            target_c = prev_k[0]
            if key[0] in OCR_FIRST.get(target_c, set()):
                alt_key = target_c + key[1:]
                if prev_k <= alt_key <= next_k:
                    accepted.add(idx)
                    repaired[idx] = target_c.upper() + sur[1:]
                    continue
        if key[0] == prev_k[0] == next_k[0]:
            for old_s, new_s in (("l", "i"), ("i", "l"), ("m", "rn"), ("rn", "m"), ("u", "n"), ("n", "u"), ("e", "c"), ("c", "e"), ("a", "o"), ("o", "a"), ("v", "y"), ("y", "v"), ("o", "e"), ("e", "o")):
                if old_s in key[1:]:
                    alt_key = key[0] + key[1:].replace(old_s, new_s, 1)
                    if prev_k <= alt_key <= next_k:
                        accepted.add(idx)
                        if old_s == "l" and new_s == "i" and re.match(r"^[BCDFGHJKLMNPQRSTVWXYZ]l[bcdfghjklmnpqrstvwxyz]", sur):
                            repaired[idx] = sur[0] + "i" + sur[2:]
                        elif old_s == "e" and new_s == "c" and "ek" in sur and (prev_k.startswith(alt_key[:4]) or next_k.startswith(alt_key[:4])):
                            repaired[idx] = sur.replace("ek", "ck", 1)
                        break
        if len(key) >= 4 and (key[:3] == prev_k[:3] or key[:3] == next_k[:3]) and (prev_k[:3] <= key[:3] <= next_k[:3]):
            accepted.add(idx)

    return accepted, repaired


def parse_pdf_file(y, pdf, path_url, do_crop=False):
    start_p, end_p = find_montclair_alpha_range(pdf, y)
    if end_p < start_p:
        print(f"  {y}: could not locate Montclair Alphabetical Directory section in {pdf}", file=sys.stderr)
        return []
    print(f"  {y}: Montclair Alphabetical Directory detected on pp. {start_p}-{end_p}", file=sys.stderr, flush=True)

    bb = subprocess.run(
        ["pdftotext", "-bbox-layout", "-f", str(start_p), "-l", str(end_p), pdf, "-"],
        capture_output=True, text=True, errors="ignore",
    ).stdout

    items = []
    page_dims = {}
    for offset, (pw, ph, rlines) in enumerate(raw_pages(bb)):
        pno = start_p + offset
        page_dims[pno] = (pw, ph)
        col_ents = list(column_entries(pw, ph, rlines, y))
        by_col = collections.defaultdict(list)
        for ce in col_ents:
            by_col[ce[0]].append(ce)
        for ci in sorted(by_col):
            ents = by_col[ci]
            for idx_c, (_, loc_edge, d, t, x0, y0, x1, y1, fb) in enumerate(ents):
                t_norm = re.sub(r"\s+", " ", t).strip()
                if t_norm:
                    items.append({
                        "pno": pno, "ci": ci, "idx_in_col": idx_c,
                        "loc_edge": loc_edge, "d": d, "t": t_norm,
                        "x0": x0, "y0": y0, "x1": x1, "y1": y1, "fb": fb,
                    })

    accepted, repaired = build_alphabetical_spine(items, y)

    out = []
    surname = None
    surname_hdr = None

    for idx, it in enumerate(items):
        t = it["t"]
        pno = it["pno"]
        pw, ph = page_dims[pno]

        if idx in accepted:
            sur, rest, _, is_guide = it["cand"]
            surname = repaired.get(idx, sur)
            surname_hdr = (pno, it["ci"], it["fb"])
            if is_guide or not rest:
                continue
            is_direct = True
        else:
            if not surname:
                continue
            is_direct = False
            if it["ditto"][0]:
                rest = it["ditto"][1]
            else:
                rest = re.sub(r"^[\s•■▪◦*.,'’‘“”`^—\-–_~]+", "", t)
                if not re.match(r"^(?:Mc|Mac|Van|Von|De|Di|Du|La|Le|St|Fitz)[A-Z]", rest):
                    rest = re.sub(r"^[A-Z](?=[A-Z][a-z]{2,}\b)", "", rest)

        t_addr = SEE_TAIL_RE.sub("", t).strip()
        if OTHER_TOWN_END.search(t_addr):
            continue

        a_std = ADDR_STD.search(t_addr)
        a_do = None if a_std else ADDR_DO.search(t_addr)
        if a_std:
            ten_code, num, raw_st = a_std.group(1), a_std.group(2), a_std.group(3)
            addr_start = a_std.start()
        elif a_do:
            num, raw_st, ten_code = a_do.group(1), a_do.group(2), a_do.group(3)
            addr_start = a_do.start()
        else:
            continue

        if re.search(r"\b(?:Church|School|Club|Hospital|Bank|Company|Corp)\b", rest[:40]):
            continue

        street = canon_street(raw_st, STREETS)
        if not street:
            continue

        rest_addr = SEE_TAIL_RE.sub("", rest).strip()
        pre = rest_addr[: max(0, len(rest_addr) - (len(t_addr) - addr_start))]
        if a_do:
            pre = re.sub(r"\band\s*$", "", pre).strip()
        given, spouse, occ = clean_person_fields(pre)

        hdr_box = None
        hdr_page = None
        if not is_direct and surname_hdr and 0 <= (pno - surname_hdr[0]) <= 2:
            hdr_box = [round(v) for v in surname_hdr[2]]
            hdr_page = surname_hdr[0]

        row = {
            "year": y,
            "surname": surname,
            "given": given,
            "spouse": spouse,
            "occ": occ,
            "tenure": TEN.get(ten_code, ten_code),
            "number": num,
            "raw_street": raw_st,
            "street": street,
            "town": "Montclair",
            "direct": is_direct,
            "src": path_url,
            "page": pno,
            "bbox": [round(it["x0"]), round(it["y0"]), round(it["x1"]), round(it["y1"])],
            "pw": pw,
            "ph": ph,
            "text": t[:200],
        }
        if hdr_box:
            row["hdr_bbox"] = hdr_box
            row["hdr_page"] = hdr_page
        out.append(row)

    if do_crop:
        crop(pdf, y, out)
    return out


def crop(pdf, y, rows):
    import glob
    from concurrent.futures import ThreadPoolExecutor
    from PIL import Image, ImageDraw, ImageFile, ImageStat
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    by_page = collections.defaultdict(list)
    for r in rows:
        if r["tenure"] != "householder" or not r["street"]:
            continue
        by_page[r["page"]].append(r)

    if not by_page:
        return

    dpi = 140
    k = dpi / 72.0
    out_dir = os.path.join(OUT, "docs", "directory", str(y))
    os.makedirs(out_dir, exist_ok=True)
    pages_sorted = sorted(by_page.keys())
    chunk_size = 24
    chunks = [pages_sorted[i : i + chunk_size] for i in range(0, len(pages_sorted), chunk_size)]

    def do_chunk(ci, chunk_pages):
        lo = min(chunk_pages)
        hi = max(chunk_pages)
        # Include any hdr_page referenced by rows in this chunk (at most 2 pages earlier)
        needed_lo = lo
        for p in chunk_pages:
            for r in by_page[p]:
                hp = r.get("hdr_page", p)
                if hp < needed_lo:
                    needed_lo = hp
        prefix = os.path.join(TMP, f"ch_{y}_{os.getpid()}_{ci}")
        rendered = {}
        try:
            subprocess.run(
                ["pdftoppm", "-r", str(dpi), "-gray", "-jpeg", "-f", str(needed_lo), "-l", str(hi), pdf, prefix],
                check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            for fn in glob.glob(prefix + "-*.jpg"):
                m = re.search(r"-(\d+)\.jpg$", fn)
                if m:
                    rendered[int(m.group(1))] = fn
            im_cache = {}

            def get_im(pno):
                if pno not in im_cache:
                    fn = rendered.get(pno)
                    if not fn:
                        single = f"{prefix}_s{pno}"
                        subprocess.run(
                            ["pdftoppm", "-r", str(dpi), "-gray", "-jpeg", "-singlefile", "-f", str(pno), "-l", str(pno), pdf, single],
                            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                        )
                        fn = single + ".jpg"
                        rendered[pno] = fn
                    im_obj = Image.open(fn)
                    im_obj.load()
                    im_cache[pno] = im_obj
                return im_cache[pno]

            for p in chunk_pages:
                im = get_im(p)
                for r in by_page[p]:
                    x0, y0, x1, y1 = r["bbox"]
                    hdr = r.get("hdr_bbox")
                    hdr_p = r.get("hdr_page", p)
                    if hdr:
                        hx0, hy0, hx1, hy1 = hdr
                        same_col_adj = (hdr_p == p) and (abs(hx0 - x0) <= 25) and (0 <= (y0 - hy1) <= 22) and (hy0 < y0)
                        if same_col_adj:
                            box = (
                                max(0, int((min(hx0, x0) - 6) * k)),
                                max(0, int((hy0 - 4) * k)),
                                min(im.width, int((max(hx1, x1) + 6) * k)),
                                min(im.height, int((y1 + 4) * k)),
                            )
                            cropped = im.crop(box)
                        else:
                            hdr_im = get_im(hdr_p)
                            hbox = (
                                max(0, int((hx0 - 6) * k)),
                                max(0, int((hy0 - 3) * k)),
                                min(hdr_im.width, int((hx1 + 6) * k)),
                                min(hdr_im.height, int((min(hy1, hy0 + 10) + 1) * k)),
                            )
                            rbox = (
                                max(0, int((x0 - 6) * k)),
                                max(0, int((y0 - 1) * k)),
                                min(im.width, int((x1 + 6) * k)),
                                min(im.height, int((y1 + 4) * k)),
                            )
                            top_im = hdr_im.crop(hbox)
                            bot_im = im.crop(rbox)
                            w_out = max(top_im.width, bot_im.width)
                            sep_h = 6
                            bg = int(ImageStat.Stat(bot_im).median[0])
                            cropped = Image.new("L", (w_out, top_im.height + sep_h + bot_im.height), color=bg)
                            cropped.paste(top_im, (0, 0))
                            cropped.paste(bot_im, (0, top_im.height + sep_h))
                            draw = ImageDraw.Draw(cropped)
                            mid_y = top_im.height + sep_h // 2
                            line_col = max(60, bg - 75)
                            for dx in range(4, w_out - 4, 8):
                                draw.line([(dx, mid_y), (min(dx + 4, w_out - 4), mid_y)], fill=line_col, width=1)
                    else:
                        box = (
                            max(0, int((x0 - 6) * k)),
                            max(0, int((y0 - 4) * k)),
                            min(im.width, int((x1 + 6) * k)),
                            min(im.height, int((y1 + 4) * k)),
                        )
                        cropped = im.crop(box)

                    rel = os.path.join("docs", "directory", str(y), f"{slug(r['street'])}-{slug(r['number'])}-p{p}-{x0}-{y0}.jpg")
                    dst = os.path.join(OUT, rel)
                    cropped.save(dst, quality=68)
                    r["crop"] = rel
            for im_obj in im_cache.values():
                im_obj.close()
        finally:
            for fn in rendered.values():
                if os.path.exists(fn):
                    os.remove(fn)

    with ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(lambda args: do_chunk(*args), enumerate(chunks)))


def process_year(y, do_crop=False):
    path_url = pdf_url_for(y)
    # Reuse sample PDF if already downloaded; otherwise download to TMP with curl -C - retry loop
    sample_pdf = os.path.join(TMP, "dir_sample", f"{y}.pdf")
    if os.path.exists(sample_pdf) and os.path.getsize(sample_pdf) > 5_000_000:
        pdf = sample_pdf
        cleanup = False
    else:
        pdf = os.path.join(TMP, f"dir_{y}.pdf")
        cleanup = True
        full_url = BASE + urllib.parse.quote(path_url, safe="/")
        for attempt in range(4):
            r = subprocess.run(
                ["curl", "-sSL", "-C", "-", "-A", TOWN["user_agent"], "--max-time", "240", "-o", pdf, full_url],
                capture_output=True,
            )
            if r.returncode == 0 and os.path.exists(pdf) and os.path.getsize(pdf) > 5_000_000:
                break
        if not os.path.exists(pdf) or os.path.getsize(pdf) < 5_000_000:
            raise RuntimeError(f"Failed to download {full_url}")

    try:
        return parse_pdf_file(y, pdf, path_url, do_crop=do_crop)
    finally:
        if cleanup and os.path.exists(pdf):
            os.remove(pdf)


if __name__ == "__main__":
    force = "--force" in sys.argv
    no_crop = "--no-crop" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    years = [int(y) for y in args[0].split(",")] if args else TOWN["directories"]["years"]
    for y in years:
        if y > CUTOFF:
            print(f"{y}: skipping (after cutoff {CUTOFF})", file=sys.stderr)
            continue
        dst = os.path.join(OUT, "data", f"dir_{y}.json")
        if os.path.exists(dst) and not force:
            print(f"{y}: already done", file=sys.stderr)
            continue
        do_crop = (y in CROP_YEARS) and not no_crop
        if do_crop:
            yr_crop_dir = os.path.join(OUT, "docs", "directory", str(y))
            if os.path.isdir(yr_crop_dir):
                for fn in os.listdir(yr_crop_dir):
                    if fn.endswith(".jpg"):
                        os.remove(os.path.join(yr_crop_dir, fn))
        try:
            rows = process_year(y, do_crop=do_crop)
        except Exception as e:
            print(f"{y}: ERROR {e}", file=sys.stderr, flush=True)
            continue
        tmp_dst = dst + ".tmp"
        json.dump(rows, open(tmp_dst, "w"))
        os.replace(tmp_dst, dst)
        print(
            f"{y}: {len(rows)} Montclair entries, {len(set(r['street'] for r in rows))} streets, {sum(1 for r in rows if r.get('crop'))} crops",
            file=sys.stderr, flush=True,
        )
