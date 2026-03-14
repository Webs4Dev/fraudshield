import streamlit as st
import requests
import random
from dotenv import load_dotenv
import os

load_dotenv()
API_URL = os.getenv("API_URL")

st.set_page_config(
    page_title="FraudShield — Fraud Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --black:       #0b0c0e;
    --surface:     #111318;
    --surface2:    #181b22;
    --border:      rgba(255,255,255,0.07);
    --border-gold: rgba(197,160,80,0.3);
    --gold:        #c5a050;
    --gold-light:  #e8c97a;
    --gold-dim:    rgba(197,160,80,0.12);
    --text:        #e8e4dc;
    --text-muted:  #6b6860;
    --text-dim:    #3a3830;
    --green-dim:   rgba(61,158,110,0.12);
    --amber-dim:   rgba(196,138,42,0.12);
    --red-dim:     rgba(184,64,64,0.12);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--black);
    color: var(--text);
}
.stApp { background: var(--black); }
.block-container { padding: 0 3rem 4rem 3rem; max-width: 1100px; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--black); }
::-webkit-scrollbar-thumb { background: rgba(197,160,80,0.2); border-radius: 10px; }

/* ── Nav ── */
.nav-bar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1.6rem 0 1.4rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2.8rem;
}
.nav-wordmark {
    font-family: 'Playfair Display', serif;
    font-weight: 700; font-size: 1.65rem; color: var(--text);
}
.nav-wordmark span { color: var(--gold); }
.nav-tagline {
    font-family: 'DM Mono', monospace; font-size: 0.6rem;
    letter-spacing: 3px; text-transform: uppercase;
    color: var(--text-muted); padding: 3px 10px;
    border: 1px solid var(--border); border-radius: 3px; margin-left: 14px;
}
.nav-right {
    display: flex; align-items: center; gap: 8px;
    font-family: 'DM Mono', monospace; font-size: 0.62rem;
    letter-spacing: 1.5px; color: var(--text-muted); text-transform: uppercase;
}
.status-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: #3d9e6e; box-shadow: 0 0 8px rgba(61,158,110,0.55);
    animation: pulse-dot 2.5s infinite;
}
@keyframes pulse-dot { 0%,100%{opacity:1;} 50%{opacity:0.3;} }

/* ── Panel ── */
.panel {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 10px; padding: 2rem 2.4rem; margin-bottom: 1.6rem;
}
.panel-header {
    display: flex; align-items: center; gap: 12px;
    margin-bottom: 1.6rem; padding-bottom: 1rem;
    border-bottom: 1px solid var(--border);
}
.panel-icon {
    width: 32px; height: 32px; background: var(--gold-dim);
    border: 1px solid var(--border-gold); border-radius: 6px;
    display: flex; align-items: center; justify-content: center; font-size: 0.9rem;
}
.panel-title    { font-family: 'Playfair Display', serif; font-size: 1rem; font-weight: 600; color: var(--text); }
.panel-subtitle { font-family: 'DM Mono', monospace; font-size: 0.58rem; letter-spacing: 2px; text-transform: uppercase; color: var(--text-muted); margin-top: 2px; }

/* ── Format guide ── */
.format-guide {
    background: var(--surface2); border: 1px solid var(--border);
    border-left: 2px solid var(--gold); border-radius: 7px;
    padding: 1rem 1.4rem; margin-bottom: 1.4rem;
    font-family: 'DM Mono', monospace;
}
.format-guide-title { font-size: 0.58rem; letter-spacing: 2.5px; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.5rem; }
.format-guide-code  { font-size: 0.72rem; color: var(--gold-light); line-height: 1.7; }
.format-guide-note  { font-size: 0.62rem; color: var(--text-muted); margin-top: 0.5rem; }

/* ── Textarea ── */
div[data-testid="stTextArea"] label {
    font-family: 'DM Mono', monospace !important; font-size: 0.6rem !important;
    letter-spacing: 2.5px !important; text-transform: uppercase !important;
    color: var(--text-muted) !important;
}
div[data-testid="stTextArea"] textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important; color: var(--text) !important;
    font-family: 'DM Mono', monospace !important; font-size: 0.8rem !important;
    line-height: 1.6 !important; padding: 1rem !important;
    transition: border-color 0.25s !important;
}
div[data-testid="stTextArea"] textarea:focus {
    border-color: var(--border-gold) !important;
    box-shadow: 0 0 0 3px rgba(197,160,80,0.07) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--border-gold) !important;
    color: var(--gold-light) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.68rem !important; letter-spacing: 3px !important;
    text-transform: uppercase !important;
    padding: 0.75rem 1.5rem !important; border-radius: 7px !important;
    width: 100% !important; transition: all 0.25s !important;
}
.stButton > button:hover {
    background: var(--gold-dim) !important;
    border-color: var(--gold) !important;
    box-shadow: 0 0 20px rgba(197,160,80,0.1) !important;
}

/* ── Verdict ── */
.verdict-box {
    border-radius: 10px; padding: 2rem 2.2rem;
    margin-top: 1.6rem; border: 1px solid; position: relative; overflow: hidden;
}
.verdict-low    { background: var(--green-dim); border-color: rgba(61,158,110,0.28); }
.verdict-medium { background: var(--amber-dim); border-color: rgba(196,138,42,0.32); }
.verdict-high   {
    background: var(--red-dim); border-color: rgba(184,64,64,0.38);
    animation: throb 2.5s ease-in-out infinite;
}
@keyframes throb {
    0%,100%{ box-shadow: 0 0 0 0 rgba(184,64,64,0); }
    50%    { box-shadow: 0 0 28px 4px rgba(184,64,64,0.14); }
}
.verdict-corner  { position: absolute; top: 1.4rem; right: 1.8rem; font-size: 3rem; opacity: 0.1; }
.verdict-label   { font-family: 'DM Mono', monospace; font-size: 0.57rem; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 0.4rem; }
.verdict-heading { font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 700; line-height: 1; margin-bottom: 0.7rem; }
.verdict-prob    { font-family: 'DM Mono', monospace; font-size: 0.75rem; opacity: 0.65; }
.prob-track      { height: 2px; background: rgba(255,255,255,0.06); border-radius: 10px; margin-top: 1.2rem; overflow: hidden; }

/* ── Sample output ── */
.sample-card {
    background: var(--surface2); border: 1px solid var(--border);
    border-left: 2px solid var(--gold); border-radius: 8px;
    padding: 1.2rem 1.5rem; margin-top: 0.8rem;
    font-family: 'DM Mono', monospace; font-size: 0.72rem;
    color: var(--gold-light); line-height: 1.8; word-break: break-all;
}
.sample-label {
    font-size: 0.57rem; letter-spacing: 2.5px; text-transform: uppercase;
    color: var(--text-muted); margin-bottom: 0.5rem;
}

/* ── Error / info ── */
div[data-testid="stAlert"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
}

/* ── Footer ── */
.site-footer {
    margin-top: 3.5rem; padding-top: 1.4rem;
    border-top: 1px solid var(--border);
    display: flex; justify-content: space-between; align-items: center;
}
.footer-brand { font-family: 'Playfair Display', serif; font-size: 0.88rem; color: var(--text-muted); }
.footer-brand span { color: var(--gold); }
.footer-meta  { font-family: 'DM Mono', monospace; font-size: 0.57rem; letter-spacing: 2px; color: var(--text-dim); text-transform: uppercase; }

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── NAV ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nav-bar">
    <div style="display:flex;align-items:baseline;">
        <div class="nav-wordmark">Fraud<span>Shield</span></div>
        <div class="nav-tagline">Fraud Intelligence</div>
    </div>
    <div class="nav-right">
        <div class="status-dot"></div>
        All Systems Operational
    </div>
</div>
""", unsafe_allow_html=True)


# ── MAIN PANEL ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="panel">
    <div class="panel-header">
        <div class="panel-icon">⚡</div>
        <div>
            <div class="panel-title">Transaction Analyzer</div>
            <div class="panel-subtitle">Paste 30 raw features — model returns fraud probability</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Format guide
st.markdown("""
<div class="format-guide">
    <div class="format-guide-title">Expected Input Format</div>
    <div class="format-guide-code">Time, V1, V2, V3, … V28, Amount</div>
    <div class="format-guide-note">30 comma-separated float values &nbsp;·&nbsp; Example: &nbsp;41250, -1.358354, -0.072781, 2.536347, … , 149.62</div>
</div>
""", unsafe_allow_html=True)

csv_input = st.text_area(
    "Transaction Features (CSV — 30 values)",
    placeholder="41250,-1.358354,-0.072781,2.536347,1.378155,-0.338321,0.462388,0.239599,0.098698,0.363787,0.090794,-0.551600,-0.617801,-0.991390,-0.311169,1.468177,-0.470401,0.207971,0.025791,0.403993,0.251412,-0.018307,0.277838,-0.110474,0.066928,0.128539,-0.189115,0.133558,-0.021053,149.62",
    height=110
)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    run_btn = st.button("◈  Run Fraud Analysis", key="analyze")

with col2:
    gen_btn = st.button("◇  Generate Sample Transaction", key="generate")


# ── GENERATE SAMPLE ───────────────────────────────────────────────────────────
if gen_btn:
    sample = (
        [round(random.uniform(0, 100000), 6)] +
        [round(random.uniform(-5, 5), 6) for _ in range(28)] +
        [round(random.uniform(1, 5000), 6)]
    )
    csv_sample = ", ".join(str(v) for v in sample)
    st.markdown(f"""
    <div class="sample-card">
        <div class="sample-label">Generated Sample — copy and paste above</div>
        {csv_sample}
    </div>
    """, unsafe_allow_html=True)


# ── ANALYZE ───────────────────────────────────────────────────────────────────
if run_btn:
    if not csv_input.strip():
        st.warning("Please enter transaction features before running analysis.")
    else:
        try:
            values = [float(x.strip()) for x in csv_input.split(",")]
            if len(values) != 30:
                st.error(f"Expected exactly 30 values — received {len(values)}.")
            else:
                with st.spinner("Scoring transaction..."):
                    response = requests.post(API_URL, json=values, timeout=5)
                    result   = response.json()

                prob       = result["fraud_probability"]
                prediction = result["fraud_prediction"]
                bar_w      = int(prob * 100)

                if prob < 0.3:
                    cls, color, heading, label, icon = (
                        "verdict-low", "#5cc494", "Legitimate", "CLEARED", "✓"
                    )
                elif prob < 0.6:
                    cls, color, heading, label, icon = (
                        "verdict-medium", "#dba84a", "Suspicious", "REVIEW", "⚠"
                    )
                else:
                    cls, color, heading, label, icon = (
                        "verdict-high", "#d96060", "Fraud Detected", "BLOCKED", "✕"
                    )

                st.markdown(f"""
                <div class="verdict-box {cls}">
                    <div class="verdict-corner">{icon}</div>
                    <div class="verdict-label" style="color:{color};">{label}</div>
                    <div class="verdict-heading" style="color:{color};">{heading}</div>
                    <div class="verdict-prob">
                        Fraud probability &nbsp;·&nbsp; <strong>{prob:.2%}</strong>
                        &nbsp;&nbsp;|&nbsp;&nbsp;
                        Model prediction &nbsp;·&nbsp; <strong>{"FRAUD" if prediction else "LEGIT"}</strong>
                    </div>
                    <div class="prob-track">
                        <div style="height:2px;width:{bar_w}%;background:{color};
                             border-radius:10px;box-shadow:0 0 6px {color}99;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        except requests.exceptions.ConnectionError:
            st.markdown("""
            <div class="verdict-box verdict-medium">
                <div class="verdict-label" style="color:#dba84a;">Connection Error</div>
                <div class="verdict-heading" style="color:#dba84a;font-size:1.3rem;">API Unreachable</div>
                <div class="verdict-prob">Ensure your FastAPI server is running on port 8000.</div>
            </div>
            """, unsafe_allow_html=True)
        except Exception:
            st.error("Invalid input — ensure all 30 values are valid numbers separated by commas.")


# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="site-footer">
    <div class="footer-brand">Fraud<span>Shield</span> &nbsp;·&nbsp; Fraud Intelligence Platform</div>
    <div class="footer-meta">Random Forest · FastAPI · Streamlit · v2.0.0</div>
</div>
""", unsafe_allow_html=True)
