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

# --- GLOBAL CSS: APPETIZING LIGHT GLASSMORPHISM THEME ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

    :root {
        --bg: #fdfaf6;
        --surface: rgba(255, 255, 255, 0.75);
        --surface-strong: #ffffff;
        --surface-soft: #fff8f4;
        --border: rgba(15, 23, 42, 0.05);
        --text: #1f2937;
        --muted: #64748b;
        --accent: #ff6b35;
        --accent-deep: #fb923c;
        --accent-2: #10b981;
        --accent-3: #1d4ed8;
        --shadow: 0 32px 64px rgba(255, 107, 53, 0.08);
        --shadow-soft: 0 16px 32px rgba(15, 23, 42, 0.04);
        --shadow-hover: 0 24px 48px rgba(255, 107, 53, 0.16);
        --radius-xl: 32px;
        --radius-lg: 24px;
        --radius-md: 16px;
    }

    html, body, [class*="css"]  {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: var(--text) !important;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(255, 107, 53, 0.08), transparent 30%),
            radial-gradient(circle at 85% 10%, rgba(16, 185, 129, 0.06), transparent 25%),
            linear-gradient(180deg, #fffdfa 0%, var(--bg) 100%);
        color: var(--text) !important;
    }

    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        pointer-events: none;
        background-image: radial-gradient(rgba(15, 23, 42, 0.03) 1px, transparent 1px);
        background-size: 24px 24px;
        z-index: 0;
    }

    .block-container {
        padding-top: 1.85rem;
        padding-bottom: 2.5rem;
        max-width: 1320px;
    }

    h1, h2, h3, h4 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #111827 !important;
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
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 247, 242, 0.8));
        backdrop-filter: blur(24px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-radius: var(--radius-xl);
        padding: 2.2rem 2.2rem 1.8rem;
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
        margin-bottom: 1.5rem;
    }

    .hero-shell::after {
        content: '';
        position: absolute;
        inset: auto -30px -50px auto;
        width: 280px;
        height: 280px;
        background: radial-gradient(circle, rgba(255, 107, 53, 0.15), transparent 70%);
        pointer-events: none;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(255, 107, 53, 0.12);
        color: var(--accent) !important;
        border: 1px solid rgba(255, 107, 53, 0.2);
        border-radius: 999px;
        padding: 0.5rem 1rem;
        font-size: 0.85rem;
        font-weight: 800;
        letter-spacing: 0.03em;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(255, 107, 53, 0.1);
    }

    .hero-title {
        font-size: clamp(2.2rem, 3.8vw, 3.5rem);
        line-height: 1.1;
        margin: 0 0 0.8rem 0;
        font-weight: 800;
        color: #0f172a !important;
    }

    .hero-subtitle {
        max-width: 800px;
        color: var(--muted) !important;
        font-size: 1.1rem;
        line-height: 1.6;
        margin: 0;
    }

    .menu-card {
        background: var(--surface);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: var(--radius-lg);
        padding: 16px;
        text-align: center;
        box-shadow: var(--shadow-soft);
        margin-bottom: 24px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .menu-card:hover {
        transform: translateY(-6px) scale(1.02);
        border-color: rgba(255, 107, 53, 0.3);
        box-shadow: var(--shadow-hover);
    }

    .menu-card img {
        width: 100%;
        height: 170px;
        object-fit: contain;
        background: white;
        border-radius: 16px;
        border: 1px solid rgba(15, 23, 42, 0.04);
        padding: 8px;
    }

    .menu-card h4 {
        margin-top: 1rem;
        margin-bottom: 0.4rem;
        font-size: 1.1rem;
        font-weight: 700;
    }

    .menu-card p {
        margin-bottom: 0.2rem;
        color: var(--muted) !important;
        font-size: 0.95rem;
    }

    .info-box {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-left: 6px solid var(--accent);
        padding: 1.4rem 1.5rem;
        border-radius: var(--radius-md);
        margin-bottom: 1.2rem;
        box-shadow: var(--shadow-soft);
    }

    .info-box h3, .info-box h4 {
        margin-top: 0;
        margin-bottom: 0.7rem;
        color: #0f172a !important;
    }

    .winner-tag {
        display: inline-flex;
        align-items: center;
        background: linear-gradient(135deg, var(--accent), var(--accent-deep));
        color: white !important;
        padding: 0.35rem 0.9rem;
        border-radius: 999px;
        font-weight: 800;
        letter-spacing: 0.04em;
        box-shadow: 0 12px 28px rgba(255, 107, 53, 0.3);
        animation: pulseSubtle 2s infinite;
    }

    @keyframes pulseSubtle {
        0% { box-shadow: 0 0 0 0 rgba(255, 107, 53, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(255, 107, 53, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 107, 53, 0); }
    }

    .section-title {
        display: flex;
        align-items: baseline;
        gap: 0.8rem;
        margin: 0.5rem 0 1rem;
    }

    .section-title h2,
    .section-title h3 {
        margin: 0;
        font-size: 1.6rem;
    }

    .section-title span {
        color: var(--muted) !important;
        font-size: 0.95rem;
    }

    .quick-strip {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 1rem;
        margin: 0 0 1.2rem;
    }

    .quick-chip {
        background: var(--surface);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 20px;
        padding: 1.1rem 1.2rem;
        box-shadow: var(--shadow-soft);
        transition: transform 0.2s ease;
    }
    
    .quick-chip:hover {
        transform: translateY(-2px);
        box-shadow: 0 16px 32px rgba(15, 23, 42, 0.08);
    }

    .quick-chip strong {
        display: block;
        font-size: 1.05rem;
        margin-bottom: 0.3rem;
        color: var(--text) !important;
    }

    .quick-chip span {
        color: var(--muted) !important;
        font-size: 0.95rem;
    }

    .topbar {
        display: grid;
        grid-template-columns: 1.2fr 1.4fr 0.9fr;
        gap: 1rem;
        align-items: center;
        margin-bottom: 1.2rem;
    }

    .topbar-brand, .topbar-meta {
        background: var(--surface);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 20px;
        padding: 0.8rem 1rem;
        box-shadow: var(--shadow-soft);
    }

    .topbar-brand {
        display: flex;
        align-items: center;
        gap: 0.9rem;
    }

    .topbar-mark {
        width: 42px;
        height: 42px;
        border-radius: 12px;
        display: grid;
        place-items: center;
        background: linear-gradient(135deg, var(--accent), var(--accent-deep));
        color: white !important;
        font-size: 1.2rem;
        font-weight: 800;
        box-shadow: 0 8px 20px rgba(255, 107, 53, 0.25);
    }

    .topbar-name {
        margin: 0;
        font-size: 1.1rem;
        line-height: 1.1;
        font-weight: 700;
    }

    .topbar-note {
        margin: 0.1rem 0 0;
        font-size: 0.85rem;
        color: var(--muted) !important;
    }

    .topbar-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.45rem 0.8rem;
        border-radius: 999px;
        background: rgba(16, 185, 129, 0.12);
        color: var(--accent-2) !important;
        font-size: 0.85rem;
        font-weight: 800;
    }

    .catalog-panel,
    .cart-panel {
        background: var(--surface);
        backdrop-filter: blur(24px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 28px;
        box-shadow: var(--shadow);
    }

    .catalog-panel {
        padding: 1.2rem 1.2rem 0.5rem;
    }

    .cart-panel {
        padding: 1.2rem;
        position: sticky;
        top: 1.2rem;
    }

    .menu-filter-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.8rem;
        margin: 0.5rem 0 1.2rem;
    }

    .filter-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.6rem 1rem;
        border-radius: 999px;
        border: 1px solid rgba(15, 23, 42, 0.06);
        background: rgba(255, 255, 255, 0.6);
        color: var(--muted) !important;
        font-size: 0.9rem;
        font-weight: 700;
        transition: all 0.2s ease;
    }

    .filter-chip:hover {
        background: rgba(255, 255, 255, 0.9);
        transform: translateY(-1px);
    }

    .filter-chip-active {
        background: linear-gradient(135deg, rgba(255, 107, 53, 0.15), rgba(251, 146, 60, 0.1));
        border-color: rgba(255, 107, 53, 0.2);
        color: var(--accent) !important;
        box-shadow: 0 4px 12px rgba(255, 107, 53, 0.08);
    }

    /* Style the Categories Radio to look like horizontal chips */
    div[data-testid="stRadio"] > div[role="radiogroup"][aria-label="Categories"] {
        flex-direction: row !important;
        gap: 0.8rem !important;
        flex-wrap: wrap !important;
    }
    
    div[data-testid="stRadio"] > div[role="radiogroup"][aria-label="Categories"] > label {
        padding: 0.6rem 1.2rem !important;
        background: rgba(255, 255, 255, 0.7) !important;
        border: 1px solid rgba(15, 23, 42, 0.06) !important;
        border-radius: 999px !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        margin: 0 !important;
        transition: all 0.2s ease !important;
    }

    div[data-testid="stRadio"] > div[role="radiogroup"][aria-label="Categories"] > label[data-checked="true"] {
        background: linear-gradient(135deg, rgba(255, 107, 53, 0.15), rgba(251, 146, 60, 0.1)) !important;
        border-color: rgba(255, 107, 53, 0.2) !important;
        color: var(--accent) !important;
    }

    .menu-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 1rem;
    }

    .product-card {
        background: white;
        border: 1px solid rgba(15, 23, 42, 0.08);
        border-radius: 32px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.03);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        height: 100%;
        display: flex;
        flex-direction: column;
        margin-bottom: 1.5rem;
    }
    
    /* Ensure Streamlit columns use flex to match card heights */
    div[data-testid="column"] {
        display: flex !important;
        flex-direction: column !important;
    }

    .product-card:hover {
        transform: translateY(-8px);
        border-color: rgba(255, 107, 53, 0.3);
        box-shadow: 0 30px 60px rgba(255, 107, 53, 0.12);
    }
    
    .product-image-container {
        width: 100%;
        height: 200px;
        overflow: hidden;
        background: #f8fafc;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0;
        border-bottom: 1px solid rgba(15, 23, 42, 0.03);
    }

    .product-image {
        width: 100% !important;
        height: 100% !important;
        object-fit: cover !important;
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    .product-card:hover .product-image {
        transform: scale(1.08);
    }

    .product-body {
        padding: 1.5rem;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        gap: 0.5rem;
    }

    .product-name {
        margin: 0;
        font-size: 1.2rem;
        font-weight: 800;
        color: #0f172a !important;
        min-height: 2.8rem;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    .product-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 0.4rem;
    }

    .product-price {
        font-weight: 900;
        color: var(--accent) !important;
        font-size: 1.3rem;
    }
    
    .product-stall {
        font-size: 0.85rem;
        font-weight: 700;
        color: var(--muted) !important;
        background: rgba(15, 23, 42, 0.05);
        padding: 0.2rem 0.6rem;
        border-radius: 8px;
    }

    .product-actions {
        margin-top: 1rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .mini-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        border-radius: 999px;
        background: rgba(16, 185, 129, 0.12);
        color: var(--accent-2) !important;
        font-size: 0.8rem;
        padding: 0.35rem 0.65rem;
        font-weight: 800;
    }

    .cart-head {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.8rem;
        margin-bottom: 1rem;
        padding-bottom: 0.8rem;
        border-bottom: 1px solid rgba(15, 23, 42, 0.06);
    }

    .cart-head h3 {
        margin: 0;
        font-size: 1.3rem;
        font-weight: 700;
    }

    .cart-subtext {
        color: var(--muted) !important;
        font-size: 0.9rem;
        margin: 0.2rem 0 0;
    }

    .cart-item {
        display: grid;
        grid-template-columns: 60px 1fr auto;
        gap: 0.9rem;
        align-items: center;
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-radius: 20px;
        padding: 0.8rem;
        margin-bottom: 0.8rem;
        box-shadow: var(--shadow-soft);
        transition: transform 0.2s ease;
    }
    
    .cart-item:hover {
        transform: translateY(-2px);
    }

    .cart-item img {
        width: 60px;
        height: 60px;
        border-radius: 14px;
        object-fit: cover;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
    }

    .cart-item-title {
        margin: 0;
        font-size: 0.95rem;
        font-weight: 800;
        color: #1f2937 !important;
    }

    .cart-item-meta {
        margin: 0.15rem 0 0;
        color: var(--muted) !important;
        font-size: 0.85rem;
    }

    .cart-summary {
        background: linear-gradient(135deg, rgba(255, 107, 53, 0.05), rgba(255, 255, 255, 0.8));
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 107, 53, 0.15);
        border-radius: 22px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-soft);
    }

    .cart-summary-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.8rem;
        margin-bottom: 0.5rem;
        font-size: 0.95rem;
    }

    .cart-summary-row strong {
        color: var(--text) !important;
        font-weight: 800;
        font-size: 1.05rem;
    }

    .payment-box {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-radius: 20px;
        padding: 1rem;
        margin-top: 1rem;
        box-shadow: var(--shadow-soft);
    }

    .action-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.8rem;
        margin-top: 1rem;
    }

    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(24px) !important;
        -webkit-backdrop-filter: blur(24px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 10px 0 40px rgba(15, 23, 42, 0.03);
    }

    [data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    .sidebar-brand {
        padding: 0.5rem 0.5rem 1.2rem;
        border-bottom: 1px solid rgba(15, 23, 42, 0.05);
        margin-bottom: 1.2rem;
    }

    .sidebar-kicker {
        display: inline-block;
        background: rgba(255, 107, 53, 0.12);
        color: var(--accent) !important;
        padding: 0.35rem 0.8rem;
        border-radius: 8px;
        font-size: 0.95rem;
        font-weight: 900;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
        border: 1px solid rgba(255, 107, 53, 0.2);
    }

    .sidebar-title {
        margin: 0;
        font-size: 1.8rem;
        line-height: 1.1;
        font-weight: 800;
    }

    section[data-testid="stSidebar"] [data-baseweb="radio"] {
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(15, 23, 42, 0.05) !important;
        border-radius: 24px !important;
        padding: 1.2rem !important;
        margin-top: 0.5rem !important;
        box-shadow: var(--shadow-soft) !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="radio"] label {
        padding: 1rem 1.2rem !important;
        border-radius: 18px !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        font-weight: 700 !important;
        margin-bottom: 0.6rem !important;
        border: 1px solid transparent !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="radio"] label:hover {
        background: rgba(255, 107, 53, 0.05);
        transform: translateX(4px);
    }

    section[data-testid="stSidebar"] [role="radiogroup"] > label[data-checked="true"] {
        background: linear-gradient(135deg, var(--accent), var(--accent-deep)) !important;
        color: white !important;
        border: 1px solid rgba(255, 107, 53, 0.4) !important;
        box-shadow: 0 12px 24px rgba(255, 107, 53, 0.3) !important;
        transform: scale(1.04) translateX(5px) !important;
    }
    
    section[data-testid="stSidebar"] [role="radiogroup"] > label[data-checked="true"] div[data-testid="stMarkdownContainer"] p {
        color: white !important;
    }

    .stRadio > div,
    .stMultiSelect,
    .stTextInput,
    .stNumberInput,
    .stSlider,
    .stSelectbox {
        margin-bottom: 0.9rem;
    }

    input, [data-baseweb="select"] > div, [data-baseweb="base-input"] > div {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid rgba(15, 23, 42, 0.12) !important;
        border-radius: 16px !important;
        padding: 0.6rem 1rem !important;
        transition: all 0.2s ease !important;
        font-weight: 600 !important;
    }
    
    input::placeholder {
        color: #94a3b8 !important;
        opacity: 1 !important;
    }

    input:focus, [data-baseweb="select"] > div:focus-within, [data-baseweb="base-input"] > div:focus-within {
        border-color: rgba(255, 107, 53, 0.6) !important;
        box-shadow: 0 0 0 4px rgba(255, 107, 53, 0.15) !important;
        background-color: #ffffff !important;
    }

    /* DROPDOWN & POPOVER FIXES - Force Light Theme */
    div[data-baseweb="popover"], 
    div[role="listbox"], 
    div[data-baseweb="menu"], 
    ul[role="listbox"],
    div[data-baseweb="select"] ul,
    div[data-baseweb="popover"] > div {
        background-color: #ffffff !important;
        background: #ffffff !important;
        border: 1px solid rgba(15, 23, 42, 0.08) !important;
        border-radius: 12px !important;
        box-shadow: 0 15px 45px rgba(15, 23, 42, 0.12) !important;
    }

    div[data-baseweb="popover"] *, 
    div[role="listbox"] *, 
    div[data-baseweb="menu"] *, 
    ul[role="listbox"] *,
    div[data-baseweb="select"] ul * {
        color: #1e293b !important;
        font-weight: 500 !important;
    }

    [role="option"]:hover, [role="menuitem"]:hover, 
    div[role="listbox"] [role="option"]:hover {
        background-color: rgba(255, 107, 53, 0.08) !important;
        color: var(--accent) !important;
    }

    /* Hide Streamlit specific layout items */
    header { visibility: hidden !important; }
    .stAppDeployButton { display: none !important; }
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    div[data-testid="stStatusWidget"] { visibility: hidden !important; }
    
    /* Ensure the main container is not squashed by hidden header */
    .stApp {
        margin-top: -50px;
    }

    .stButton > button {
        background: linear-gradient(135deg, var(--accent), var(--accent-deep)) !important;
        color: white !important;
        border: none !important;
        border-radius: 18px !important;
        padding: 0.75rem 1.2rem !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
        box-shadow: 0 12px 28px rgba(255, 107, 53, 0.25);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 16px 36px rgba(255, 107, 53, 0.35);
        background: linear-gradient(135deg, #ff7a45, #fc9f50) !important;
    }

    .stButton > button:active {
        transform: translateY(1px);
    }

    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-radius: var(--radius-md);
        padding: 1.2rem;
        box-shadow: var(--shadow-soft);
        transition: transform 0.2s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-4px);
    }

    div[data-testid="metric-container"] label {
        color: var(--muted) !important;
        font-size: 0.95rem;
        font-weight: 600;
    }

    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: -0.04em;
        color: var(--accent) !important;
    }

    div[data-testid="stDataFrame"], div[data-testid="stTable"] {
        border-radius: var(--radius-md);
        overflow: hidden;
        box-shadow: var(--shadow-soft);
        border: 1px solid rgba(255,255,255,0.6);
    }

    .block-container .stTabs [data-baseweb="tab-list"] {
        gap: 0.6rem;
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(12px);
        padding: 0.4rem;
        border-radius: 999px;
        border: 1px solid rgba(255, 255, 255, 0.5);
    }

    .block-container .stTabs [data-baseweb="tab"] {
        border-radius: 999px;
        font-weight: 700;
        color: var(--muted) !important;
        background: transparent;
        padding: 0.6rem 1.2rem;
    }

    .block-container .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(255, 107, 53, 0.15), rgba(251, 146, 60, 0.1)) !important;
        color: var(--accent) !important;
        box-shadow: 0 4px 12px rgba(255, 107, 53, 0.08);
    }

    .stImage img {
        border-radius: 28px !important;
        box-shadow: var(--shadow);
        border: 1px solid rgba(255, 255, 255, 0.6);
        transition: all 0.4s ease !important;
    }
    
    .stImage:hover img {
        transform: scale(1.02);
        box-shadow: 0 32px 80px rgba(255, 107, 53, 0.15);
    }

    /* Modern Navbar Search Bar styling */
    .search-navbar {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(15, 23, 42, 0.05);
        border-radius: 24px;
        padding: 0.6rem 1.2rem;
        display: flex;
        align-items: center;
        gap: 1.5rem;
        box-shadow: var(--shadow-soft);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .search-navbar:hover {
        border-color: rgba(255, 107, 53, 0.3);
        box-shadow: 0 12px 36px rgba(255, 107, 53, 0.08);
    }

    .stCaption {
        color: var(--muted) !important;
        font-weight: 600;
        margin-top: 0.5rem;
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
    st.markdown("<div class='search-navbar'>", unsafe_allow_html=True)
    nb_col1, nb_col2 = st.columns([1, 2.5])
    with nb_col1:
        st.markdown(
            """
            <div style='display: flex; align-items: center; gap: 0.8rem;'>
                <div class='topbar-mark'>F</div>
                <div style='line-height:1'>
                    <h3 style='margin:0; font-size:1.2rem;'>FlavorFlow</h3>
                    <p style='margin:0.2rem 0 0; font-size:0.8rem; color:var(--muted)'>Smart Canteen App</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with nb_col2:
        st.text_input("Search everything here", placeholder="Search dashboard menu, items, and labs...", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

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
        # Removing redundant manual chip rendering loop as requested

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

        grid_cols = st.columns(3, gap="large")
        for index, item in enumerate(filtered_menu):
            col = grid_cols[index % 3]
            with col:
                st.markdown(
                    f"""
                    <div class='product-card'>
                        <div class='product-image-container'>
                            <img class='product-image' src='{item['image']}' alt='{item['name']}'>
                        </div>
                        <div class='product-body'>
                            <h4 class='product-name'>{item['name']}</h4>
                            <div class='product-meta'>
                                <span class='product-price'>₹{item['price']}</span>
                                <span class='product-stall'>{item['stall']}</span>
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
                if st.button(action_label if item['id'] in st.session_state.cart_item_ids else "Add to Cart", key=button_key, width="stretch" if hasattr(st, 'button') else True):
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
    st.image("https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=1200", use_container_width=True)
    
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
            st.markdown(
                f"""
                <div class='product-card'>
                    <div class='product-image-container'>
                        <img class='product-image' src='{itm['image']}' alt='{itm['name']}'>
                    </div>
                    <div class='product-body'>
                        <h4 class='product-name'>{itm['name']}</h4>
                        <div class='product-meta'>
                            <span class='product-price'>₹{itm['price']}</span>
                            <span class='product-stall'>{itm['stall']}</span>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

# --- 3. MEAL BUDGET OPTIMIZER ---
elif nav == "💰 Meal Budget Optimizer":
    render_hero(
        "Budget Meal Planner (0/1 Knapsack)",
        "Choose a budget and let dynamic programming build the best possible meal tray by calorie yield.",
        "Optimization Lab",
    )
    st.image("https://images.unsplash.com/photo-1543353071-873f17a7a088?w=1200", use_container_width=True)
    
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
                st.markdown(
                    f"""
                    <div class='product-card'>
                        <div class='product-image-container'>
                            <img class='product-image' src='{itm['image']}' alt='{itm['name']}'>
                        </div>
                        <div class='product-body'>
                            <h4 class='product-name'>{itm['name']}</h4>
                            <div class='product-meta'>
                                <span class='product-price'>₹{itm['price']}</span>
                                <span class='product-stall'>{itm['stall']}</span>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# --- 4. STAFF & SHIFT LOGIC ---
elif nav == "👨‍🍳 Staff & Shift Logic":
    render_hero(
        "Kitchen Operations & Staffing",
        "Use greedy scheduling and graph coloring to keep kitchen work fast and conflict-free.",
        "Operations Control",
    )
    st.image("https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=1200", use_container_width=True)
    
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
    st.image("https://images.unsplash.com/photo-1509062522246-3755977927d7?w=1200", use_container_width=True)
    
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