/* House page: "From the library archive" section.
   Reads the archive/ folder built by tools/archive/*.py (Montclair History Online pre-1951 directories).
   If that folder is absent, this section stays hidden. */
(function () {
  const MW = window.MW;
  const ROOT = "archive/";
  const SUF = { RD: "ROAD", AV: "AVENUE", AVE: "AVENUE", ST: "STREET", PL: "PLACE", TER: "TERRACE", TERR: "TERRACE", DR: "DRIVE", CT: "COURT", LN: "LANE", LA: "LANE", PKWY: "PARKWAY", PKY: "PARKWAY", BLVD: "BOULEVARD", CIR: "CIRCLE" };
  const OCC = [[/\b(clk|elk)\b/g, "clerk"], [/\bslsman\b/g, "salesman"], [/\bslswn\b/g, "saleswoman"], [/\bmgr\b/g, "manager"], [/\bacct\b/g, "accountant"],
    [/\bemp\b/g, "employee"], [/\bwid\b/g, "widow of"], [/\btchr\b/g, "teacher"], [/\bsupt\b/g, "superintendent"], [/\b(engr|eng)\b/g, "engineer"],
    [/\bmech\b/g, "mechanic"], [/\bbkpr\b/g, "bookkeeper"], [/\bbkkpr\b/g, "bookkeeper"], [/\bsteno\b/g, "stenographer"], [/\bins\b/g, "insurance"], [/\bN ?Y\b/g, "New York"],
    [/\barcht?\b/g, "architect"], [/\bphys\b/g, "physician"], [/\bcontr\b/g, "contractor"], [/\bpres\b/g, "president"], [/\btreas\b/g, "treasurer"],
    [/\bsec\b/g, "secretary"], [/\bopr\b/g, "operator"], [/\bcarp\b/g, "carpenter"], [/\blab\b/g, "laborer"], [/\bchauf\b/g, "chauffeur"],
    [/\bdom\b/g, "domestic"], [/\bstud\b/g, "student"], [/\bagt\b/g, "agent"], [/\bmfr\b/g, "manufacturer"], [/\bmkr\b/g, "maker"],
    [/\bdraftsman\b/g, "draftsman"], [/\bTelCo\b/g, "the Telephone Co."], [/\bPruInsCo\b/g, "Prudential Insurance"], [/\bhousekpr\b/g, "housekeeper"],
    [/\bsupvr?\b/g, "supervisor"], [/\bforemn\b/g, "foreman"], [/\bpntr\b/g, "painter"], [/\bplmbr\b/g, "plumber"], [/\bdrftsmn\b/g, "draftsman"]];

  const esc = MW.esc;
  const expandOcc = o => OCC.reduce((s, [re, w]) => s.replace(re, w), (o || "").replace(/\s+/g, " ").replace(/^[a-z]?[A-Z]\s(?=[A-Z])/, "").trim())
    .replace(/\s+(New York|Newark|Bloomfield|Glen Ridge|Verona|Caldwell|Orange|East Orange|West Orange|Paterson|Passaic|Jersey City)$/, ", $1");
  const nice = s => s.toLowerCase().replace(/\b\w/g, c => c.toUpperCase());
  const person = l => `${l.given ? l.given.replace(/\b([A-Z])\b(?!\.)/g, "$1.") + " " : ""}${l.surname}`;

  function normRoad(r) {
    if (!r) return null;
    const w = r.toUpperCase().replace(/[^A-Z0-9 ]/g, " ").split(/\s+/).filter(Boolean);
    if (w.length && SUF[w[w.length - 1]]) w[w.length - 1] = SUF[w[w.length - 1]];
    return w.join(" ");
  }
  const slug = s => s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");

  async function getJSON(u) { const r = await fetch(u); if (!r.ok) throw new Error(r.status); return r.json(); }

  function matchStreet(index, road) {
    const n = normRoad(road); if (!n) return null;
    if (index[slug(n)]) return slug(n);
    const DIR = { N: "NORTH", S: "SOUTH", E: "EAST", W: "WEST", UP: "UPPER", UPR: "UPPER", NORTH: "NORTH", SOUTH: "SOUTH", EAST: "EAST", WEST: "WEST", UPPER: "UPPER" };
    let alt = n
      .replace(/\bGLEN RIDGE\b/g, "GLENRIDGE")
      .replace(/\bCLAIRMONT\b/g, "CLAREMONT")
      .replace(/\bBELLEVIEW\b/g, "BELLEVUE")
      .replace(/\bSAINT LUKES\b/g, "ST LUKES")
      .replace(/\bST LUKE\b/g, "ST LUKES")
      .replace(/\bMT HEBRON\b/g, "MOUNT HEBRON")
      .replace(/\bPKY\b/g, "PARKWAY")
      .replace(/^([NS]|UP|UPR)\s+/, (_, d) => DIR[d] + " ");
    const dm = alt.match(/^(.+)\s+(N|S|E|W|NORTH|SOUTH|EAST|WEST)$/);
    if (dm) alt = DIR[dm[2]] + " " + dm[1];
    if (alt === "CRESCENT") alt = "THE CRESCENT";
    if (alt === "BELLAIR DRIVE") alt = "BELAIR DRIVE";
    if (alt === "CLAIRWILL AVENUE") alt = "CLAREWILL AVENUE";
    if (alt === "MOUNTAIN VIEW PLACE") alt = "MOUNT VIEW PLACE";
    if (index[slug(alt)]) return slug(alt);
    const bare = alt.replace(/\s+(ROAD|AVENUE|STREET|PLACE|TERRACE|DRIVE|COURT|LANE|PARKWAY|WAY|CIRCLE|BOULEVARD)$/, "");
    const hasSuffix = bare !== alt;
    const matches = Object.keys(index).filter(k => index[k].name.replace(/\s+(ROAD|AVENUE|STREET|PLACE|TERRACE|DRIVE|COURT|LANE|PARKWAY|WAY|CIRCLE|BOULEVARD)$/, "") === bare);
    if (matches.length === 1) return matches[0];
    return !hasSuffix && matches.length ? matches[0] : null;
  }

  function story(addr, ls) {
    if (!ls.length) return "";
    const byYear = {}; ls.forEach(l => (byYear[l.year] = byYear[l.year] || []).push(l));
    const years = Object.keys(byYear).map(Number).sort((a, b) => a - b);
    const first = years[0], last = years[years.length - 1];
    const named = l => l.given && l.surname && /^[A-Z][a-z]/.test(l.given);
    const firstNamed = ls.find(l => named(l) && l.tenure === "householder") || ls.find(named) || ls[0];
    const head = firstNamed;
    const spans = {};
    ls.forEach(l => { if (!l.surname) return; const s = spans[l.surname] = spans[l.surname] || { min: l.year, max: l.year, n: new Set() }; s.min = Math.min(s.min, l.year); s.max = Math.max(s.max, l.year); s.n.add(l.year); });
    const longest = Object.entries(spans).sort((a, b) => (b[1].max - b[1].min) - (a[1].max - a[1].min))[0];
    const fams = Object.values(spans).filter(v => v.n.size >= 2).length;
    const occs = [...new Set(ls.map(l => expandOcc(l.occ).replace(/[^A-Za-z ,.&'-]/g, "")).filter(o => o && o.length > 3 && /^[a-z]/.test(o) && !/^(r|h)\b|widow|^[a-z]{1,2}\b/.test(o)))]
      .filter((o, i, a) => !a.some((x, j) => j < i && x.replace(/\W/g, "") === o.replace(/\W/g, ""))).slice(0, 4);
    let t = `The earliest city directory in our indexed archive that lists <b>${esc(addr)}</b> is from <b>${first}</b>. ` +
      `${head.year === first ? "That year" : `By ${head.year}`} ${esc(person(head))}${head.spouse ? ` and ${esc(head.spouse)}` : ""} ${head.tenure === "householder" ? "headed the household" : "lived here"}${head.occ ? `, listed as "${esc(expandOcc(head.occ))}"` : ""}. `;
    if (longest && longest[1].max > longest[1].min) t += `The <b>${esc(longest[0])}</b> name appears here from ${longest[1].min} to at least ${longest[1].max}, about ${longest[1].max - longest[1].min} years. `;
    t += fams <= 1 ? `The archive has ${years.length} directory year${years.length === 1 ? "" : "s"} listing this address between ${first} and ${last}. `
      : `Across ${years.length} directory years between ${first} and ${last}, ${fams} family names appear here more than once. `;
    if (occs.length > 1) t += `Occupations recorded here include ${occs.map(o => `"${esc(o)}"`).join(", ")}.`;
    return t;
  }

  function snip(t, num) {
    const i = Math.max(0, (t || "").search(new RegExp("\\b" + num + "\\b")));
    const s = t.slice(Math.max(0, i - 140), i + 180);
    return (i > 140 ? "…" : "") + s.replace(/^\S*\s/, "") + "…";
  }

  const cleanLabel = s => { try { return decodeURIComponent(s || ""); } catch (e) { return (s || "").replace(/%26/g, "&"); } };

  function render(el, addr, street, num, house, streetData) {
    const ls = (house && house.listings) || [], cards = (house && house.cards) || [], news = (house && house.news) || [];
    const byYear = {}; ls.forEach(l => (byYear[l.year] = byYear[l.year] || []).push(l));
    const docs = ls.filter(l => l.crop).reduce((a, l) => (a.some(x => x.crop === l.crop) ? a : a.concat(l)), []);
    const hasLoc = news.some(n => n.iiif), hasScrap = news.some(n => !n.iiif);

    const minYr = ls.length ? Math.min(...ls.map(l => l.year)) : 9999;
    const nInt = parseInt(num, 10);
    const nearbyOld = (streetData && !isNaN(nInt) && minYr >= 1920)
      ? [nInt - 2, nInt + 2].map(c => String(c)).map(c => {
          const ch = streetData.houses[c];
          if (!ch || !ch.listings || !ch.listings.length) return null;
          const yrs = ch.listings.map(l => l.year).sort((a, b) => a - b);
          const maxY = yrs[yrs.length - 1];
          if (maxY > 1920 || maxY >= minYr) return null;
          const firstNamed = ch.listings.find(l => l.given && l.surname) || ch.listings[0];
          return { num: c, first: yrs[0], last: maxY, who: person(firstNamed) };
        }).filter(Boolean)
      : [];

    el.innerHTML = `<div class="wrap">
      <div class="arch-head reveal">
        <div class="eyebrow">From Montclair History Online</div>
        <h2>The record for ${esc(addr)}</h2>
        <p class="lede">${ls.length ? story(addr, ls) : `Our indexed pre-1951 Montclair city directories don't list this exact number. The house may be newer, the number may have changed, or the scanned text may have garbled it.`}</p>
        <p class="arch-local small">Residents come from the Price &amp; Lee Montclair city directories (1910–1949) digitized by the Montclair Public Library and Montclair History Center on <a href="https://www.digifind-it.com/montclair/views/view.php?id=2" target="_blank" rel="noopener">Montclair History Online</a>. Every entry links back to the original scanned page. Directory names are shown only through 1950.</p>
      </div>
      <div class="arch-grid ${cards.length ? "" : "nophoto"}">
        <div class="residents reveal d1">
          <h3>Who lived here <span class="small muted">(city directories, 1910–1949)</span></h3>
          ${ls.length ? `<ol class="rlist">${Object.keys(byYear).sort().map(y => `<li><span class="ry">${y}</span><div>${byYear[y].map(l =>
            `<div class="rp"><b>${esc(person(l))}</b>${l.spouse ? ` <span class="muted">(${esc(l.spouse)})</span>` : ""} · <span class="muted">${esc(l.tenure === "householder" ? "head of household" : l.tenure)}${l.occ ? ", " + esc(expandOcc(l.occ)) : ""}</span> <a class="src" href="${l.src}" target="_blank" rel="noopener" title="See the scanned page">scan ↗</a></div>`).join("")}</div></li>`).join("")}</ol>`
            : `<p class="muted">No directory listings found for this number through 1949.</p>`}
          ${nearbyOld.length ? `<p class="small muted" style="margin-top:.8rem;padding:.65rem .8rem;background:rgba(227,163,58,.12);border-radius:10px"><b>Earlier numbering nearby (unconfirmed):</b> ${nearbyOld.map(o => `<a href="house.html?q=${encodeURIComponent(o.num + " " + nice(street))}">#${esc(o.num)} ${esc(nice(street))}</a> (${o.first === o.last ? o.first : `${o.first}–${o.last}`}${o.who ? `, ${esc(o.who)}` : ""})`).join(" and ")} disappeared after ${Math.max(...nearbyOld.map(o => o.last))}. Some early houses were renumbered—check the 1907 Sanborn map or deed chain to confirm whether it was this house or an adjacent lot.</p>` : ""}
          <p class="small muted">The text was read by computer from the scans, so names can be misspelled. The scanned lines below, and the "scan ↗" links, show the originals.</p>
        </div>
      </div>
      ${news.length ? `<div class="news reveal"><h3>In the news</h3><p class="small muted">${hasLoc && hasScrap ? "Newspaper pages from the Library of Congress and library clippings that mention this address." : hasLoc ? "Newspaper pages that mention this address, cropped from the scans." : "Clippings that mention this address."}</p>
        <div class="news-grid">${news.slice().sort((a, b) => (a.kind === "ad") - (b.kind === "ad") || parseInt(a.year, 10) - parseInt(b.year, 10)).slice(0, 8).map(n => n.iiif
          ? `<a class="clip loc" href="${n.src}" target="_blank" rel="noopener"><span class="doc-year">${esc(String(n.year))}</span><img src="${n.iiif}" alt="Newspaper page, ${esc(n.date)}" loading="lazy"><span class="doc-cap">${n.kind === "ad" ? "Classified ad · " : ""}${esc(nice(n.paper || "newspaper").replace(/\s*\(.*$/, ""))}, ${esc(n.date)}</span><span class="clip-snip">${esc(snip(n.snippet, num))}</span></a>`
          : `<a class="clip" href="${n.src}" target="_blank" rel="noopener"><span class="doc-year">${esc(String(n.year))}</span><img src="${ROOT + n.crop}" alt="Newspaper clipping, ${esc(String(n.year))}" loading="lazy"><span class="doc-cap">Archive clipping, ${esc(String(n.year))}</span></a>`).join("")}</div></div>` : ""}
      ${docs.length ? `<div class="docs reveal"><h3>Documents from the era</h3><p class="small muted">The actual directory lines for this address, cropped from the Montclair History Online scans. For ditto-dash (—) entries, the surname header from higher in the column is shown above a dashed line; click any scan to open the full page.</p>
        <div class="doc-strip">${docs.map(l => `<a class="doc" href="${l.src}" target="_blank" rel="noopener"><span class="doc-year">${l.year}</span><img src="${ROOT + l.crop}" alt="Directory line, ${l.year}" loading="lazy"><span class="doc-cap">${l.year} city directory${l.surname || l.given ? ` · ${esc(person(l))}` : ""}</span></a>`).join("")}</div></div>` : ""}
    </div>`;
    el.hidden = false;
    MW.observeReveals(el);
  }

  MW.Archive = {
    async show(hit, q, el) {
      el.hidden = true; el.innerHTML = "";
      let index; try { index = await getJSON(ROOT + "data/street_index.json"); } catch (e) { return; }
      const m = (q || "").match(/^\s*(\d+[A-Za-z]?)\s+([^,]+)/);
      const num = String(hit.number || (m && m[1]) || "").replace(/[^0-9]/g, "");
      const road = hit.road || (m && m[2]) || (!m && (q || "").replace(/,.*$/, "").trim());
      const key = matchStreet(index, road);
      if (!key) return;
      let sd; try { sd = await getJSON(ROOT + "data/streets/" + key + ".json"); } catch (e) { return; }
      if (!num) {
        const nums = Object.keys(sd.houses || {}).sort((a, b) => parseInt(a, 10) - parseInt(b, 10) || a.localeCompare(b));
        if (!nums.length) return;
        const stName = nice(sd.name);
        el.innerHTML = `<div class="wrap"><div class="arch-head reveal">
          <div class="eyebrow">From Montclair History Online</div>
          <h2>Houses on ${esc(stName)} (1910–1949)</h2>
          <p class="lede">Select a house number on <b>${esc(stName)}</b> to see its 1910–1949 Montclair city directory listings and scanned line crops.</p>
          <div class="house-nums">${nums.map(n => `<a class="hnum" href="house.html?q=${encodeURIComponent(n + " " + stName)}">${esc(n)}</a>`).join("")}</div>
        </div></div>`;
        el.hidden = false;
        MW.observeReveals(el);
        return;
      }
      const house = sd.houses[num];
      render(el, `${num} ${nice(sd.name)}`, sd.name, num, house, sd);
    }
  };
})();
