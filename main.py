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
    /* Force White Background and Black Text everywhere */
    .stApp { background-color: #FFFFFF !important; color: #000000 !important; }
    h1, h2, h3, h4, p, span, label, li, div { color: #000000 !important; font-family: 'Segoe UI', sans-serif !important; }
    
    /* Uniform Menu Cards */
    .menu-card {
        background-color: #FFFFFF;
        border: 1px solid #EEEEEE;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .menu-card img {
        width: 100%;
        height: 180px;
        object-fit: contain; /* Full image visible */
        background-color: #FAFAFA;
        border-radius: 10px;
    }

    /* Input Box Styles: White bg, Orange border, Black text */
    input, [data-baseweb="select"] > div, [data-baseweb="base-input"] > div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #FF4B2B !important;
    }

    .info-box {
        background-color: #FFF5F2;
        border-left: 5px solid #FF4B2B;
        padding: 25px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    .winner-tag {
        background-color: #FF4B2B; color: white; padding: 4px 12px; border-radius: 20px; font-weight: bold;
    }
    
    /* Navigation Sidebar */
    [data-testid="stSidebar"] { background-color: #FDFDFD !important; border-right: 1px solid #EEEEEE; }
    </style>
    """, unsafe_allow_html=True)

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

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='color:#FF4B2B;'>FlavorFlow Pro</h1>", unsafe_allow_html=True)
    nav = st.radio("SELECT FEATURE", ["🏠 Project Dashboard", "🍱 Order & Pickup Path", "💰 Meal Budget Optimizer", "👨‍🍳 Staff & Shift Logic", "🧪 Algorithmic Lab"])

# --- 1. HOME DASHBOARD ---
if nav == "🏠 Project Dashboard":
    st.title("Smart Canteen: Algorithmic Optimization System")
    st.image("https://images.unsplash.com/photo-1556742044-3c52d6e88c62?w=1200", caption="Optimizing Canteen Flow with DAA")
    
    st.markdown("""
    <div class='info-box'>
        <h3>Project Vision & DAA Integration</h3>
        <p>This project is designed for <b>T.Y. B.Tech Computer Engineering</b>, applying fundamental algorithms to automate a canteen.</p>
        <ul>
            <li><b>Searching (Unit II):</b> Comparing Linear vs Binary Search for menu items.</li>
            <li><b>Multiplication (Unit II):</b> Karatsuba algorithm for bulk financial costing.</li>
            <li><b>Greedy Strategy (Unit II):</b> Dijkstra for shortest path and Job Scheduling for kitchen tasks.</li>
            <li><b>Dynamic Programming (Unit III):</b> 0/1 Knapsack for budget meals and Floyd-Warshall for map distances.</li>
            <li><b>Backtracking (Unit IV):</b> Graph Coloring for conflict-free staff shift assignments.</li>
            <li><b>Branch & Bound (Unit IV):</b> TSP for delivery route optimization.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- 2. ORDER & PICKUP PATH ---
elif nav == "🍱 Order & Pickup Path":
    st.title("Smart Ordering & Multi-Stop Route")
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
    st.subheader("Select Multiple Items")
    selected_names = st.multiselect("🍱 Pick Items from Menu:", [i['name'] for i in MENU])
    
    if selected_names:
        st.session_state.order_stalls = [i['stall'] for i in MENU if i['name'] in selected_names]
        time_res, route = get_multi_stop_route(CANTEEN_MAP, st.session_state.order_stalls)
        st.markdown(f"<div class='info-box'><h4>📍 Optimized Pickup Path (Dijkstra's Greedy Strategy)</h4><p>Route: {' ➔ '.join(route)}</p><h3>Total Walk Time: {time_res} Mins</h3></div>", unsafe_allow_html=True)

    st.subheader("Today's Menu")
    cols = st.columns(3)
    for i, itm in enumerate(MENU):
        with cols[i % 3]:
            st.markdown(f"<div class='menu-card'><img src='{itm['image']}'><h4>{itm['name']}</h4><p>₹{itm['price']} | {itm['stall']}</p></div>", unsafe_allow_html=True)

# --- 3. MEAL BUDGET OPTIMIZER ---
elif nav == "💰 Meal Budget Optimizer":
    st.title("Budget Meal Planner (0/1 Knapsack)")
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
        st.subheader(f"Optimal Tray for ₹{budget}")
        cols = st.columns(len(items_dp))
        for i, itm in enumerate(items_dp):
            with cols[i]:
                st.markdown(f"<div class='menu-card'><img src='{itm['image']}'><br><b>{itm['name']}</b></div>", unsafe_allow_html=True)

# --- 4. STAFF & SHIFT LOGIC ---
elif nav == "👨‍🍳 Staff & Shift Logic":
    st.title("Kitchen Operations & Staffing")
    st.image("https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=1000", width=600)
    
    tab1, tab2 = st.tabs(["Kitchen Scheduling", "Staff Management"])
    with tab1:
        st.subheader("Priority Cooking Sequence (Greedy Job Scheduling)")
        jobs = [{'name': i['name'], 'deadline': 2, 'profit': i['price']} for i in MENU if i['stall'] in st.session_state.order_stalls]
        if jobs:
            schedule = job_scheduling_deadlines(jobs)
            st.write("🔥 **Priority Order:** " + " ➔ ".join(schedule))

    with tab2:
        st.subheader("Shift Assignment (Backtracking - Graph Coloring)")
        st.markdown("<div class='info-box'>No two chefs working in the same stall zone can have the same Shift Slot. We use Backtracking to assign conflict-free shifts.</div>", unsafe_allow_html=True)
        active_stalls = list(set(st.session_state.order_stalls))
        staff_map = {f"Chef {stall}": [f"Chef {s}" for s in active_stalls if s != stall] for stall in active_stalls}
        coloring = graph_coloring(staff_map, 3, list(staff_map.keys()))
        if coloring:
            for chef, slot in coloring.items():
                st.success(f"👨‍🍳 **{chef}** assigned to **Shift Slot {slot}**")

# --- 5. ALGORITHMIC LAB ---
elif nav == "🧪 Algorithmic Lab":
    st.title("DAA Performance Laboratory")
    st.image("https://images.unsplash.com/photo-1551288049-bbbda536339a?w=1000", width=600)
    
    # 1. KARATSUBA
    st.subheader("1. Bulk Calculation (Divide & Conquer: Karatsuba)")
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
    st.subheader("2. All-Pairs Shortest Path (Dynamic Programming: Floyd-Warshall)")
    st.write("We pre-calculate the distance between every stall in the canteen. Complexity: O(V³).")
    st.table(pd.DataFrame(floyd_warshall(CANTEEN_MAP, list(CANTEEN_MAP.keys()))))

    # 4. TSP B&B
    st.subheader("3. Delivery Robot (Branch & Bound: TSP)")
    st.markdown("<div class='info-box'><b>Branch & Bound:</b> This NP-Hard problem is solved using the Least Cost (LC) search approach. It prunes paths that exceed the current minimum, finding the absolute shortest delivery cycle.</div>", unsafe_allow_html=True)
    path, cost = tsp_branch_and_bound()
    st.success(f"Shortest Delivery Path: {' ➔ '.join(path)} (Cost: {cost})")