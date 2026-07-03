import datetime
import pandas as pd
import calendar
import streamlit as st

from manajer_keuangan import ManajerKeuangan
from model import Transaksi, LogKegiatan, TargetTabungan, Tagihan, ItemBelanja
from konfigurasi import (
    APP_NAME, APP_TAGLINE,
    KATEGORI_PENGELUARAN, KATEGORI_PEMASUKAN, KATEGORI_LOG,
    KATEGORI_TAGIHAN, ITEM_BELANJA_DEFAULT
)

# PAGE CONFIG
st.set_page_config(
    page_title="KostMate",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

:root {
    --primer: #9FA1FF;
    --primer-tua: #7B7DE5;
    --primer-muda: #B5BAFF;
    --ice-blue: #AEE2FF;
    --mint-green: #D9F9DF;
    --text-dark: #2A2C42;
    --text-muted: #6E7191;
    --bg-main: #F5F6FC;
    --bg-sidebar: linear-gradient(180deg, #EAEAFF 0%, #D4D7FF 100%);
    --card-shadow: 0 10px 25px rgba(159, 161, 255, 0.08);
    --card-shadow-hover: 0 15px 30px rgba(159, 161, 255, 0.18);
}

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
    color: var(--text-dark);
}

/* ── MAIN AREA ── */
.main .block-container {
    padding: 1.5rem 3rem 3rem 3rem;
    max-width: 1360px;
}
[data-testid="stAppViewContainer"] {
    background: var(--bg-main);
}

/* ── SIDEBAR BASE ── */
[data-testid="stSidebar"] {
    background: var(--bg-sidebar) !important;
    border-right: 1px solid rgba(159, 161, 255, 0.2) !important;
    box-shadow: 6px 0 30px rgba(159, 161, 255, 0.1);
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
}
[data-testid="stSidebar"] * {
    color: var(--text-dark);
}
[data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
    color: var(--text-muted);
}

/* ── SIDEBAR BRAND HEADER ── */
.brand-header-wrap {
    background: rgba(255, 255, 255, 0.35);
    border-bottom: 1px solid rgba(159, 161, 255, 0.15);
    padding: 1.2rem 1.1rem 1rem 1.1rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-radius: 0 0 16px 16px;
}
.brand-left {
    display: flex;
    align-items: center;
    gap: 0.7rem;
}
.brand-icon-box {
    width: 2.6rem;
    height: 2.6rem;
    border-radius: 12px;
    background: linear-gradient(135deg, var(--primer), var(--primer-muda));
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    box-shadow: 0 4px 14px rgba(159, 161, 255, 0.4);
    flex-shrink: 0;
    color: #FFFFFF !important;
}
.brand-text .brand-name {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 800;
    font-size: 1.1rem;
    color: var(--text-dark) !important;
    letter-spacing: 0.05em;
    line-height: 1.1;
}
.brand-text .brand-sub {
    font-size: 0.65rem;
    color: var(--text-muted) !important;
    font-weight: 600;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    margin-top: 0.1rem;
}

/* ── PROFILE CARD ── */
.profile-card {
    margin: 0.8rem 0.8rem 0.5rem 0.8rem;
    background: rgba(255, 255, 255, 0.45);
    border: 1px solid rgba(159, 161, 255, 0.2);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 1rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    transition: all 0.25s ease;
}
.profile-card:hover {
    background: rgba(255, 255, 255, 0.65);
    border-color: var(--primer);
    box-shadow: 0 4px 15px rgba(159, 161, 255, 0.15);
}
.profile-avatar {
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--primer) 0%, var(--primer-muda) 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    flex-shrink: 0;
    box-shadow: 0 4px 10px rgba(159, 161, 255, 0.25);
    color: #FFFFFF !important;
}
.profile-info .profile-name {
    font-weight: 700;
    font-size: 0.875rem;
    color: var(--text-dark) !important;
    line-height: 1.2;
}
.profile-info .profile-role {
    font-size: 0.7rem;
    color: var(--text-muted) !important;
    margin-top: 0.15rem;
}
.profile-badge {
    margin-left: auto;
    background: var(--mint-green);
    border: 1px solid rgba(30, 90, 52, 0.2);
    border-radius: 999px;
    padding: 0.2rem 0.6rem;
    font-size: 0.65rem;
    font-weight: 600;
    color: #1E5A34 !important;
    letter-spacing: 0.04em;
}

/* ── NAV SECTION LABEL ── */
.nav-section-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted) !important;
    padding: 0.9rem 1.1rem 0.35rem 1.1rem;
}

/* ── NAV BUTTONS ── */
[data-testid="stSidebar"] .stButton button {
    width: 100%;
    text-align: left;
    background: transparent !important;
    border: none !important;
    border-radius: 999px !important;
    color: var(--text-dark) !important;
    font-weight: 600;
    font-size: 0.9rem;
    padding: 0.75rem 1.25rem !important;
    margin-bottom: 0.25rem;
    box-shadow: none !important;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(159, 161, 255, 0.15) !important;
    color: var(--primer-tua) !important;
    transform: translateX(4px);
}
[data-testid="stSidebar"] .nav-active .stButton button {
    background: linear-gradient(90deg, var(--primer) 0%, var(--primer-muda) 100%) !important;
    color: #FFFFFF !important;
    font-weight: 700;
    box-shadow: 0 4px 15px rgba(159, 161, 255, 0.25) !important;
    border-left: none !important;
    padding-left: 1.25rem !important;
    border-radius: 999px !important;
}
[data-testid="stSidebar"] .nav-active .stButton button * {
    color: #FFFFFF !important;
}
[data-testid="stSidebar"] .nav-active .stButton button:hover {
    background: linear-gradient(90deg, var(--primer-tua) 0%, var(--primer) 100%) !important;
    color: #FFFFFF !important;
}

/* ── SIDEBAR DIVIDER ── */
.sidebar-divider {
    border: none;
    border-top: 1px solid rgba(159, 161, 255, 0.2);
    margin: 0.6rem 1rem;
}

/* ── DATE WIDGET ── */
.sidebar-date-box {
    margin: 0.5rem 0.8rem;
    background: rgba(255, 255, 255, 0.4);
    border: 1px solid rgba(159, 161, 255, 0.15);
    border-radius: 12px;
    padding: 0.8rem 1rem;
}
.sidebar-date-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-muted) !important;
    margin-bottom: 0.3rem;
}
.sidebar-date-val {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-dark) !important;
}

/* ── LOGOUT BUTTON ── */
.logout-wrap .stButton button {
    background: rgba(255, 255, 255, 0.4) !important;
    border: 1px solid rgba(159, 161, 255, 0.2) !important;
    border-radius: 999px !important;
    color: var(--text-dark) !important;
    font-weight: 600;
    font-size: 0.85rem;
    text-align: center !important;
    transition: all 0.2s;
}
.logout-wrap .stButton button:hover {
    background: #FFF1F2 !important;
    border-color: #FECDD3 !important;
    color: #E11D48 !important;
    transform: translateY(-1px);
}

/* ── SIDEBAR TOGGLE BUTTON (when hidden) ── */
.sidebar-toggle-btn button {
    position: fixed !important;
    top: 0.9rem !important;
    left: 0.9rem !important;
    z-index: 999999 !important;
    background: linear-gradient(135deg, var(--primer), var(--primer-muda)) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 999px !important;
    width: 2.6rem !important;
    height: 2.6rem !important;
    font-size: 1.1rem !important;
    box-shadow: 0 4px 14px rgba(159, 161, 255, 0.4) !important;
    padding: 0 !important;
}
.sidebar-toggle-btn button:hover {
    background: linear-gradient(135deg, var(--primer-tua), var(--primer)) !important;
    transform: scale(1.05);
}

/* ── HIDE SIDEBAR CSS ── */
.sidebar-hidden [data-testid="stSidebar"] {
    display: none !important;
}

/* Streamlit Selectboxes & inputs inside Sidebar text styling */
[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div {
    background-color: rgba(255, 255, 255, 0.6) !important;
    border: 1.5px solid rgba(159, 161, 255, 0.3) !important;
    border-radius: 20px !important;
}
[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div:focus-within {
    border-color: var(--primer) !important;
}
[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] * {
    color: var(--text-dark) !important;
}

/* ── TOPBAR / PAGE HEADER ── */
.topbar {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(16px);
    border-bottom: 1px solid rgba(159, 161, 255, 0.15);
    padding: 1.2rem 2.5rem;
    margin: -1.5rem -3rem 2rem -3rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 4px 20px rgba(159, 161, 255, 0.05);
    position: sticky;
    top: 0;
    z-index: 99;
    border-radius: 0 0 20px 20px;
}
.topbar-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: var(--text-dark);
    letter-spacing: -0.02em;
    line-height: 1.1;
}
.topbar-subtitle {
    font-size: 0.85rem;
    color: var(--text-muted);
    margin-top: 0.2rem;
    font-weight: 400;
}
.topbar-right {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.topbar-date-chip {
    background: var(--ice-blue);
    border: 1px solid rgba(159, 161, 255, 0.2);
    border-radius: 999px;
    padding: 0.4rem 1rem;
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--text-dark);
}

/* ── METRIC CARDS ── */
.metric-card {
    background: #ffffff;
    border: 1.5px solid rgba(159, 161, 255, 0.15);
    border-radius: 24px;
    padding: 1.5rem;
    box-shadow: var(--card-shadow);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
.metric-card:hover {
    box-shadow: var(--card-shadow-hover);
    transform: translateY(-5px);
    border-color: var(--primer);
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 5px;
    background: linear-gradient(90deg, var(--primer), var(--primer-muda));
    border-radius: 24px 24px 0 0;
}
.metric-card.green::before { background: linear-gradient(90deg, #8CD69D, var(--mint-green)); }
.metric-card.red::before { background: linear-gradient(90deg, #FF9B9B, #FFE3E3); }
.metric-card.blue::before { background: linear-gradient(90deg, var(--primer-muda), var(--ice-blue)); }
.metric-card.yellow::before { background: linear-gradient(90deg, #FFD285, #FFEED4); }

.metric-icon-box {
    width: 2.6rem;
    height: 2.6rem;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    margin-bottom: 1rem;
}
.metric-icon-box.green { background: var(--mint-green); color: #1E5A34; }
.metric-icon-box.red { background: #FFE6E6; color: #C53030; }
.metric-icon-box.blue { background: var(--ice-blue); color: var(--primer-tua); }
.metric-icon-box.yellow { background: #FFF7E6; color: #B7791F; }

.metric-label {
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.4rem;
}
.metric-value {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.55rem;
    font-weight: 800;
    color: var(--text-dark);
    line-height: 1.2;
}
.metric-value.green { color: #1E5A34; }
.metric-value.red { color: #C53030; }
.metric-value.blue { color: var(--primer-tua); }

.metric-delta {
    font-size: 0.75rem;
    margin-top: 0.45rem;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 0.25rem;
}

/* ── SECTION CARDS ── */
.section-card {
    background: #ffffff;
    border: 1.5px solid rgba(159, 161, 255, 0.12);
    border-radius: 24px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.5rem;
    box-shadow: var(--card-shadow);
    transition: all 0.3s ease;
}
.section-card:hover {
    box-shadow: var(--card-shadow-hover);
    border-color: rgba(159, 161, 255, 0.25);
}
.section-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.05rem;
    font-weight: 800;
    color: var(--text-dark);
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.section-title::before {
    content: '';
    display: inline-block;
    width: 4px;
    height: 1.2rem;
    background: var(--primer);
    border-radius: 2px;
}

/* ── PROGRESS BARS ── */
.progress-wrap {
    background: #EBF0FF;
    border-radius: 999px;
    height: 10px;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, var(--primer-muda), var(--primer));
    transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}
.progress-fill.done {
    background: linear-gradient(90deg, #9DECB4, var(--mint-green));
}

/* ── BADGES ── */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.03em;
}
.badge-green { background: var(--mint-green); color: #1E5A34; border: 1px solid rgba(30, 90, 52, 0.2); }
.badge-red { background: #FFE6E6; color: #C53030; border: 1px solid rgba(197, 48, 48, 0.2); }
.badge-blue { background: var(--ice-blue); color: var(--primer-tua); border: 1px solid rgba(159, 161, 255, 0.3); }
.badge-yellow { background: #FFF7E6; color: #B7791F; border: 1px solid rgba(183, 121, 31, 0.2); }
.badge-gray { background: #F1F3F9; color: var(--text-muted); border: 1px solid rgba(110, 113, 145, 0.2); }

/* ── INFO / ALERT BOXES ── */
.info-box {
    background: #F0F4FF;
    border-left: 4px solid var(--primer);
    border-radius: 4px 16px 16px 4px;
    padding: 1.1rem 1.3rem;
    margin: 1rem 0;
    font-size: 0.85rem;
    color: var(--primer-tua);
    box-shadow: 0 2px 8px rgba(159, 161, 255, 0.05);
}
.success-box {
    background: #F3FDF5;
    border-left: 4px solid #8CD69D;
    border-radius: 4px 16px 16px 4px;
    padding: 1.1rem 1.3rem;
    margin: 1rem 0;
    font-size: 0.85rem;
    color: #1E5A34;
    box-shadow: 0 2px 8px rgba(140, 214, 157, 0.05);
}
.warning-box {
    background: #FFFBEB;
    border-left: 4px solid #F5B041;
    border-radius: 4px 16px 16px 4px;
    padding: 1.1rem 1.3rem;
    margin: 1rem 0;
    font-size: 0.85rem;
    color: #B7791F;
    box-shadow: 0 2px 8px rgba(245, 176, 65, 0.05);
}

/* ── LOG ITEMS ── */
.log-item {
    display: flex;
    align-items: flex-start;
    gap: 0.9rem;
    padding: 1rem 1.2rem;
    border-radius: 16px;
    border: 1.5px solid rgba(159, 161, 255, 0.12);
    background: #FFFFFF;
    margin-bottom: 0.65rem;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 2px 6px rgba(159, 161, 255, 0.03);
}
.log-item:hover {
    background: #FAF9FF;
    border-color: var(--primer);
    transform: translateX(4px);
    box-shadow: 0 4px 12px rgba(159, 161, 255, 0.08);
}
.log-item.done {
    opacity: 0.7;
    background: #F8F9FC;
    border-color: rgba(159, 161, 255, 0.08);
}
.log-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: var(--primer);
    margin-top: 6px;
    flex-shrink: 0;
    box-shadow: 0 0 8px rgba(159, 161, 255, 0.5);
}
.log-dot.done { 
    background: #8CD69D; 
    box-shadow: 0 0 8px rgba(140, 214, 157, 0.5);
}
.log-name {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-dark);
}
.log-meta {
    font-size: 0.78rem;
    color: var(--text-muted);
    margin-top: 0.25rem;
}

/* ── FORM INPUTS ── */
.stTextInput input, .stNumberInput input, .stTextArea textarea, .stDateInput input {
    border-radius: 20px !important;
    border: 1.5px solid rgba(159, 161, 255, 0.2) !important;
    font-size: 0.9rem !important;
    background: #FFFFFF !important;
    padding: 0.6rem 1rem !important;
    transition: all 0.2s ease-in-out !important;
    color: var(--text-dark) !important;
}
.stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus, .stDateInput input:focus {
    border-color: var(--primer) !important;
    box-shadow: 0 0 0 3px rgba(159, 161, 255, 0.2) !important;
    outline: none !important;
}
.stSelectbox [data-baseweb="select"] > div {
    border-radius: 20px !important;
    border: 1.5px solid rgba(159, 161, 255, 0.2) !important;
    background: #FFFFFF !important;
    transition: all 0.2s ease-in-out !important;
}
.stSelectbox [data-baseweb="select"] > div:focus-within {
    border-color: var(--primer) !important;
    box-shadow: 0 0 0 3px rgba(159, 161, 255, 0.2) !important;
}

/* ── BUTTONS ── */
.stButton button {
    border-radius: 999px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.65rem 1.5rem !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    letter-spacing: 0.01em;
    border: 1.5px solid rgba(159, 161, 255, 0.25) !important;
    color: var(--primer-tua) !important;
    background: #FFFFFF !important;
}
.stButton button:hover {
    border-color: var(--primer) !important;
    color: var(--primer-tua) !important;
    background: rgba(159, 161, 255, 0.05) !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 10px rgba(159, 161, 255, 0.08) !important;
}
.stButton button[kind="primary"] {
    background: linear-gradient(135deg, var(--primer), var(--primer-tua)) !important;
    border: none !important;
    color: white !important;
    box-shadow: 0 4px 14px rgba(159, 161, 255, 0.3) !important;
}
.stButton button[kind="primary"]:hover {
    background: linear-gradient(135deg, var(--primer-tua), var(--primer)) !important;
    box-shadow: 0 6px 20px rgba(159, 161, 255, 0.4) !important;
    transform: translateY(-2px) !important;
    color: white !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background: rgba(159, 161, 255, 0.08);
    border-radius: 999px !important;
    padding: 6px;
    border: 1px solid rgba(159, 161, 255, 0.15);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 999px !important;
    padding: 0.6rem 1.5rem;
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--text-muted);
    background: transparent;
    transition: all 0.25s ease;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--primer) 0%, var(--primer-muda) 100%) !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 15px rgba(159, 161, 255, 0.25) !important;
    font-weight: 700 !important;
    border-radius: 999px !important;
}
.stTabs [aria-selected="true"] * {
    color: #FFFFFF !important;
}

/* Sidebar text override fix for active nav button capsules */
[data-testid="stSidebar"] .nav-active .stButton button p,
[data-testid="stSidebar"] .nav-active .stButton button span {
    color: #FFFFFF !important;
}

/* Tab text override fix for active tab capsules */
.stTabs [aria-selected="true"] p,
.stTabs [aria-selected="true"] span,
.stTabs [aria-selected="true"] div {
    color: #FFFFFF !important;
}

/* Sub-page input labels */
.stTextInput label p, .stNumberInput label p, .stTextArea label p, .stDateInput label p, .stSelectbox label p, .stRadio label p {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    color: var(--text-dark) !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.02em !important;
}

/* ── DATAFRAME ── */
.stDataFrame {
    border-radius: 16px !important;
    border: 1.5px solid rgba(159, 161, 255, 0.15) !important;
    overflow: hidden !important;
    box-shadow: var(--card-shadow) !important;
}

/* ── EMPTY STATE ── */
.empty-state {
    text-align: center;
    padding: 3.5rem 1.5rem;
    color: var(--text-muted);
}
.empty-state-icon { font-size: 3rem; margin-bottom: 0.8rem; opacity: 0.6; }
.empty-state-text { font-size: 0.95rem; font-weight: 600; color: var(--text-dark); }
.empty-state-sub { font-size: 0.8rem; color: var(--text-muted); margin-top: 0.35rem; }

/* ── DIVIDER ── */
.divider {
    border: none;
    border-top: 1.5px solid rgba(159, 161, 255, 0.12);
    margin: 1.2rem 0;
}

/* ── HIDE STREAMLIT DEFAULT UI ── */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

/* ── STAT ROW (Tagihan) ── */
.stat-chip {
    flex: 1;
    border-radius: 16px;
    padding: 1rem;
    text-align: center;
    border: 1px solid rgba(159, 161, 255, 0.1);
    box-shadow: 0 2px 4px rgba(159, 161, 255, 0.02);
    transition: transform 0.2s ease;
}
.stat-chip:hover {
    transform: translateY(-2px);
}
.stat-chip-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.35rem;
}
.stat-chip-val {
    font-size: 1.35rem;
    font-weight: 800;
}
</style>

""", unsafe_allow_html=True)

# ── HELPERS ────────────────────────────────────────────────
def format_rp(amount: float) -> str:
    return f"Rp {amount:,.0f}".replace(",", ".")

def saldo_color(amount: float) -> str:
    if amount > 0: return "green"
    if amount < 0: return "red"
    return ""

@st.cache_resource
def get_manajer() -> ManajerKeuangan:
    return ManajerKeuangan()

def clear_cache():
    st.cache_data.clear()

def page_header(title: str, subtitle: str, icon: str = ""):
    today = datetime.date.today()
    day_names = ["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu","Minggu"]
    month_names = ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agu","Sep","Okt","Nov","Des"]
    day_str = f"{day_names[today.weekday()]}, {today.day} {month_names[today.month-1]} {today.year}"
    st.markdown(f"""
        <div class="topbar">
            <div class="topbar-left">
                <div class="topbar-title">{icon + ' ' if icon else ''}{title}</div>
                <div class="topbar-subtitle">{subtitle}</div>
            </div>
            <div class="topbar-right">
                <div class="topbar-date-chip">📅 {day_str}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def metric_card(icon: str, label: str, value: str, color: str = "", delta: str = ""):
    delta_html = f'<div class="metric-delta">{delta}</div>' if delta else ""
    st.markdown(f"""
        <div class="metric-card {color}">
            <div class="metric-icon-box {color}">{icon}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-value {color}">{value}</div>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)

def empty_state(icon: str, text: str, sub: str = ""):
    sub_html = f'<div class="empty-state-sub">{sub}</div>' if sub else ""
    st.markdown(f"""
        <div class="empty-state">
            <div class="empty-state-icon">{icon}</div>
            <div class="empty-state-text">{text}</div>
            {sub_html}
        </div>
    """, unsafe_allow_html=True)

def set_toast(msg: str, is_error: bool = False):
    st.session_state["_toast_msg"] = msg
    st.session_state["_toast_is_error"] = is_error

def render_toast():
    if "_toast_msg" in st.session_state:
        msg = st.session_state.pop("_toast_msg")
        is_error = st.session_state.pop("_toast_is_error", False)
        if is_error:
            st.error(msg)
        else:
            st.success(msg)

# ── SIDEBAR ─────────────────────────────────────────────────
MENU_ITEMS = [
    ("Dashboard", "🏡", "Dashboard"),
    ("Keuangan", "💸", "Keuangan"),
    ("Log Kegiatan", "📋", "Log Kegiatan"),
    ("Target Tabungan", "🎯", "Target Tabungan"),
    ("Kebutuhan Kos", "🛒", "Kebutuhan Kos"),
]

def render_sidebar():
    if "sidebar_visible" not in st.session_state:
        st.session_state["sidebar_visible"] = True
    if "main_nav" not in st.session_state:
        st.session_state["main_nav"] = "Dashboard"

    # ── Sidebar hidden state ──
    if not st.session_state["sidebar_visible"]:
        # Inject CSS to hide sidebar + compensate layout
        st.markdown("""
            <style>
            [data-testid="stSidebar"] { display: none !important; }
            .main .block-container { padding-left: 1rem !important; }
            </style>
        """, unsafe_allow_html=True)
        # Floating toggle button to show sidebar again
        st.markdown('<div class="sidebar-toggle-btn">', unsafe_allow_html=True)
        if st.button("☰", key="btn_show_sidebar", help="Tampilkan menu"):
            st.session_state["sidebar_visible"] = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with st.sidebar:
        # ── Brand header with hide button ──
        col_brand, col_hide = st.columns([5, 1])
        with col_brand:
            st.markdown("""
                <div class="brand-left" style="padding:0.9rem 0 0.9rem 0.1rem;">
                    <div class="brand-icon-box">🏠</div>
                    <div class="brand-text">
                        <div class="brand-name">KOSTMATE</div>
                        <div class="brand-sub">Manajemen Kos</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        with col_hide:
            st.markdown("<div style='margin-top:0.85rem;'>", unsafe_allow_html=True)
            if st.button("✕", key="btn_hide_sidebar", help="Sembunyikan menu"):
                st.session_state["sidebar_visible"] = False
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

        # ── Profile card ──
        st.markdown("""
            <div class="profile-card">
                <div class="profile-avatar">🏠</div>
                <div class="profile-info">
                    <div class="profile-name">Penghuni Kos</div>
                    <div class="profile-role">Manajemen Pribadi</div>
                </div>
                <div class="profile-badge">AKTIF</div>
            </div>
        """, unsafe_allow_html=True)

        # ── Nav menu ──
        st.markdown('<div class="nav-section-label">Menu Utama</div>', unsafe_allow_html=True)

        for label, icon, value in MENU_ITEMS:
            is_active = st.session_state["main_nav"] == value
            wrapper_class = "nav-active" if is_active else "nav-inactive"
            st.markdown(f'<div class="{wrapper_class}">', unsafe_allow_html=True)
            if st.button(f"{icon}  {label}", key=f"nav_{value}", use_container_width=True):
                st.session_state["main_nav"] = value
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

        # ── Filter periode ──
        st.markdown('<div class="nav-section-label">Filter Periode</div>', unsafe_allow_html=True)
        today = datetime.date.today()
        bulan_names = ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agu","Sep","Okt","Nov","Des"]

        col_m, col_y = st.columns(2)
        with col_m:
            bulan_sel = st.selectbox("Bulan", range(1, 13),
                                     format_func=lambda x: bulan_names[x-1],
                                     index=today.month - 1,
                                     key="sel_bulan",
                                     label_visibility="collapsed")
        with col_y:
            tahun_sel = st.selectbox("Tahun", range(today.year - 3, today.year + 1),
                                     index=3,
                                     key="sel_tahun",
                                     label_visibility="collapsed")

        # ── Date info box ──
        st.markdown(f"""
            <div class="sidebar-date-box">
                <div class="sidebar-date-label">📅 Hari Ini</div>
                <div class="sidebar-date-val">{today.strftime('%d %B %Y')}</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Logout button ──
        st.markdown('<div class="logout-wrap">', unsafe_allow_html=True)
        if st.button("🚪  Keluar", key="btn_logout", use_container_width=True):
            for k in ["sidebar_visible", "main_nav"]:
                st.session_state.pop(k, None)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

    return st.session_state["main_nav"], bulan_sel, tahun_sel


# ── PAGE: DASHBOARD ─────────────────────────────────────────
def page_dashboard(mk: ManajerKeuangan, bulan: int, tahun: int):
    render_toast()
    today = datetime.date.today()
    bulan_names = ["Januari","Februari","Maret","April","Mei","Juni",
                   "Juli","Agustus","September","Oktober","November","Desember"]

    page_header("Dashboard", f"Ringkasan keuangan & aktivitas — {bulan_names[bulan-1]} {tahun}", "🏡")

    total_masuk = mk.hitung_total("pemasukan", bulan=bulan, tahun=tahun)
    total_keluar = mk.hitung_total("pengeluaran", bulan=bulan, tahun=tahun)
    saldo = total_masuk - total_keluar

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("💰", "Total Pemasukan", format_rp(total_masuk), "green")
    with c2:
        metric_card("💸", "Total Pengeluaran", format_rp(total_keluar), "red")
    with c3:
        metric_card("📊", "Saldo Bulan Ini", format_rp(saldo), saldo_color(saldo))
    with c4:
        df_log = mk.get_dataframe_log(tanggal=today)
        selesai = int(df_log[df_log["selesai"] == 1].shape[0]) if df_log is not None and not df_log.empty else 0
        total_log = int(df_log.shape[0]) if df_log is not None and not df_log.empty else 0
        metric_card("✅", "Tugas Selesai Hari Ini", f"{selesai}/{total_log}", "blue")

    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_r = st.columns([3, 2])
    with col_l:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📈 Tren Keuangan Harian</div>', unsafe_allow_html=True)
        df_tren = mk.get_tren_harian(bulan, tahun)
        if df_tren is not None and not df_tren.empty:
            df_tren["tanggal"] = pd.to_datetime(df_tren["tanggal"])
            df_tren = df_tren.set_index("tanggal")
            st.line_chart(df_tren[["pemasukan", "pengeluaran"]], height=220, color=["#8CD69D", "#FF9B9B"])
        else:
            empty_state("📈", "Belum ada data transaksi", "Tambahkan transaksi untuk melihat tren")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🗂️ Pengeluaran per Kategori</div>', unsafe_allow_html=True)
        cat_data = mk.get_pengeluaran_per_kategori(bulan=bulan, tahun=tahun)
        if cat_data:
            df_cat = pd.DataFrame(list(cat_data.items()), columns=["Kategori", "Total"])
            df_cat = df_cat.sort_values("Total", ascending=True).tail(6)
            st.bar_chart(df_cat.set_index("Kategori"), height=220, color="#9FA1FF")
        else:
            empty_state("🗂️", "Belum ada data", "Tambahkan pengeluaran terlebih dahulu")
        st.markdown('</div>', unsafe_allow_html=True)

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🕐 Transaksi Terbaru</div>', unsafe_allow_html=True)
        df_tr = mk.get_dataframe_transaksi(bulan=bulan, tahun=tahun)
        if df_tr is not None and not df_tr.empty:
            recent = df_tr.head(5)
            for _, row in recent.iterrows():
                icon = "➕" if row["tipe"] == "pemasukan" else "➖"
                color = "#1E5A34" if row["tipe"] == "pemasukan" else "#C53030"
                bg = "#D9F9DF" if row["tipe"] == "pemasukan" else "#FFE6E6"
                border_color = "#B5ECD0" if row["tipe"] == "pemasukan" else "#FFCDCD"
                st.markdown(f"""
                    <div style="display:flex;justify-content:space-between;align-items:center;
                                padding:0.8rem 1rem;border-left:4px solid {color};
                                border-radius:12px;margin-bottom:0.5rem;background:{bg};
                                border-top: 1px solid {border_color};
                                border-right: 1px solid {border_color};
                                border-bottom: 1px solid {border_color};">
                        <div>
                            <div style="font-size:0.875rem;font-weight:600;color:var(--text-dark);">
                                {icon} {row['deskripsi']}
                            </div>
                            <div style="font-size:0.75rem;color:var(--text-muted);margin-top:0.2rem;">
                                {row['kategori']} · {row['tanggal']}
                            </div>
                        </div>
                        <div style="font-weight:700;font-size:0.9rem;color:{color};margin-left:1rem;">
                            {format_rp(row['jumlah'])}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            empty_state("💳", "Belum ada transaksi")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🎯 Progress Target Tabungan</div>', unsafe_allow_html=True)
        df_tgt = mk.get_dataframe_target()
        if df_tgt is not None and not df_tgt.empty:
            for _, row in df_tgt.head(4).iterrows():
                pct = min((row["terkumpul"] / row["jumlah_target"]) * 100, 100) if row["jumlah_target"] > 0 else 0
                fill_class = "done" if pct >= 100 else ""
                st.markdown(f"""
                    <div style="margin-bottom:1.1rem;">
                        <div style="display:flex;justify-content:space-between;margin-bottom:0.4rem;">
                            <span style="font-size:0.875rem;font-weight:600;color:var(--text-dark);">{row['nama_target']}</span>
                            <span style="font-size:0.85rem;font-weight:700;color:{'#1E5A34' if pct>=100 else '#7B7DE5'};">{pct:.0f}%</span>
                        </div>
                        <div class="progress-wrap">
                            <div class="progress-fill {fill_class}" style="width:{pct}%;"></div>
                        </div>
                        <div style="font-size:0.75rem;color:var(--text-muted);margin-top:0.35rem;">
                            {format_rp(row['terkumpul'])} / {format_rp(row['jumlah_target'])}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            empty_state("🎯", "Belum ada target tabungan", "Tambahkan di menu Target Tabungan")
        st.markdown('</div>', unsafe_allow_html=True)

# ── PAGE: KEUANGAN ──────────────────────────────────────────
def page_keuangan(mk: ManajerKeuangan, bulan: int, tahun: int):
    render_toast()
    page_header("Keuangan", "Kelola pemasukan, pengeluaran, dan riwayat transaksi kamu", "💸")

    tab_tambah, tab_riwayat, tab_ringkasan = st.tabs(
        ["  ➕  Tambah Transaksi  ", "  📋  Riwayat  ", "  📊  Ringkasan  "]
    )

    with tab_tambah:
        st.markdown("<br>", unsafe_allow_html=True)
        col_form, col_info = st.columns([3, 2])

        with col_form:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📝 Formulir Transaksi Baru</div>', unsafe_allow_html=True)

            tipe = st.radio("Tipe Transaksi", ["💸 Pengeluaran", "💰 Pemasukan"],
                            horizontal=True, key="tipe_trx")
            is_pengeluaran = "Pengeluaran" in tipe

            deskripsi = st.text_input("Deskripsi *", placeholder="Contoh: Makan siang warung Bu Tini", key="trx_desc")
            jumlah = st.number_input("Jumlah (Rp) *", min_value=0.0, step=1000.0, format="%.0f", key="trx_amount")

            kat_list = KATEGORI_PENGELUARAN if is_pengeluaran else KATEGORI_PEMASUKAN
            kategori = st.selectbox("Kategori", kat_list, key="trx_kat")

            col_d, col_c = st.columns(2)
            with col_d:
                tanggal = st.date_input("Tanggal", value=datetime.date.today(), key="trx_date")
            with col_c:
                catatan = st.text_input("Catatan (opsional)", placeholder="...", key="trx_note")

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Simpan Transaksi", type="primary", use_container_width=True):
                if not deskripsi.strip():
                    st.error("⚠️ Deskripsi tidak boleh kosong.")
                elif jumlah <= 0:
                    st.error("⚠️ Jumlah harus lebih dari 0.")
                else:
                    trx = Transaksi(
                        tipe="pengeluaran" if is_pengeluaran else "pemasukan",
                        deskripsi=deskripsi.strip(),
                        jumlah=jumlah,
                        kategori=kategori,
                        tanggal=tanggal,
                        catatan=catatan.strip()
                    )
                    if mk.tambah_transaksi(trx):
                        clear_cache()
                        set_toast(f"✅ Transaksi '{deskripsi}' berhasil disimpan!")
                        st.rerun()
                    else:
                        st.error("❌ Gagal menyimpan transaksi. Coba lagi.")

            st.markdown('</div>', unsafe_allow_html=True)

        with col_info:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
                <div class="info-box">
                    <strong>💡 Tips Mencatat Transaksi</strong><br>
                    Biasakan mencatat pengeluaran di hari yang sama agar lebih akurat dan memudahkan perencanaan bulanan kamu.
                </div>
            """, unsafe_allow_html=True)
            total_hari = mk.hitung_total("pengeluaran", tanggal=datetime.date.today())
            total_masuk_hari = mk.hitung_total("pemasukan", tanggal=datetime.date.today())
            st.markdown(f"""
                <div class="section-card" style="margin-top:1rem;">
                    <div class="section-title">📅 Hari Ini</div>
                    <div style="margin-bottom:1rem; padding-bottom: 0.8rem; border-bottom: 1px solid rgba(159, 161, 255, 0.15);">
                        <div style="font-size:0.75rem;font-weight:700;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.35rem;">Pengeluaran</div>
                        <div style="font-size:1.45rem;font-weight:800;color:#C53030;">{format_rp(total_hari)}</div>
                    </div>
                    <div>
                        <div style="font-size:0.75rem;font-weight:700;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.35rem;">Pemasukan</div>
                        <div style="font-size:1.45rem;font-weight:800;color:#1E5A34;">{format_rp(total_masuk_hari)}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    with tab_riwayat:
        st.markdown("<br>", unsafe_allow_html=True)
        col_f1, col_f2, col_f3 = st.columns([2, 2, 1])
        with col_f1:
            filter_tipe = st.selectbox("Filter Tipe", options=["Semua", "Pengeluaran", "Pemasukan"], key="riwayat_tipe")
        with col_f2:
            filter_periode = st.selectbox("Filter Periode", ["Bulan Ini", "Hari Ini", "Semua Data"], key="riwayat_periode")
        with col_f3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Refresh", use_container_width=True):
                clear_cache()
                st.rerun()

        tipe_filter = None if filter_tipe == "Semua" else filter_tipe.lower()
        tgl_filter = datetime.date.today() if filter_periode == "Hari Ini" else None
        bln_filter = bulan if filter_periode == "Bulan Ini" else None
        thn_filter = tahun if filter_periode == "Bulan Ini" else None

        df = mk.get_dataframe_transaksi(tipe=tipe_filter, tanggal=tgl_filter, bulan=bln_filter, tahun=thn_filter)

        if df is None or df.empty:
            empty_state("📭", "Tidak ada transaksi ditemukan", "Tambahkan transaksi baru melalui tab 'Tambah Transaksi'")
        else:
            df_display = df.copy()
            df_display["jumlah"] = df_display["jumlah"].apply(format_rp)
            df_display.columns = [c.title().replace("_", " ") for c in df_display.columns]
            st.dataframe(df_display, use_container_width=True, hide_index=True, height=min(400, 56 + len(df_display) * 35))

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🗑️ Hapus Transaksi</div>', unsafe_allow_html=True)
            col_del1, col_del2 = st.columns([2, 1])
            with col_del1:
                id_hapus = st.number_input("Masukkan ID Transaksi yang ingin dihapus:", min_value=1, step=1, key="id_hapus_trx")
            with col_del2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️ Hapus", key="btn_hapus_trx", use_container_width=True):
                    st.session_state["konfirmasi_hapus_trx"] = int(id_hapus)

            if "konfirmasi_hapus_trx" in st.session_state:
                st.markdown(f"""
                    <div class="warning-box">
                        ⚠️ Yakin ingin menghapus transaksi ID <strong>{st.session_state['konfirmasi_hapus_trx']}</strong>?
                        Tindakan ini tidak dapat dibatalkan.
                    </div>
                """, unsafe_allow_html=True)
                c_ya, c_batal = st.columns(2)
                with c_ya:
                    if st.button("✅ Ya, Hapus", type="primary", use_container_width=True):
                        if mk.hapus_transaksi(st.session_state["konfirmasi_hapus_trx"]):
                            clear_cache()
                            del st.session_state["konfirmasi_hapus_trx"]
                            set_toast("✅ Transaksi berhasil dihapus.")
                            st.rerun()
                        else:
                            st.error("Gagal menghapus. Pastikan ID benar.")
                with c_batal:
                    if st.button("❌ Batal", use_container_width=True):
                        del st.session_state["konfirmasi_hapus_trx"]
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    with tab_ringkasan:
        st.markdown("<br>", unsafe_allow_html=True)
        bulan_names = ["Januari","Februari","Maret","April","Mei","Juni",
                       "Juli","Agustus","September","Oktober","November","Desember"]
        total_masuk = mk.hitung_total("pemasukan", bulan=bulan, tahun=tahun)
        total_keluar = mk.hitung_total("pengeluaran", bulan=bulan, tahun=tahun)
        saldo = total_masuk - total_keluar

        c1, c2, c3 = st.columns(3)
        with c1:
            metric_card("💰", f"Pemasukan {bulan_names[bulan-1]}", format_rp(total_masuk), "green")
        with c2:
            metric_card("💸", f"Pengeluaran {bulan_names[bulan-1]}", format_rp(total_keluar), "red")
        with c3:
            metric_card("📊", "Saldo Bersih", format_rp(saldo), saldo_color(saldo))

        st.markdown("<br>", unsafe_allow_html=True)
        cat_data = mk.get_pengeluaran_per_kategori(bulan=bulan, tahun=tahun)
        if cat_data:
            df_cat = pd.DataFrame(list(cat_data.items()), columns=["Kategori", "Total (Rp)"])
            df_cat = df_cat.sort_values("Total (Rp)", ascending=False).reset_index(drop=True)
            df_cat["Total (Rp)"] = df_cat["Total (Rp)"].apply(format_rp)
            col_tbl, col_chart = st.columns(2)
            with col_tbl:
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">🗂️ Tabel Kategori</div>', unsafe_allow_html=True)
                st.dataframe(df_cat, use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with col_chart:
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">📊 Grafik Kategori</div>', unsafe_allow_html=True)
                df_chart = pd.DataFrame(list(cat_data.items()), columns=["Kategori", "Total"])
                st.bar_chart(df_chart.set_index("Kategori"), color="#9FA1FF", height=280)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            empty_state("📊", "Belum ada data pengeluaran di bulan ini")

# ── PAGE: LOG KEGIATAN ──────────────────────────────────────
def page_log(mk: ManajerKeuangan):
    render_toast()
    page_header("Log Kegiatan Harian", "Pantau dan catat rutinitas harianmu agar lebih terstruktur", "📋")

    tab_hari_ini, tab_tambah_log, tab_semua = st.tabs(
        ["  📅  Hari Ini  ", "  ➕  Tambah Log  ", "  📚  Semua Riwayat  "]
    )

    with tab_hari_ini:
        st.markdown("<br>", unsafe_allow_html=True)
        today = datetime.date.today()
        df_log = mk.get_dataframe_log(tanggal=today)

        if df_log is None or df_log.empty:
            empty_state("📋", "Belum ada log untuk hari ini", "Tambahkan kegiatan harianmu di tab 'Tambah Log'")
        else:
            selesai_count = int(df_log[df_log["selesai"] == 1].shape[0])
            total_count = len(df_log)
            pct = int((selesai_count / total_count) * 100) if total_count > 0 else 0

            st.markdown(f"""
                <div style="margin-bottom:1.2rem;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.55rem;">
                        <span style="font-size:0.875rem;font-weight:700;color:var(--text-dark);">Progress Hari Ini</span>
                        <span style="font-size:0.875rem;font-weight:700;color:var(--primer-tua);">{selesai_count}/{total_count} selesai</span>
                    </div>
                    <div class="progress-wrap" style="height:10px;">
                        <div class="progress-fill {'done' if pct==100 else ''}" style="width:{pct}%;"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            for _, row in df_log.iterrows():
                done = int(row["selesai"]) == 1
                done_class = "done" if done else ""
                dot_class = "done" if done else ""
                durasi_str = f"{row['durasi_menit']} menit" if row.get('durasi_menit', 0) > 0 else ""
                waktu_str = f"⏰ {row['waktu']}" if row.get('waktu') else ""
                meta_parts = [p for p in [waktu_str, durasi_str, row.get('kategori','')] if p]

                col_log, col_act = st.columns([8, 2])
                with col_log:
                    st.markdown(f"""
                        <div class="log-item {done_class}">
                            <div class="log-dot {dot_class}"></div>
                            <div>
                                <div class="log-name">{'✅ ' if done else ''}{row['aktivitas']}</div>
                                <div class="log-meta">{' · '.join(meta_parts)}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                with col_act:
                    btn_label = "↩️ Batal" if done else "✅ Selesai"
                    if st.button(btn_label, key=f"toggle_log_{row['id']}", use_container_width=True):
                        if mk.toggle_selesai(int(row["id"])):
                            status = "dibatalkan" if done else "diselesaikan"
                            set_toast(f"✅ Kegiatan '{row['aktivitas']}' berhasil {status}!")
                            st.rerun()
                        else:
                            st.error("❌ Gagal mengubah status kegiatan.")

    with tab_tambah_log:
        st.markdown("<br>", unsafe_allow_html=True)
        col_f, col_i = st.columns([3, 2])

        with col_f:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📝 Tambah Log Kegiatan</div>', unsafe_allow_html=True)

            aktivitas = st.text_input("Nama Aktivitas *", placeholder="Contoh: Olahraga pagi 30 menit", key="log_act")
            col_k, col_d2 = st.columns(2)
            with col_k:
                kat_log = st.selectbox("Kategori", KATEGORI_LOG, key="log_kat")
            with col_d2:
                durasi = st.number_input("Durasi (menit)", min_value=0, step=5, key="log_dur", value=30)

            col_tgl, col_wkt = st.columns(2)
            with col_tgl:
                tgl_log = st.date_input("Tanggal", value=datetime.date.today(), key="log_date")
            with col_wkt:
                waktu_log = st.text_input("Waktu (opsional)", placeholder="07:00", key="log_time")

            catatan_log = st.text_area("Catatan (opsional)", placeholder="Keterangan tambahan...", key="log_note", height=80)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Simpan Log", type="primary", use_container_width=True):
                if not aktivitas.strip():
                    st.error("⚠️ Nama aktivitas tidak boleh kosong.")
                else:
                    log = LogKegiatan(
                        aktivitas=aktivitas.strip(),
                        kategori=kat_log,
                        durasi_menit=durasi,
                        tanggal=tgl_log,
                        waktu=waktu_log.strip(),
                        catatan=catatan_log.strip()
                    )
                    if mk.tambah_log(log):
                        set_toast(f"✅ Log '{aktivitas}' berhasil disimpan!")
                        st.rerun()
                    else:
                        st.error("❌ Gagal menyimpan log.")

            st.markdown('</div>', unsafe_allow_html=True)

        with col_i:
            st.markdown("""
                <div class="info-box" style="margin-top:1rem;">
                    <strong>📌 Tips Produktivitas</strong><br>
                    Catat kegiatanmu setiap hari untuk membangun kebiasaan positif. Tandai sebagai selesai setelah aktivitas dilakukan!
                </div>
            """, unsafe_allow_html=True)

    with tab_semua:
        st.markdown("<br>", unsafe_allow_html=True)
        col_rf, col_rb = st.columns([4, 1])
        with col_rb:
            if st.button("🔄 Refresh", use_container_width=True, key="refresh_log"):
                st.rerun()

        df_all = mk.get_dataframe_log()
        if df_all is None or df_all.empty:
            empty_state("📚", "Belum ada log kegiatan", "Mulai catat aktivitasmu sekarang!")
        else:
            df_all["selesai"] = df_all["selesai"].apply(lambda x: "✅ Selesai" if x else "⏳ Belum")
            df_display = df_all.drop(columns=["catatan"], errors="ignore")
            df_display.columns = [c.title().replace("_", " ") for c in df_display.columns]
            st.dataframe(df_display, use_container_width=True, hide_index=True, height=350)

            st.markdown('<div class="section-card" style="margin-top:1rem;">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🗑️ Hapus Log</div>', unsafe_allow_html=True)
            col_del1, col_del2 = st.columns([3, 1])
            with col_del1:
                id_log_hapus = st.number_input("ID Log yang akan dihapus:", min_value=1, step=1, key="id_hapus_log")
            with col_del2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️ Hapus Log", key="btn_hapus_log", use_container_width=True):
                    if mk.hapus_log(int(id_log_hapus)):
                        set_toast(f"✅ Log ID {int(id_log_hapus)} berhasil dihapus!")
                        st.rerun()
                    else:
                        st.error(f"❌ Gagal menghapus log. Pastikan ID {int(id_log_hapus)} benar.")
            st.markdown('</div>', unsafe_allow_html=True)

# ── PAGE: KEBUTUHAN KOS ─────────────────────────────────────
def page_kebutuhan(mk: ManajerKeuangan):
    render_toast()
    page_header("Kebutuhan Kos", "Pantau tagihan bulanan dan checklist belanja harianmu", "🛒")

    tab_tagihan, tab_belanja = st.tabs(
        ["  🔔  Tagihan Bulanan  ", "  🛒  Checklist Belanja  "]
    )

    with tab_tagihan:
        st.markdown("<br>", unsafe_allow_html=True)
        col_list, col_form = st.columns([3, 2])

        with col_list:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🔔 Daftar Tagihan</div>', unsafe_allow_html=True)

            df_tagihan = mk.get_dataframe_tagihan()
            if df_tagihan is None or df_tagihan.empty:
                empty_state("🔔", "Belum ada tagihan", "Tambahkan tagihan di sebelah kanan")
            else:
                belum_bayar = df_tagihan[df_tagihan["sudah_bayar"] == 0]
                sudah_bayar = df_tagihan[df_tagihan["sudah_bayar"] == 1]
                total_tagihan = df_tagihan["jumlah"].sum()

                st.markdown(f"""
                    <div style="display:flex;gap:0.75rem;margin-bottom:1.2rem;">
                        <div class="stat-chip" style="background:#FFE6E6; border: 1px solid rgba(197, 48, 48, 0.2);">
                            <div class="stat-chip-label" style="color:#C53030;">Belum Bayar</div>
                            <div class="stat-chip-val" style="color:#C53030;">{len(belum_bayar)}</div>
                        </div>
                        <div class="stat-chip" style="background:#D9F9DF; border: 1px solid rgba(30, 90, 52, 0.2);">
                            <div class="stat-chip-label" style="color:#1E5A34;">Lunas</div>
                            <div class="stat-chip-val" style="color:#1E5A34;">{len(sudah_bayar)}</div>
                        </div>
                        <div class="stat-chip" style="background:#F0F4FF; border: 1px solid rgba(159, 161, 255, 0.2);">
                            <div class="stat-chip-label" style="color:#7B7DE5;">Total</div>
                            <div class="stat-chip-val" style="color:#7B7DE5;font-size:1.2rem;">{format_rp(total_tagihan)}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                for _, row in df_tagihan.iterrows():
                    lunas = int(row["sudah_bayar"]) == 1
                    badge = '<span class="badge badge-green">✅ Lunas</span>' if lunas else '<span class="badge badge-red">⏳ Belum</span>'
                    col_t, col_a = st.columns([7, 3])
                    with col_t:
                        st.markdown(f"""
                            <div class="log-item {'done' if lunas else ''}">
                                <div class="log-dot {'done' if lunas else ''}"></div>
                                <div style="flex:1;">
                                    <div style="display:flex;justify-content:space-between;align-items:center;">
                                        <div class="log-name">{row['nama']}</div>
                                        {badge}
                                    </div>
                                    <div class="log-meta">
                                        {row['kategori']} · Jatuh tempo: {row['tanggal_jatuh_tempo']} · {format_rp(row['jumlah'])}
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    with col_a:
                        btn_label = "↩️ Batal" if lunas else "✅ Lunas"
                        col_b1, col_b2 = st.columns(2)
                        with col_b1:
                            if st.button(btn_label, key=f"bayar_{row['id']}", use_container_width=True):
                                if mk.toggle_bayar_tagihan(int(row["id"])):
                                    status_baru = "belum dibayar" if lunas else "lunas"
                                    set_toast(f"✅ Tagihan '{row['nama']}' ditandai {status_baru}!")
                                    st.rerun()
                                else:
                                    st.error("❌ Gagal mengubah status tagihan.")
                        with col_b2:
                            if st.button("🗑️", key=f"hapus_tagihan_{row['id']}", use_container_width=True):
                                if mk.hapus_tagihan(int(row["id"])):
                                    set_toast(f"✅ Tagihan '{row['nama']}' berhasil dihapus!")
                                    st.rerun()
                                else:
                                    st.error("❌ Gagal menghapus tagihan.")

            st.markdown('</div>', unsafe_allow_html=True)

        with col_form:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">➕ Tambah Tagihan</div>', unsafe_allow_html=True)

            nama_tagihan = st.text_input("Nama Tagihan *", placeholder="Contoh: Sewa kos bulan Juli", key="t_nama")
            kat_tagihan = st.selectbox("Kategori", options=KATEGORI_TAGIHAN, key="t_kat")
            jumlah_tagihan = st.number_input("Jumlah (Rp) *", min_value=0.0, step=10000.0, format="%.0f", key="t_jumlah")
            jatuh_tempo = st.date_input("Tanggal Jatuh Tempo", key="t_tempo")
            catatan_tagihan = st.text_input("Catatan (opsional)", key="t_catatan")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Simpan Tagihan", type="primary", use_container_width=True, key="btn_simpan_tagihan"):
                if not nama_tagihan.strip():
                    st.error("⚠️ Nama tagihan tidak boleh kosong.")
                elif jumlah_tagihan <= 0:
                    st.error("⚠️ Jumlah harus lebih dari 0.")
                else:
                    tgh = Tagihan(
                        nama=nama_tagihan.strip(),
                        kategori=kat_tagihan,
                        jumlah=jumlah_tagihan,
                        tanggal_jatuh_tempo=jatuh_tempo,
                        catatan=catatan_tagihan.strip()
                    )
                    if mk.tambah_tagihan(tgh):
                        set_toast(f"✅ Tagihan '{nama_tagihan}' berhasil ditambahkan!")
                        st.rerun()
                    else:
                        st.error("❌ Gagal menyimpan tagihan.")

            st.markdown('</div>', unsafe_allow_html=True)

    with tab_belanja:
        st.markdown("<br>", unsafe_allow_html=True)
        col_list2, col_form2 = st.columns([3, 2])

        with col_list2:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🛒 Daftar Belanja</div>', unsafe_allow_html=True)

            df_belanja = mk.get_dataframe_belanja()
            if df_belanja is None or df_belanja.empty:
                empty_state("🛒", "Daftar belanja kosong", "Tambahkan item atau gunakan template default")
            else:
                sudah = int(df_belanja[df_belanja["sudah_beli"] == 1].shape[0])
                total_b = len(df_belanja)
                pct_b = int((sudah / total_b) * 100) if total_b > 0 else 0

                st.markdown(f"""
                    <div style="margin-bottom:1.2rem;">
                        <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
                            <span style="font-size:0.875rem;font-weight:700;color:var(--text-dark);">Progress Belanja</span>
                            <span style="font-size:0.875rem;font-weight:700;color:var(--primer-tua);">{sudah}/{total_b} item</span>
                        </div>
                        <div class="progress-wrap" style="height:10px;">
                            <div class="progress-fill {'done' if pct_b==100 else ''}" style="width:{pct_b}%;"></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                for _, row in df_belanja.iterrows():
                    beli = int(row["sudah_beli"]) == 1
                    col_item, col_aksi = st.columns([7, 3])
                    with col_item:
                        st.markdown(f"""
                            <div class="log-item {'done' if beli else ''}">
                                <div class="log-dot {'done' if beli else ''}"></div>
                                <div>
                                    <div class="log-name">{'✅ ' if beli else ''}{row['nama']}</div>
                                    <div class="log-meta">Qty: {row['jumlah']}{' · ' + row['catatan'] if row.get('catatan') else ''}</div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    with col_aksi:
                        btn_b = "↩️ Batal" if beli else "✅ Beli"
                        cb1, cb2 = st.columns(2)
                        with cb1:
                            if st.button(btn_b, key=f"beli_{row['id']}", use_container_width=True):
                                if mk.toggle_beli(int(row["id"])):
                                    status_baru = "belum dibeli" if beli else "sudah dibeli"
                                    set_toast(f"✅ '{row['nama']}' ditandai {status_baru}!")
                                    st.rerun()
                                else:
                                    st.error("❌ Gagal mengubah status item.")
                        with cb2:
                            if st.button("🗑️", key=f"hapus_belanja_{row['id']}", use_container_width=True):
                                if mk.hapus_item_belanja(int(row["id"])):
                                    set_toast(f"✅ '{row['nama']}' berhasil dihapus dari daftar!")
                                    st.rerun()
                                else:
                                    st.error("❌ Gagal menghapus item belanja.")

            st.markdown('</div>', unsafe_allow_html=True)

        with col_form2:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">➕ Tambah Item Belanja</div>', unsafe_allow_html=True)

            nama_item = st.text_input("Nama Item *", placeholder="Contoh: Sabun mandi", key="b_nama")
            jumlah_item = st.text_input("Jumlah", placeholder="Contoh: 1 botol, 500gr", key="b_jumlah", value="1")
            catatan_item = st.text_input("Catatan (opsional)", placeholder="...", key="b_catatan")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Tambah Item", type="primary", use_container_width=True, key="btn_tambah_item"):
                if not nama_item.strip():
                    st.error("⚠️ Nama item tidak boleh kosong.")
                else:
                    itm = ItemBelanja(
                        nama=nama_item.strip(),
                        jumlah=jumlah_item.strip(),
                        catatan=catatan_item.strip()
                    )
                    if mk.tambah_item_belanja(itm):
                        set_toast(f"✅ '{nama_item}' ditambahkan ke daftar belanja!")
                        st.rerun()
                    else:
                        st.error("❌ Gagal menambahkan item.")

            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown('<div style="font-size:0.8rem;font-weight:600;color:#64748b;margin-bottom:0.5rem;">⚡ Template Cepat</div>', unsafe_allow_html=True)
            if st.button("📋 Tambahkan Semua Item Umum", use_container_width=True, key="btn_template"):
                berhasil = 0
                for nama_default in ITEM_BELANJA_DEFAULT:
                    itm = ItemBelanja(nama=nama_default, jumlah="1")
                    if mk.tambah_item_belanja(itm):
                        berhasil += 1
                set_toast(f"✅ {berhasil} item berhasil ditambahkan ke daftar belanja!")
                st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

# ── PAGE: TARGET TABUNGAN ───────────────────────────────────
def page_target(mk: ManajerKeuangan):
    render_toast()
    page_header("Target Tabungan", "Tetapkan tujuan keuangan dan pantau progres menabungmu", "🎯")

    tab_list, tab_add = st.tabs(["  🎯  Target Saya  ", "  ➕  Buat Target Baru  "])

    with tab_list:
        st.markdown("<br>", unsafe_allow_html=True)
        df_tgt = mk.get_dataframe_target()

        if df_tgt is None or df_tgt.empty:
            empty_state("🎯", "Belum ada target tabungan", "Buat target pertamamu di tab 'Buat Target Baru'")
        else:
            for _, row in df_tgt.iterrows():
                pct = min((row["terkumpul"] / row["jumlah_target"]) * 100, 100) if row["jumlah_target"] > 0 else 0
                fill_class = "done" if pct >= 100 else ""
                sisa = max(row["jumlah_target"] - row["terkumpul"], 0)
                deadline_str = f"🗓️ {row['deadline']}" if row.get('deadline') else ""
                pct_color = "#1E5A34" if pct >= 100 else "#7B7DE5"

                st.markdown(f"""
                    <div class="section-card">
                        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.9rem;">
                            <div>
                                <div style="font-size:1.05rem;font-weight:800;color:var(--text-dark);">{row['nama_target']}</div>
                                <div style="font-size:0.78rem;color:var(--text-muted);margin-top:0.25rem;">{row.get('deskripsi','')} {deadline_str}</div>
                            </div>
                            <div style="text-align:right;">
                                <div style="font-size:1.4rem;font-weight:800;color:{pct_color};">{pct:.0f}%</div>
                                <div style="font-size:0.68rem;color:var(--text-muted);font-weight:600;text-transform:uppercase;letter-spacing:0.05em;">terkumpul</div>
                            </div>
                        </div>
                        <div class="progress-wrap" style="height:10px;">
                            <div class="progress-fill {fill_class}" style="width:{pct:.1f}%;"></div>
                        </div>
                        <div style="display:flex;justify-content:space-between;margin-top:0.75rem;font-size:0.78rem;color:var(--text-muted);">
                            <span>Terkumpul: <strong style="color:#1E5A34;">{format_rp(row['terkumpul'])}</strong></span>
                            <span>Target: <strong style="color:#7B7DE5;">{format_rp(row['jumlah_target'])}</strong></span>
                            <span>Sisa: <strong style="color:#C53030;">{format_rp(sisa)}</strong></span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                col_tambah, col_hapus = st.columns([3, 1])
                with col_tambah:
                    tambahan = st.number_input(
                        f"Tambah tabungan (ID {row['id']})", min_value=0.0, step=10000.0, format="%.0f",
                        key=f"tambah_tgt_{row['id']}", label_visibility="collapsed",
                        placeholder=f"Tambah dana ke '{row['nama_target']}'..."
                    )
                    if st.button(f"➕ Tambah Dana", key=f"btn_tambah_tgt_{row['id']}"):
                        if tambahan <= 0:
                            st.warning("⚠️ Masukkan jumlah dana yang ingin ditambahkan.")
                        elif mk.update_terkumpul(int(row["id"]), tambahan):
                            set_toast(f"✅ {format_rp(tambahan)} berhasil ditambahkan ke '{row['nama_target']}'!")
                            st.rerun()
                        else:
                            st.error("❌ Gagal menambahkan dana.")
                with col_hapus:
                    if st.button("🗑️ Hapus", key=f"btn_hapus_tgt_{row['id']}", use_container_width=True):
                        if mk.hapus_target(int(row["id"])):
                            set_toast(f"✅ Target '{row['nama_target']}' berhasil dihapus!")
                            st.rerun()
                        else:
                            st.error("❌ Gagal menghapus target.")

    with tab_add:
        st.markdown("<br>", unsafe_allow_html=True)
        col_f, col_i = st.columns([3, 2])

        with col_f:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🎯 Buat Target Tabungan Baru</div>', unsafe_allow_html=True)

            nama_target = st.text_input("Nama Target *", placeholder="Contoh: Laptop baru, Mudik Lebaran...", key="tgt_name")
            jumlah_target = st.number_input("Jumlah Target (Rp) *", min_value=0.0, step=50000.0, format="%.0f", key="tgt_amount")
            terkumpul_awal = st.number_input("Sudah Terkumpul (Rp)", min_value=0.0, step=10000.0, format="%.0f", key="tgt_terkumpul")

            col_dl, col_desc = st.columns(2)
            with col_dl:
                gunakan_deadline = st.checkbox("Tambah deadline", key="tgt_use_dl")
                if gunakan_deadline:
                    deadline_val = st.date_input("Deadline",
                                                  value=datetime.date.today() + datetime.timedelta(days=90),
                                                  key="tgt_deadline")
                else:
                    deadline_val = None
            with col_desc:
                deskripsi_tgt = st.text_input("Deskripsi singkat", placeholder="Untuk apa target ini?", key="tgt_desc")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Buat Target", type="primary", use_container_width=True):
                if not nama_target.strip():
                    st.error("⚠️ Nama target tidak boleh kosong.")
                elif jumlah_target <= 0:
                    st.error("⚠️ Jumlah target harus lebih dari 0.")
                else:
                    tgt = TargetTabungan(
                        nama_target=nama_target.strip(),
                        jumlah_target=jumlah_target,
                        terkumpul=terkumpul_awal,
                        deadline=deadline_val,
                        deskripsi=deskripsi_tgt.strip()
                    )
                    if mk.tambah_target(tgt):
                        set_toast(f"✅ Target '{nama_target}' berhasil dibuat!")
                        st.rerun()
                    else:
                        st.error("❌ Gagal membuat target.")

            st.markdown('</div>', unsafe_allow_html=True)

        with col_i:
            st.markdown("""
                <div class="success-box" style="margin-top:1rem;">
                    <strong>🌟 Kenapa penting punya target?</strong><br>
                    Punya tujuan keuangan yang jelas membantu kamu lebih disiplin dalam mengelola uang saku dan menghindari pengeluaran impulsif.
                </div>
                <div class="info-box" style="margin-top:0.75rem;">
                    <strong>💡 Strategi menabung</strong><br>
                    Coba metode 50/30/20: 50% kebutuhan, 30% keinginan, 20% tabungan. Sesuaikan dengan kondisi kamu!
                </div>
            """, unsafe_allow_html=True)

# ── MAIN ────────────────────────────────────────────────────
def main():
    menu, bulan, tahun = render_sidebar()
    mk = get_manajer()

    if menu == "Dashboard":
        page_dashboard(mk, bulan, tahun)
    elif menu == "Keuangan":
        page_keuangan(mk, bulan, tahun)
    elif menu == "Log Kegiatan":
        page_log(mk)
    elif menu == "Target Tabungan":
        page_target(mk)
    elif menu == "Kebutuhan Kos":
        page_kebutuhan(mk)

if __name__ == "__main__":
    main()