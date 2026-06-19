import streamlit as st
import pandas as pd
from hybrid_engine import (
    hybrid_recommend,
    sku_dict,
    retailer_features
)

st.set_page_config(
    page_title="O2R Recommendation Engine",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "show_engine" not in st.session_state:
    st.session_state.show_engine = False

if "cf_s" not in st.session_state: st.session_state.cf_s = 60
if "cf_i" not in st.session_state: st.session_state.cf_i = 60
if "reg_s" not in st.session_state: st.session_state.reg_s = 25
if "reg_i" not in st.session_state: st.session_state.reg_i = 25
if "pop_s" not in st.session_state: st.session_state.pop_s = 15
if "pop_i" not in st.session_state: st.session_state.pop_i = 15

def sync_w_cf_from_s(): st.session_state.cf_i = st.session_state.cf_s
def sync_w_cf_from_i(): st.session_state.cf_s = st.session_state.cf_i
def sync_w_reg_from_s(): st.session_state.reg_i = st.session_state.reg_s
def sync_w_reg_from_i(): st.session_state.reg_s = st.session_state.reg_i
def sync_w_pop_from_s(): st.session_state.pop_i = st.session_state.pop_s
def sync_w_pop_from_i(): st.session_state.pop_s = st.session_state.pop_i

# ── Global styles (no HTML content mixed in) ───────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0A0F1E;
    color: #E2E8F0;
}
#MainMenu, footer, header { visibility: hidden; }

section[data-testid="stSidebar"] {
    background: #0D1424 !important;
    border-right: 1px solid #1E293B;
}
section[data-testid="stSidebar"] .block-container {
    padding: 2rem 1.25rem !important;
    max-width: 100% !important;
}

[data-testid="stMetric"] {
    background: #0F172A;
    border: 1px solid #1E293B;
    border-radius: 10px;
    padding: 1rem 1.25rem;
}
[data-testid="stMetricLabel"] {
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #475569 !important;
}
[data-testid="stMetricValue"] {
    font-size: 1.25rem !important;
    font-weight: 700 !important;
    color: #E2E8F0 !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.01em !important;
    box-shadow: 0 0 24px rgba(99,102,241,0.2) !important;
}
.stButton > button[kind="primary"]:hover { opacity: 0.85 !important; }

.stButton > button[kind="secondary"] {
    background: #1E293B !important;
    color: #94A3B8 !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 0.82rem !important;
}
.stButton > button[kind="secondary"]:hover {
    background: #263548 !important;
    color: #E2E8F0 !important;
}

.stSelectbox > div > div {
    background: #111827 !important;
    border-color: #1E293B !important;
    color: #E2E8F0 !important;
    border-radius: 8px !important;
}
.stSpinner > div { border-top-color: #6366F1 !important; }
hr { border-color: #1E293B !important; }
.stAlert { border-radius: 8px !important; border: 1px solid #1E293B !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# LANDING PAGE
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.show_engine:

    st.markdown("""
    <style>
    .block-container {
        padding: 3rem 4rem !important;
        max-width: 900px !important;
        margin: 0 auto !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Headline
    st.markdown("""
    <div style="text-align:center;">
        <h1 style="font-size:clamp(2rem,4.5vw,3.2rem);font-weight:800;
                   letter-spacing:-0.03em;line-height:1.15;color:#F8FAFC;
                   margin:0 auto 1rem auto;max-width:680px;">
            Smarter ordering starts with<br>
            <span style="background:linear-gradient(135deg,#818CF8 0%,#6366F1 60%,#4F46E5 100%);
                         -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                         background-clip:text;">knowing what sells next</span>
        </h1>
        <p style="color:#64748B;font-size:0.95rem;line-height:1.7;
                  max-width:520px;margin:0 auto 1.75rem auto;">
            The O2R Recommendation Engine analyses purchase history, regional demand,
            and product co-occurrence patterns to surface the right products for each
            retailer - before they ask.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Pills row
    st.markdown("""
    <div style="display:flex;justify-content:center;flex-wrap:wrap;
                gap:0.5rem;margin-bottom:2rem;">
        <span style="background:#1E293B;border:1px solid #334155;color:#94A3B8;
                     font-size:0.72rem;font-weight:500;
                     font-family:'JetBrains Mono',monospace;
                     padding:0.25rem 0.65rem;border-radius:999px;">
            Collaborative Filtering
        </span>
        <span style="background:#1E293B;border:1px solid #334155;color:#94A3B8;
                     font-size:0.72rem;font-weight:500;
                     font-family:'JetBrains Mono',monospace;
                     padding:0.25rem 0.65rem;border-radius:999px;">
            FP-Growth Association Rules
        </span>
        <span style="background:#1E293B;border:1px solid #334155;color:#94A3B8;
                     font-size:0.72rem;font-weight:500;
                     font-family:'JetBrains Mono',monospace;
                     padding:0.25rem 0.65rem;border-radius:999px;">
            Regional Trend Signals
        </span>
        <span style="background:#1E293B;border:1px solid #334155;color:#94A3B8;
                     font-size:0.72rem;font-weight:500;
                     font-family:'JetBrains Mono',monospace;
                     padding:0.25rem 0.65rem;border-radius:999px;">
            Popularity Scoring
        </span>
    </div>
    """, unsafe_allow_html=True)

    # CTA button
    col_l, col_c, col_r = st.columns([1.5, 2, 1.5])
    with col_c:
        if st.button("Proceed to Engine \u2192", type="primary", use_container_width=True):
            st.session_state.show_engine = True
            st.rerun()

    st.markdown("<div style='margin-top:2.5rem;'></div>", unsafe_allow_html=True)

    # Stats strip
    n_retailers = retailer_features["customerId"].nunique()
    n_skus      = len(sku_dict)

    st.markdown(f"""
    <div style="background:#0D1424;border:1px solid #1E293B;border-radius:12px;
                padding:1.75rem 2rem;display:flex;justify-content:space-around;
                flex-wrap:wrap;gap:1.5rem;margin-bottom:2.5rem;">
        <div style="text-align:center;">
            <span style="font-size:1.75rem;font-weight:800;color:#818CF8;
                         font-family:'JetBrains Mono',monospace;
                         letter-spacing:-0.03em;display:block;">{n_retailers:,}</span>
            <div style="font-size:0.68rem;font-weight:600;letter-spacing:0.1em;
                        text-transform:uppercase;color:#475569;margin-top:0.25rem;">
                Active Retailers
            </div>
        </div>
        <div style="text-align:center;">
            <span style="font-size:1.75rem;font-weight:800;color:#818CF8;
                         font-family:'JetBrains Mono',monospace;
                         letter-spacing:-0.03em;display:block;">{n_skus:,}</span>
            <div style="font-size:0.68rem;font-weight:600;letter-spacing:0.1em;
                        text-transform:uppercase;color:#475569;margin-top:0.25rem;">
                Tracked SKUs
            </div>
        </div>
        <div style="text-align:center;">
            <span style="font-size:1.75rem;font-weight:800;color:#818CF8;
                         font-family:'JetBrains Mono',monospace;
                         letter-spacing:-0.03em;display:block;">4</span>
            <div style="font-size:0.68rem;font-weight:600;letter-spacing:0.1em;
                        text-transform:uppercase;color:#475569;margin-top:0.25rem;">
                Signal Sources
            </div>
        </div>
        <div style="text-align:center;">
            <span style="font-size:1.75rem;font-weight:800;color:#818CF8;
                         font-family:'JetBrains Mono',monospace;
                         letter-spacing:-0.03em;display:block;">Hybrid</span>
            <div style="font-size:0.68rem;font-weight:600;letter-spacing:0.1em;
                        text-transform:uppercase;color:#475569;margin-top:0.25rem;">
                Engine Type
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # How it works header
    st.markdown("""
    <div style="text-align:center;margin-bottom:1.5rem;">
        <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.14em;
                    text-transform:uppercase;color:#475569;margin-bottom:0.4rem;">
            Under the hood
        </div>
        <div style="font-size:1.4rem;font-weight:700;color:#F1F5F9;letter-spacing:-0.02em;">
            Four signals. One ranked list.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # How it works cards — 2x2 grid via columns
    c1, c2 = st.columns(2)
    card_style = ("background:#111827;border:1px solid #1E293B;border-radius:12px;"
                  "padding:1.5rem;height:100%;")
    tag_style  = ("display:inline-block;margin-top:0.85rem;"
                  "font-family:'JetBrains Mono',monospace;font-size:0.65rem;"
                  "color:#6366F1;background:rgba(99,102,241,0.06);"
                  "border:1px solid rgba(99,102,241,0.18);"
                  "padding:0.15rem 0.5rem;border-radius:4px;")

    with c1:
        st.markdown(f"""
        <div style="{card_style}">
            <div style="font-size:0.875rem;font-weight:700;color:#E2E8F0;margin-bottom:0.4rem;">
                Collaborative Filtering
            </div>
            <div style="font-size:0.78rem;color:#64748B;line-height:1.6;">
                Finds retailers with similar purchase histories and recommends
                products they have bought that the target retailer has not tried yet.
            </div>
            <span style="{tag_style}">user-similarity</span>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div style="{card_style}">
            <div style="font-size:0.875rem;font-weight:700;color:#E2E8F0;margin-bottom:0.4rem;">
                FP-Growth Rules
            </div>
            <div style="font-size:0.78rem;color:#64748B;line-height:1.6;">
                Mines frequent product co-occurrence patterns from order history.
                If retailers who buy A also buy B, B surfaces as a recommendation.
            </div>
            <span style="{tag_style}">association-rules</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown(f"""
        <div style="{card_style}">
            <div style="font-size:0.875rem;font-weight:700;color:#E2E8F0;margin-bottom:0.4rem;">
                Regional Trends
            </div>
            <div style="font-size:0.78rem;color:#64748B;line-height:1.6;">
                Weights recommendations by what is selling well in the retailer's
                hub region, capturing local demand patterns that global models miss.
            </div>
            <span style="{tag_style}">geo-signals</span>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div style="{card_style}">
            <div style="font-size:0.875rem;font-weight:700;color:#E2E8F0;margin-bottom:0.4rem;">
                Popularity Scoring
            </div>
            <div style="font-size:0.78rem;color:#64748B;line-height:1.6;">
                Blends overall product popularity as a calibration signal, ensuring
                high-velocity SKUs are not buried by niche patterns.
            </div>
            <span style="{tag_style}">global-popularity</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:2.5rem;'></div>", unsafe_allow_html=True)

    # Bottom CTA
    st.markdown("""
    <div style="text-align:center;padding:1.5rem 0 0.5rem 0;
                border-top:1px solid #1E293B;">
        <div style="font-size:1.2rem;font-weight:700;color:#F1F5F9;
                    margin-bottom:0.4rem;letter-spacing:-0.02em;">
            Ready to explore recommendations?
        </div>
        <div style="color:#475569;font-size:0.85rem;margin-bottom:1.5rem;">
            Select a retailer ID and run the hybrid engine to see ranked product suggestions.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_l2, col_c2, col_r2 = st.columns([1.5, 2, 1.5])
    with col_c2:
        if st.button("Open Recommendation Engine \u2192",
                     type="primary", use_container_width=True, key="cta2"):
            st.session_state.show_engine = True
            st.rerun()

    st.markdown("""
    <div style="text-align:center;padding:2rem 0 1rem 0;">
        <span style="font-size:0.72rem;color:#1E293B;
                     font-family:'JetBrains Mono',monospace;">
            O2R Recommendation Engine
        </span>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ENGINE PAGE
# ══════════════════════════════════════════════════════════════════════════════
else:
    st.markdown("""
    <style>
    .block-container {
        padding: 2rem 2.5rem 3rem 2.5rem !important;
        max-width: 1200px !important;
        margin: 0 auto !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="margin-bottom:1.5rem;">
            <div style="font-size:1.05rem;font-weight:700;
                        color:#E2E8F0;margin-bottom:0.25rem;">
                &#9881;&#65039; Control Panel
            </div>
            <div style="font-size:0.78rem;color:#475569;">
                Configure retailer and engine settings
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Hierarchical Filters
        hubs = ["All"] + sorted(retailer_features["hub_name"].dropna().unique().tolist())
        selected_hub = st.selectbox("Filter by Hub", hubs)

        shop_types = ["All"] + sorted(retailer_features["shop_type"].dropna().unique().tolist())
        selected_shop_type = st.selectbox("Filter by Shop Type", shop_types)

        # Apply Filters
        filtered_retailers = retailer_features.copy()
        if selected_hub != "All":
            filtered_retailers = filtered_retailers[filtered_retailers["hub_name"] == selected_hub]
        if selected_shop_type != "All":
            filtered_retailers = filtered_retailers[filtered_retailers["shop_type"] == selected_shop_type]

        customer_list = sorted(filtered_retailers["customerId"].unique())
        
        if len(customer_list) > 0:
            customer_id = st.selectbox(
                "Retailer ID",
                customer_list,
                help="Select a retailer to load their profile and run recommendations."
            )
        else:
            st.warning("No retailers found for this combination.")
            customer_id = None
            
        st.markdown("<div style='margin-top:1.25rem;'></div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin-bottom:1rem;">
            <div style="font-size:0.9rem;font-weight:700;color:#E2E8F0;margin-bottom:0.25rem;">
                Engine Weights
            </div>
            <div style="font-size:0.72rem;color:#475569;">
                Adjust recommendation signals
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='font-size:0.8rem;color:#E2E8F0;margin-bottom:0.2rem;'>Collaborative Filtering (%)</div>", unsafe_allow_html=True)
        col_s1, col_i1 = st.columns([3, 1.2])
        with col_s1:
            st.slider("CF", 0, 100, value=st.session_state.cf_s, key="cf_s", on_change=sync_w_cf_from_s, label_visibility="collapsed")
        with col_i1:
            st.number_input("CF", 0, 100, value=st.session_state.cf_i, key="cf_i", on_change=sync_w_cf_from_i, label_visibility="collapsed")

        st.markdown("<div style='font-size:0.8rem;color:#E2E8F0;margin-bottom:0.2rem;margin-top:0.25rem;'>Regional Trends (%)</div>", unsafe_allow_html=True)
        col_s2, col_i2 = st.columns([3, 1.2])
        with col_s2:
            st.slider("Reg", 0, 100, value=st.session_state.reg_s, key="reg_s", on_change=sync_w_reg_from_s, label_visibility="collapsed")
        with col_i2:
            st.number_input("Reg", 0, 100, value=st.session_state.reg_i, key="reg_i", on_change=sync_w_reg_from_i, label_visibility="collapsed")

        st.markdown("<div style='font-size:0.8rem;color:#E2E8F0;margin-bottom:0.2rem;margin-top:0.25rem;'>Popularity (%)</div>", unsafe_allow_html=True)
        col_s3, col_i3 = st.columns([3, 1.2])
        with col_s3:
            st.slider("Pop", 0, 100, value=st.session_state.pop_s, key="pop_s", on_change=sync_w_pop_from_s, label_visibility="collapsed")
        with col_i3:
            st.number_input("Pop", 0, 100, value=st.session_state.pop_i, key="pop_i", on_change=sync_w_pop_from_i, label_visibility="collapsed")

        total_w = st.session_state.cf_i + st.session_state.reg_i + st.session_state.pop_i
        if total_w != 100:
            st.markdown(f"<div style='color:#ef4444;font-size:0.75rem;margin-top:0.5rem;font-weight:600;'>&#9888;&#65039; Weights must sum to 100. Current: {total_w}</div>", unsafe_allow_html=True)
            valid_weights = False
        else:
            w_cf = st.session_state.cf_i / 100.0
            w_reg = st.session_state.reg_i / 100.0
            w_pop = st.session_state.pop_i / 100.0
            valid_weights = True

        st.markdown("<div style='margin-top:1.25rem;'></div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:#111827;border:1px solid #1E293B;border-radius:8px;
                    padding:0.75rem 1rem;margin-bottom:0.6rem;
                    font-size:0.8rem;color:#94A3B8;">
            Dataset size &nbsp;&middot;&nbsp;
            <strong style="color:#E2E8F0;">{retailer_features.shape[0]} retailers</strong>
        </div>
        <div style="background:#111827;border:1px solid #1E293B;border-radius:8px;
                    padding:0.75rem 1rem;margin-bottom:0.6rem;
                    font-size:0.8rem;color:#94A3B8;">
            Unique retailer IDs &nbsp;&middot;&nbsp;
            <strong style="color:#E2E8F0;">{retailer_features["customerId"].nunique()}</strong>
        </div>
        <div style="background:#111827;border:1px solid #1E293B;border-radius:8px;
                    padding:0.75rem 1rem;margin-bottom:0.6rem;
                    font-size:0.8rem;color:#94A3B8;">
            Feature dimensions &nbsp;&middot;&nbsp;
            <strong style="color:#E2E8F0;">{retailer_features.shape[1]} columns</strong>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
        if st.button("\u2190 Back to Overview", use_container_width=True, key="back_sidebar"):
            st.session_state.show_engine = False
            st.rerun()

    # Back button (top of page)
    col_back, _ = st.columns([1, 5])
    with col_back:
        if st.button("\u2190 Overview", key="back_top"):
            st.session_state.show_engine = False
            st.rerun()

    st.markdown("<div style='margin-bottom:0.75rem;'></div>", unsafe_allow_html=True)

    # Page header
    st.markdown("""
    <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.25rem;">
        <span style="font-size:1.6rem;">&#128722;</span>
        <h1 style="font-size:1.75rem;font-weight:800;letter-spacing:-0.02em;
                   background:linear-gradient(135deg,#818CF8 0%,#6366F1 50%,#4F46E5 100%);
                   -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                   background-clip:text;margin:0;">
            O2R Recommendation Engine
        </h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="color:#64748B;font-size:0.875rem;margin-bottom:1.75rem;line-height:1.6;">
        AI-powered product recommendations for retailer ordering intelligence.&nbsp;
        <span style="background:#1E293B;border:1px solid #334155;color:#94A3B8;
                     font-size:0.72rem;font-weight:500;
                     font-family:'JetBrains Mono',monospace;
                     padding:0.2rem 0.55rem;border-radius:999px;margin-right:0.3rem;">
            Collaborative Filtering
        </span>
        <span style="background:#1E293B;border:1px solid #334155;color:#94A3B8;
                     font-size:0.72rem;font-weight:500;
                     font-family:'JetBrains Mono',monospace;
                     padding:0.2rem 0.55rem;border-radius:999px;margin-right:0.3rem;">
            FP-Growth
        </span>
        <span style="background:#1E293B;border:1px solid #334155;color:#94A3B8;
                     font-size:0.72rem;font-weight:500;
                     font-family:'JetBrains Mono',monospace;
                     padding:0.2rem 0.55rem;border-radius:999px;margin-right:0.3rem;">
            Regional Trends
        </span>
        <span style="background:#1E293B;border:1px solid #334155;color:#94A3B8;
                     font-size:0.72rem;font-weight:500;
                     font-family:'JetBrains Mono',monospace;
                     padding:0.2rem 0.55rem;border-radius:999px;">
            Popularity Scoring
        </span>
    </p>
    """, unsafe_allow_html=True)

    # Profile section
    if customer_id is not None:
        profile = retailer_features[retailer_features["customerId"] == customer_id]

        st.markdown("""
        <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.12em;
                    text-transform:uppercase;color:#475569;margin-bottom:0.6rem;
                    display:flex;align-items:center;gap:0.5rem;">
            Retailer Profile
            <span style="flex:1;height:1px;background:#1E293B;display:inline-block;"></span>
        </div>
        <div style="font-size:1.15rem;font-weight:700;color:#F1F5F9;
                    margin-bottom:1rem;letter-spacing:-0.01em;">
            &#128100; Profile &amp; Statistics
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Hub", profile["hub_name"].iloc[0])
        with col2:
            st.metric("Top Brand", profile["favorite_brand"].iloc[0])
        with col3:
            st.metric("Top Category", profile["favorite_category"].iloc[0])
        with col4:
            st.metric("Spend Segment", profile["spend_segment"].iloc[0])

        st.markdown("<div style='margin-top:0.75rem;'></div>", unsafe_allow_html=True)

        col5, col6, col7 = st.columns(3)
        with col5:
            st.metric("Total Orders", int(profile["total_orders"].iloc[0]))
        with col6:
            st.metric("Unique Products", int(profile["unique_products"].iloc[0]))
        with col7:
            st.metric("Total Quantity", int(profile["total_qty"].iloc[0]))

        st.markdown("<div style='margin:1.75rem 0;'></div>", unsafe_allow_html=True)

    # Recommendations section
    st.markdown("""
    <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.12em;
                text-transform:uppercase;color:#475569;margin-bottom:0.6rem;
                display:flex;align-items:center;gap:0.5rem;">
        Engine Output
        <span style="flex:1;height:1px;background:#1E293B;display:inline-block;"></span>
    </div>
    <div style="font-size:1.15rem;font-weight:700;color:#F1F5F9;
                margin-bottom:1rem;letter-spacing:-0.01em;">
        &#127919; Generate Recommendations
    </div>
    """, unsafe_allow_html=True)

    if customer_id is not None and st.button("Run Recommendation Engine", type="primary", use_container_width=True, disabled=not valid_weights):
        with st.spinner("Running hybrid recommendation engine..."):
            recs = hybrid_recommend(customer_id, top_n=10, weight_cf=w_cf, weight_region=w_reg, weight_pop=w_pop)
            results = []
            for i, (sku, score) in enumerate(recs, start=1):
                results.append({
                    "Rank": i,
                    "SKU": sku,
                    "Product": sku_dict.get(sku, sku),
                    "Score": score
                })
            result_df = pd.DataFrame(results)

        if len(result_df) > 0:
            top_product = result_df.iloc[0]["Product"]
            top_score   = result_df.iloc[0]["Score"]

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1e1b4b 0%,#1E293B 100%);
                        border:1px solid #6366F1;border-radius:10px;
                        padding:1rem 1.25rem;margin-bottom:1.25rem;
                        display:flex;align-items:center;gap:0.75rem;">
                <span style="font-size:1.4rem;">&#127942;</span>
                <div>
                    <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.1em;
                                text-transform:uppercase;color:#818CF8;">
                        Top Recommendation
                    </div>
                    <div style="font-size:1rem;font-weight:600;color:#E2E8F0;">
                        {top_product}
                    </div>
                </div>
                <div style="margin-left:auto;text-align:right;">
                    <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.1em;
                                text-transform:uppercase;color:#818CF8;">Score</div>
                    <div style="font-family:'JetBrains Mono',monospace;color:#818CF8;
                                font-size:1rem;font-weight:600;">
                        {round(top_score, 3)}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            max_score = result_df["Score"].max()

            # Table header
            st.markdown("""
            <div style="display:grid;grid-template-columns:64px 1fr 200px;
                        padding:0.5rem 0.75rem;border-bottom:1px solid #1E293B;
                        margin-top:0.5rem;">
                <span style="font-size:0.65rem;font-weight:700;letter-spacing:0.1em;
                             text-transform:uppercase;color:#475569;">Rank</span>
                <span style="font-size:0.65rem;font-weight:700;letter-spacing:0.1em;
                             text-transform:uppercase;color:#475569;">Product</span>
                <span style="font-size:0.65rem;font-weight:700;letter-spacing:0.1em;
                             text-transform:uppercase;color:#475569;">Score</span>
            </div>
            """, unsafe_allow_html=True)

            for _, row in result_df.iterrows():
                rank    = int(row["Rank"])
                product = row["Product"]
                score   = row["Score"]
                pct     = (score / max_score * 100) if max_score > 0 else 0

                if rank == 1:
                    badge_bg, badge_color, badge_border = "#6366F1", "#ffffff", "#6366F1"
                elif rank in (2, 3):
                    badge_bg, badge_color, badge_border = "#1E293B", "#818CF8", "#6366F1"
                else:
                    badge_bg, badge_color, badge_border = "#0F172A", "#475569", "#1E293B"

                col_rank, col_product, col_score = st.columns([0.45, 4, 1.8])

                with col_rank:
                    st.markdown(
                        f'<div style="display:flex;align-items:center;height:46px;">'
                        f'<span style="display:inline-flex;align-items:center;'
                        f'justify-content:center;width:30px;height:30px;border-radius:6px;'
                        f'background:{badge_bg};color:{badge_color};'
                        f'border:1px solid {badge_border};'
                        f'font-size:0.72rem;font-weight:700;'
                        f'font-family:JetBrains Mono,monospace;">#{rank}</span></div>',
                        unsafe_allow_html=True
                    )
                with col_product:
                    st.markdown(
                        f'<div style="display:flex;align-items:center;height:46px;">'
                        f'<span style="color:#E2E8F0;font-weight:500;'
                        f'font-size:0.875rem;">{product}</span></div>',
                        unsafe_allow_html=True
                    )
                with col_score:
                    st.markdown(
                        f'<div style="display:flex;align-items:center;gap:0.5rem;height:46px;">'
                        f'<div style="flex:1;height:5px;background:#1E293B;'
                        f'border-radius:999px;overflow:hidden;min-width:60px;">'
                        f'<div style="width:{pct:.1f}%;height:100%;border-radius:999px;'
                        f'background:linear-gradient(90deg,#4F46E5,#818CF8);"></div>'
                        f'</div>'
                        f'<span style="font-family:JetBrains Mono,monospace;font-size:0.75rem;'
                        f'color:#818CF8;white-space:nowrap;width:36px;text-align:right;">'
                        f'{score:.3f}</span></div>',
                        unsafe_allow_html=True
                    )

                st.markdown(
                    "<div style='border-bottom:1px solid #0F172A;'></div>",
                    unsafe_allow_html=True
                )

        else:
            st.warning("No recommendations could be generated for this retailer.")
    elif customer_id is None:
        st.info("Please adjust filters to find a valid Retailer ID.")

    # Footer
    st.markdown("<div style='margin-top:3rem;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="border-top:1px solid #1E293B;padding-top:1rem;
                display:flex;align-items:center;justify-content:space-between;
                flex-wrap:wrap;gap:0.5rem;">
        <span style="font-size:0.75rem;color:#334155;
                     font-family:'JetBrains Mono',monospace;">
            O2R Recommendation Engine
        </span>
        <span style="font-size:0.72rem;color:#1E293B;">
            Collaborative Filtering &middot; FP-Growth &middot;
            Regional Trends &middot; Popularity Scoring
        </span>
    </div>
    """, unsafe_allow_html=True)