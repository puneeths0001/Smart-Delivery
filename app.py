import math, random, datetime as dt
import numpy as np, requests, streamlit as st, folium, qrcode, cv2
from PIL import Image, ImageDraw
from streamlit_folium import st_folium

st.set_page_config(page_title="Smart Delivery", page_icon="🛵", layout="wide")

# ───────────────────────── Claymorphism styling ─────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"], .stApp {font-family:'Inter',sans-serif; color:#14110f;}
.stApp {background:radial-gradient(900px 600px at 90% -5%, #ffe2cd, transparent 60%), radial-gradient(700px 500px at 0% 100%, #ffffff, transparent 70%), #f7f1ec;}
[data-testid="stToolbar"], footer, #MainMenu {display:none;}
header {background:transparent;}
.block-container {padding-top:2rem; max-width:1200px;}
@keyframes up {from{opacity:0;transform:translateY(28px) scale(.97)}to{opacity:1;transform:none}}
@keyframes bob {0%,100%{transform:translateY(0)}50%{transform:translateY(-14px)}}
@keyframes grow {from{transform:scaleY(.05)}to{transform:scaleY(1)}}
.clay {position:relative;border-radius:26px;padding:22px 26px;margin:7px 0;background:#fff;border:1px solid #f0e6dc;box-shadow:0 10px 30px rgba(120,80,40,.08);
 animation:up .8s cubic-bezier(.2,.9,.3,1) both; transition:transform .45s cubic-bezier(.2,.9,.3,1), box-shadow .45s, border-color .45s;}
.clay:hover {transform:translateY(-8px) scale(1.02);border-color:#ff6a1a;box-shadow:0 24px 50px rgba(255,106,26,.22);}
.c0{background:linear-gradient(145deg,#fff6e0,#fff)} .c1{background:linear-gradient(145deg,#e9f5ff,#fff)}
.c2{background:linear-gradient(145deg,#ffe9e2,#fff)} .c3{background:linear-gradient(145deg,#fff0e4,#fff)}
.c4{background:linear-gradient(145deg,#e6f8ec,#fff)}
.eyebrow {color:#8a7f76;font-size:.75rem;letter-spacing:.22em;text-transform:uppercase;} .lbl {color:#7a6f66;font-size:.92rem;}
h1.hero {font-size:4rem;font-weight:800;line-height:1.02;margin:14px 0;color:#14110f;letter-spacing:-.03em;animation:up .9s both;}
h1.hero span {color:#ff6a1a;}
.college {font-size:1.5rem;font-weight:800;text-align:center;} .year {text-align:center;font-weight:700;color:#ff6a1a;}
.stat {font-size:2.2rem;font-weight:800;color:#14110f;line-height:1.1;}
.stats {display:flex;margin-top:26px;} .stats div {padding:0 26px;border-left:1px solid #d9cdc2;} .stats div:first-child {padding-left:0;border:0;}
.stats b {font-size:1.5rem;font-weight:800;display:block;}
.tile {width:46px;height:46px;border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:1.3rem;font-weight:800;color:#fff;
 background:linear-gradient(135deg,#ff8a3d,#ff5a0a);margin-bottom:12px;box-shadow:0 8px 20px rgba(255,106,26,.4);}
.name {font-size:1.05rem;font-weight:700;}
.bars {display:flex;align-items:flex-end;gap:10px;height:120px;margin-top:14px;}
.bar {flex:1;border-radius:8px;background:linear-gradient(180deg,#ff8a3d,#ff5a0a);transform-origin:bottom;animation:grow 1.1s cubic-bezier(.2,.9,.3,1) both;}
.sw {display:inline-block;width:42px;height:42px;border-radius:14px;margin:8px 8px 0 0;transition:transform .3s;border:1px solid #eee;} .sw:hover {transform:translateY(-6px) rotate(-6deg);}
.dot {display:inline-block;width:12px;height:12px;border-radius:50%;margin-right:8px;vertical-align:middle;}
.art {animation:bob 6s ease-in-out infinite;filter:drop-shadow(0 30px 30px rgba(120,70,30,.25));}
section[data-testid="stSidebar"] {background:linear-gradient(180deg,#ffffff 0%,#fff1e6 100%);border-right:1px solid #f0e6dc;}
.brand {font-size:1.7rem;font-weight:800;margin:6px 0 24px 6px;letter-spacing:-.03em;} .brand span {color:#ff6a1a;}
section[data-testid="stSidebar"] div[role="radiogroup"] {gap:6px;}
section[data-testid="stSidebar"] div[role="radiogroup"] label {width:100%;padding:11px 18px;border-radius:999px;transition:background .3s, transform .3s;cursor:pointer;}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {background:#ffe3cf;transform:translateX(6px);}
section[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {display:none;}
section[data-testid="stSidebar"] div[role="radiogroup"] label p {font-weight:500;}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {background:#14110f;}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {color:#fff;font-weight:700;}
.stButton>button {border:0;border-radius:999px;padding:.55rem 1.6rem;color:#fff;font-weight:600;background:#14110f;transition:transform .3s, box-shadow .3s;}
.stButton>button:hover {transform:translateY(-3px) scale(1.04);color:#fff;box-shadow:0 12px 26px rgba(20,17,15,.3);}
[data-testid="stForm"] {background:#fff;border-radius:999px;padding:8px 12px;border:1px solid #f0e6dc;box-shadow:0 14px 34px rgba(120,80,40,.12);}
[data-testid="stForm"] div[data-baseweb="select"]>div {background:transparent;border:0;box-shadow:none;}
[data-testid="stForm"] button {width:48px;height:48px;padding:0;border-radius:50%;background:#ff6a1a;font-size:1.3rem;box-shadow:0 10px 22px rgba(255,106,26,.45);}
</style>
""", unsafe_allow_html=True)

def card(html, cls="white", delay=0):
    st.markdown(f'<div class="clay {cls}" style="animation-delay:{delay}s">{html}</div>', unsafe_allow_html=True)

# ───────────────────────── Math helpers ─────────────────────────
def hav(a, b):
    """Haversine great-circle distance in km between (lat, lon) points."""
    R = 6371.0
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dphi, dl = p2 - p1, math.radians(b[1] - a[1])
    h = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))

def rush(h):
    """Rush-hour intensity: two Gaussian peaks at 9:00 and 18:00 over a 0.25 base."""
    return min(1.0, 0.25 + math.exp(-(h - 9) ** 2 / 4.5) + math.exp(-(h - 18) ** 2 / 4.5))

def congestion(lat, lon, bucket, h):
    """Deterministic pseudo-random congestion c in [0,1] per ~110 m road cell, scaled by rush(h)."""
    x = math.sin(round(lat, 3) * 127.1 + round(lon, 3) * 311.7 + bucket * 17.3) * 43758.5453
    return min(1.0, (x - math.floor(x)) * rush(h) * 1.45)

V0 = 35.0  # free-flow urban speed km/h
def seg_time_h(d_km, c):
    return d_km / (V0 * (1 - 0.75 * c))  # speed drops linearly with congestion

def segments(coords, bucket, h, step=6):
    out = []
    for i in range(0, len(coords) - 1, step):
        s = coords[i:i + step + 1]
        mid = s[len(s) // 2]
        d = sum(hav(s[j], s[j + 1]) for j in range(len(s) - 1))
        out.append((s, congestion(mid[0], mid[1], bucket, h), d))
    return out

def tsp(M):
    """Nearest-neighbour start + 2-opt improvement (open path starting at node 0)."""
    n = len(M); order = [0]; left = set(range(1, n))
    while left:
        j = min(left, key=lambda k: M[order[-1]][k]); order.append(j); left.remove(j)
    cost = lambda o: sum(M[o[i]][o[i + 1]] for i in range(len(o) - 1))
    better = True
    while better:
        better = False
        for i in range(1, n - 1):
            for k in range(i + 1, n):
                new = order[:i] + order[i:k + 1][::-1] + order[k + 1:]
                if cost(new) < cost(order) - 1e-9:
                    order, better = new, True
    return order

def lev(a, b):
    """Levenshtein edit distance (dynamic programming)."""
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[-1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]

# ───────────────────────── Routing (OSRM + fallback) ─────────────────────────
OSRM = "https://router.project-osrm.org"
def _fmt(pts): return ";".join(f"{lo},{la}" for la, lo in pts)

def _osrm(pts, alts="false"):
    r = requests.get(f"{OSRM}/route/v1/driving/{_fmt(pts)}",
                     params=dict(overview="full", geometries="geojson", alternatives=alts), timeout=8).json()
    return [[(la, lo) for lo, la in rt["geometry"]["coordinates"]] for rt in r["routes"]]

def _overlap(r1, r2):
    """Share of road points two routes have in common (0 = totally different roads)."""
    s1, s2 = {(round(a, 4), round(b, 4)) for a, b in r1}, {(round(a, 4), round(b, 4)) for a, b in r2}
    return len(s1 & s2) / max(1, min(len(s1), len(s2)))

def _via(a, b, side):
    """Point beside the middle of a->b (perpendicular offset) used to force a different road."""
    return ((a[0] + b[0]) / 2 - (b[1] - a[1]) * .2 * side, (a[1] + b[1]) / 2 + (b[0] - a[0]) * .2 * side)

@st.cache_data(ttl=600, show_spinner=False)
def leg_routes(a, b):
    """Up to 3 genuinely different road routes between two points."""
    try:
        cands = []
        try: cands = _osrm([a, b], "3")
        except Exception: pass
        if not cands: cands = _osrm([a, b])
        for side in (1, -1):                      # OSRM often returns 1 route -> force detours via a side waypoint
            if len(cands) >= 3: break
            try:
                for rt in _osrm([a, _via(a, b, side), b]):
                    if all(_overlap(rt, c) < .75 for c in cands): cands.append(rt)
            except Exception: pass
        return cands[:3]
    except Exception:  # offline fallback: straight line
        return [[(a[0] + (b[0] - a[0]) * t / 20, a[1] + (b[1] - a[1]) * t / 20) for t in range(21)]]

@st.cache_data(ttl=600, show_spinner=False)
def get_routes(pts):
    """Full-trip alternatives: route j takes the j-th alternative on every leg (works for multi-drop too)."""
    legs = [leg_routes(a, b) for a, b in zip(pts, pts[1:])]
    return [[p for l in legs for p in l[min(j, len(l) - 1)]] for j in range(max(len(l) for l in legs))]

@st.cache_data(ttl=600, show_spinner=False)
def get_matrix(pts):
    try:
        r = requests.get(f"{OSRM}/table/v1/driving/{_fmt(pts)}", params=dict(annotations="duration"), timeout=8).json()
        return [[x / 3600 for x in row] for row in r["durations"]]
    except Exception:
        return [[hav(a, b) * 1.35 / V0 for b in pts] for a in pts]

PLACES = {"Majestic (Warehouse)": (12.9767, 77.5713), "Indiranagar": (12.9784, 77.6408),
          "Koramangala": (12.9352, 77.6245), "Jayanagar": (12.9308, 77.5838),
          "Malleshwaram": (13.0035, 77.5646), "Whitefield": (12.9698, 77.7500),
          "HSR Layout": (12.9116, 77.6474), "Rajajinagar": (12.9910, 77.5520),
          "Hebbal": (13.0358, 77.5970), "Electronic City": (12.8452, 77.6602)}

COL = lambda c: "#ef4444" if c > 0.6 else ("#f5b301" if c > 0.3 else "#22c55e")

# ───────────────────────── Pages ─────────────────────────
ART = """<svg class="art" viewBox="0 0 520 420" xmlns="http://www.w3.org/2000/svg">
<polygon points="20,310 260,410 505,290 270,190" fill="#fff" stroke="#efe5db"/>
<polygon points="95,300 270,372 470,276 300,206" fill="#37302b"/>
<polyline points="95,300 270,372 470,276" fill="none" stroke="#ff7a1a" stroke-width="4"/>
<polygon points="300,70 405,18 405,140 300,195" fill="#ff7a1a"/>
<polygon points="115,120 115,250 235,308 235,178" fill="#fff"/>
<polygon points="235,178 235,308 360,246 360,116" fill="#efe9e3"/>
<polygon points="115,120 235,178 360,116 240,58" fill="#fbf9f6"/>
<polygon points="140,190 140,252 190,276 190,214" fill="#ff7a1a"/>
<text transform="translate(262,212) skewY(-26.5)" font-family="Inter,sans-serif" font-weight="800" font-size="24" fill="#14110f">smart<tspan fill="#ff6a1a">.</tspan></text>
<polygon points="150,236 150,262 175,274 175,248" fill="#d9a566"/><polygon points="150,236 175,248 200,236 175,224" fill="#ecc189"/>
<polygon points="320,286 320,330 395,364 395,320" fill="#fff"/><polygon points="395,320 395,364 440,342 440,298" fill="#f1ece6"/>
<polygon points="320,286 395,320 440,298 365,264" fill="#fff"/><polygon points="395,322 440,300 440,314 395,336" fill="#ff7a1a"/>
<polygon points="400,326 436,308 436,330 400,348" fill="#2a2523"/>
<circle cx="345" cy="338" r="10" fill="#14110f"/><circle cx="420" cy="354" r="10" fill="#14110f"/>
<polygon points="400,330 400,370 440,390 440,350" fill="#d9a566"/><polygon points="440,350 440,390 478,372 478,332" fill="#c4914f"/><polygon points="400,330 440,350 478,332 438,312" fill="#ecc189"/>
<circle cx="60" cy="230" r="34" fill="#6e9a5b"/><circle cx="82" cy="215" r="26" fill="#7fae6a"/><rect x="42" y="258" width="44" height="22" rx="4" fill="#fff"/>
<circle cx="462" cy="150" r="30" fill="#6e9a5b"/><rect x="446" y="176" width="34" height="20" rx="4" fill="#fff"/>
</svg>"""

def home():
    names = list(PLACES)
    def go():
        st.session_state.wh = st.session_state.pk or names[0]
        st.session_state.drops = [st.session_state.dl or "Indiranagar"]
        st.session_state.page = "Live Traffic"
    card('<div class="college">BGS College of Engineering and Technology</div>', "c3")
    card('<div class="year">🎓 1st Year</div>', "c4", .1)
    l, r = st.columns([1.05, 1])
    with l:
        st.markdown('<div class="eyebrow" style="margin-top:20px">Delivering a brighter tomorrow</div>'
                    '<h1 class="hero">Send<br>Anything.<br><span>Anywhere.</span></h1>'
                    '<p class="lbl" style="font-size:1.05rem;max-width:420px">Fast, reliable and smart delivery - live traffic routing, multi-drop planning and damage-proof QR scanning, all powered by maths.</p>', unsafe_allow_html=True)
        with st.form("quick"):
            c1, c2, c3 = st.columns([1, 1, .3])
            c1.selectbox("p", names, index=None, placeholder="📦 Pickup location", key="pk", label_visibility="collapsed")
            c2.selectbox("d", names[1:], index=None, placeholder="Delivery location", key="dl", label_visibility="collapsed")
            c3.form_submit_button("→", on_click=go)
        st.markdown('<div class="stats"><div><b>5</b><span class="lbl">Team members</span></div><div><b>3</b><span class="lbl">Smart modules</span></div><div><b>24/7</b><span class="lbl">Live routing</span></div></div>', unsafe_allow_html=True)
    with r:
        st.markdown(ART, unsafe_allow_html=True)
    st.markdown("#### Our Team")
    team = ["PUNEETH S", "MANU G N", "V RAGHUNANDHAN", "PANCHAM GOWDA V R", "PRABHAKAR"]
    for i, (c, n) in enumerate(zip(st.columns(5), team)):
        with c:
            card(f'<div class="tile">{n[0]}</div><div class="name">{n}</div><div class="lbl">Team member {i+1}</div>', f"c{i%5}", .1 * i)
    l, r = st.columns([2, 1])
    with l:
        hrs = list(range(6, 24, 2))
        bars = "".join(f'<div class="bar" style="height:{int(rush(h)*100)}%;animation-delay:{.08*k}s"></div>' for k, h in enumerate(hrs))
        card(f'<div class="name">Rush-hour traffic model</div><div class="lbl">Congestion intensity, 6 AM to 10 PM</div><div class="bars">{bars}</div>', "white", .2)
    with r:
        sw = "".join(f'<span class="sw" style="background:{c}"></span>' for c in ["#ff6a1a", "#14110f", "#22c55e", "#f5b301", "#38bdf8", "#ef4444"])
        card(f'<div class="name">Route colours</div><div class="lbl">Red · yellow · green on the map</div>{sw}', "white", .3)

def traffic():
    st.markdown("## 🗺️ Live Traffic & Delivery Route")
    names = list(PLACES)
    c1, c2 = st.columns([1, 2])
    st.session_state.setdefault("wh", names[0]); st.session_state.setdefault("drops", ["Indiranagar", "Koramangala", "Jayanagar"])
    wh = c1.selectbox("Warehouse / start", names, key="wh")
    drops = c2.multiselect("Delivery stops (1 stop = fastest route, 2+ = optimised multi-drop)", names[1:], key="drops")
    now = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
    hour = st.slider("Time of day (hours, IST)", 0.0, 24.0, round(now.hour + now.minute / 60, 1), 0.5)
    if not drops:
        st.info("Pick at least one delivery stop."); return
    bucket = int(now.timestamp() // 300)  # traffic refreshes every 5 min
    pts = tuple([PLACES[wh]] + [PLACES[d] for d in drops])
    scale = 1 + 0.8 * rush(hour)
    if len(pts) > 2:
        M = [[x * scale for x in row] for row in get_matrix(pts)]
        order = tsp(M); pts = tuple(pts[i] for i in order); stops = [wh] + [drops[i - 1] for i in order[1:]]
    else:
        stops = [wh, drops[0]]
    routes = get_routes(pts)
    info = []
    for rt in routes:
        segs = segments(rt, bucket, hour)
        info.append((rt, segs, sum(seg_time_h(d, c) for _, c, d in segs) * 60, sum(d for *_, d in segs)))
    best = min(range(len(info)), key=lambda i: info[i][2])

    # ---- route chooser (Google-Maps style: pick one of the alternatives) ----
    labels = [f"Route {i+1} · {e:.0f} min · {d:.1f} km" + ("  ⚡ Fastest" if i == best else "") for i, (_, _, e, d) in enumerate(info)]
    if len(info) > 1:
        sel = labels.index(st.radio("🛣️ Choose a route", labels, index=best, horizontal=True))
        slowest = max(i[2] for i in info)
        st.caption(f"{len(info)} different road routes found - the fastest saves {slowest - info[best][2]:.0f} min vs the slowest. Grey = alternatives, coloured = selected route (traffic).")
    else:
        sel = best
        st.caption("Only one road route exists for this trip.")

    # ---- map: centre + zoom computed by hand so the route is always framed correctly ----
    allpts = [p for rt, *_ in info for p in rt]
    lats, lons = [p[0] for p in allpts], [p[1] for p in allpts]
    ctr = ((min(lats) + max(lats)) / 2, (min(lons) + max(lons)) / 2)
    span_lon, span_lat = max(max(lons) - min(lons), 1e-3), max(max(lats) - min(lats), 1e-3)
    zoom = min(math.log2(800 * 360 / (256 * span_lon)), math.log2(450 * 360 * math.cos(math.radians(ctr[0])) / (256 * span_lat)))
    m = folium.Map(location=ctr, zoom_start=max(3, min(16, int(zoom))), tiles=None)
    folium.TileLayer("OpenStreetMap", name="Street map").add_to(m)   # free, no API key
    folium.TileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                     attr="Esri, Maxar, Earthstar Geographics", name="Satellite").add_to(m)

    for i, (rt, segs, eta, dist) in enumerate(info):        # alternatives first (grey, underneath)
        if i == sel: continue
        folium.PolyLine(rt, color="#ffffff", weight=10, opacity=.9).add_to(m)
        folium.PolyLine(rt, color="#8a94a6", weight=6, opacity=.95,
                        tooltip=f"Route {i+1}: {eta:.0f} min · {dist:.1f} km").add_to(m)
    rt, segs, eta, dist = info[sel]                          # selected route on top, coloured by congestion
    folium.PolyLine(rt, color="#22c55e" if sel == best else "#4c9cf0", weight=16, opacity=.35).add_to(m)
    folium.PolyLine(rt, color="#ffffff", weight=11, opacity=1).add_to(m)
    for s, c, d in segs:
        folium.PolyLine(s, color=COL(c), weight=7, opacity=1, tooltip=f"Route {sel+1}: congestion {c:.0%}").add_to(m)
    for i, s in enumerate(stops):
        folium.Marker(PLACES[s], tooltip=s, icon=folium.DivIcon(html=f'<div style="font-size:26px;transform:translate(-50%,-100%)">{"🏭" if i==0 else "📦"}</div>')).add_to(m)
    p = st.slider("🛵 Rider progress", 0, 100, 0, help="Drag to move the delivery bike along the route")
    pos = rt[min(len(rt) - 1, int(p / 100 * (len(rt) - 1)))]
    folium.Circle(pos, radius=250, color="#4c9cf0", fill=True, fill_opacity=.3).add_to(m)
    folium.Marker(pos, tooltip="Delivery rider", icon=folium.DivIcon(html='<div style="font-size:38px;transform:translate(-50%,-50%)">🛵</div>')).add_to(m)
    folium.LayerControl(collapsed=True).add_to(m)
    a, b, c = st.columns(3)
    with a: card(f'<div class="stat">{eta:.0f} min</div><div class="lbl">ETA (Route {sel+1}{" · fastest" if sel == best else ""})</div>', "c4")
    with b: card(f'<div class="stat">{dist:.1f} km</div><div class="lbl">Distance</div>', "c1", .1)
    with c: card('<span class="dot" style="background:#ef4444"></span>Congested<br><span class="dot" style="background:#f5b301"></span>Slightly busy<br><span class="dot" style="background:#22c55e"></span>Clear', "c0", .2)
    st.markdown("**Delivery order:** " + " → ".join(stops))
    st_folium(m, height=520, use_container_width=True, returned_objects=[])
    with st.expander("📐 Math used here"):
        st.markdown("""
- **Haversine:** `d = 2R·asin√(sin²(Δφ/2) + cosφ₁cosφ₂sin²(Δλ/2))`, R = 6371 km.
- **Rush-hour model:** `rush(h) = 0.25 + e^(-(h-9)²/4.5) + e^(-(h-18)²/4.5)` (Gaussian peaks at 9 AM and 6 PM).
- **Speed & time per segment:** `v = v₀(1 − 0.75c)`, `t = d / v`; route time = Σt. Fastest route = `argmin` of total time.
- **Alternatives:** OSRM alternatives + detours through a side waypoint (kept only if < 75 % of road points overlap). Every route is timed with the congestion model; the fastest gets a green glow.\n- **Colours:** c > 0.6 red, 0.3–0.6 yellow, else green (selected route); alternatives are grey.
- **Multi-drop (TSP):** time matrix → nearest-neighbour start → **2-opt** swaps while total time drops.
- Roads come from OSRM (OpenStreetMap). Free OSRM has no live traffic, so congestion is modelled; plug in a TomTom/Google Traffic API key for real data.
""")

def qr_tool():
    st.markdown("## 📦 Damage-proof QR Delivery Scanner")
    ss = st.session_state
    ss.setdefault("parcels", {})
    t1, t2 = st.tabs(["🏬 Store manager", "🛵 Delivery person"])
    with t1:
        txt = st.text_area("Paste codes (one per line, optional `code, item`)", height=120)
        n = st.number_input("…or generate demo parcels", 1, 30, 6)
        a, b = st.columns(2)
        if a.button("Load pasted codes"):
            for ln in txt.splitlines():
                if ln.strip():
                    code, _, item = ln.partition(",")
                    ss.parcels[code.strip().upper()] = dict(item=item.strip() or "Parcel", status="Pending")
        if b.button("Generate demo batch"):
            codes = []
            while len(codes) < n:  # keep every pair at edit distance >= 6 → errors are correctable
                c = "SD" + "".join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ23456789", k=10))
                if all(lev(c, o) >= 6 for o in codes): codes.append(c)
            ss.parcels = {c: dict(item=f"Parcel {i+1}", status="Pending") for i, c in enumerate(codes)}
        cols = st.columns(4)
        for i, (code, v) in enumerate(ss.parcels.items()):
            q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=5, border=2)
            q.add_data(code); q.make(fit=True)
            with cols[i % 4]:
                st.image(q.make_image().get_image(), caption=f"{code}\n{v['status']}")
    with t2:
        if not ss.parcels:
            st.info("Manager must load codes first."); return
        done = sum(v["status"] != "Pending" for v in ss.parcels.values())
        st.progress(done / len(ss.parcels), f"{done}/{len(ss.parcels)} delivered")
        maxd = st.slider("Max damaged characters tolerated", 0, 5, 3)
        cam = st.camera_input("Scan parcel QR")
        up = st.file_uploader("…or upload a photo", type=["png", "jpg", "jpeg"])
        typed = st.text_input("…or type what you can read of the code")
        raw = ""
        img = cam or up
        if img:
            arr = cv2.cvtColor(np.array(Image.open(img).convert("RGB")), cv2.COLOR_RGB2BGR)
            det = cv2.QRCodeDetector()
            for s in (1, .5, 1.5, 2):
                im = cv2.resize(arr, None, fx=s, fy=s)
                g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                for x in (im, cv2.threshold(g, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]):
                    raw = det.detectAndDecode(x)[0] or raw
                if raw: break
            if not raw: st.warning("QR too damaged to decode - type the visible characters below.")
        raw = (raw or typed).strip().upper()
        if raw:
            ranked = sorted((lev(raw, c), c) for c in ss.parcels)
            (d1, best), d2 = ranked[0], (ranked[1][0] if len(ranked) > 1 else 99)
            if d1 <= maxd and d2 - d1 >= 2:
                ss.parcels[best]["status"] = "Delivered ✅"
                card(f'<b>✅ Matched {best}</b><br>Item: {ss.parcels[best]["item"]}<br>Damaged characters: {d1} · confidence {1 - d1/len(best):.0%}', "c4")
            else:
                card(f'<b>❌ No safe match</b><br>Closest: {best} (distance {d1}, runner-up {d2}). Rescan or type more characters.', "c2")
        with st.expander("🧪 Damage lab"):
            code = st.selectbox("Pick a code", list(ss.parcels))
            k = st.slider("Corrupt characters", 0, 6, 2)
            bad = list(code)
            for i in random.sample(range(len(bad)), k): bad[i] = random.choice("#?*")
            bad = "".join(bad); d, c = min((lev(bad, x), x) for x in ss.parcels)
            st.write(f"Scanner read: `{bad}` → nearest `{c}` (distance {d}) → {'✅ correct' if c == code and d <= maxd else '❌ rejected'}")
    with st.expander("📐 Math used here"):
        st.markdown("""
- **Reed–Solomon over GF(256):** QR level **H** adds redundancy so up to ~30% of the symbol can be missing and still decode.
- **Levenshtein distance** (dynamic programming) = minimum insert/delete/substitute edits between the scanned and stored code.
- **Error-correcting code design:** generated codes keep pairwise distance `D ≥ 6`, so any read with ≤ `⌊(D−1)/2⌋ = 2` errors has exactly one nearest code.
- **Accept rule:** nearest distance ≤ limit **and** runner-up is ≥ 2 edits further away (margin test) → no wrong parcel is ever marked delivered.
- **Confidence** = `1 − d/length`.
""")

# ───────────────────────── Navigation ─────────────────────────
with st.sidebar:
    st.markdown('<div class="brand">smart<span>.</span></div>', unsafe_allow_html=True)
    st.radio("nav", ["Home", "Live Traffic", "QR Scanner"], key="page", label_visibility="collapsed")
    page = st.session_state.page
{"Home": home, "Live Traffic": traffic, "QR Scanner": qr_tool}[page]()
