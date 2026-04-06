import streamlit as st
import pandas as pd
import plotly.express as px
import time
from data.canteen_data import MENU, CANTEEN_MAP
from core.searching import binary_search, linear_search, karatsuba_multiplication
from core.optimization import knapsack_dp, knapsack_greedy
from core.scheduling import job_scheduling_deadlines
from core.pathfinding import dijkstra, get_multi_stop_route, floyd_warshall
from core.constraints import graph_coloring, tsp_branch_and_bound

# Page Settings
st.set_page_config(page_title="FlavorFlow Pro | DAA Academic Project", layout="wide")

# --- GLOBAL CSS: PURE WHITE THEME, ORANGE ACCENTS, BLACK TEXT ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

    :root {
        --bg: #f4f6fb;
        --surface: rgba(255, 255, 255, 0.92);
        --surface-strong: #ffffff;
        --surface-soft: #fff8f4;
        --border: rgba(15, 23, 42, 0.08);
        --text: #0f172a;
        --muted: #5b6475;
        --accent: #ff5a1f;
        --accent-deep: #d94816;
        --accent-2: #0f766e;
        --accent-3: #1d4ed8;
        --shadow: 0 24px 72px rgba(15, 23, 42, 0.12);
        --shadow-soft: 0 12px 30px rgba(15, 23, 42, 0.08);
        --radius-xl: 30px;
        --radius-lg: 22px;
        --radius-md: 16px;
    }

    html, body, [class*="css"]  {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: var(--text) !important;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(255, 90, 31, 0.14), transparent 26%),
            radial-gradient(circle at 85% 10%, rgba(29, 78, 216, 0.10), transparent 18%),
            radial-gradient(circle at top right, rgba(15, 118, 110, 0.10), transparent 24%),
            linear-gradient(180deg, #fffdfb 0%, var(--bg) 100%);
        color: var(--text) !important;
    }

    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        pointer-events: none;
        background-image: linear-gradient(rgba(15, 23, 42, 0.02) 1px, transparent 1px), linear-gradient(90deg, rgba(15, 23, 42, 0.02) 1px, transparent 1px);
        background-size: 32px 32px;
        mask-image: linear-gradient(180deg, rgba(0,0,0,0.18), transparent 70%);
        z-index: 0;
    }

    .block-container {
        padding-top: 1.85rem;
        padding-bottom: 2.5rem;
        max-width: 1320px;
    }

    h1, h2, h3, h4 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: var(--text) !important;
        letter-spacing: -0.03em;
    }

    p, span, label, li {
        color: var(--text) !important;
    }

    .stMarkdown p,
    .stMarkdown li {
        color: var(--muted) !important;
        line-height: 1.7;
    }

    .hero-shell {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.96), rgba(255, 247, 242, 0.92));
        border: 1px solid rgba(255, 90, 31, 0.14);
        border-radius: var(--radius-xl);
        padding: 2rem 2rem 1.55rem;
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
        margin-bottom: 1.3rem;
    }

    .hero-shell::after {
        content: '';
        position: absolute;
        inset: auto -70px -90px auto;
        width: 240px;
        height: 240px;
        background: radial-gradient(circle, rgba(255, 90, 31, 0.18), transparent 65%);
        pointer-events: none;
    }

    .hero-shell::before {
        content: '';
        position: absolute;
        inset: 0 auto auto 0;
        width: 180px;
        height: 180px;
        background: radial-gradient(circle, rgba(29, 78, 216, 0.10), transparent 70%);
        pointer-events: none;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(255, 90, 31, 0.10);
        color: var(--accent) !important;
        border: 1px solid rgba(255, 90, 31, 0.18);
        border-radius: 999px;
        padding: 0.45rem 0.85rem;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        margin-bottom: 0.85rem;
    }

    .hero-title {
        font-size: clamp(2rem, 3.6vw, 3.2rem);
        line-height: 1.04;
        margin: 0 0 0.65rem 0;
    }

    .hero-subtitle {
        max-width: 760px;
        color: var(--muted) !important;
        font-size: 1.02rem;
        line-height: 1.7;
        margin: 0;
    }

    .menu-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(255,255,255,0.92));
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 14px;
        text-align: center;
        box-shadow: var(--shadow-soft);
        margin-bottom: 20px;
        transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
    }

    .menu-card:hover {
        transform: translateY(-4px);
        border-color: rgba(255, 90, 31, 0.26);
        box-shadow: 0 20px 40px rgba(15, 23, 42, 0.12);
    }

    .menu-card img {
        width: 100%;
        height: 180px;
        object-fit: contain;
        background: linear-gradient(180deg, #fffaf6 0%, #ffffff 100%);
        border-radius: 14px;
        border: 1px solid rgba(15, 23, 42, 0.06);
        padding: 6px;
    }

    .menu-card h4 {
        margin-top: 0.8rem;
        margin-bottom: 0.35rem;
        font-size: 1.05rem;
    }

    .menu-card p {
        margin-bottom: 0.15rem;
        color: var(--muted) !important;
        font-size: 0.92rem;
    }

    .info-box {
        background: linear-gradient(135deg, rgba(255, 90, 31, 0.08), rgba(255, 255, 255, 0.98));
        border: 1px solid rgba(255, 90, 31, 0.12);
        border-left: 6px solid var(--accent);
        padding: 1.2rem 1.25rem;
        border-radius: var(--radius-md);
        margin-bottom: 1rem;
        box-shadow: var(--shadow-soft);
    }

    .info-box h3, .info-box h4 {
        margin-top: 0;
        margin-bottom: 0.6rem;
    }

    .winner-tag {
        display: inline-flex;
        align-items: center;
        background: linear-gradient(135deg, var(--accent), #ff8f59);
        color: white !important;
        padding: 0.28rem 0.8rem;
        border-radius: 999px;
        font-weight: 800;
        letter-spacing: 0.02em;
        box-shadow: 0 10px 24px rgba(255, 90, 31, 0.24);
    }

    .section-title {
        display: flex;
        align-items: baseline;
        gap: 0.7rem;
        margin: 0.4rem 0 0.75rem;
    }

    .section-title h2,
    .section-title h3 {
        margin: 0;
        font-size: 1.55rem;
    }

    .section-title span {
        color: var(--muted) !important;
        font-size: 0.92rem;
    }

    .quick-strip {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.85rem;
        margin: 0 0 1rem;
    }

    .quick-chip {
        background: rgba(255,255,255,0.78);
        border: 1px solid rgba(15, 23, 42, 0.08);
        border-radius: 18px;
        padding: 0.9rem 1rem;
        box-shadow: var(--shadow-soft);
    }

    .quick-chip strong {
        display: block;
        font-size: 0.98rem;
        margin-bottom: 0.25rem;
        color: var(--text) !important;
    }

    .quick-chip span {
        color: var(--muted) !important;
        font-size: 0.9rem;
    }

    .topbar {
        display: grid;
        grid-template-columns: 1.2fr 1.4fr 0.9fr;
        gap: 0.9rem;
        align-items: center;
        margin-bottom: 1rem;
    }

    .topbar-brand {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        background: rgba(255,255,255,0.8);
        border: 1px solid rgba(15, 23, 42, 0.08);
        border-radius: 18px;
        padding: 0.75rem 0.9rem;
        box-shadow: var(--shadow-soft);
    }

    .topbar-mark {
        width: 38px;
        height: 38px;
        border-radius: 12px;
        display: grid;
        place-items: center;
        background: linear-gradient(135deg, var(--accent), #ff8f59);
        color: white !important;
        font-size: 1.05rem;
        font-weight: 800;
    }

    .topbar-name {
        margin: 0;
        font-size: 1.05rem;
        line-height: 1.1;
    }

    .topbar-note {
        margin: 0.08rem 0 0;
        font-size: 0.84rem;
        color: var(--muted) !important;
    }

    .topbar-search,
    .topbar-meta {
        background: rgba(255,255,255,0.8);
        border: 1px solid rgba(15, 23, 42, 0.08);
        border-radius: 18px;
        padding: 0.65rem 0.8rem;
        box-shadow: var(--shadow-soft);
    }

    .topbar-meta {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.7rem;
    }

    .topbar-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.4rem 0.7rem;
        border-radius: 999px;
        background: rgba(255, 90, 31, 0.10);
        color: var(--accent) !important;
        font-size: 0.8rem;
        font-weight: 800;
    }

    .catalog-panel,
    .cart-panel {
        background: rgba(255,255,255,0.9);
        border: 1px solid rgba(15, 23, 42, 0.08);
        border-radius: 26px;
        box-shadow: var(--shadow);
    }

    .catalog-panel {
        padding: 1rem 1rem 0.25rem;
    }

    .cart-panel {
        padding: 1rem;
        position: sticky;
        top: 1rem;
    }

    .menu-filter-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.65rem;
        margin: 0.25rem 0 1rem;
    }

    .filter-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        padding: 0.55rem 0.9rem;
        border-radius: 999px;
        border: 1px solid rgba(15, 23, 42, 0.08);
        background: rgba(255,255,255,0.76);
        color: var(--muted) !important;
        font-size: 0.88rem;
        font-weight: 700;
    }

    .filter-chip-active {
        background: linear-gradient(135deg, rgba(255, 90, 31, 0.14), rgba(255, 122, 69, 0.18));
        border-color: rgba(255, 90, 31, 0.18);
        color: var(--text) !important;
    }

    .menu-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.95rem;
    }

    .product-card {
        background: #ffffff;
        border: 1px solid rgba(15, 23, 42, 0.08);
        border-radius: 22px;
        overflow: hidden;
        box-shadow: var(--shadow-soft);
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        height: 100%;
    }

    .product-card:hover {
        transform: translateY(-4px);
        border-color: rgba(255, 90, 31, 0.22);
        box-shadow: 0 18px 36px rgba(15, 23, 42, 0.12);
    }

    .product-image {
        height: 175px;
        width: 100%;
        object-fit: cover;
        display: block;
    }

    .product-body {
        padding: 0.85rem 0.9rem 0.95rem;
    }

    .product-name {
        margin: 0 0 0.35rem;
        font-size: 1rem;
        line-height: 1.2;
    }

    .product-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.7rem;
        color: var(--muted) !important;
        font-size: 0.84rem;
    }

    .product-price {
        font-weight: 900;
        color: var(--text) !important;
    }

    .product-actions {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.6rem;
    }

    .mini-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        border-radius: 999px;
        background: rgba(15, 118, 110, 0.10);
        color: var(--accent-2) !important;
        font-size: 0.76rem;
        padding: 0.3rem 0.55rem;
        font-weight: 800;
    }

    .cart-head {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.8rem;
        margin-bottom: 0.8rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid rgba(15, 23, 42, 0.08);
    }

    .cart-head h3 {
        margin: 0;
        font-size: 1.2rem;
    }

    .cart-subtext {
        color: var(--muted) !important;
        font-size: 0.84rem;
        margin: 0.12rem 0 0;
    }

    .cart-item {
        display: grid;
        grid-template-columns: 54px 1fr auto;
        gap: 0.75rem;
        align-items: center;
        background: rgba(255,255,255,0.9);
        border: 1px solid rgba(15, 23, 42, 0.08);
        border-radius: 18px;
        padding: 0.7rem;
        margin-bottom: 0.7rem;
        box-shadow: var(--shadow-soft);
    }

    .cart-item img {
        width: 54px;
        height: 54px;
        border-radius: 14px;
        object-fit: cover;
    }

    .cart-item-title {
        margin: 0;
        font-size: 0.94rem;
        font-weight: 800;
    }

    .cart-item-meta {
        margin: 0.1rem 0 0;
        color: var(--muted) !important;
        font-size: 0.82rem;
    }

    .cart-summary {
        background: linear-gradient(135deg, rgba(255, 90, 31, 0.08), rgba(255,255,255,0.96));
        border: 1px solid rgba(255, 90, 31, 0.10);
        border-radius: 20px;
        padding: 0.85rem;
        margin: 0.8rem 0;
    }

    .cart-summary-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.8rem;
        margin-bottom: 0.35rem;
        font-size: 0.92rem;
    }

    .cart-summary-row strong {
        color: var(--text) !important;
    }

    .payment-box {
        background: rgba(255,255,255,0.84);
        border: 1px solid rgba(15, 23, 42, 0.08);
        border-radius: 18px;
        padding: 0.8rem;
        margin-top: 0.85rem;
    }

    .action-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.65rem;
        margin-top: 0.85rem;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(255,255,255,0.99), rgba(255,249,244,0.96)) !important;
        border-right: 1px solid rgba(15, 23, 42, 0.06);
        box-shadow: 10px 0 36px rgba(15, 23, 42, 0.05);
    }

    [data-testid="stSidebar"] > div {
        padding-top: 1.2rem;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: var(--text) !important;
    }

    .sidebar-brand {
        padding: 0.35rem 0.35rem 1rem;
        border-bottom: 1px solid rgba(15, 23, 42, 0.08);
        margin-bottom: 1rem;
    }

    .sidebar-kicker {
        color: var(--accent) !important;
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }

    .sidebar-title {
        margin: 0;
        font-size: 1.7rem;
        line-height: 1;
    }

    section[data-testid="stSidebar"] [data-baseweb="radio"] {
        background: rgba(255,255,255,0.75);
        border: 1px solid rgba(15, 23, 42, 0.08);
        border-radius: 18px;
        padding: 0.25rem;
        box-shadow: var(--shadow-soft);
    }

    section[data-testid="stSidebar"] [data-baseweb="radio"] label {
        padding: 0.75rem 0.85rem;
        border-radius: 14px;
        transition: background 0.18s ease, transform 0.18s ease;
    }

    section[data-testid="stSidebar"] [data-baseweb="radio"] label:hover {
        background: rgba(255, 90, 31, 0.06);
        transform: translateX(2px);
    }

    section[data-testid="stSidebar"] [role="radiogroup"] > label[data-checked="true"] {
        background: linear-gradient(135deg, rgba(255, 90, 31, 0.12), rgba(255, 122, 69, 0.10));
    }

    .stRadio > div,
    .stMultiSelect,
    .stTextInput,
    .stNumberInput,
    .stSlider,
    .stSelectbox {
        margin-bottom: 0.8rem;
    }

    input, [data-baseweb="select"] > div, [data-baseweb="base-input"] > div {
        background-color: rgba(255,255,255,0.96) !important;
        color: var(--text) !important;
        border: 1px solid rgba(15, 23, 42, 0.14) !important;
        border-radius: 14px !important;
        box-shadow: inset 0 1px 2px rgba(15, 23, 42, 0.03);
    }

    input:focus, [data-baseweb="select"] > div:focus-within, [data-baseweb="base-input"] > div:focus-within {
        border-color: rgba(255, 90, 31, 0.55) !important;
        box-shadow: 0 0 0 4px rgba(255, 90, 31, 0.12) !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, var(--accent), #ff7a45) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.65rem 1rem !important;
        font-weight: 800 !important;
        box-shadow: 0 12px 24px rgba(255, 90, 31, 0.22);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 14px 28px rgba(255, 90, 31, 0.28);
    }

    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.88);
        border: 1px solid rgba(15, 23, 42, 0.08);
        border-radius: var(--radius-md);
        padding: 0.95rem 1rem;
        box-shadow: var(--shadow-soft);
    }

    div[data-testid="metric-container"] label {
        color: var(--muted) !important;
        font-size: 0.92rem;
    }

    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: -0.04em;
    }

    div[data-testid="stDataFrame"] {
        border-radius: var(--radius-md);
        overflow: hidden;
        box-shadow: var(--shadow-soft);
    }

    div[data-testid="stTable"] {
        border-radius: var(--radius-md);
        overflow: hidden;
        box-shadow: var(--shadow-soft);
    }

    .block-container .stTabs [data-baseweb="tab-list"] {
        gap: 0.55rem;
        background: rgba(255,255,255,0.55);
        padding: 0.35rem;
        border-radius: 999px;
    }

    .block-container .stTabs [data-baseweb="tab"] {
        border-radius: 999px;
        font-weight: 700;
        color: var(--muted) !important;
        background: transparent;
    }

    .block-container .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(255, 90, 31, 0.16), rgba(255, 122, 69, 0.22)) !important;
        color: var(--text) !important;
    }

    .stImage img {
        border-radius: 24px !important;
        box-shadow: var(--shadow);
        border: 1px solid rgba(15, 23, 42, 0.06);
    }

    .stCaption {
        color: var(--muted) !important;
    }

    @media (max-width: 768px) {
        .hero-shell {
            padding: 1.25rem 1rem 1rem;
        }

        .hero-title {
            font-size: 1.8rem;
        }

        .menu-card img {
            height: 160px;
        }

        .quick-strip {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def render_hero(title, subtitle, badge="FlavorFlow Pro"):
    st.markdown(
        f"""
        <div class='hero-shell'>
            <div class='hero-badge'>{badge}</div>
            <h1 class='hero-title'>{title}</h1>
            <p class='hero-subtitle'>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_title(title, subtitle):
    st.markdown(
        f"""
        <div class='section-title'>
            <h3>{title}</h3>
            <span>{subtitle}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_quick_strip(items):
    cards = "".join(
        f"<div class='quick-chip'><strong>{heading}</strong><span>{body}</span></div>"
        for heading, body in items
    )
    st.markdown(f"<div class='quick-strip'>{cards}</div>", unsafe_allow_html=True)

# Helper for Clean White Graphs (No Gridlines)
def show_white_graph(df, x, y, title, color_hex):
    fig = px.bar(df, x=x, y=y, title=title, template="plotly_white", color_discrete_sequence=[color_hex])
    fig.update_layout(
        font=dict(color="black", size=14),
        plot_bgcolor='white', paper_bgcolor='white',
        xaxis=dict(showgrid=False, linecolor='black', tickfont=dict(color='black')),
        yaxis=dict(showgrid=False, linecolor='black', tickfont=dict(color='black'))
    )
    st.plotly_chart(fig, use_container_width=True)

# Shared state to track stalls
if 'order_stalls' not in st.session_state:
    st.session_state.order_stalls = ["Counter 1"]

if 'cart_item_ids' not in st.session_state:
    st.session_state.cart_item_ids = []

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown(
        """
        <div class='sidebar-brand'>
            <div class='sidebar-kicker'>Smart Canteen Suite</div>
            <h1 class='sidebar-title'>FlavorFlow Pro</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )
    nav = st.radio("SELECT FEATURE", ["🏠 Project Dashboard", "🍱 Order & Pickup Path", "💰 Meal Budget Optimizer", "👨‍🍳 Staff & Shift Logic", "🧪 Algorithmic Lab"])

# --- 1. HOME DASHBOARD ---
if nav == "🏠 Project Dashboard":
    top_search, top_lang, top_status = st.columns([2.6, 1.1, 0.9])
    with top_search:
        st.markdown(
            """
            <div class='topbar-brand'>
                <div class='topbar-mark'>F</div>
                <div>
                    <h3 class='topbar-name'>FlavorFlow</h3>
                    <p class='topbar-note'>Smart canteen ordering and optimization</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top_lang:
        st.text_input("Search everything here...", placeholder="Search everything here...", label_visibility="collapsed")
    with top_status:
        st.selectbox("Language", ["Select Language", "English", "Hindi"], label_visibility="collapsed")

    render_hero(
        "Special Menu For You",
        "A canteen-style dashboard inspired by modern food ordering apps, with fast filtering, cart preview, and an order summary on the right.",
        "Canteen Overview",
    )

    st.markdown("""
    <div class='quick-strip'>
        <div class='quick-chip'><strong>Fast Search</strong><span>Find dishes instantly</span></div>
        <div class='quick-chip'><strong>Smart Cart</strong><span>Track your current order</span></div>
        <div class='quick-chip'><strong>Algorithmic Core</strong><span>DAA logic stays intact</span></div>
    </div>
    """, unsafe_allow_html=True)

    menu_root, order_root = st.columns([2.35, 1], gap="large")
    with menu_root:
        st.markdown("<div class='catalog-panel'>", unsafe_allow_html=True)
        render_section_title("Today's Menu", "Cards, filters, and a clean grid layout")
        category_labels = ["All", "Counter 1", "Pizza Oven", "Juice Bar"]
        active_category = st.radio("Categories", category_labels, horizontal=True, label_visibility="collapsed")
        st.markdown("<div class='menu-filter-row'>", unsafe_allow_html=True)
        for label in category_labels:
            active_class = "filter-chip-active" if active_category == label else ""
            st.markdown(f"<span class='filter-chip {active_class}'>{label}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        filtered_menu = MENU if active_category == "All" else [item for item in MENU if item['stall'] == active_category]
        search_term = st.text_input("", placeholder="Search by dish name", label_visibility="collapsed")
        if search_term:
            filtered_menu = [item for item in filtered_menu if search_term.lower() in item['name'].lower()]

        menu_html = []
        for item in filtered_menu:
            is_active = item['id'] in st.session_state.cart_item_ids
            action_label = "Remove" if is_active else "Add to Cart"
            badge_text = f"{item['calories']} cal"
            menu_html.append(item)

        grid_cols = st.columns(2)
        for index, item in enumerate(filtered_menu):
            col = grid_cols[index % 2]
            with col:
                st.markdown(
                    f"""
                    <div class='product-card'>
                        <img class='product-image' src='{item['image']}' alt='{item['name']}'>
                        <div class='product-body'>
                            <h4 class='product-name'>{item['name']}</h4>
                            <div class='product-meta'>
                                <span class='product-price'>₹{item['price']}</span>
                                <span>{item['stall']}</span>
                            </div>
                            <div class='product-actions'>
                                <span class='mini-badge'>{item['calories']} cal</span>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                button_key = f"cart_btn_{item['id']}"
                if st.button(action_label if item['id'] in st.session_state.cart_item_ids else "Add to Cart", key=button_key):
                    if item['id'] in st.session_state.cart_item_ids:
                        st.session_state.cart_item_ids.remove(item['id'])
                    else:
                        st.session_state.cart_item_ids.append(item['id'])
                    st.session_state.order_stalls = [m['stall'] for m in MENU if m['id'] in st.session_state.cart_item_ids]
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with order_root:
        st.markdown("<div class='cart-panel'>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class='cart-head'>
                <div>
                    <h3>Current Order</h3>
                    <p class='cart-subtext'>{len(st.session_state.cart_item_ids)} item(s) selected</p>
                </div>
                <span class='topbar-chip'>Live</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        cart_items = [item for item in MENU if item['id'] in st.session_state.cart_item_ids]
        if not cart_items:
            st.markdown(
                """
                <div class='info-box'>
                    <h4>Your cart is empty</h4>
                    <p>Select items from the menu grid to build a live order summary.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            total_price = sum(item['price'] for item in cart_items)
            total_calories = sum(item['calories'] for item in cart_items)
            for item in cart_items:
                st.markdown(
                    f"""
                    <div class='cart-item'>
                        <img src='{item['image']}' alt='{item['name']}'>
                        <div>
                            <p class='cart-item-title'>{item['name']}</p>
                            <p class='cart-item-meta'>{item['stall']} • ₹{item['price']}</p>
                        </div>
                        <strong>₹{item['price']}</strong>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown(
                f"""
                <div class='cart-summary'>
                    <div class='cart-summary-row'><span>Subtotal</span><strong>₹{total_price}</strong></div>
                    <div class='cart-summary-row'><span>Total Calories</span><strong>{total_calories}</strong></div>
                    <div class='cart-summary-row'><span>Delivery</span><strong>₹20</strong></div>
                    <div class='cart-summary-row'><span>Total</span><strong>₹{total_price + 20}</strong></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("<div class='payment-box'><b>Payment Method</b></div>", unsafe_allow_html=True)
            st.radio("", ["Cash", "UPI", "Card"], horizontal=True, label_visibility="collapsed")
            st.markdown("<div class='action-row'>", unsafe_allow_html=True)
            if st.button("Clear Cart"):
                st.session_state.cart_item_ids = []
                st.session_state.order_stalls = ["Counter 1"]
                st.rerun()
            st.button("Place Order")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# --- 2. ORDER & PICKUP PATH ---
elif nav == "🍱 Order & Pickup Path":
    render_hero(
        "Smart Ordering & Multi-Stop Route",
        "Find items quickly, compare search strategies, and generate an optimized pickup path across stalls.",
        "Ordering Flow",
    )
    st.image("https://images.unsplash.com/photo-1512428559087-560fa5ceab42?w=1000", width=600)
    
    st.subheader("🔍 Intelligent Item Search")
    query = st.text_input("Search for a dish (e.g. Pizza, Burger):")
    if query:
        item_b, steps_b = binary_search(MENU, query)
        _, steps_l = linear_search(MENU, query)
        c1, c2 = st.columns(2)
        c1.markdown(f"<div class='info-box'><b>Linear Search</b><br>Steps: {steps_l}<br>Complexity: O(n)</div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='info-box'><b>Binary Search</b><br>Steps: {steps_b}<br><span class='winner-tag'>WINNER: O(log n)</span></div>", unsafe_allow_html=True)

    st.markdown("---")
    render_section_title("Select Multiple Items", "Choose dishes to generate a route")
    selected_names = st.multiselect("🍱 Pick Items from Menu:", [i['name'] for i in MENU])
    
    if selected_names:
        st.session_state.order_stalls = [i['stall'] for i in MENU if i['name'] in selected_names]
        time_res, route = get_multi_stop_route(CANTEEN_MAP, st.session_state.order_stalls)
        st.markdown(f"<div class='info-box'><h4>📍 Optimized Pickup Path (Dijkstra's Greedy Strategy)</h4><p>Route: {' ➔ '.join(route)}</p><h3>Total Walk Time: {time_res} Mins</h3></div>", unsafe_allow_html=True)

    render_section_title("Today's Menu", "A consistent card grid for all items")
    cols = st.columns(3)
    for i, itm in enumerate(MENU):
        with cols[i % 3]:
            st.markdown(f"<div class='menu-card'><img src='{itm['image']}'><h4>{itm['name']}</h4><p>₹{itm['price']} | {itm['stall']}</p></div>", unsafe_allow_html=True)

# --- 3. MEAL BUDGET OPTIMIZER ---
elif nav == "💰 Meal Budget Optimizer":
    render_hero(
        "Budget Meal Planner (0/1 Knapsack)",
        "Choose a budget and let dynamic programming build the best possible meal tray by calorie yield.",
        "Optimization Lab",
    )
    st.image("https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=1000", width=600)
    
    st.markdown("<div class='info-box'><b>Algorithm: Dynamic Programming (DP)</b><br>We build a DP Table to find the absolute best calorie combination for your budget. We compare it with the Greedy Strategy.</div>", unsafe_allow_html=True)
    
    budget = st.slider("Select your Budget (₹)", 50, 600, 250)
    val_dp, items_dp = knapsack_dp(budget, MENU)
    val_greedy = knapsack_greedy(budget, MENU)
    
    c1, c2 = st.columns(2)
    c1.metric("Greedy Calorie Yield", val_greedy)
    c2.metric("DP Calorie Yield (Optimal)", val_dp)
    
    if items_dp:
        st.session_state.order_stalls = [i['stall'] for i in items_dp]
        render_section_title(f"Optimal Tray for ₹{budget}", "Best value combination from the DP table")
        cols = st.columns(len(items_dp))
        for i, itm in enumerate(items_dp):
            with cols[i]:
                st.markdown(f"<div class='menu-card'><img src='{itm['image']}'><br><b>{itm['name']}</b></div>", unsafe_allow_html=True)

# --- 4. STAFF & SHIFT LOGIC ---
elif nav == "👨‍🍳 Staff & Shift Logic":
    render_hero(
        "Kitchen Operations & Staffing",
        "Use greedy scheduling and graph coloring to keep kitchen work fast and conflict-free.",
        "Operations Control",
    )
    st.image("https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=1000", width=600)
    
    tab1, tab2 = st.tabs(["Kitchen Scheduling", "Staff Management"])
    with tab1:
        render_section_title("Priority Cooking Sequence", "Greedy job ordering for fast service")
        jobs = [{'name': i['name'], 'deadline': 2, 'profit': i['price']} for i in MENU if i['stall'] in st.session_state.order_stalls]
        if jobs:
            schedule = job_scheduling_deadlines(jobs)
            st.write("🔥 **Priority Order:** " + " ➔ ".join(schedule))

    with tab2:
        render_section_title("Shift Assignment", "Backtracking-based conflict-free allocation")
        st.markdown("<div class='info-box'>No two chefs working in the same stall zone can have the same Shift Slot. We use Backtracking to assign conflict-free shifts.</div>", unsafe_allow_html=True)
        active_stalls = list(set(st.session_state.order_stalls))
        staff_map = {f"Chef {stall}": [f"Chef {s}" for s in active_stalls if s != stall] for stall in active_stalls}
        coloring = graph_coloring(staff_map, 3, list(staff_map.keys()))
        if coloring:
            for chef, slot in coloring.items():
                st.success(f"👨‍🍳 **{chef}** assigned to **Shift Slot {slot}**")

# --- 5. ALGORITHMIC LAB ---
elif nav == "🧪 Algorithmic Lab":
    render_hero(
        "DAA Performance Laboratory",
        "A compact showcase of the algorithms behind the app, with direct comparisons and route calculations.",
        "Algorithm Lab",
    )
    st.image("https://images.unsplash.com/photo-1551288049-bbbda536339a?w=1000", width=600)
    
    # 1. KARATSUBA
    render_section_title("1. Bulk Calculation", "Divide and conquer: Karatsuba")
    st.markdown("<div class='info-box'><b>Why Karatsuba?</b> Standard multiplication is O(n²). Karatsuba reduces the recursive steps to T(n) = 3T(n/2) + O(n), giving a complexity of O(n^1.58). This is much faster for bulk canteen orders.</div>", unsafe_allow_html=True)
    n1 = st.number_input("Quantity (kg)", 12345)
    n2 = st.number_input("Unit Price (₹)", 6789)
    st.success(f"Result: ₹{karatsuba_multiplication(n1, n2)}")

    # 2. GRAPHS
    col1, col2 = st.columns(2)
    with col1:
        show_white_graph(pd.DataFrame({'Algo': ['Linear Search', 'Binary Search'], 'Efficiency': [30, 98]}), 'Algo', 'Efficiency', "Search Strategy Efficiency", "#FF4B2B")
    with col2:
        show_white_graph(pd.DataFrame({'Algo': ['Greedy Knapsack', 'DP Knapsack'], 'Accuracy': [70, 100]}), 'Algo', 'Accuracy', "Optimization Accuracy", "#2563EB")

    # 3. FLOYD-WARSHALL
    render_section_title("2. All-Pairs Shortest Path", "Dynamic programming: Floyd-Warshall")
    st.write("We pre-calculate the distance between every stall in the canteen. Complexity: O(V³).")
    st.table(pd.DataFrame(floyd_warshall(CANTEEN_MAP, list(CANTEEN_MAP.keys()))))

    # 4. TSP B&B
    render_section_title("3. Delivery Robot", "Branch and bound: TSP")
    st.markdown("<div class='info-box'><b>Branch & Bound:</b> This NP-Hard problem is solved using the Least Cost (LC) search approach. It prunes paths that exceed the current minimum, finding the absolute shortest delivery cycle.</div>", unsafe_allow_html=True)
    path, cost = tsp_branch_and_bound()
    st.success(f"Shortest Delivery Path: {' ➔ '.join(path)} (Cost: {cost})")