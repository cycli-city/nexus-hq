from memory import save_session, build_memory_context, get_all_sessions, get_session_count, delete_all_memory, save_company_fact, get_company_facts
import streamlit as st
import os
import zipfile
import io
import time
import re
from datetime import datetime
from crewai import Crew, Process
from agents import cto, cpo, cmo, coo
from tasks import create_tasks
from department_tasks import create_department_tasks
from memory import save_session, build_memory_context, get_all_sessions, get_session_count, delete_all_memory, save_company_fact, get_company_facts

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE CONFIG
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(page_title="Nexus HQ", page_icon="◆", layout="wide", initial_sidebar_state="expanded")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CSS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif;
}
.stApp {
    background: #09090d;
}
header[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer { visibility: hidden; }

/* ── Typography ── */
h1, h2, h3, h4, h5 {
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
    color: #ffffff !important;
}
p, li, span { color: #a1a1aa; }

/* ── Hero ── */
.hero-wrap {
    padding: 2.5rem 0 1rem 0;
}
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.25);
    color: #a5b4fc;
    padding: 5px 14px;
    border-radius: 100px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.hero-title {
    font-size: 3.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff 0%, #c7d2fe 40%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.05;
    letter-spacing: -0.04em;
    margin: 0 0 0.75rem 0;
}
.hero-sub {
    color: #52525b;
    font-size: 1rem;
    line-height: 1.6;
}

/* ── Live badge ── */
.live-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: rgba(34,197,94,0.08);
    border: 1px solid rgba(34,197,94,0.2);
    color: #22c55e;
    padding: 6px 14px;
    border-radius: 100px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.live-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #22c55e;
    box-shadow: 0 0 10px #22c55e;
    animation: blink 1.8s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0.3;} }

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.07) 30%, rgba(255,255,255,0.07) 70%, transparent 100%);
    margin: 2rem 0;
    border: none;
}

/* ── Metric cards ── */
.metric-card {
    background: linear-gradient(145deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.01) 100%);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 1.6rem 1.4rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.12), transparent);
}
.metric-card:hover { border-color: rgba(129,140,248,0.25); }
.metric-icon { font-size: 1.4rem; margin-bottom: 0.8rem; }
.metric-label {
    color: #52525b;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.metric-value {
    color: #ffffff;
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1;
    margin-bottom: 0.4rem;
}
.metric-sub { color: #3f3f46; font-size: 0.78rem; }
.metric-up { color: #22c55e; font-size: 0.78rem; }

/* ── Agent cards ── */
.agent-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 0;
}
.agent-card {
    background: linear-gradient(145deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.01) 100%);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.3rem;
    transition: all 0.3s ease;
    position: relative;
}
.agent-card:hover {
    border-color: rgba(129,140,248,0.35);
    background: linear-gradient(145deg, rgba(99,102,241,0.08) 0%, rgba(139,92,246,0.04) 100%);
}
.agent-emoji { font-size: 2rem; display: block; margin-bottom: 0.6rem; }
.agent-abbr {
    color: #fff;
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: -0.01em;
}
.agent-title { color: #52525b; font-size: 0.75rem; margin-bottom: 0.8rem; }
.agent-ready {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    color: #22c55e;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.05em;
}
.rdy-dot { width:5px;height:5px;border-radius:50%;background:#22c55e;box-shadow:0 0 6px #22c55e; }

/* ── Mode radio ── */
div[data-testid="stRadio"] > div {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 6px 8px;
    gap: 6px;
    flex-direction: row !important;
}
div[data-testid="stRadio"] label {
    border-radius: 10px !important;
    padding: 8px 18px !important;
    color: #71717a !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    transition: all 0.2s !important;
    border: 1px solid transparent !important;
}
div[data-testid="stRadio"] label[data-checked="true"],
div[data-testid="stRadio"] label:has(input:checked) {
    background: rgba(99,102,241,0.15) !important;
    color: #a5b4fc !important;
    border-color: rgba(99,102,241,0.3) !important;
}

/* ── Text area ── */
.stTextArea textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 14px !important;
    color: #ffffff !important;
    font-size: 0.95rem !important;
    padding: 1.1rem 1.2rem !important;
    line-height: 1.6 !important;
    transition: border-color 0.2s !important;
    resize: none !important;
}
.stTextArea textarea:focus {
    border-color: rgba(99,102,241,0.5) !important;
    box-shadow: 0 0 0 4px rgba(99,102,241,0.08) !important;
    outline: none !important;
}
.stTextArea textarea::placeholder { color: #3f3f46 !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.01em !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 16px rgba(99,102,241,0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(99,102,241,0.45) !important;
}
.stButton > button:disabled {
    background: rgba(255,255,255,0.06) !important;
    color: #3f3f46 !important;
    box-shadow: none !important;
    transform: none !important;
}

/* ── Download buttons ── */
.stDownloadButton > button {
    background: rgba(255,255,255,0.05) !important;
    color: #a1a1aa !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 9px !important;
    font-weight: 500 !important;
    font-size: 0.82rem !important;
    transition: all 0.2s !important;
    box-shadow: none !important;
}
.stDownloadButton > button:hover {
    background: rgba(99,102,241,0.1) !important;
    border-color: rgba(99,102,241,0.3) !important;
    color: #a5b4fc !important;
    transform: translateY(-1px) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 5px 6px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 10px !important;
    color: #52525b !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    padding: 8px 18px !important;
    transition: all 0.2s !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(99,102,241,0.14) !important;
    color: #c7d2fe !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 1.5rem !important;
}

/* ── Tab content card ── */
.tab-content-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 1.8rem;
    margin-bottom: 1rem;
}

/* ── Section label ── */
.section-label {
    color: #3f3f46;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}

/* ── Expander (department agents) ── */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
    color: #a1a1aa !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
}
.streamlit-expanderContent {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-top: none !important;
    border-radius: 0 0 12px 12px !important;
    padding: 1rem 1.2rem !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #06060a !important;
    border-right: 1px solid rgba(255,255,255,0.05) !important;
}
[data-testid="stSidebar"] * { color: #71717a; }
[data-testid="stSidebar"] strong { color: #a1a1aa; }

/* ── Progress bar ── */
.stProgress > div > div {
    background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
    border-radius: 100px !important;
}
.stProgress > div {
    background: rgba(255,255,255,0.06) !important;
    border-radius: 100px !important;
}

/* ── Alert / success ── */
.stSuccess {
    background: rgba(34,197,94,0.08) !important;
    border: 1px solid rgba(34,197,94,0.2) !important;
    border-radius: 12px !important;
    color: #86efac !important;
}
</style>
""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SESSION STATE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if "history" not in st.session_state:
    st.session_state.history = []
if "results" not in st.session_state:
    st.session_state.results = None

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SIDEBAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with st.sidebar:
    st.markdown("""
    <div style='display:flex;align-items:center;gap:10px;padding:1rem 0 1.5rem 0;border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:1.5rem;'>
        <div style='width:34px;height:34px;border-radius:9px;background:linear-gradient(135deg,#6366f1,#8b5cf6);display:flex;align-items:center;justify-content:center;font-size:1rem;font-weight:900;color:#fff;'>◆</div>
        <div>
            <div style='font-weight:700;font-size:0.95rem;color:#fff;letter-spacing:-0.01em;'>NEXUS HQ</div>
            <div style='font-size:0.7rem;color:#3f3f46;letter-spacing:0.05em;'>AI COMMAND CENTER</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">OPERATOR</div>', unsafe_allow_html=True)
    st.markdown("**Divyansh Khanna**")
    st.markdown('<div style="color:#52525b;font-size:0.78rem;margin-bottom:0.8rem;">Chief Executive Officer</div>', unsafe_allow_html=True)
    st.markdown('<span class="live-badge"><span class="live-dot"></span>ONLINE</span>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">WORKFORCE</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='display:grid;grid-template-columns:1fr 1fr;gap:8px;'>
        <div style='background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:10px;padding:10px 12px;'>
            <div style='color:#fff;font-size:1.3rem;font-weight:700;'>4</div>
            <div style='color:#3f3f46;font-size:0.65rem;letter-spacing:0.08em;'>EXECUTIVES</div>
        </div>
        <div style='background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:10px;padding:10px 12px;'>
            <div style='color:#fff;font-size:1.3rem;font-weight:700;'>15</div>
            <div style='color:#3f3f46;font-size:0.65rem;letter-spacing:0.08em;'>DEPT AGENTS</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">INFRASTRUCTURE</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#52525b;font-size:0.8rem;line-height:1.8;">🟢 Groq · Llama 3.1 8B<br>🟢 CrewAI · Sequential<br>🟢 Streamlit · Local<br>🟢 Auto-save · Enabled</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">SESSION LOG</div>', unsafe_allow_html=True)
    past = get_all_sessions()
    if past:
        for row in past[:6]:
            sid, ts, goal_text, mode_text, *_ = row
            st.markdown(f'<div style="font-size:0.75rem;color:#3f3f46;padding:4px 0;border-bottom:1px solid rgba(255,255,255,0.04);">🕐 {ts[:16]}<br><span style="color:#52525b;">{goal_text[:38]}...</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="color:#27272a;font-size:0.78rem;">No sessions yet.</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Memory", use_container_width=True):
        delete_all_memory()
        st.success("Memory cleared!")
        st.rerun()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HERO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
left, right = st.columns([3, 1])
with left:
    st.markdown(f"""
    <div class='hero-wrap'>
        <div class='hero-eyebrow'>◆ Nexus HQ · AI Company OS</div>
        <div class='hero-title'>Command Center</div>
        <div class='hero-sub'>Orchestrate your AI workforce. Issue a directive and watch<br>19 specialized agents build your entire strategy.</div>
    </div>
    """, unsafe_allow_html=True)
with right:
    st.markdown(f"""
    <div style='text-align:right;padding-top:2.5rem;'>
        <span class='live-badge'><span class='live-dot'></span>ALL SYSTEMS GO</span>
        <div style='color:#27272a;font-size:0.75rem;margin-top:0.6rem;'>{datetime.now().strftime("%A, %B %d · %Y")}</div>
        <div style='color:#27272a;font-size:0.75rem;'>{datetime.now().strftime("%I:%M %p")}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# METRICS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
c1, c2, c3, c4 = st.columns(4)
metrics = [
    ("📋", "Sessions Run", str(get_session_count()), "Persistent memory", ""),
    ("🤖", "Total Agents", "19 / 19", "● All operational", "metric-up"),
    ("⚡", "LLM Engine", "Groq", "Llama 3.1 · 8B Instant", ""),
    ("💰", "Total API Cost", "$0.00", "Free tier · No limits", "metric-up"),
]
for col, (icon, label, val, sub, cls) in zip([c1,c2,c3,c4], metrics):
    with col:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-icon'>{icon}</div>
            <div class='metric-label'>{label}</div>
            <div class='metric-value'>{val}</div>
            <div class='{cls if cls else "metric-sub"}'>{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# AGENT ROSTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown('<div class="section-label">EXECUTIVE TEAM</div>', unsafe_allow_html=True)
a1, a2, a3, a4 = st.columns(4)
execs = [
    ("🔧", "CTO", "Chief Technology Officer", "Engineering & Infra", a1),
    ("📦", "CPO", "Chief Product Officer", "Product & Design", a2),
    ("📣", "CMO", "Chief Marketing Officer", "Growth & Brand", a3),
    ("⚙️", "COO", "Chief Operating Officer", "Ops & Revenue", a4),
]
for icon, abbr, title, dept, col in execs:
    with col:
        st.markdown(f"""
        <div class='agent-card'>
            <span class='agent-emoji'>{icon}</span>
            <div class='agent-abbr'>{abbr}</div>
            <div class='agent-title'>{title}</div>
            <div style='color:#3f3f46;font-size:0.7rem;margin-bottom:0.7rem;'>{dept}</div>
            <span class='agent-ready'><span class='rdy-dot'></span>READY</span>
        </div>""", unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INPUT + MODE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown('<div class="section-label">EXECUTIVE DIRECTIVE</div>', unsafe_allow_html=True)

mode = st.radio("", [
    "⚡  Quick Mode — C-Suite only (~60s)",
    "🏢  Full Company — All 19 Agents (~4 min)"
], horizontal=True)

goal = st.text_area("",
    placeholder="Describe your company goal, product launch, or business challenge — your AI workforce will build the full strategy...",
    height=120, label_visibility="collapsed")

bc1, bc2, bc3 = st.columns([1.2, 1, 5])
with bc1:
    deploy = st.button("🚀  Deploy Team", disabled=not goal, use_container_width=True)
with bc2:
    if st.button("🗑️  Clear", use_container_width=True):
        st.session_state.results = None
        st.rerun()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXECUTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if deploy:
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">LIVE EXECUTION</div>', unsafe_allow_html=True)
    bar = st.progress(0, text="🟣  Initializing executive team...")

    # Phase 1: C-Suite
    # ━━━ Helper: retry on rate limit ━━━
    import re
    def run_with_retry(agent, task, max_attempts=10):
        for attempt in range(max_attempts):
            try:
                Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff()
                return task.output.raw
            except Exception as e:
                err = str(e)
                if "rate_limit" in err.lower() or "RateLimitError" in err:
                    m = re.search(r'try again in ([\d.]+)s', err)
                    wait = max(float(m.group(1)) + 10 if m else 60, 60)
                    bar.progress(bar_pct, text=f"⏳ Rate limit — retrying in {int(wait)}s... ({attempt+1}/{max_attempts})")
                    time.sleep(wait)
                elif "shutdown" in err.lower() or "futures" in err.lower():
                    # Thread pool issue — wait and retry
                    bar.progress(bar_pct, text=f"⚙️ Restarting agent thread... ({attempt+1}/{max_attempts})")
                    time.sleep(5)
                else:
                    raise e
        raise Exception("Max retries exceeded")

    # ━━━ Phase 1: C-Suite ━━━
    bar_pct = 10
    memory_context = build_memory_context(limit=2)
    cto_t, cpo_t, cmo_t, coo_t = create_tasks(goal, memory_context)
    csuite = [(cto, cto_t, "🔧 CTO"), (cpo, cpo_t, "📦 CPO"), (cmo, cmo_t, "📣 CMO"), (coo, coo_t, "⚙️ COO")]

    for i, (agent, task, label) in enumerate(csuite):
        bar_pct = 10 + (i * 8)
        bar.progress(bar_pct, text=f"{label} drafting strategy...")
        run_with_retry(agent, task)
        if i < 3:
            time.sleep(15)

    bar.progress(45, text="✅  C-Suite strategy complete")

    results = {
        "goal": goal, "mode": mode,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cto": cto_t.output.raw, "cpo": cpo_t.output.raw,
        "cmo": cmo_t.output.raw, "coo": coo_t.output.raw,
    }

    # ━━━ Phase 2: Departments ━━━
    if "Full Company" in mode:
        dept_tasks = create_department_tasks(goal, results["cto"], results["cpo"], results["cmo"], results["coo"])
        steps = [
            ("engineering", "🔧  Engineering team executing...", 58),
            ("product", "📦  Product team executing...", 72),
            ("marketing", "📣  Marketing team executing...", 86),
            ("operations", "⚙️  Operations team executing...", 96),
        ]
        for key, msg, pct in steps:
            bar_pct = pct
            bar.progress(pct, text=msg)
            tasks_list = dept_tasks[key]
            results[key] = {}
            for task in tasks_list:
                run_with_retry(task.agent, task)
                results[key][task.agent.role] = task.output.raw
                time.sleep(15)

    bar.progress(100, text="✅  All agents have reported in!")
    st.session_state.results = results
    st.session_state.history.append({"time": datetime.now().strftime("%H:%M"), "goal": goal})
    save_session(results)

    # Auto-save
    os.makedirs("outputs", exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    for name, content in [("CTO", results["cto"]),("CPO", results["cpo"]),("CMO", results["cmo"]),("COO", results["coo"])]:
        with open(f"outputs/{ts}_{name}.md", "w", encoding="utf-8") as f:
            f.write(f"# {name} Plan\n\n{content}")
    st.success("✅ All plans saved automatically to /outputs")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# RESULTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if st.session_state.results:
    r = st.session_state.results
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # Header row
    rh1, rh2 = st.columns([3, 1])
    with rh1:
        st.markdown('<div class="section-label">STRATEGIC OUTPUT</div>', unsafe_allow_html=True)
        st.markdown(f"<div style='color:#52525b;font-size:0.85rem;'>📌 {r['goal']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='color:#27272a;font-size:0.75rem;margin-top:3px;'>Generated · {r['timestamp']}</div>", unsafe_allow_html=True)
    with rh2:
        # Build ZIP
        zb = io.BytesIO()
        with zipfile.ZipFile(zb, "w", zipfile.ZIP_DEFLATED) as zf:
            for k,v in [("CTO",r["cto"]),("CPO",r["cpo"]),("CMO",r["cmo"]),("COO",r["coo"])]:
                zf.writestr(f"Executive/{k}_Plan.md", v)
            for dept in ["engineering","product","marketing","operations"]:
                if dept in r:
                    for role, content in r[dept].items():
                        zf.writestr(f"Departments/{dept.title()}/{role}.md", content)
        st.download_button("⬇️  Download All Reports (.zip)", data=zb.getvalue(),
            file_name=f"NexusHQ_Reports_{r['timestamp']}.zip", mime="application/zip", use_container_width=True)

    # ── C-Suite tabs ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">EXECUTIVE STRATEGIES</div>', unsafe_allow_html=True)
    t1, t2, t3, t4 = st.tabs(["🔧  CTO · Technical Plan", "📦  CPO · Product Roadmap", "📣  CMO · Marketing Plan", "⚙️  COO · Operations Plan"])

    tab_data = [(t1,"cto","CTO_Technical_Plan"),(t2,"cpo","CPO_Product_Roadmap"),
                (t3,"cmo","CMO_Marketing_Plan"),(t4,"coo","COO_Operations_Plan")]

    for tab, key, filename in tab_data:
        with tab:
            st.markdown(f"<div class='tab-content-card'>{r[key]}</div>", unsafe_allow_html=True)
            st.download_button(f"⬇️  Download {filename.replace('_',' ')}.md",
                data=r[key], file_name=f"{filename}.md",
                mime="text/markdown", key=f"dl_{key}")

    # ── Department tabs ──
    if "engineering" in r:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-label">DEPARTMENTAL EXECUTION PLANS</div>', unsafe_allow_html=True)
        d1, d2, d3, d4 = st.tabs(["🔧  Engineering Team", "📦  Product Team", "📣  Marketing Team", "⚙️  Operations Team"])
        dept_map = [("engineering",d1),("product",d2),("marketing",d3),("operations",d4)]
        for dept_key, tab in dept_map:
            with tab:
                for role, content in r[dept_key].items():
                    with st.expander(f"👤  {role}", expanded=False):
                        st.markdown(content)
                        st.download_button(f"⬇️  Download {role} report",
                            data=content, file_name=f"{role.replace(' ','_')}.md",
                            mime="text/markdown", key=f"dl_{dept_key}_{role}")