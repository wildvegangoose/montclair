"""Automated ground-truth and structural accuracy regression suite for Montclair Through Time.

Run with:
    python3 -m unittest discover -s tests -v
or:
    python3 tests/test_accuracy.py
"""
import json
import pathlib
import re
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "archive"
STREETS_DIR = ARCHIVE / "data" / "streets"
sys.path.insert(0, str(ROOT / "tools" / "archive"))
import common  # noqa: E402


def _load_street(slug_name):
    p = STREETS_DIR / f"{slug_name}.json"
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def _eval_js_data():
    script = f"""
    global.window = global;
    global.MW = {{}};
    MW.esc = s => String(s).replace(/[&<>"']/g, c => ({{ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }}[c]));
    require({json.dumps(str(ROOT / "js/data.js"))});
    require({json.dumps(str(ROOT / "js/landmarks-data.js"))});
    require({json.dumps(str(ROOT / "js/people-data.js"))});
    require({json.dumps(str(ROOT / "js/webstories.js"))});
    require({json.dumps(str(ROOT / "js/housephotos.js"))});
    require({json.dumps(str(ROOT / "js/sanborn-data.js"))});
    require({json.dumps(str(ROOT / "js/sanborn.js"))});
    console.log(JSON.stringify({{
      eras: MW.eras,
      seats: MW.seats,
      places: MW.places,
      landmarks: MW.landmarks,
      people: MW.people,
      stories: MW.webStories,
      housePhotos: MW.housePhotos,
      storyNorthMtn: MW.storiesFor("30", "N Mountain Ave").length,
      storySouthMtn30: MW.storiesFor("30", "South Mountain Avenue").length,
      storySouthMtn66: MW.storiesFor("66", "S Mountain Av").length,
      storyGlenridge: MW.storiesFor("159", "Glen Ridge Ave").length,
      storyClaremont: MW.storiesFor("369", "Clairmont Ave").length,
      photoRappaport: MW.housePhotosFor("7", "Greenview Way").length,
      photoForstmann: MW.housePhotosFor("196", "Up Mountain Ave").length,
      sanbornGlenridge: MW.sanbornFor("159", "Glen Ridge Ave"),
      sanbornBloomfield: MW.sanbornFor("647", "Bloomfield Ave"),
      sanbornBloomfieldHtml: MW.sanbornHTML("647", "Bloomfield Ave"),
      sanbornBellevue: MW.sanbornFor("275", "Belleview Ave"),
      sanbornNorthMtn: MW.sanbornFor("30", "N Mountain Ave")
    }}));
    """
    out = subprocess.check_output(["node", "-e", script], text=True)
    return json.loads(out)


# 60 hand-verified ground-truth Montclair directory cases across 1910–1949 covering:
# - all 4 milestone crop years (1910, 1925, 1935, 1949) and 12 additional directory editions
# - notable Montclair households, landmarks, directional streets (N/S/Upper Mountain, N/S Fullerton),
#   compound Dutch surnames (VanVleck), and Italian-American Pine Street residents
GROUND_TRUTH_CASES = [
    # (street_slug, number, year, expected_surname, expected_given_prefix, expected_spouse, require_crop)
    ("north-mountain-avenue", "30", 1910, "Shultz", "Charles S", None, True),
    ("north-mountain-avenue", "30", 1914, "Shultz", "Charles S", None, False),
    ("eagle-rock-way", "68", 1923, "Gilbreth", "Frank B", None, False),
    ("eagle-rock-way", "68", 1931, "Gilbreth", "Lillian M", None, False),
    ("eagle-rock-way", "68", 1935, "Gilbreth", "Lillian M", None, True),
    ("eagle-rock-way", "68", 1941, "Gilbreth", "Lillian M", None, False),
    ("eagle-rock-way", "68", 1935, "Grieves", "Thomas", None, False),
    ("the-crescent", "30", 1945, "Gilbreth", "Lillian M", None, False),
    ("the-crescent", "30", 1949, "Gilbreth", "Lillian M", None, True),
    ("orange-road", "247", 1945, "Harris", "Herbert E", "Jessie F", False),
    ("orange-road", "247", 1949, "Harris", "Herbert E", "Jessie F", True),
    ("south-mountain-avenue", "66", 1910, "Gates", "Frederick T", None, True),
    ("south-mountain-avenue", "66", 1914, "Gates", "Frederick T", None, False),
    ("south-mountain-avenue", "66", 1925, "Gates", "Frederick T", None, True),
    ("north-mountain-avenue", "37", 1931, "Weston", "Edward", None, False),
    ("north-mountain-avenue", "37", 1935, "Weston", "Edward", None, True),
    ("upper-mountain-avenue", "105", 1910, "Couper", "William", None, True),
    ("upper-mountain-avenue", "105", 1925, "Couper", "William", None, True),
    ("berkeley-place", "14", 1935, "Couper", "William", "Eliza C", True),
    ("hawthorne-place", "36", 1925, "Lang", "Henry", None, True),
    ("hawthorne-place", "36", 1935, "Lang", "Florence R", None, True),
    ("walnut-crescent", "21", 1912, "Evans", "William T", None, False),
    ("upper-mountain-avenue", "95", 1910, "Presby", "Frank H", None, True),
    ("upper-mountain-avenue", "95", 1920, "Presby", "Frank H", None, False),
    ("upper-mountain-avenue", "474", 1925, "Walther", "Frederick P", None, True),
    ("upper-mountain-avenue", "474", 1949, "Walther", "Frederick P", "Barbara F", True),
    ("russell-terrace", "1", 1920, "Lewis", "Isaac N", None, False),
    ("russell-terrace", "1", 1925, "Lewis", "Isaac N", None, True),
    ("north-mountain-avenue", "338", 1925, "Cushman", "J Clydesdale", None, True),
    ("north-mountain-avenue", "338", 1935, "Cushman", "J Clydesdale", "Helen G", True),
    ("north-mountain-avenue", "338", 1949, "Cushman", "J Clydesdale", "Helen G", True),
    ("llewellyn-road", "32", 1910, "Adams", "W I Lincoln", None, True),
    ("llewellyn-road", "32", 1925, "Adams", "W I Lincoln", None, True),
    ("melrose-place", "54", 1935, "Adams", "W I Lincoln", "Grace M", True),
    ("warfield-street", "29", 1925, "Faulkner", "Bayard H", None, True),
    ("warfield-street", "36", 1939, "Faulkner", "Bayard H", "Eleanor R", False),
    ("bloomfield-avenue", "415", 1920, "Foster", "Alice Hooe", None, False),
    ("bloomfield-avenue", "415", 1923, "Foster", "Alice Hooe", None, False),
    ("claremont-avenue", "276", 1910, "Spaulding", "Randall", None, True),
    ("claremont-avenue", "276", 1914, "Spaulding", "Randall", None, False),
    ("watchung-avenue", "92", 1937, "Jones", "Robert T", None, False),
    ("montclair-avenue", "114", 1949, "Jones", "Robert T", None, True),
    ("upper-mountain-avenue", "246", 1910, "Townsend", "Edward W", None, True),
    ("union-street", "93", 1910, "Batten", "George", None, True),
    ("north-mountain-avenue", "320", 1935, "Viskniskki", "Guy T", "Virginia", True),
    ("trinity-place", "18", 1935, "Bradford", "Stella S", None, True),
    ("north-mountain-avenue", "26", 1949, "Bradford", "Stella S", None, True),
    ("llewellyn-road", "75", 1935, "Barus", "Maxwell", "Jane G", True),
    ("irving-street", "33", 1945, "Richardson", "Edward L", "Pearl G", False),
    ("irving-street", "34", 1935, "Kenney", "John A", "Frieda A", True),
    ("madison-avenue", "39", 1945, "Kenney", "John A Jr", "Fern", False),
    ("highland-terrace", "3", 1925, "Hovey", "George R", None, True),
    ("yale-terrace", "7", 1935, "Lochhead", "Archie", "Suzanne A", True),
    ("upper-mountain-avenue", "59", 1910, "VanVleck", "Joseph", None, True),
    ("van-vleck-street", "21", 1935, "VanVleck", "Joseph Jr", "Mary", True),
    ("watchung-avenue", "149", 1949, "Arny", "Robert A", "Mary W T", True),
    ("watchung-avenue", "120", 1910, "Hupfeld", "Frederica", None, False),
    ("greenview-way", "7", 1935, "Rappaport", "Percy", "Jean", True),
    ("upper-mountain-avenue", "196", 1949, "Forstmann", "Curt E", "Elizabeth A", True),
    ("glenridge-avenue", "159", 1910, "Allien", "Henry", None, True),
    ("pine-street", "70", 1910, "DeNapoli", "Francesco", None, True),
]


class MontclairAccuracyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.street_cache = {}
        cls.js = _eval_js_data()
        cls.conf_streets = json.loads((ARCHIVE / "data" / "streets.json").read_text(encoding="utf-8"))
        cls.street_index = json.loads((ARCHIVE / "data" / "street_index.json").read_text(encoding="utf-8"))

    def _house_listings(self, st_slug, num):
        if st_slug not in self.street_cache:
            self.street_cache[st_slug] = _load_street(st_slug)
        return self.street_cache[st_slug]["houses"].get(str(num), {}).get("listings", [])

    def test_ground_truth_directory_cases(self):
        self.assertGreaterEqual(len(GROUND_TRUTH_CASES), 55)
        for st_slug, num, yr, exp_sur, exp_giv, exp_sp, req_crop in GROUND_TRUTH_CASES:
            with self.subTest(address=f"{num} {st_slug}", year=yr, person=f"{exp_sur}, {exp_giv}"):
                yr_rows = [r for r in self._house_listings(st_slug, num) if r["year"] == yr]
                self.assertTrue(yr_rows, f"No {yr} listings found at {num} {st_slug}")
                matches = [
                    r for r in yr_rows
                    if r["surname"] == exp_sur and (r.get("given") or "").startswith(exp_giv)
                ]
                self.assertTrue(
                    matches,
                    f"Expected ({exp_sur}, {exp_giv}*) at {num} {st_slug} in {yr}, got: {[(r['surname'], r.get('given'), r.get('spouse')) for r in yr_rows]}",
                )
                hit = matches[0]
                if exp_sp is not None:
                    self.assertEqual(hit.get("spouse"), exp_sp)
                if req_crop:
                    self.assertTrue(hit.get("crop"), f"Missing crop path on householder {exp_sur} at {num} {st_slug} ({yr})")
                    crop_file = ARCHIVE / hit["crop"]
                    self.assertTrue(crop_file.is_file(), f"Crop JPEG missing on disk: {crop_file}")
                    self.assertGreater(crop_file.stat().st_size, 500)

    def test_zero_crop_collisions_and_zero_missing_jpegs(self):
        crop_owners = {}
        missing = []
        collisions = []
        total_listings = 0
        for p in sorted(STREETS_DIR.glob("*.json")):
            data = json.loads(p.read_text(encoding="utf-8"))
            st = data["name"]
            for num, rec in data["houses"].items():
                for r in rec.get("listings", []):
                    total_listings += 1
                    self.assertLessEqual(r["year"], 1950, f"Post-1950 directory listing leaked at {num} {st}")
                    c = r.get("crop")
                    if c:
                        if not (ARCHIVE / c).is_file():
                            missing.append((st, num, r["year"], c))
                        owner = (st, num, r["year"])
                        if c in crop_owners and crop_owners[c] != owner:
                            collisions.append((c, crop_owners[c], owner))
                        crop_owners[c] = owner
        self.assertGreater(total_listings, 190000)
        self.assertGreater(len(crop_owners), 25000)
        self.assertEqual(missing, [], f"Missing crop JPEGs: {missing[:5]}")
        self.assertEqual(collisions, [], f"Colliding crop JPEGs: {collisions[:5]}")

    def test_zero_split_names_and_digit_middle_initials(self):
        split_sp, split_gv, mid_digit, edge_quote = [], [], [], []
        for p in sorted(STREETS_DIR.glob("*.json")):
            data = json.loads(p.read_text(encoding="utf-8"))
            st = data["name"]
            for num, rec in data["houses"].items():
                for r in rec.get("listings", []):
                    sur = r.get("surname") or ""
                    gv = r.get("given") or ""
                    sp = r.get("spouse") or ""
                    if sur != sur.strip(" ,.;:'’‘\"“”`"):
                        edge_quote.append((st, num, r["year"], sur))
                    if re.search(r"(?:^|\s)[A-Z]\s+[a-z]{2,}", sp):
                        split_sp.append((st, num, r["year"], sp))
                    if re.search(r"(?:^|\s)[A-Z]\s+[a-z]{2,}", gv):
                        split_gv.append((st, num, r["year"], gv))
                    if re.search(r"(?:^|\s)[01](?:\s|$)", gv) or re.search(r"(?:^|\s)[01](?:\s|$)", sp):
                        mid_digit.append((st, num, r["year"], gv, sp))
        self.assertEqual(edge_quote, [])
        self.assertEqual(split_sp, [])
        self.assertEqual(split_gv, [])
        self.assertEqual(mid_digit, [])

    def test_montclair_street_canonicalization(self):
        self.assertEqual(common.canon_street("Glen Ridge av", self.conf_streets), "GLENRIDGE AVENUE")
        self.assertEqual(common.canon_street("Clairmont av", self.conf_streets), "CLAREMONT AVENUE")
        self.assertEqual(common.canon_street("Belleview av", self.conf_streets), "BELLEVUE AVENUE")
        self.assertEqual(common.canon_street("N Mountain av", self.conf_streets), "NORTH MOUNTAIN AVENUE")
        self.assertEqual(common.canon_street("S Mountain av", self.conf_streets), "SOUTH MOUNTAIN AVENUE")
        self.assertEqual(common.canon_street("Up Mountain av", self.conf_streets), "UPPER MOUNTAIN AVENUE")
        self.assertEqual(common.canon_street("N Fullerton av", self.conf_streets), "NORTH FULLERTON AVENUE")
        self.assertEqual(common.canon_street("S Fullerton av", self.conf_streets), "SOUTH FULLERTON AVENUE")
        self.assertEqual(common.canon_street("St Lukes pl", self.conf_streets), "ST LUKES PLACE")
        self.assertEqual(common.canon_street("Bloomfield av", self.conf_streets), "BLOOMFIELD AVENUE")

    def test_sanborn_1885_and_1907_matching(self):
        # Verify 1885 (g3814mm) and 1907 (g3814em) Sanborn matching & IIIF URLs
        sb_bloom = self.js["sanbornBloomfield"]
        self.assertTrue(any(h["year"] == "1885" and h["sheets"] for h in sb_bloom), f"Expected 1885 Sanborn on Bloomfield Ave: {sb_bloom}")
        self.assertTrue(any(h["year"] == "1907" and h["exact"] and h["sheets"] == [37] for h in sb_bloom), f"Expected 1907 Sanborn sheet 37 on 647 Bloomfield Ave: {sb_bloom}")
        sb_html = self.js["sanbornBloomfieldHtml"]
        self.assertIn("g3814mm", sb_html, "Missing 1885 Sanborn IIIF prefix g3814mm")
        self.assertIn("g3814em", sb_html, "Missing 1907 Sanborn IIIF prefix g3814em")

        sb_glen = self.js["sanbornGlenridge"]
        self.assertTrue(any(h["year"] == "1907" and h["sheets"] for h in sb_glen), f"Expected 1907 Sanborn on Glenridge Ave: {sb_glen}")

        sb_bell = self.js["sanbornBellevue"]
        self.assertTrue(any(h["year"] == "1907" and h["sheets"] for h in sb_bell), f"Expected 1907 Sanborn on Bellevue Ave: {sb_bell}")

        sb_nmtn = self.js["sanbornNorthMtn"]
        self.assertTrue(any(h["year"] == "1907" and h["sheets"] for h in sb_nmtn), f"Expected 1907 Sanborn on N Mountain Ave: {sb_nmtn}")

    def test_curated_historical_facts_assets_and_privacy_rules(self):
        seats = {s["id"]: s for s in self.js.get("seats", [])}
        self.assertEqual(seats["seat-newark"]["to"], 1811)
        self.assertEqual(seats["seat-bloomfield"]["from"], 1812)
        self.assertEqual(seats["seat-bloomfield"]["to"], 1867)
        self.assertEqual(seats["seat-early-mc"]["from"], 1868)
        self.assertEqual(seats["seat-647"]["from"], 1904)
        self.assertEqual(seats["seat-205"]["from"], 1969)

        # Strict privacy: living or undated people NEVER have home addresses attached
        for person in self.js["people"]:
            if person.get("living") or not person.get("died"):
                self.assertFalse(person.get("homes"), f"Living or undated person has home address attached: {person['name']}")
            url = person.get("url") or ""
            self.assertEqual(url.count("("), url.count(")"), f"Truncated URL on {person['name']}: {url}")

        # Verify all 16 landmarks, their hero photos, and all 16 x 11 = 176 Through-the-Ages crops exist
        landmarks = self.js["landmarks"]
        self.assertEqual(len(landmarks), 16)
        ages_files = [
            "1888-map.jpg", "1898-map.jpg", "1906-map.jpg", "1924-map.jpg",
            "1930-aerial.jpg", "1947-map.jpg", "1955-map.jpg", "1972-map.jpg",
            "1995-aerial.jpg", "2007-aerial.jpg", "2020-aerial.jpg",
        ]
        for lm_id, lm in landmarks.items():
            photos = lm.get("photos") or []
            self.assertTrue(photos, f"Landmark {lm_id} missing photos")
            for ph in photos:
                fpath = ROOT / ph["src"]
                self.assertTrue(fpath.is_file() and fpath.stat().st_size > 5000, f"Missing landmark photo: {fpath}")
            for af in ages_files:
                ap = ROOT / "img" / "ages" / lm_id / af
                self.assertTrue(ap.is_file() and ap.stat().st_size > 1000, f"Missing ages crop: {ap}")

        # Verify all 7 USGS historic topo WebP overlays exist
        for yr in (1888, 1898, 1906, 1924, 1947, 1955, 1972):
            tp = ROOT / "img" / "maps" / f"topo{yr}.webp"
            self.assertTrue(tp.is_file() and tp.stat().st_size > 10000, f"Missing topo overlay: {tp}")

        # Verify all house photos exist on disk
        for hp in self.js["housePhotos"]:
            fp = ROOT / hp["src"]
            self.assertTrue(fp.is_file() and fp.stat().st_size > 5000, f"Missing house photo: {fp}")

        # Verify directional story & photo normalization
        self.assertEqual(self.js["storyNorthMtn"], 1)
        self.assertEqual(self.js["storySouthMtn30"], 0)
        self.assertEqual(self.js["storySouthMtn66"], 1)
        self.assertEqual(self.js["storyGlenridge"], 1)
        self.assertEqual(self.js["storyClaremont"], 1)
        self.assertEqual(self.js["photoRappaport"], 3)
        self.assertEqual(self.js["photoForstmann"], 2)

    def test_seo_metadata_sitemap_cloudflare_and_static_landmarks(self):
        import html as html_lib
        import xml.etree.ElementTree as ET

        cfg = json.loads((ROOT / "tools" / "town.json").read_text(encoding="utf-8"))
        site_url = cfg["site_url"].rstrip("/") + "/"
        cf_token = cfg["cloudflare_beacon_token"]
        self.assertEqual(cf_token, "03a9b2df20a44828802f80f6401c4ec3")

        robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("User-agent: *", robots)
        self.assertIn("Allow: /", robots)
        self.assertIn(f"Sitemap: {site_url}sitemap.xml", robots)

        tree = ET.parse(ROOT / "sitemap.xml")
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = [el.text for el in tree.getroot().findall("sm:url/sm:loc", ns)]
        self.assertEqual(len(locs), len(set(locs)), "Duplicate URLs in sitemap.xml")
        expected_count = 7 + len(self.js["landmarks"])
        self.assertEqual(len(locs), expected_count)
        self.assertNotIn(f"{site_url}landmark.html", locs)

        lm_shell = (ROOT / "landmark.html").read_text(encoding="utf-8")
        self.assertIn('content="noindex, follow"', lm_shell)
        self.assertIn(cf_token, lm_shell, "Missing Cloudflare beacon on landmark.html")

        titles, descs = set(), set()
        for loc in locs:
            self.assertTrue(loc.startswith(site_url), f"Unexpected domain in sitemap: {loc}")
            rel = loc[len(site_url) :] or "index.html"
            fpath = ROOT / rel
            self.assertTrue(fpath.is_file(), f"Sitemap URL missing on disk: {fpath}")
            txt = fpath.read_text(encoding="utf-8")
            self.assertIn('content="index, follow"', txt, f"Missing index, follow on {rel}")
            self.assertIn(f'<link rel="canonical" href="{html_lib.escape(loc, quote=True)}">', txt, f"Canonical mismatch on {rel}")

            tm = re.search(r"<title>([\s\S]*?)</title>", txt)
            dm = re.search(r'<meta name="description" content="([^"]+)"', txt)
            om = re.search(r'<meta property="og:image" content="([^"]+)"', txt)
            jm = re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>', txt)
            self.assertTrue(tm and tm.group(1).strip(), f"Missing <title> on {rel}")
            self.assertTrue(dm and 50 <= len(html_lib.unescape(dm.group(1))) <= 165, f"Bad meta description on {rel}")
            self.assertTrue(om, f"Missing og:image on {rel}")
            self.assertTrue(jm, f"Missing JSON-LD on {rel}")

            t_val, d_val = tm.group(1).strip(), dm.group(1).strip()
            self.assertNotIn(t_val, titles, f"Duplicate <title> across pages: {t_val}")
            self.assertNotIn(d_val, descs, f"Duplicate meta description across pages: {d_val}")
            titles.add(t_val)
            descs.add(d_val)

            og_img = html_lib.unescape(om.group(1))
            self.assertTrue(og_img.startswith(site_url), f"og:image not absolute on {rel}: {og_img}")
            og_file = ROOT / og_img[len(site_url) :]
            self.assertTrue(og_file.is_file() and og_file.stat().st_size > 1000, f"Missing og:image file {og_file} on {rel}")

            ld = json.loads(jm.group(1))
            self.assertEqual(ld.get("@context"), "https://schema.org")
            self.assertTrue(ld.get("@graph"), f"Empty JSON-LD @graph on {rel}")
            self.assertIn(cf_token, txt, f"Missing Cloudflare beacon on {rel}")
            if rel.startswith("landmarks/"):
                self.assertRegex(txt, r"<h1>[^<]+</h1>", f"Static landmark missing <h1> on {rel}")

        house_html = (ROOT / "house.html").read_text(encoding="utf-8")
        self.assertEqual(len(re.findall(r'href="house\.html\?q=[^"]+"', house_html)), len(self.street_index))
        idx_txt = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("https://wildvegangoose.github.io/south-orange/", idx_txt)
        if cfg.get("google_site_verification"):
            self.assertIn(
                f'<meta name="google-site-verification" content="{cfg["google_site_verification"]}"',
                idx_txt,
            )
        self.assertIn("https://wildvegangoose.github.io/south-orange/people.html", (ROOT / "people.html").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
