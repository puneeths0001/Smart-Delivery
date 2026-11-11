import math, random, datetime as dt
import numpy as np, requests, streamlit as st, folium, qrcode, cv2
from PIL import Image, ImageDraw
from streamlit_folium import st_folium

st.set_page_config(page_title="Smart Delivery", page_icon="🛵", layout="wide")

# ───────────────────────── Claymorphism styling ─────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&display=swap');
html, body, [class*="css"], .stApp {font-family:'Fredoka',sans-serif; color:#3b2a6b;}
.stApp {background:#e9e4ff;}
#MainMenu, header, footer {visibility:hidden;}
.block-container {padding-top:1.5rem; max-width:1150px;}
.orb {position:fixed; border-radius:50%; z-index:0; pointer-events:none; animation:float 6s ease-in-out infinite;}
.o1 {width:120px;height:120px;top:90px;right:8%;background:radial-gradient(circle at 30% 30%,#ffe29a,#f5a623 70%);box-shadow:0 20px 40px rgba(245,166,35,.35);}
.o2 {width:90px;height:90px;bottom:60px;right:4%;background:radial-gradient(circle at 30% 30%,#ffb3cf,#ec5b8f 70%);box-shadow:0 20px 40px rgba(236,91,143,.35);animation-delay:-3s;}
@keyframes float {0%,100%{transform:translateY(0)}50%{transform:translateY(-18px)}}
@keyframes up {from{opacity:0;transform:translateY(30px) scale(.96)}to{opacity:1;transform:none}}
.badge {display:inline-block;padding:8px 22px;border-radius:22px;color:#fff;font-weight:600;
 background:linear-gradient(135deg,#ff9ec0,#f2689b);box-shadow:0 10px 20px rgba(242,104,155,.4), inset 0 -4px 8px rgba(0,0,0,.12), inset 0 4px 8px rgba(255,255,255,.5);}
h1.hero {font-size:3.4rem;font-weight:700;line-height:1.05;margin:14px 0 6px;color:#3b2a6b;}
.sub {color:#6b5d94;font-size:1.1rem;}
.clay {border-radius:32px;padding:22px 26px;margin:12px 0;animation:up .8s cubic-bezier(.2,.9,.3,1) both;
 transition:transform .45s cubic-bezier(.2,.9,.3,1), box-shadow .45s;
 box-shadow:14px 18px 34px rgba(150,125,220,.30), -8px -8px 20px rgba(255,255,255,.9), inset 0 -6px 12px rgba(120,100,200,.12), inset 0 6px 12px rgba(255,255,255,.9);}
.clay:hover {transform:translateY(-10px) scale(1.025);box-shadow:20px 30px 50px rgba(150,125,220,.40), -8px -8px 20px rgba(255,255,255,.95), inset 0 -6px 12px rgba(120,100,200,.12), inset 0 6px 12px rgba(255,255,255,.9);}
.white {background:linear-gradient(145deg,#fff,#f3efff);}
.c0{background:linear-gradient(145deg,#fff3d1,#ffe9b0)} .c1{background:linear-gradient(145deg,#e4f3ff,#cfe8ff)}
.c2{background:linear-gradient(145deg,#ffe8f1,#ffd3e4)} .c3{background:linear-gradient(145deg,#efe7ff,#e0d3ff)}
.c4{background:linear-gradient(145deg,#e1fbe9,#c9f3d6)}
.college {font-size:1.7rem;font-weight:700;text-align:center;}
.year {text-align:center;font-size:1.3rem;font-weight:600;}
.avatar {width:64px;height:64px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.6rem;font-weight:700;color:#fff;
 background:radial-gradient(circle at 30% 30%,#9fd0ff,#4c9cf0 75%);box-shadow:0 10px 20px rgba(76,156,240,.4), inset 0 -5px 8px rgba(0,0,0,.15);margin-bottom:10px;}
.name {font-size:1.25rem;font-weight:600;} .role{color:#6b5d94;font-size:.95rem;}
div[role="radiogroup"] {gap:10px;flex-wrap:wrap;}
div[role="radiogroup"] label {background:#fff;border-radius:999px;padding:8px 20px;box-shadow:6px 8px 16px rgba(150,125,220,.28), inset 0 3px 6px #fff;transition:transform .3s;}
div[role="radiogroup"] label:hover {transform:translateY(-4px);}
div[role="radiogroup"] label > div:first-child {display:none;}
.stButton>button {border:0;border-radius:999px;padding:.6rem 1.8rem;color:#fff;font-weight:600;font-family:'Fredoka';
 background:linear-gradient(135deg,#8fd0ff,#4c9cf0);box-shadow:8px 12px 22px rgba(76,156,240,.4), inset 0 -4px 8px rgba(0,0,0,.12), inset 0 4px 8px rgba(255,255,255,.5);transition:transform .3s;}
.stButton>button:hover {transform:translateY(-4px) scale(1.04);color:#fff;}
.stat {font-size:1.9rem;font-weight:700;} .lbl{color:#6b5d94;}
.dot {display:inline-block;width:14px;height:14px;border-radius:50%;margin-right:6px;vertical-align:middle;}
</style>
<div class="orb o1"></div><div class="orb o2"></div>
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

@st.cache_data(ttl=600, show_spinner=False)
def get_routes(pts, alts):
    try:
        r = requests.get(f"{OSRM}/route/v1/driving/{_fmt(pts)}",
                         params=dict(overview="full", geometries="geojson", alternatives=str(alts).lower()), timeout=8).json()
        return [[(la, lo) for lo, la in rt["geometry"]["coordinates"]] for rt in r["routes"]]
    except Exception:  # offline fallback: straight lines
        line = []
        for a, b in zip(pts, pts[1:]):
            line += [(a[0] + (b[0] - a[0]) * t / 20, a[1] + (b[1] - a[1]) * t / 20) for t in range(21)]
        return [line]

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
def home():
    l, r = st.columns([1.3, 1])
    with l:
        st.markdown('<span class="badge">Smart Delivery</span><h1 class="hero">Deliveries that feel smooth &amp; smart.</h1>'
                    '<p class="sub">Live traffic routing, multi-drop optimisation and damage-proof QR scanning - powered by maths.</p>', unsafe_allow_html=True)
    with r:
        card('<b>Modules</b><br><br>🗺️ Live traffic route<br>📦 Multi-drop planner<br>🔍 Damage-proof QR scan', "white", .1)
    card('<div class="college">BGS College of Engineering and Technology</div>', "c3")
    card('<div class="year">🎓 1st Year</div>', "c0", .1)
    st.markdown("### Our Team")
    team = ["PUNEETH S", "MANU G N", "V RAGHUNANDHAN", "PANCHAM GOWDA V R", "PRABHAKAR"]
    cols = st.columns(5)
    for i, (c, n) in enumerate(zip(cols, team)):
        with c:
            card(f'<div class="avatar">{n[0]}</div><div class="name">{n}</div><div class="role">Team member {i+1}</div>', f"c{i%5}", .15 * i)

def traffic():
    st.markdown("## 🗺️ Live Traffic & Delivery Route")
    names = list(PLACES)
    c1, c2 = st.columns([1, 2])
    wh = c1.selectbox("Warehouse / start", names, 0)
    drops = c2.multiselect("Delivery stops (1 stop = fastest route, 2+ = optimised multi-drop)", names[1:], ["Indiranagar", "Koramangala", "Jayanagar"])
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
    routes = get_routes(pts, len(pts) == 2)
    info = []
    for rt in routes:
        segs = segments(rt, bucket, hour)
        info.append((rt, segs, sum(seg_time_h(d, c) for _, c, d in segs) * 60, sum(d for *_, d in segs)))
    best = min(range(len(info)), key=lambda i: info[i][2])
    m = folium.Map(location=pts[0], zoom_start=12, tiles="CartoDB positron")
    for i, (rt, segs, eta, dist) in enumerate(info):
        if i == best:
            folium.PolyLine(rt, color="#22c55e", weight=15, opacity=.35).add_to(m)  # green halo = fastest
        for s, c, d in segs:
            folium.PolyLine(s, color=COL(c), weight=6 if i == best else 4, opacity=1 if i == best else .6,
                            tooltip=f"Route {i+1}: congestion {c:.0%}").add_to(m)
    for i, s in enumerate(stops):
        folium.Marker(PLACES[s], tooltip=s, icon=folium.DivIcon(html=f'<div style="font-size:26px;transform:translate(-50%,-100%)">{"🏭" if i==0 else "📦"}</div>')).add_to(m)
    path = info[best][0]
    p = st.slider("🛵 Rider progress", 0, 100, 0, help="Drag to move the delivery bike along the route")
    pos = path[min(len(path) - 1, int(p / 100 * (len(path) - 1)))]
    folium.Circle(pos, radius=250, color="#4c9cf0", fill=True, fill_opacity=.3).add_to(m)
    folium.Marker(pos, tooltip="Delivery rider", icon=folium.DivIcon(html='<div style="font-size:38px;transform:translate(-50%,-50%)">🛵</div>')).add_to(m)
    m.fit_bounds(path)
    a, b, c = st.columns(3)
    with a: card(f'<div class="stat">{info[best][2]:.0f} min</div><div class="lbl">Fastest ETA (Route {best+1})</div>', "c4")
    with b: card(f'<div class="stat">{info[best][3]:.1f} km</div><div class="lbl">Distance</div>', "c1", .1)
    with c: card('<span class="dot" style="background:#ef4444"></span>Congested<br><span class="dot" style="background:#f5b301"></span>Slightly busy<br><span class="dot" style="background:#22c55e"></span>Clear / fastest', "c0", .2)
    st.markdown("**Delivery order:** " + " → ".join(stops))
    st_folium(m, height=520, use_container_width=True, returned_objects=[])
    with st.expander("📐 Math used here"):
        st.markdown("""
- **Haversine:** `d = 2R·asin√(sin²(Δφ/2) + cosφ₁cosφ₂sin²(Δλ/2))`, R = 6371 km.
- **Rush-hour model:** `rush(h) = 0.25 + e^(-(h-9)²/4.5) + e^(-(h-18)²/4.5)` (Gaussian peaks at 9 AM and 6 PM).
- **Speed & time per segment:** `v = v₀(1 − 0.75c)`, `t = d / v`; route time = Σt. Fastest route = `argmin` of total time.
- **Colours:** c > 0.6 red, 0.3–0.6 yellow, else green. Fastest route gets a green glow.
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
page = st.radio("nav", ["🏠 Home", "🗺️ Live Traffic", "📦 QR Scanner"], horizontal=True, label_visibility="collapsed")
{"🏠 Home": home, "🗺️ Live Traffic": traffic, "📦 QR Scanner": qr_tool}[page]()
