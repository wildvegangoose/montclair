/* Sanborn fire-insurance maps: find the sheet(s) that show an address, and render them.
   Data: js/sanborn-data.js (Library of Congress, 1885 & 1907 Montclair volumes, public domain). */
(function () {
  const MW = window.MW;
  const SUF = { RD: "ROAD", AV: "AVENUE", AVE: "AVENUE", ST: "STREET", PL: "PLACE", TER: "TERRACE", TERR: "TERRACE", DR: "DRIVE", CT: "COURT", LN: "LANE", LA: "LANE", PKWY: "PARKWAY", PKY: "PARKWAY" };
  const DIR = { N: "NORTH", S: "SOUTH", E: "EAST", W: "WEST", UP: "UPPER", UPR: "UPPER" };
  const norm = r => {
    if (!r) return "";
    let w = r.toUpperCase().replace(/[^A-Z0-9 ]/g, " ").split(/\s+/).filter(Boolean)
      .map((x, i, a) => (i === a.length - 1 && SUF[x]) || (i === 0 && a.length > 2 && DIR[x]) || x);
    let s = w.join(" ");
    s = s.replace(/\bGLEN RIDGE\b/g, "GLENRIDGE")
      .replace(/\bCLAIRMONT\b/g, "CLAREMONT")
      .replace(/\bBELLEVIEW\b/g, "BELLEVUE")
      .replace(/\bSAINT LUKES\b/g, "ST LUKES")
      .replace(/\bST LUKE\b/g, "ST LUKES")
      .replace(/\bMT HEBRON\b/g, "MOUNT HEBRON");
    return s;
  };
  const bare = s => s.replace(/\s+(ROAD|AVENUE|STREET|PLACE|TERRACE|DRIVE|COURT|LANE|WAY|PARKWAY)$/, "");

  /* -> [{ year, label, sheets: [n], exact, range: "101–183", street, note }]
     Note: 1885 (4 sheets, downtown Montclair) and 1907 (68 Montclair sheets in Essex County Vol. 3)
     have independent sheet numbering and pre-1900 downtown house numbers differed, so each volume
     is matched strictly on its own index. */
  MW.sanbornFor = function (number, road) {
    if (!MW.sanborn || !road) return [];
    const st = norm(road), n = parseInt(number, 10);
    return Object.entries(MW.sanborn).map(([y, v]) => {
      let rows = v.rows.filter(r => r[0] === st);
      if (!rows.length && bare(st) === st) rows = v.rows.filter(r => bare(r[0]) === st);
      if (!rows.length) return null;
      let hit = n ? rows.filter(r => r[1] != null && n >= r[1] && n <= r[2]) : [];
      if (hit.length > 1) { const same = hit.filter(r => r[1] % 2 === n % 2); if (same.length) hit = same; }
      const exact = hit.length > 0;
      const use = exact ? hit : rows;
      const sheets = [...new Set(use.flatMap(r => r[3]))].filter(s => v.sheets[s]);
      if (!sheets.length) return null;
      const note = exact ? (hit[0][4] || "") : (rows.length === 1 ? (rows[0][4] || "") : "");
      return { year: y, label: v.label, item: v.item, sheets, exact, range: exact && hit[0][1] != null ? `${hit[0][1]}–${hit[0][2]}` : "", street: rows[0][0], note };
    }).filter(Boolean);
  };

  const img = (v, s, w) => `https://tile.loc.gov/image-services/iiif/service:gmd:gmd381m:g3814m:${v.prefix}:${v.svc}:${v.sheets[s][1]}/full/${w},/0/default.jpg`;
  const page = (v, s) => `https://www.loc.gov/resource/${v.res}/?sp=${v.sheets[s][0]}`;
  const nice = s => s.toLowerCase().replace(/\b\w/g, c => c.toUpperCase());

  MW.sanbornHTML = function (number, road, opts = {}) {
    const hits = MW.sanbornFor(number, road);
    if (!hits.length) return "";
    const cards = hits.flatMap(h => {
      const v = MW.sanborn[h.year];
      return h.sheets.slice(0, h.exact ? 2 : 3).map(s => `<figure class="sb-card">
        <a href="${page(v, s)}" target="_blank" rel="noopener"><img src="${img(v, s, 640)}" alt="Sanborn map ${h.year}, sheet ${s}" loading="lazy"></a>
        <figcaption><b>${esc(h.year)}</b> · sheet ${s}${h.exact ? ` · covers ${h.range} ${esc(nice(h.street))}` : h.year === "1885" ? ` · downtown core (${esc(nice(h.street))})` : ` · one of the sheets for ${esc(nice(h.street))}`}
          <a href="${page(v, s)}" target="_blank" rel="noopener">Zoom in at the Library of Congress ↗</a></figcaption></figure>`);
    }).join("");
    const exact = hits.some(h => h.exact);
    const has1885 = hits.some(h => h.year === "1885");
    return `<div class="eyebrow">Fire-insurance maps</div><h2>${opts.title || "This street on the Sanborn maps"}</h2>
      <p class="muted">Sanborn maps were drawn for fire insurers and show every building: yellow for wood frame, pink for brick, blue for stone, with porches, stories and outbuildings. ${exact ? "We matched this address to the sheet in the 1907 street index." : "The index doesn't give a number range here, so these are the sheets for this street."} ${has1885 ? "The 4-sheet 1885 edition covers Montclair's downtown core using pre-renumbering house numbers. " : ""}${number ? "Check the house numbers written along the street on the sheet." : ""}</p>
      <div class="sb-grid">${cards}</div>
      <p class="small muted">${MW.sanbornCredit || "Sanborn Map Company"}. Library of Congress, Geography and Map Division, Sanborn Maps Collection (public domain).</p>`;
  };
  const esc = s => MW.esc(s);
})();
