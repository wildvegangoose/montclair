/* Historic photographs of specific Montclair houses: Gottscho-Schleisner Collection, Library of Congress
   (each item's rights statement: "No known restrictions on publication"). Owner names only for photos up to 1950. */
var MW = window.MW = window.MW || {};
MW.housePhotos = [
  {
    "address": "7 Greenview Way",
    "src": "img/houses/7-greenview-way-2018743121.jpg",
    "year": 1944,
    "caption": "Living room, toward the fireplace · residence of Mrs. Percy Rappaport",
    "credit": "Gottscho-Schleisner, Inc. / Library of Congress",
    "license": "No known restrictions on publication",
    "link": "https://www.loc.gov/item/2018743121/"
  },
  {
    "address": "7 Greenview Way",
    "src": "img/houses/7-greenview-way-2018743122.jpg",
    "year": 1944,
    "caption": "Dining room, toward the sideboard · residence of Mrs. Percy Rappaport",
    "credit": "Gottscho-Schleisner, Inc. / Library of Congress",
    "license": "No known restrictions on publication",
    "link": "https://www.loc.gov/item/2018743122/"
  },
  {
    "address": "7 Greenview Way",
    "src": "img/houses/7-greenview-way-2018743123.jpg",
    "year": 1944,
    "caption": "Dining room, toward the etageres · residence of Mrs. Percy Rappaport",
    "credit": "Gottscho-Schleisner, Inc. / Library of Congress",
    "license": "No known restrictions on publication",
    "link": "https://www.loc.gov/item/2018743123/"
  },
  {
    "address": "196 Upper Mountain Avenue",
    "src": "img/houses/196-upper-mountain-avenue-2018724451.jpg",
    "year": 1951,
    "caption": "General view of living room (Upper Montclair residence)",
    "credit": "Gottscho-Schleisner, Inc. / Library of Congress",
    "license": "No known restrictions on publication",
    "link": "https://www.loc.gov/item/2018724451/"
  },
  {
    "address": "196 Upper Mountain Avenue",
    "src": "img/houses/196-upper-mountain-avenue-2018724452.jpg",
    "year": 1951,
    "caption": "Living room, view toward painting (Upper Montclair residence)",
    "credit": "Gottscho-Schleisner, Inc. / Library of Congress",
    "license": "No known restrictions on publication",
    "link": "https://www.loc.gov/item/2018724452/"
  }
];
MW.housePhotosFor = (number, road) => {
  const n = s => (s || "").toUpperCase().replace(/[^A-Z ]/g, "")
    .replace(/\bN\b/g, "NORTH").replace(/\bS\b/g, "SOUTH").replace(/\bE\b/g, "EAST").replace(/\bW\b/g, "WEST")
    .replace(/\bUP\b/g, "UPPER")
    .replace(/\b(AVENUE|AVE|AV|ROAD|RD|STREET|ST|PLACE|PL|TERRACE|TER|DRIVE|DR|COURT|CT|WAY|LANE|LN)\b/g, "")
    .replace(/\s+/g, " ").trim();
  return MW.housePhotos.filter(p => {
    const m = p.address.match(/^(\d+)\s+(.+)$/);
    return m && String(number) === m[1] && n(road) === n(m[2]);
  });
};
