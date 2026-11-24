/* ==========================================================================
   Montclair Through Time: the historical dataset.
   Every dated fact below comes from one of the sources in MW.sources.
   Where sources disagree, the text notes the discrepancy explicitly.
   Narrative passages ("what it was like") are our own synthesis of those facts.
   ========================================================================== */
var MW = window.MW = window.MW || {};

MW.town = {
  name: "Montclair", state: "NJ", siteTitle: "Montclair Through Time",
  tagline: "A fan history of Montclair, NJ",
  siteUrl: "https://wildvegangoose.github.io/montclair/",
  center: [40.8259, -74.2090], geocodeSuffix: ", Montclair, NJ", todayLabel: "today's township",
  neighbor: { name: "South Orange", url: "https://wildvegangoose.github.io/south-orange/" }
};

MW.sources = {
  wiki:        { label: "Wikipedia: Montclair, New Jersey", url: "https://en.wikipedia.org/wiki/Montclair,_New_Jersey" },
  mhc:         { label: "Montclair History Center", url: "https://www.montclairhistory.org/" },
  mhcCrane:    { label: "Montclair History Center: Crane House & Historic YWCA", url: "https://www.montclairhistory.org/crane-house-and-historic-ywca" },
  mhcSpaulding:{ label: "Montclair History Center: Randall Spaulding & Montclair High School", url: "https://www.montclairhistory.org/new-blog/2020/8/30/randall-spaulding-the-father-of-montclair-high-school-part-1" },
  mhcAtlas:    { label: "Montclair History Center: Musings on the 1906 Atlas", url: "https://www.montclairhistory.org/new-blog/2020/3/21/musings-on-the-1906-atlas-part-2-of-2" },
  mhcWwi:      { label: "Montclair History Center: Montclair's WWI Memorials", url: "https://www.montclairhistory.org/new-blog/2020/5/21/montclairs-wwi-memorials" },
  mplLocal:    { label: "Montclair Public Library: Local History Collection", url: "https://montclairlibrary.org/local-history/" },
  directories: { label: "Montclair History Online: City Directories (1870–1950, Digifind-IT)", url: "https://www.digifind-it.com/montclair/views/view.php?id=2" },
  hpElement:   { label: "Township of Montclair: Historic Preservation Plan Element (2016)", url: "https://www.montclairnjusa.org/files/sharedassets/public/v/1/government/departments/planning-and-community-development/documents/2016-historic-preservation-plan-element.pdf" },
  hpc:         { label: "Township of Montclair: Historic Preservation Commission", url: "https://www.montclairnjusa.org/Government/Boards-and-Commissions/Historic-Preservation-Commission" },
  nrhpMps:     { label: "National Register: Historic Resources of Montclair MPS (NPGallery)", url: "https://npgallery.nps.gov/pdfhost/docs/NRHP/Text/64000493.pdf" },
  nrCrane:     { label: "National Register: Israel Crane House (NRIS 73001091)", url: "https://npgallery.nps.gov/AssetDetail/NRIS/73001091" },
  nrBond:      { label: "National Register: Van Reyper-Bond House (NRIS 79001483)", url: "https://npgallery.nps.gov/AssetDetail/NRIS/79001483" },
  nrShultz:    { label: "National Register: Charles S. Shultz House (NRIS 79001482)", url: "https://npgallery.nps.gov/AssetDetail/NRIS/79001482" },
  nrCarnegie:  { label: "National Register: Montclair Carnegie Library (NRIS 86003074)", url: "https://npgallery.nps.gov/AssetDetail/NRIS/86003074" },
  nrAnchorage: { label: "National Register: The Anchorage (NRIS 86003061)", url: "https://npgallery.nps.gov/AssetDetail/NRIS/86003061" },
  nrAnderson:  { label: "National Register nomination: Anderson Park (2009)", url: "https://friendsofandersonpark.com/wp-content/uploads/2017/11/AndersonPark-NationalRegister-NominatioReport.pdf" },
  nrLackawanna:{ label: "Wikipedia: Lackawanna Terminal (Montclair, NJ)", url: "https://en.wikipedia.org/wiki/Lackawanna_Terminal_(Montclair,_New_Jersey)" },
  craneWiki:   { label: "Wikipedia: Crane House and Historic YWCA", url: "https://en.wikipedia.org/wiki/Crane_House_and_Historic_YWCA" },
  mhcWiki:     { label: "Wikipedia: Montclair History Center", url: "https://en.wikipedia.org/wiki/Montclair_History_Center" },
  bondWiki:    { label: "Wikipedia: Van Reyper-Bond House", url: "https://en.wikipedia.org/wiki/Van_Reyper-Bond_House" },
  pineWiki:    { label: "Wikipedia: Pine Street Historic District (Montclair, NJ)", url: "https://en.wikipedia.org/wiki/Pine_Street_Historic_District_(Montclair,_New_Jersey)" },
  shultzWiki:  { label: "Wikipedia: Charles S. Shultz House", url: "https://en.wikipedia.org/wiki/Charles_S._Shultz_House" },
  anchorageWiki:{ label: "Wikipedia: The Anchorage (Montclair, NJ)", url: "https://en.wikipedia.org/wiki/The_Anchorage_(Montclair,_New_Jersey)" },
  andersonWiki:{ label: "Wikipedia: Anderson Park (New Jersey)", url: "https://en.wikipedia.org/wiki/Anderson_Park_(New_Jersey)" },
  andersonFriends:{ label: "Friends of Anderson Park: The Donor and the Deal", url: "https://friendsofandersonpark.com/the-donor-and-the-deal/" },
  oakcroft:    { label: "Historic Oakcroft: Building Oakcroft, a 'Residential Park'", url: "https://historicoakcroft.org/building-oakcroft-a-residential-park/" },
  howardWiki:  { label: "Wikipedia: John Galen Howard (Carnegie Library)", url: "https://en.wikipedia.org/wiki/John_Galen_Howard" },
  upperMcWiki: { label: "Wikipedia: Upper Montclair station", url: "https://en.wikipedia.org/wiki/Upper_Montclair_station" },
  watchungWiki:{ label: "Wikipedia: Watchung Avenue station", url: "https://en.wikipedia.org/wiki/Watchung_Avenue_station" },
  heightsWiki: { label: "Wikipedia: Montclair Heights station", url: "https://en.wikipedia.org/wiki/Montclair_Heights_station" },
  boontonWiki: { label: "Wikipedia: Montclair–Boonton Line", url: "https://en.wikipedia.org/wiki/Montclair%E2%80%93Boonton_Line" },
  msuWiki:     { label: "Wikipedia: Montclair State University", url: "https://en.wikipedia.org/wiki/Montclair_State_University" },
  mamWiki:     { label: "Wikipedia: Montclair Art Museum", url: "https://en.wikipedia.org/wiki/Montclair_Art_Museum" },
  mamHist:     { label: "Montclair Art Museum: MAM's History", url: "https://www.montclairartmuseum.org/mams-history" },
  cliffsideWiki:{ label: "Wikipedia: Cliffside Hose Company No. 4", url: "https://en.wikipedia.org/wiki/Cliffside_Hose_Company_No._4" },
  congWiki:    { label: "Wikipedia: Congregational Church (Montclair, NJ)", url: "https://en.wikipedia.org/wiki/Congregational_Church_(Montclair,_New_Jersey)" },
  wellmontWiki:{ label: "Wikipedia: Wellmont Theater", url: "https://en.wikipedia.org/wiki/Wellmont_Theater" },
  presbyWiki:  { label: "Wikipedia: Presby Memorial Iris Gardens", url: "https://en.wikipedia.org/wiki/Presby_Memorial_Iris_Gardens" },
  presbySite:  { label: "Presby Memorial Iris Gardens: History", url: "https://www.presbyirisgardens.org/history/" },
  essexPresby: { label: "Essex County Parks: Presby Memorial Iris Gardens", url: "https://essexcountyparks.org/parks/presby-memorial-iris-gardens/about" },
  essexBrook:  { label: "Essex County Parks: Brookdale Park", url: "https://essexcountyparks.org/parks/brookdale-park/about" },
  edgemontWiki:{ label: "Wikipedia: Edgemont Memorial Park", url: "https://en.wikipedia.org/wiki/Edgemont_Memorial_Park" },
  glenfieldWiki:{ label: "Wikipedia: Glenfield Park (New Jersey)", url: "https://en.wikipedia.org/wiki/Glenfield_Park_(New_Jersey)" },
  vanVleckWiki:{ label: "Wikipedia: Van Vleck House and Gardens", url: "https://en.wikipedia.org/wiki/Van_Vleck_House_and_Gardens" },
  howeFriends: { label: "Friends of the Howe House (369 Claremont Avenue)", url: "https://www.friendsofthehowehouse.org/" },
  mpsMagnet:   { label: "Montclair Public Schools: Magnet System Historical Perspective", url: "https://www.montclairps.org/district/magnet_system/historical_perspective" },
  podMagnet:   { label: "The Montclair Pod: The Journey to Montclair's Magnet System", url: "https://montclairpod.com/the-journey-to-montclairs-magnet-system-a-timeline-marked-by-segregation-activism-and-choice/" },
  shaw:        { label: "Shaw, History of Essex and Hudson Counties (1884)", url: "https://archive.org/details/historyofessexh02shaw" },
  whittemore:  { label: "Whittemore, History of Montclair Township (1894)", url: "https://archive.org/details/historyofmontcla00whit" },
  doremus:     { label: "Doremus, Reminiscences of Montclair (1908)", url: "https://archive.org/details/reminiscencesofm00dore" },
  bloomWiki:   { label: "Wikipedia: Bloomfield, New Jersey", url: "https://en.wikipedia.org/wiki/Bloomfield,_New_Jersey" },
  newark:      { label: "Wikipedia: Old First Presbyterian Church, Newark (town meeting house)", url: "https://en.wikipedia.org/wiki/Old_First_Presbyterian_Church_(Newark,_New_Jersey)" },
  sanborn1885: { label: "Sanborn Fire Insurance Map, Montclair, 1885 (Library of Congress, public domain)", url: "https://www.loc.gov/item/sanborn05557_001/" },
  sanborn1907: { label: "Sanborn Fire Insurance Map, Essex County Vol. 3: Montclair, 1907 (Library of Congress, public domain)", url: "https://www.loc.gov/item/sanborn05475_003/" },
  tiger:       { label: "U.S. Census TIGER municipal boundaries (outlines before 1868 are approximations)", url: "https://tigerweb.geo.census.gov/" }
};

/* U.S. Census counts for Montclair (first enumerated separately in 1870 after 1868 split from Bloomfield). */
MW.census = [
  [1870, 2853], [1880, 5147], [1890, 8636], [1900, 13962], [1910, 21550], [1920, 28810],
  [1930, 42017], [1940, 39807], [1950, 43927], [1960, 43129], [1970, 44043], [1980, 38321],
  [1990, 37729], [2000, 38977], [2010, 37669], [2020, 40921], [2025, 44633]
];
MW.populationFor = function (year) {
  const c = MW.census;
  if (year < 1666) return { approx: true, label: "Lenape homeland" };
  if (year < 1812) return { approx: true, label: "farmsteads in Cranetown & Speertown" };
  if (year < 1856) return { approx: true, label: "rural villages in Bloomfield Township" };
  if (year < 1870) return { approx: true, label: "growing railroad villages (~2,500 by 1868)" };
  if (year >= c[c.length - 1][0]) return { value: c[c.length - 1][1] };
  for (let i = 0; i < c.length - 1; i++) {
    const [y0, p0] = c[i], [y1, p1] = c[i + 1];
    if (year >= y0 && year <= y1) return { value: Math.round(p0 + (p1 - p0) * (year - y0) / (y1 - y0)) };
  }
  return { value: c[0][1] };
};

/* --------------------------------------------------------------------------
   What the place was called at each moment in time.
   -------------------------------------------------------------------------- */
MW.names = [
  { from: 1500, to: 1665, name: "Lenapehoking", sub: "the Lenape homeland along First Watchung Mountain" },
  { from: 1666, to: 1811, name: "Cranetown & Speertown", sub: "English and Dutch mountain settlements in Newark Township" },
  { from: 1812, to: 1859, name: "West Bloomfield & Speertown", sub: "western villages of Bloomfield Township" },
  { from: 1860, to: 1867, name: "Montclair (Bloomfield Twp.)", sub: "renamed for \"clear mountain,\" still inside Bloomfield Township" },
  { from: 1868, to: 1893, name: "Montclair Township", sub: "incorporated April 15, 1868 to finance a second railroad" },
  { from: 1894, to: 1979, name: "Town of Montclair", sub: "reincorporated as a town on February 24, 1894" },
  { from: 1980, to: 2100, name: "Township of Montclair", sub: "reclassified in 1980 (Council–Manager form since 1988)" }
];
MW.nameFor = y => MW.names.find(n => y >= n.from && y <= n.to) || MW.names[MW.names.length - 1];

/* Seats of local government */
MW.seats = [
  { id: "seat-newark", from: 1666, to: 1811, title: "Newark town meeting", place: "Newark's meeting house on Broad Street, about 6 miles southeast",
    lat: 40.7357, lon: -74.1714, offmap: true,
    text: "For nearly 150 years the farms of Cranetown and Speertown were governed by Newark's town meeting, which confirmed the early mountain land grants to Jasper Crane's sons and neighboring settlers.",
    sources: ["shaw", "newark"] },
  { id: "seat-bloomfield", from: 1812, to: 1867, title: "Bloomfield Township", place: "Bloomfield Town Green, about 2 miles east",
    lat: 40.79689, lon: -74.19689, offmap: true,
    text: "Bloomfield Township broke off from Newark on March 23, 1812, taking in today's Bloomfield, Montclair, Glen Ridge, Belleville and Nutley (Belleville and Nutley split off in 1839). Montclair remained Bloomfield's western section until 1868.",
    sources: ["bloomWiki", "whittemore"] },
  { id: "seat-early-mc", from: 1868, to: 1903, title: "Early Montclair Township offices", place: "Bloomfield Avenue & Valley Road (central Cranetown)",
    lat: 40.8152, lon: -74.2202,
    text: "After splitting from Bloomfield on April 15, 1868, Montclair's township committee—and after 1894, its Town Council—met in rented halls and early municipal rooms near Bloomfield Avenue before erecting a dedicated municipal building in 1904.",
    sources: ["whittemore", "hpElement"] },
  { id: "seat-647", from: 1904, to: 1968, title: "Old Municipal Building", place: "647 Bloomfield Avenue",
    lat: 40.81477, lon: -74.21868,
    text: "Built in 1904 on Bloomfield Avenue as Montclair's Town Hall and public safety headquarters. When general municipal offices moved to Claremont Avenue in 1969, 647 Bloomfield remained Montclair Police Headquarters and Municipal Court.",
    sources: ["hpElement", "wiki"] },
  { id: "seat-205", from: 1969, to: 2100, title: "Montclair Municipal Building", place: "205 Claremont Avenue",
    lat: 40.81732, lon: -74.21541,
    text: "Montclair's modern Town Hall, built in 1969 on Claremont Avenue between Park Street and North Fullerton Avenue, houses the Township Council chambers, Township Manager and municipal departments.",
    sources: ["wiki", "hpc"] }
];
MW.seatsFor = y => MW.seats.filter(s => y >= s.from && y <= s.to);

/* Approximate jurisdiction outlines (data/boundaries.js, built by tools/boundaries/build_eras.py) */
MW.jurisdictionsFor = y => (window.MW_JURISDICTIONS || []).filter(j => y >= j.from && y <= j.to);

/* --------------------------------------------------------------------------
   Eras: what it was like. Narrative is our synthesis of the sourced facts.
   -------------------------------------------------------------------------- */
MW.eras = [
  {
    id: "lenape", from: 1500, to: 1665, name: "Lenapehoking",
    tagline: "First Watchung Mountain before colonial deeds",
    palette: ["#f3d9a4", "#c98b5b"],
    story: [
      "Before European settlement, the basalt ridge of First Watchung Mountain and the brooks draining east toward the Passaic and Newark Bay lay inside Lenapehoking, the homeland of the Lenape (Delaware) people.",
      "Local histories record that Native footpaths climbed the mountain gap along what became Bloomfield Avenue and crossed the flats of today's Brookdale Park and Speertown. The ridge gave clear views east across the meadows toward the Hudson.",
      "No intact Lenape settlement site has been excavated within today's Montclair, so this earliest chapter is told through the landscape itself: the traprock ridge, Toney's Brook and the Third River watershed."
    ],
    sources: ["wiki", "essexBrook", "hpElement"]
  },
  {
    id: "cranetown", from: 1666, to: 1811, name: "Cranetown & Speertown",
    tagline: "English Puritans to the south, Dutch farmers to the north",
    palette: ["#f1e3bd", "#9c7a4a"],
    story: [
      "After Puritan founders settled Newark in 1666, they pushed west to the First Mountain. Jasper Crane surveyed the slope in 1675 and left 300 mountain acres to his sons Azariah and Jasper Jr.; by 1694 Azariah Crane had settled near today's Orange Road and Myrtle Avenue, giving southern Montclair the name Cranetown.",
      "To the north—beyond today's Watchung Avenue—Dutch families from Hackensack and Acquackanonk (including the Speer, Van Giesen, Sigler and Vreeland families) cleared farms along Speertown Road (today's Valley Road), forming the quiet farming village of Speertown.",
      "Oral tradition holds that George Washington paused in Cranetown and Speertown during the Revolutionary War (commemorated by 20th-century markers), though no contemporary written record confirms his stay. In 1796 twenty-one-year-old entrepreneur Israel Crane built his Federal mansion on Old Road (Glenridge Avenue); records show he enslaved at least five people there—Bill, Joe, Jack, Bett and Dine."
    ],
    sources: ["hpElement", "mhcCrane", "craneWiki", "shaw"]
  },
  {
    id: "westbloomfield", from: 1812, to: 1855, name: "West Bloomfield & the Turnpike",
    tagline: "Bloomfield Township, toll roads and the first Black homeowner",
    palette: ["#efe4c8", "#7d6847"],
    story: [
      "On March 23, 1812 Bloomfield Township separated from Newark, pulling Cranetown and Speertown into its western hills as \"West Bloomfield.\" Israel Crane championed the Newark–Pompton Turnpike (today's Bloomfield Avenue), turning the mountain climb into a bustling toll road linking Newark to northern New Jersey.",
      "Mills, tanneries, cider presses and general stores clustered along Toney's Brook and the turnpike, while Speertown remained a landscape of stone farmhouses and orchards.",
      "In 1831 Nathaniel Crane's will confirmed the freedom of James Howe—manumitted in 1817—and left him six acres, $400 and the c. 1780 house at 369 Claremont Avenue, making Howe the first documented African American homeowner in Montclair."
    ],
    sources: ["hpElement", "bloomWiki", "howeFriends", "doremus"]
  },
  {
    id: "railroads", from: 1856, to: 1879, name: "Two Railroads & Breakaway",
    tagline: "West Bloomfield becomes Montclair—and splits from Bloomfield",
    palette: ["#e5ddc6", "#6b5a42"],
    story: [
      "The Newark & Bloomfield Railroad reached West Bloomfield in 1856 (later leased by the Delaware, Lackawanna & Western), putting Manhattan within an hour's commute. In 1860 residents adopted the French-inspired name \"Montclair\"—clear mountain—for the sunlit views along the ridge.",
      "When Montclair boosters wanted to bond a second railroad north through Speertown and Bloomfield Township balked at the tax, Montclair won state legislation to break away as an independent township on April 15, 1868. The Montclair Railway (soon the Erie's New York & Greenwood Lake line) opened in 1873 with stations through Walnut Street, Park Street (Watchung Ave), Upper Montclair and Montclair Heights.",
      "Meanwhile Montclair built a statewide reputation for public education: Central School opened at Church Street and Valley Road in 1860, graduated its first Montclair High School class in 1874, and won praise at the 1876 Philadelphia Centennial Exposition under superintendent Randall Spaulding."
    ],
    sources: ["wiki", "whittemore", "mhcSpaulding", "watchungWiki"]
  },
  {
    id: "estates", from: 1880, to: 1907, name: "Estates, Artists & Town Charter",
    tagline: "George Inness, Mountain Avenue mansions and an Olmsted park",
    palette: ["#dce5d8", "#4d6b57"],
    story: [
      "Two rail lines and cool mountain air turned Montclair into one of New York's premier commuter suburbs. Landscape painter George Inness moved to Grove Street in 1885, anchoring an artists' colony that drew sculptors, illustrators and collectors. Following a February 1894 referendum, Montclair reincorporated as a Town.",
      "Wealthy commuters lined North, South and Upper Mountain Avenues with grand houses—including Charles S. Shultz's fire-resistant \"Evergreens\" (1896) by Michel LeBrun—while working-class Italian and African American families built vibrant neighborhoods around Pine Street, Glenridge Avenue, Frog Hollow and the South End.",
      "Civic infrastructure raced to keep up: Cliffside Hose Company No. 4 opened in Upper Montclair (1901), Charles W. Anderson donated parkland designed by the Olmsted Brothers (1903), John Galen Howard designed Montclair's Carnegie Library (1904), and a new Municipal Building rose at 647 Bloomfield Avenue (1904)."
    ],
    sources: ["nrhpMps", "shultzWiki", "pineWiki", "nrAnderson", "howardWiki"]
  },
  {
    id: "civicboom", from: 1908, to: 1930, name: "Civic Monuments & the 1920s Boom",
    tagline: "From 21,550 to 42,017 residents in twenty years",
    palette: ["#e5d5bc", "#8a5a3a"],
    story: [
      "Between 1908 and 1930 Montclair built the institutions that still define its skyline: the New Jersey State Normal School opened College Hall in 1908; Lackawanna Terminal opened in 1913 (designed by Titanic victim William Hull Botsford); the Montclair Art Museum opened in 1914 as New Jersey's first public art museum; Bertram Goodhue's First Congregational Church rose by 1920; and the Wellmont Theater opened in 1922.",
      "The population nearly doubled from 21,550 in 1910 to 42,017 in 1930. Developers built out Oakcroft, Marlboro Park, Watchung Plaza and Upper Montclair with Tudor, Colonial Revival and Craftsman homes, while Presby Memorial Iris Gardens bloomed on Upper Mountain Avenue in 1927.",
      "In 1920 the segregated Montclair–North Essex YWCA—founded in 1912 by Alice Hooe Foster—bought the 1796 Israel Crane House as a residence and center for Black women and girls. In September 1930 Thomas Edison drove the inaugural electric train on the Lackawanna's Montclair Branch."
    ],
    sources: ["wiki", "msuWiki", "nrLackawanna", "mamHist", "wellmontWiki", "mhcCrane", "boontonWiki"]
  },
  {
    id: "midcentury", from: 1931, to: 1964, name: "Depression, War & Full Buildout",
    tagline: "Brookdale Park, Overseas Neighbors and a built-out town",
    palette: ["#cfdbe2", "#3e5968"],
    story: [
      "During the Great Depression, WPA and ERA crews finished the Olmsted Brothers' Brookdale Park on Montclair's northeastern edge in 1937. Population dipped slightly in 1940 before climbing to 43,927 by 1950—nearly full buildout of the town's 6.2 square miles.",
      "Not all mid-century chapters were proud ones: in 1933 the Board of Education redrew attendance lines to concentrate Black students at Glenfield School, sparking a parent boycott led by Mary Allen and decades of organizing by the Montclair NAACP (founded 1913).",
      "After World War II, Montclair residents launched \"Overseas Neighbors\" in 1949 to aid war-torn Graz, Austria—establishing a formal sister-city partnership in 1950 that endures today. In 1955 Montclair Public Library moved into a modern building on South Fullerton Avenue, and in 1958 Montclair State Teachers College became Montclair State College."
    ],
    sources: ["essexBrook", "podMagnet", "msuWiki", "wiki"]
  },
  {
    id: "preservation", from: 1965, to: 1995, name: "Preservation & the Magnet Model",
    tagline: "Moving the Crane House, integrating the schools, saving landmarks",
    palette: ["#e2e6d6", "#3b3b4a"],
    story: [
      "On August 25, 1965, grassroots preservationists rolled the 1796 Israel Crane House one mile from 159 Glenridge Avenue to 110 Orange Road to save it from demolition, founding what is now the Montclair History Center. Montclair opened a new Municipal Building at 205 Claremont Avenue in 1969, and its population reached a 20th-century peak of 44,043 in 1970.",
      "Following court battles and mandatory busing in 1972, Montclair launched a pioneering voluntary magnet school system in September 1977—turning school choice into a nationally studied model of racial integration.",
      "In 1980 voters reclassified Montclair from a Town back to a Township for federal revenue-sharing equity (and adopted the Council–Manager Faulkner Act in 1988). Rail service left Lackawanna Terminal for Bay Street in 1981, dozens of Montclair buildings joined the National Register in 1984–1988, and Montclair State earned university status in 1994."
    ],
    sources: ["mhcCrane", "mpsMagnet", "podMagnet", "wiki", "nrLackawanna", "nrhpMps", "msuWiki"]
  },
  {
    id: "today", from: 1996, to: 2026, name: "Midtown Direct & Cultural Hub",
    tagline: "The Montclair Connection, film festivals and living history",
    palette: ["#e2eedb", "#2d4a32"],
    story: [
      "On September 30, 2002, NJ Transit opened the Montclair Connection, linking the former Lackawanna and Erie lines into a single Montclair–Boonton Line with Midtown Direct trains straight to New York Penn Station. A new Montclair State University station opened in 2004, and after a 2006 fire destroyed Upper Montclair's 1892 depot, a faithful stone replica reopened in 2010.",
      "Montclair's arts and dining renaissance accelerated: the Montclair Art Museum doubled in size in 2001, the Wellmont Theater reopened as a premier live concert venue in 2008, and the Montclair Film Festival launched in 2012.",
      "History remained urgent: Essex County partnered to preserve Presby Memorial Iris Gardens in 2009, the Montclair History Center expanded the Crane House story in 2014 to center its 45 years as a Black YWCA, and community advocates rescued the c. 1780 James Howe House on Claremont Avenue in 2022–2023. By 2025 Montclair's population was estimated at 44,633."
    ],
    sources: ["boontonWiki", "upperMcWiki", "mamHist", "wellmontWiki", "essexPresby", "howeFriends", "wiki"]
  }
];
MW.eraFor = y => MW.eras.find(e => y >= e.from && y <= e.to) || MW.eras[MW.eras.length - 1];

/* --------------------------------------------------------------------------
   Places & events. All 16 landmarks are flagged `landmark: true`.
   `scope: "township"` marks Bloomfield-era places outside modern Montclair
   (shown only while shared, 1812–1867).
   -------------------------------------------------------------------------- */
MW.places = [
  { id: "lenape-ridge", year: 1500, title: "First Watchung Mountain & Lenape Trails", kind: "nature", address: "First Watchung Mountain ridge",
    lat: 40.8220, lon: -74.2280,
    text: "Before colonial deeds, the basalt crest of First Watchung Mountain and the valley brooks below belonged to Lenapehoking. Local histories note that Bloomfield Avenue and Speertown's valleys followed older Lenape footpaths.",
    sources: ["wiki", "essexBrook", "hpElement"] },
  { id: "crane-grant", year: 1694, title: "Azariah Crane Settlement (Cranetown)", kind: "house", address: "55 Myrtle Avenue & Orange Road (approx.)",
    lat: 40.8132, lon: -74.2236,
    text: "Jasper Crane surveyed the Newark Mountain slope in 1675 and willed 300 acres to his sons. In 1694 Azariah Crane built one of the first colonial homes here near Orange Road, anchoring the hamlet long called Cranetown.",
    sources: ["mhcCrane", "hpElement"] },
  { id: "speertown", year: 1700, title: "Speertown Dutch Farming Settlement", kind: "house", address: "Valley Road north of Watchung Avenue",
    lat: 40.8445, lon: -74.2072,
    text: "Dutch settlers from Hackensack and Acquackanonk—led by the Speer, Van Giesen and Sigler families—cleared farms north of Watchung Avenue along Speertown Road (today's Valley Road). The area kept its rural character until the 1873 railroad.",
    sources: ["hpElement", "whittemore"] },
  { id: "howe-house", year: 1780, title: "James Howe House", kind: "house", address: "369 Claremont Avenue",
    lat: 40.82292, lon: -74.22468,
    text: "Built around 1780. James Howe, formerly enslaved by Nathaniel Crane and manumitted in 1817, inherited this house, six acres and $400 under Crane's 1831 will—becoming the first documented African American homeowner in Montclair. Community preservationists saved it from demolition in 2022–2023.",
    sources: ["howeFriends"] },
  { id: "crane-house", year: 1796, title: "Israel Crane House & Historic YWCA", kind: "house", address: "110 Orange Road (moved from 159 Glenridge Ave in 1965)",
    lat: 40.81158, lon: -74.22279, landmark: true,
    text: "Federal mansion built in 1796 by turnpike builder Israel Crane on Old Road (159 Glenridge Ave), where at least five enslaved people lived and worked. From 1920 to 1965 it served as the Montclair–North Essex YWCA for Black women and girls before preservationists rolled it one mile to Orange Road in 1965.",
    sources: ["mhcCrane", "craneWiki", "nrCrane"] },
  { id: "turnpike", year: 1806, title: "Newark–Pompton Turnpike (Bloomfield Avenue)", kind: "transport", address: "Bloomfield Avenue",
    lat: 40.8151, lon: -74.2191,
    text: "Championed by Israel Crane, the Newark–Pompton Turnpike climbed the Watchung gap along today's Bloomfield Avenue, linking Newark to northern New Jersey and turning Cranetown into a busy toll-road crossroads.",
    sources: ["hpElement", "craneWiki"] },
  { id: "bloomfield-twp", year: 1812, end: 1867, scope: "township", title: "Bloomfield Township Green (Shared Seat)", kind: "civic", address: "Bloomfield Town Green, Bloomfield",
    lat: 40.79689, lon: -74.19689,
    text: "When Bloomfield Township separated from Newark on March 23, 1812, Cranetown and Speertown became its western hills (\"West Bloomfield\"). Township governance centered on Bloomfield Green until Montclair broke away in 1868.",
    sources: ["bloomWiki", "whittemore"] },
  { id: "nathaniel-crane", year: 1818, title: "Nathaniel Crane House", kind: "house", address: "110 Orange Road",
    lat: 40.81140, lon: -74.22260,
    text: "Built in 1818 by Captain Nathaniel Crane Jr., Israel Crane's cousin, on original Jasper Crane family land. Donated in 1974 and moved 75 feet south to join the Montclair History Center campus, where it houses a 19th-century general store and schoolroom exhibit.",
    sources: ["mhcWiki"] },
  { id: "dlw-1856", year: 1856, title: "Newark & Bloomfield Railroad Arrives", kind: "transport", address: "Lackawanna Plaza & Bloomfield Avenue",
    lat: 40.8112, lon: -74.2122,
    text: "Montclair's first railroad reached West Bloomfield in 1856 (later leased by the Delaware, Lackawanna & Western), connecting the mountain villages to Newark and New York ferries and sparking commuter growth.",
    sources: ["wiki", "boontonWiki"] },
  { id: "central-school", year: 1860, title: "Central School & Early Montclair High", kind: "civic", address: "22 Valley Road (Church Street & Valley Road)",
    lat: 40.8152, lon: -74.2212,
    text: "Montclair's primary and grammar school opened here in late 1860 (today's Board of Education offices). A high school division formed in 1866 and graduated its first class of 13 students in June 1874; the school system won honors at the 1876 Philadelphia Centennial Exposition.",
    sources: ["mhcSpaulding"] },
  { id: "name-montclair", year: 1860, title: "West Bloomfield Adopts the Name \"Montclair\"", kind: "event", address: "Montclair Center",
    lat: 40.8142, lon: -74.2175,
    text: "Residents chose \"Montclair\" (from the French mont clair, \"clear mountain\") in 1860 to distinguish the growing commuter village from Bloomfield and celebrate its views from First Watchung Mountain.",
    sources: ["wiki", "whittemore"] },
  { id: "montclair-twp", year: 1868, title: "Montclair Township Incorporated", kind: "event", address: "Township-wide",
    lat: 40.8165, lon: -74.2165,
    text: "On April 15, 1868 Montclair separated from Bloomfield Township so residents could bond and build a second rail line—the Montclair Railway—north through Upper Montclair.",
    sources: ["wiki", "whittemore"] },
  { id: "van-reyper-bond", year: 1872, title: "Van Reyper-Bond House", kind: "house", address: "848 Valley Road",
    lat: 40.85589, lon: -74.19883, landmark: true,
    text: "Italianate farmhouse built in 1872 by Thomas C. Van Reyper, whose wife Caroline Speer descended from Speertown's founding Dutch settlers. Now preserved on the campus of Montclair State University; added to the National Register in 1979.",
    sources: ["bondWiki", "nrBond"] },
  { id: "erie-1873", year: 1873, title: "Montclair Railway Opens North to Speertown", kind: "transport", address: "Walnut Street station & corridor",
    lat: 40.81701, lon: -74.20969,
    text: "Opened January 1, 1873 (soon absorbed as the Erie's New York & Greenwood Lake Railway), cutting north through Walnut Street, Park Street (Watchung Ave), Upper Montclair and Montclair Heights and turning rural Speertown into commuter neighborhoods.",
    sources: ["watchungWiki", "heightsWiki", "hpElement"] },
  { id: "heights-station", year: 1874, title: "Montclair Heights Station", kind: "transport", address: "Normal Avenue & Valley Road",
    lat: 40.85762, lon: -74.20258,
    text: "Opened around 1874 near Mount Hebron Road on the Montclair Railway and relocated to Normal Avenue by the Erie Railroad in 1905. After its 1905 depot burned in 1970, modern platforms were rebuilt in 1998.",
    sources: ["heightsWiki"] },
  { id: "pine-street", year: 1880, title: "Pine Street Historic District", kind: "house", address: "Pine Street & Glenridge Avenue",
    lat: 40.81104, lon: -74.20826, landmark: true,
    text: "Dense working-class neighborhood of three- and four-story Classical Revival and Italianate brick buildings constructed from the 1880s through the 1930s near the Lackawanna freight yards—historically home to Italian American and African American families.",
    sources: ["pineWiki", "hpElement"] },
  { id: "inness-studio", year: 1885, end: 1894, title: "George Inness Home & Studio", kind: "culture", address: "190 Grove Street",
    lat: 40.81973, lon: -74.20368,
    text: "Celebrated American landscape painter George Inness lived and painted in Montclair from 1885 until his death in 1894, making the town a magnet for painters and sculptors and inspiring the creation of the Montclair Art Museum.",
    sources: ["mamHist", "nrhpMps"] },
  { id: "central-pres", year: 1886, title: "Central Presbyterian Church", kind: "culture", address: "46 Park Street",
    lat: 40.81723, lon: -74.21718,
    text: "Landmark downtown sanctuary on Park Street (added to the National Register in 1986), part of Montclair's remarkable turn-of-the-century concentration of high-style churches designed by leading American architects.",
    sources: ["nrhpMps", "wiki"] },
  { id: "upper-montclair-station", year: 1892, title: "Upper Montclair Station", kind: "transport", address: "275 Bellevue Avenue",
    lat: 40.84208, lon: -74.20951, landmark: true,
    text: "Service began in 1873; the Erie Railroad built its beloved Richardsonian Romanesque stone depot in 1892 next to Bellevue Avenue and Anderson Park. After a 2006 fire destroyed much of the depot, NJ Transit and local partners reopened a faithful stone reconstruction in June 2010.",
    sources: ["upperMcWiki", "boontonWiki"] },
  { id: "mhs-1893", year: 1893, end: 1935, title: "First Stand-Alone Montclair High School (site)", kind: "civic", address: "Orange Road near Hillside Avenue",
    lat: 40.8138, lon: -74.2225,
    text: "Designed by Boston architects Loring & Phipps and opened in September 1893 as Montclair's first dedicated high school building. Later repurposed as Spaulding Elementary School and demolished in the mid-1930s.",
    sources: ["mhcSpaulding"] },
  { id: "town-1894", year: 1894, title: "Town of Montclair Incorporated", kind: "event", address: "Town-wide",
    lat: 40.8155, lon: -74.2185,
    text: "Following a referendum on February 21, 1894, Montclair reincorporated three days later as the Town of Montclair—replacing its township committee with a Town Council.",
    sources: ["wiki"] },
  { id: "clark-house", year: 1894, title: "James Henry Clark House", kind: "house", address: "108 Orange Road",
    lat: 40.81178, lon: -74.22285,
    text: "Queen Anne house built in 1894 for Dr. James Henry Clark Jr. and Carrie Schenck on original Crane family land. Purchased by the Montclair Historical Society in 1985, it now houses the Montclair History Center offices and Albert Payson Terhune Library.",
    sources: ["mhcWiki"] },
  { id: "shultz-house", year: 1896, title: "Charles S. Shultz House (\"Evergreens\")", kind: "house", address: "30 North Mountain Avenue",
    lat: 40.82118, lon: -74.22311, landmark: true,
    text: "Built in 1896 for Hoboken banker Charles S. Shultz by architect Michel LeBrun (co-designer of Manhattan's Metropolitan Life Tower), featuring a fire-resistant masonry first floor, early gas-and-electric lighting and a home elevator. Added to the National Register in 1979.",
    sources: ["shultzWiki", "nrShultz"] },
  { id: "walther-house", year: 1898, title: "Walther House", kind: "house", address: "474 Upper Mountain Avenue",
    lat: 40.85050, lon: -74.20595,
    text: "Queen Anne/Colonial Revival residence built in 1898 on Upper Mountain Avenue. Longtime home of Barbara Walther, who curated the adjacent Presby Memorial Iris Gardens for over 50 years; purchased in 1977 as the gardens' headquarters.",
    sources: ["presbySite", "essexPresby"] },
  { id: "cliffside-hose", year: 1901, title: "Cliffside Hose Company No. 4", kind: "civic", address: "588 Valley Road",
    lat: 40.84053, lon: -74.20811, landmark: true,
    text: "Built in 1901 to protect Upper Montclair and Montclair's rapidly growing north end. Still an active firehouse serving Montclair Fire Department Engine 2 and Truck 2; added to the National Register on July 1, 1988.",
    sources: ["cliffsideWiki", "hpElement"] },
  { id: "anderson-park", year: 1903, title: "Anderson Park", kind: "nature", address: "274 Bellevue Avenue",
    lat: 40.84152, lon: -74.21065, landmark: true,
    text: "14.85-acre Essex County neighborhood park donated in 1903 by Charles W. Anderson and designed by Olmsted Brothers (John Charles Olmsted and Frederick Law Olmsted Jr.). Called Montclair Park until 1909; added to the National Register in 2009.",
    sources: ["nrAnderson", "andersonFriends", "andersonWiki"] },
  { id: "carnegie-library", year: 1904, title: "Montclair Carnegie Library", kind: "civic", address: "73 Church Street",
    lat: 40.81498, lon: -74.22114, landmark: true,
    text: "Designed in 1902–1904 by architect John Galen Howard (founder of UC Berkeley's School of Architecture) with an Andrew Carnegie grant. Served as Montclair's main public library until 1955; added to the National Register in 1988.",
    sources: ["howardWiki", "nrCarnegie"] },
  { id: "old-townhall", year: 1904, title: "Municipal Building & Police HQ", kind: "civic", address: "647 Bloomfield Avenue",
    lat: 40.81477, lon: -74.21868,
    text: "Built in 1904 on Bloomfield Avenue to house Montclair's municipal government and public safety offices. Remains Montclair's Police Headquarters and Municipal Court.",
    sources: ["hpElement"] },
  { id: "watchung-station", year: 1904, title: "Watchung Avenue Station", kind: "transport", address: "106 Watchung Avenue",
    lat: 40.82951, lon: -74.20699, landmark: true,
    text: "Opened January 1, 1873 as Park Street on the Montclair Railway; the Erie Railroad built this elevated timber depot above Watchung Avenue in 1904 and renamed it Watchung Avenue in 1919. Added to the National Register in 1984.",
    sources: ["watchungWiki"] },
  { id: "edgemont-park", year: 1906, title: "Edgemont Memorial Park", kind: "nature", address: "274 Valley Road",
    lat: 40.83070, lon: -74.21254,
    text: "Purchased in 1906 via a $100,000 town bond issue led by William B. Dickson on a former golf course (the Harrison Tract), landscaped by Olmsted Brothers around a dammed pond on Toney's Brook. Charles Keck's World War I memorial obelisk was dedicated on the island on November 11, 1925.",
    sources: ["edgemontWiki", "mhcWwi"] },
  { id: "oakcroft-sub", year: 1907, title: "Oakcroft Residential Park", kind: "house", address: "Godfrey Road & Princeton Place",
    lat: 40.8386, lon: -74.2098,
    text: "Subdivision laid out starting in 1907 south of Anderson Park by Aaron W. Godfrey's Godfrey Land & Building Co., adding 72 Craftsman, Colonial and Tudor homes by 1926—including 25 Princeton Place, childhood home of Apollo 11 astronaut Buzz Aldrin.",
    sources: ["oakcroft"] },
  { id: "normal-school", year: 1908, title: "Montclair State Normal School (College Hall)", kind: "culture", address: "1 Normal Avenue",
    lat: 40.85836, lon: -74.19945, landmark: true,
    text: "Opened September 28, 1908 as the New Jersey State Normal School at Montclair in its signature Spanish Colonial Revival College Hall. Evolved into Montclair State Teachers College (1927), Montclair State College (1958) and Montclair State University (1994).",
    sources: ["msuWiki"] },
  { id: "glenfield-park", year: 1910, title: "Glenfield Park", kind: "nature", address: "Maple Avenue & Bloomfield Avenue",
    lat: 40.80424, lon: -74.21110,
    text: "Twenty-acre park in southeastern Montclair donated by the town to the Essex County Park System in 1910 and designed by the Olmsted Brothers.",
    sources: ["glenfieldWiki", "hpElement"] },
  { id: "st-marks", year: 1912, title: "Montclair YWCA & Black Civic Organizing", kind: "culture", address: "51 Elm Street & Glenridge Avenue",
    lat: 40.80814, lon: -74.21474,
    text: "Alice Hooe Foster—the first African American woman to graduate from Montclair High School—founded the Montclair YWCA for Black women in 1912; the Montclair branch of the NAACP followed in 1913, anchoring a century of civil rights activism.",
    sources: ["mhcCrane", "podMagnet"] },
  { id: "lackawanna-terminal", year: 1913, title: "Lackawanna Railroad Terminal", kind: "transport", address: "1 Lackawanna Plaza",
    lat: 40.81103, lon: -74.21258, landmark: true,
    text: "Opened June 28, 1913 as the Grecian-Doric brick-and-concrete western terminus of the DL&W Montclair Branch, designed by William Hull Botsford—who died aboard the Titanic in 1912. Added to the National Register in 1973; closed to trains in 1981 and adapted into Lackawanna Plaza.",
    sources: ["nrLackawanna", "boontonWiki"] },
  { id: "bellevue-branch", year: 1914, title: "Bellevue Avenue Branch Library", kind: "civic", address: "185 Bellevue Avenue",
    lat: 40.84073, lon: -74.20457,
    text: "Built in 1914 with Carnegie funds to serve Upper Montclair's growing village center. Added to the National Register of Historic Places in 1988.",
    sources: ["hpElement", "nrhpMps"] },
  { id: "montclair-art-museum", year: 1914, title: "Montclair Art Museum", kind: "culture", address: "3 South Mountain Avenue",
    lat: 40.81860, lon: -74.22424, landmark: true,
    text: "Opened January 15, 1914 as New Jersey's first public museum dedicated solely to art, founded with gifts from William T. Evans and Florence Rand Lang in a Neoclassical building by Albert Randolph Ross. Renowned for its George Inness gallery and Native North American art collection; NRHP 1986.",
    sources: ["mamWiki", "mamHist"] },
  { id: "mhs-1915", year: 1915, title: "Montclair High School (Chestnut Street)", kind: "civic", address: "100 Chestnut Street",
    lat: 40.82324, lon: -74.21284,
    text: "Montclair High School moved into its stately Georgian Revival main building on Chestnut Street in 1915, succeeding the 1893 Orange Road high school.",
    sources: ["mhcSpaulding"] },
  { id: "van-vleck", year: 1916, title: "Van Vleck House & Gardens", kind: "house", address: "21 Van Vleck Street",
    lat: 40.82439, lon: -74.22140,
    text: "Mediterranean/Italianate estate mansion built in 1916 for Joseph Van Vleck Jr., celebrated for its nearly six acres of formal gardens, rhododendrons and century-old wisteria vines. Gifted to The Montclair Foundation and open to the public.",
    sources: ["vanVleckWiki"] },
  { id: "gilbreth-house", year: 1919, end: 1942, title: "Gilbreth House (\"Cheaper by the Dozen\")", kind: "house", address: "68 Eagle Rock Way",
    lat: 40.80274, lon: -74.22820,
    text: "Home of industrial engineering pioneers Frank B. and Lillian Moller Gilbreth and their twelve children—immortalized in the 1948 memoir Cheaper by the Dozen. City directories list Lillian M. Gilbreth at 68 Eagle Rock Way into the 1930s (and at 30 The Crescent by 1949).",
    sources: ["directories", "wiki"] },
  { id: "first-congregational", year: 1920, title: "First Congregational Church", kind: "culture", address: "40–42 South Fullerton Avenue",
    lat: 40.81246, lon: -74.21816, landmark: true,
    text: "Congregation founded in 1870; after fire destroyed its earlier church in 1914, architect Bertram Grosvenor Goodhue designed this soaring Perpendicular Gothic stone sanctuary (completed 1916–1920). Added to the National Register on July 1, 1988.",
    sources: ["congWiki", "nrhpMps"] },
  { id: "wellmont-theater", year: 1922, title: "Wellmont Theater", kind: "culture", address: "5 Seymour Street",
    lat: 40.81266, lon: -74.21665, landmark: true,
    text: "Designed by Reilly & Hall and opened June 16, 1922 as a live vaudeville and theater palace before converting to movies in 1929. Restored in 2008 as a major live-music venue and flagship home of the Montclair Film Festival.",
    sources: ["wellmontWiki"] },
  { id: "presby-iris", year: 1927, title: "Presby Memorial Iris Gardens", kind: "nature", address: "474 Upper Mountain Avenue",
    lat: 40.85039, lon: -74.20580, landmark: true,
    text: "Living museum of thousands of iris varieties founded in 1927 to honor American Iris Society co-founder Frank H. Presby and curated for over 50 years by Barbara Walther. Preserved in 2009 through an Essex County–Montclair–Citizens Committee partnership.",
    sources: ["presbyWiki", "presbySite", "essexPresby"] },
  { id: "anchorage", year: 1930, title: "The Anchorage", kind: "house", address: "155 Wildwood Avenue",
    lat: 40.83629, lon: -74.20354, landmark: true,
    text: "Georgian/Colonial Revival mansion designed in 1930 by Montclair architect Francis A. Nelson after Virginia's Westover Plantation, built with James River clay bricks and landscaped by Ralph Hancock. Added to the National Register on July 1, 1988.",
    sources: ["anchorageWiki", "nrAnchorage", "nrhpMps"] },
  { id: "electric-1930", year: 1930, title: "Edison Drives the First Electric Train", kind: "transport", address: "Lackawanna Terminal, 1 Lackawanna Plaza",
    lat: 40.8108, lon: -74.2119,
    text: "In September 1930 the Lackawanna's Montclair Branch became the first electrified suburban commuter line in the region; Thomas Edison himself took the controls for the inaugural electric run.",
    sources: ["boontonWiki"] },
  { id: "school-boycott", year: 1933, title: "School Segregation Redistricting & Parent Boycott", kind: "event", address: "Glenfield School & Nishuane neighborhood",
    lat: 40.8035, lon: -74.2125,
    text: "When the Board of Education redrew attendance lines in 1933 to transfer Black students from mixed Nishuane School into predominantly Black Glenfield School, parent Mary Allen and Black families organized a boycott—an early chapter in Montclair's decades-long fight for school integration.",
    sources: ["podMagnet"] },
  { id: "brookdale-park", year: 1937, title: "Brookdale Park Completed", kind: "nature", address: "Watchung Avenue & Grove Street",
    lat: 40.83421, lon: -74.18881,
    text: "Land purchases began in 1928 on the historic Stonehouse Plains farms; designed by the Olmsted Brothers and completed by WPA and ERA crews in 1937 (121 acres straddling Montclair and Bloomfield, with a Rose Garden added in 1959).",
    sources: ["essexBrook"] },
  { id: "graz-1950", year: 1950, title: "Overseas Neighbors & Sister City Graz", kind: "event", address: "Town-wide (Montclair–Graz)",
    lat: 40.8160, lon: -74.2170,
    text: "Born out of postwar relief packages sent to war-damaged Graz, Austria (including medical equipment from Mountainside Hospital), Montclair's Overseas Neighbors formalized one of America's earliest municipal sister-city partnerships in April 1950.",
    sources: ["wiki"] },
  { id: "mpl-1955", year: 1955, title: "Montclair Public Library (South Fullerton)", kind: "civic", address: "50 South Fullerton Avenue",
    lat: 40.81172, lon: -74.21837,
    text: "Montclair Public Library moved from the 1904 Church Street Carnegie building into a modern main library on South Fullerton Avenue in 1955, housing one of northern New Jersey's deepest local-history collections.",
    sources: ["mplLocal", "wiki"] },
  { id: "muni-1969", year: 1969, title: "New Municipal Building Opens", kind: "civic", address: "205 Claremont Avenue",
    lat: 40.81732, lon: -74.21541,
    text: "Montclair relocated its main municipal administration from 647 Bloomfield Avenue into a new office-style Town Hall at 205 Claremont Avenue in 1969.",
    sources: ["wiki", "hpc"] },
  { id: "magnet-1977", year: 1977, title: "Voluntary Magnet School System Launches", kind: "event", address: "District-wide (22 Valley Road)",
    lat: 40.8154, lon: -74.2206,
    text: "Following the 1966 Rice v. Montclair Board of Education suit and 1972 mandatory busing, Montclair launched its voluntary magnet school system in September 1977—expanding districtwide by 1979 into a national model for integrated public education.",
    sources: ["mpsMagnet", "podMagnet"] },
  { id: "twp-1980", year: 1980, title: "Reclassified as Township of Montclair", kind: "event", address: "Township-wide",
    lat: 40.8180, lon: -74.2150,
    text: "In 1980 Montclair voters approved a referendum changing the municipality back from a Town to a Township to qualify for equitable federal revenue sharing. In 1988 Montclair adopted the Council–Manager Faulkner Act form of government.",
    sources: ["wiki"] },
  { id: "bay-street", year: 1981, title: "Bay Street Station Replaces Lackawanna Terminal", kind: "transport", address: "Bay Street & Pine Street",
    lat: 40.80819, lon: -74.20874,
    text: "On March 2, 1981 rail service ended at the 1913 Lackawanna Terminal and shifted east to Bay Street station, setting the stage for the future Montclair Connection.",
    sources: ["nrLackawanna", "boontonWiki"] },
  { id: "connection-2002", year: 2002, title: "Montclair Connection & Midtown Direct Open", kind: "transport", address: "Bay Street to Walnut Street junction",
    lat: 40.8125, lon: -74.2090,
    text: "On September 30, 2002 NJ Transit opened the long-awaited Montclair Connection, joining the former Lackawanna Montclair Branch and Erie Boonton Line into one electrified Midtown Direct corridor to New York Penn Station.",
    sources: ["boontonWiki", "watchungWiki"] },
  { id: "film-2012", year: 2012, title: "First Montclair Film Festival", kind: "culture", address: "5 Seymour Street (Wellmont Theater) & Bloomfield Avenue",
    lat: 40.8130, lon: -74.2162,
    text: "Launched in 2012 with venues anchored by the Wellmont Theater and Clairidge Cinema, turning downtown Montclair into a spring destination for independent film and arts.",
    sources: ["wellmontWiki", "wiki"] }
];
MW.places.sort((a, b) => a.year - b.year);
MW.localPlaces = () => MW.places.filter(p => p.scope !== "township");

/* --------------------------------------------------------------------------
   Montclair neighborhoods. Assignment on house.html is by nearest center.
   -------------------------------------------------------------------------- */
MW.sections = [
  { id: "southend", name: "the South End", lat: 40.7995, lon: -74.2195,
    colonial: "This was southern Cranetown, where early farms followed Orange Road and Cedar Avenue toward the Orange line. By the late 1800s Black and working-class families built a close-knit community here around Nishuane Park and Orange Road.",
    growth: "Residential streets filled in between 1890 and 1930 with two-family homes, Queen Anne cottages and Colonial Revivals, centered on the South End business district at Orange Road and Cedar Avenue.",
    sources: ["wiki", "hpElement", "podMagnet"] },
  { id: "pinestreet", name: "Pine Street & Bay Street", lat: 40.8098, lon: -74.2088,
    colonial: "Lying just east of the 1856 railroad yards and freight sidings along Glenridge Avenue, this flat ground turned early from orchards into workers' housing and small factories.",
    growth: "Between the 1880s and 1930s Italian American and African American families built three- and four-story brick tenements, storefronts and churches along Pine, Bay, Grant and Sherman streets—now recognized on the National Register as the Pine Street Historic District.",
    sources: ["pineWiki", "hpElement"] },
  { id: "center", name: "Montclair Center (old Cranetown)", lat: 40.8145, lon: -74.2180,
    colonial: "This is the heart of old Cranetown, where Azariah Crane settled in 1694, Israel Crane built his 1796 mansion on Old Road (Glenridge Avenue) and the Newark–Pompton Turnpike climbed the hill.",
    growth: "After the 1856 railroad arrived, Bloomfield Avenue and Church Street became Montclair's commercial spine—anchored by the 1904 Carnegie Library, 1904 Municipal Building, 1913 Lackawanna Terminal, 1920 First Congregational Church and 1922 Wellmont Theater.",
    sources: ["mhcCrane", "hpElement", "wellmontWiki", "nrLackawanna"] },
  { id: "estate", name: "the Estate Section & South Mountain", lat: 40.8095, lon: -74.2280,
    colonial: "Steep wooded slopes rising up First Watchung Mountain west of Orange Road and South Mountain Avenue, quarried for traprock and timbered before suburban roads climbed the ridge.",
    growth: "From the 1880s through the 1920s wealthy New York executives and families built broad-lawned Colonial Revival, Shingle and Tudor estates along South Mountain Avenue, Llewellyn Road, Undercliff Road and Eagle Rock Way (including the Gilbreths' Cheaper by the Dozen home at 68 Eagle Rock Way).",
    sources: ["nrhpMps", "hpElement"] },
  { id: "mountain", name: "the Mountain District & Van Vleck", lat: 40.8245, lon: -74.2215,
    colonial: "The slope along Claremont Avenue and North Mountain Avenue holds some of Montclair's deepest early roots, including the c. 1780 James Howe House at 369 Claremont Avenue.",
    growth: "Turn-of-the-century estates—from Charles S. Shultz's 1896 \"Evergreens\" and the 1914 Montclair Art Museum to the 1916 Van Vleck estate—set the architectural tone along North and Upper Mountain Avenues.",
    sources: ["shultzWiki", "mamWiki", "vanVleckWiki", "howeFriends"] },
  { id: "froghollow", name: "Frog Hollow & Walnut Street", lat: 40.8185, lon: -74.2115,
    colonial: "Low-lying ground along Toney's Brook and the 1873 Montclair Railway corridor, historically known along Valley Road as Frog Hollow and home to early mills, dairies and diverse working-class families.",
    growth: "The Walnut Street station spurred brick commercial blocks, Victorian cottages and two-family homes from the 1880s through the 1920s; George Inness painted nearby on Grove Street from 1885 to 1894.",
    sources: ["wiki", "podMagnet", "mhcAtlas"] },
  { id: "watchung", name: "Watchung Plaza & Marlboro Park", lat: 40.8305, lon: -74.2080,
    colonial: "Once the dividing line between Cranetown to the south and Dutch Speertown to the north, anchored by farms along Valley Road and the Park Street (later Watchung Avenue) rail stop of 1873.",
    growth: "The 1904 elevated Watchung Avenue depot, Edgemont Memorial Park (1906), Oakcroft (1907) and Marlboro Park filled the neighborhood with Tudor shops, Craftsman homes and tree-lined residential blocks before World War II.",
    sources: ["watchungWiki", "edgemontWiki", "oakcroft", "hpElement"] },
  { id: "uppermc", name: "Upper Montclair (old Speertown)", lat: 40.8425, lon: -74.2070,
    colonial: "Settled around 1700 by Dutch farming families along Speertown Road (Valley Road), Speertown remained rural farmland until the Montclair Railway arrived in 1873.",
    growth: "The 1892 Upper Montclair station, Cliffside Hose Co. No. 4 (1901), Olmsted-designed Anderson Park (1903) and Tudor Revival shops along Bellevue Avenue and Valley Road turned Upper Montclair into a village-within-a-town, crowned by Presby Memorial Iris Gardens (1927) and The Anchorage (1930).",
    sources: ["hpElement", "nrAnderson", "upperMcWiki", "presbyWiki", "anchorageWiki"] },
  { id: "heights", name: "Montclair Heights", lat: 40.8555, lon: -74.2015,
    colonial: "The northernmost farms of old Speertown—where Thomas C. Van Reyper and Caroline Speer built their 1872 Italianate farmhouse on Valley Road—bounded by traprock quarries along the ridge.",
    growth: "Transformed by the Montclair Heights rail station (1874/1905) and the opening of the New Jersey State Normal School (now Montclair State University) in 1908, surrounded by 1920s–1950s residential streets.",
    sources: ["bondWiki", "heightsWiki", "msuWiki"] }
];

/* Historic roads & rail corridors (Census TIGERweb geometry clipped to Montclair). */
MW.oldRoads = [
  { name: "Bloomfield Avenue (Newark–Pompton Turnpike, 1806)", from: 1500,
    pts: [[40.82805, -74.23913], [40.82604, -74.23434], [40.82517, -74.22873], [40.82313, -74.22651], [40.81861, -74.22361], [40.81512, -74.21914], [40.81088, -74.21386], [40.80564, -74.20845], [40.8011, -74.20432]] },
  { name: "Valley Road (old Speertown Road, c. 1700)", from: 1700,
    pts: [[40.81503, -74.22136], [40.82012, -74.22111], [40.82407, -74.21886], [40.82817, -74.21585], [40.82916, -74.21258], [40.83426, -74.20728], [40.8387, -74.20759], [40.84253, -74.20812], [40.84639, -74.2057], [40.85015, -74.2029], [40.85453, -74.19968], [40.85728, -74.19773], [40.86163, -74.19471]] },
  { name: "Orange Road (old Cranetown road, 1694)", from: 1694,
    pts: [[40.7885, -74.2189], [40.79216, -74.219], [40.79608, -74.21875], [40.80172, -74.21876], [40.80649, -74.22021], [40.81064, -74.22266], [40.81242, -74.22273], [40.81783, -74.22263]] },
  { name: "Claremont Avenue (by 1780)", from: 1780,
    pts: [[40.82911, -74.23544], [40.82772, -74.23207], [40.82505, -74.22791], [40.82034, -74.22107], [40.81715, -74.2158], [40.8146, -74.21145], [40.81284, -74.20839], [40.81232, -74.20601]] },
  { name: "Mountain & Upper Mountain Avenue (ridge road)", from: 1850,
    pts: [[40.80208, -74.23352], [40.80865, -74.23021], [40.81573, -74.22681], [40.81924, -74.22442], [40.8241, -74.22058], [40.82964, -74.21649], [40.83591, -74.2131], [40.84188, -74.21197], [40.84616, -74.20858], [40.85074, -74.2053], [40.85852, -74.20389]] },
  { name: "Watchung Avenue (Cranetown–Speertown line)", from: 1850,
    pts: [[40.83492, -74.21532], [40.83256, -74.21073], [40.83062, -74.20605], [40.82993, -74.20258], [40.82934, -74.19961], [40.82805, -74.19353], [40.8286, -74.18757]] },
  { name: "Grove Street", from: 1856,
    pts: [[40.81007, -74.213], [40.81509, -74.20806], [40.81965, -74.20361], [40.82564, -74.20002], [40.83066, -74.19753], [40.8385, -74.19558], [40.8473, -74.1943], [40.85407, -74.19234], [40.86026, -74.18744]] },
  { name: "the Lackawanna Montclair Branch (1856)", from: 1856,
    pts: [[40.8030, -74.2040], [40.80819, -74.20874], [40.81103, -74.21258]] },
  { name: "the Montclair Railway / Erie Line (1873)", from: 1873,
    pts: [[40.80819, -74.20874], [40.81701, -74.20969], [40.82951, -74.20699], [40.84211, -74.20940], [40.84884, -74.20547], [40.85762, -74.20258]] }
];

/* Architectural styles common in Montclair (Historic Preservation Plan Element & NRHP MPS). */
MW.styles = [
  { id: "colonial", name: "Colonial & Federal Farmhouse", from: 1690, to: 1835, desc: "Timber-frame and stone farmhouses of Cranetown and Speertown, from the c. 1780 James Howe House to the 1796 Israel Crane House." },
  { id: "cottage", name: "Greek Revival & Early Victorian", from: 1836, to: 1867, desc: "Columned Greek Revivals, Gothic cottages and early commuter villas built as the first railroad reached West Bloomfield." },
  { id: "secondempire", name: "Italianate & Second Empire", from: 1868, to: 1884, desc: "Bracketed eaves, tall windows and mansard roofs from the early years of independent Montclair, like the 1872 Van Reyper-Bond House." },
  { id: "queenanne", name: "Queen Anne & Shingle Style", from: 1885, to: 1904, desc: "Asymmetrical gables, wraparound porches, turrets and stone bases—seen on Clark House (1894), Shultz House (1896) and Mountain Avenue." },
  { id: "colrev", name: "Colonial Revival & Craftsman", from: 1905, to: 1919, desc: "Symmetrical Colonial Revivals, American Foursquares and Arts-and-Crafts bungalows filling Oakcroft, Marlboro Park and Upper Montclair." },
  { id: "tudor", name: "Tudor & Georgian Revival", from: 1920, to: 1940, desc: "Half-timbered Tudors, brick Georgians like The Anchorage (1930) and refined brick apartment blocks from Montclair's interwar boom." },
  { id: "ranch", name: "Postwar Cape, Ranch & Split-Level", from: 1941, to: 1969, desc: "Mid-century infill homes on remaining northern and hillside tracts as Montclair reached full buildout." },
  { id: "modern", name: "Contemporary & Transit-Oriented", from: 1970, to: 2100, desc: "Modern infill residences and mixed-use buildings rising around Bloomfield Avenue, Bay Street and Montclair's rail stations." }
];
MW.styleFor = y => MW.styles.find(s => y >= s.from && y <= s.to) || MW.styles[MW.styles.length - 1];

/* Geography helpers */
MW.geo = {
  distM(a, b) {
    const R = 6371000, toR = Math.PI / 180;
    const dLat = (b[0] - a[0]) * toR, dLon = (b[1] - a[1]) * toR;
    const s = Math.sin(dLat / 2) ** 2 + Math.cos(a[0] * toR) * Math.cos(b[0] * toR) * Math.sin(dLon / 2) ** 2;
    return 2 * R * Math.asin(Math.sqrt(s));
  },
  distToLineM(p, pts) {
    const k = 111320, kx = k * Math.cos(p[0] * Math.PI / 180);
    const Q = pts.map(q => [(q[1] - p[1]) * kx, (q[0] - p[0]) * k]);
    let best = Infinity;
    for (let i = 0; i < Q.length - 1; i++) {
      const [ax, ay] = Q[i], [bx, by] = Q[i + 1];
      const dx = bx - ax, dy = by - ay;
      const t = Math.max(0, Math.min(1, (-ax * dx - ay * dy) / (dx * dx + dy * dy || 1)));
      best = Math.min(best, Math.hypot(ax + t * dx, ay + t * dy));
    }
    return best;
  },
  inPolygon(p, poly) {
    if (!poly) return true;
    const rings = poly.type === "MultiPolygon" ? poly.coordinates.map(r => r[0]) : [poly.coordinates[0]];
    return rings.some(r => {
      let inside = false;
      for (let i = 0, j = r.length - 1; i < r.length; j = i++) {
        const [xi, yi] = r[i], [xj, yj] = r[j];
        if ((yi > p[0]) !== (yj > p[0]) && p[1] < (xj - xi) * (p[0] - yi) / (yj - yi) + xi) inside = !inside;
      }
      return inside;
    });
  },
  inTown(p) { return MW.geo.inPolygon(p, window.MW_BOUNDARY); },
  fmt(m) {
    const mi = m / 1609.34;
    if (mi < 0.1) return Math.round(m * 3.281 / 10) * 10 + " feet";
    return mi.toFixed(mi < 1 ? 2 : 1) + " miles";
  },
  walkMin(m) { return Math.max(1, Math.round(m / 80)); }
};
