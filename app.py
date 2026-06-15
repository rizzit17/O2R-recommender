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
    initial_sidebar_state="expanded"
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0A0F1E;
    color: #E2E8F0;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2rem 2.5rem 3rem 2.5rem;
    max-width: 1200px;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0D1424 !important;
    border-right: 1px solid #1E293B;
}
section[data-testid="stSidebar"] .block-container {
    padding: 2rem 1.25rem;
}

/* ── Page title ── */
.page-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.25rem;
}
.page-title {
    font-size: 1.75rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #818CF8 0%, #6366F1 50%, #4F46E5 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
}
.page-subtitle {
    color: #64748B;
    font-size: 0.875rem;
    margin-bottom: 1.75rem;
    line-height: 1.6;
}
.pill {
    display: inline-block;
    background: #1E293B;
    border: 1px solid #334155;
    color: #94A3B8;
    font-size: 0.72rem;
    font-weight: 500;
    font-family: 'JetBrains Mono', monospace;
    padding: 0.2rem 0.55rem;
    border-radius: 999px;
    margin-right: 0.35rem;
    letter-spacing: 0.02em;
}

/* ── Cards ── */
.card {
    background: #111827;
    border: 1px solid #1E293B;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.25rem;
}
.card-title {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 1rem;
}

/* ── Metric overrides ── */
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

/* ── Section headings ── */
.section-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #1E293B;
}
.section-heading {
    font-size: 1.15rem;
    font-weight: 700;
    color: #F1F5F9;
    margin-bottom: 1rem;
    letter-spacing: -0.01em;
}

/* ── Recommendation table ── */
.rec-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.875rem;
}
.rec-table thead tr {
    border-bottom: 1px solid #1E293B;
}
.rec-table thead th {
    padding: 0.6rem 1rem;
    text-align: left;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #475569;
}
.rec-table tbody tr {
    border-bottom: 1px solid #0F172A;
    transition: background 0.15s;
}
.rec-table tbody tr:hover {
    background: #1E293B44;
}
.rec-table tbody td {
    padding: 0.75rem 1rem;
    color: #CBD5E1;
    vertical-align: middle;
}
.rank-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 26px;
    height: 26px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}
.rank-1 { background: #6366F1; color: #fff; }
.rank-2 { background: #1E293B; color: #818CF8; border: 1px solid #6366F1; }
.rank-3 { background: #1E293B; color: #818CF8; border: 1px solid #6366F1; }
.rank-other { background: #0F172A; color: #475569; border: 1px solid #1E293B; }
.product-name {
    color: #E2E8F0;
    font-weight: 500;
}
.score-bar-wrap {
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.score-bar-bg {
    flex: 1;
    height: 5px;
    background: #1E293B;
    border-radius: 999px;
    overflow: hidden;
    min-width: 80px;
}
.score-bar-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #4F46E5, #818CF8);
}
.score-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #818CF8;
    white-space: nowrap;
    min-width: 38px;
}
.top-rec-banner {
    background: linear-gradient(135deg, #1e1b4b 0%, #1E293B 100%);
    border: 1px solid #6366F1;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin-bottom: 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.top-rec-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #818CF8;
}
.top-rec-name {
    font-size: 1rem;
    font-weight: 600;
    color: #E2E8F0;
}

/* ── Sidebar widgets ── */
.sidebar-stat {
    background: #111827;
    border: 1px solid #1E293B;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.6rem;
    font-size: 0.8rem;
    color: #94A3B8;
}
.sidebar-stat strong {
    color: #E2E8F0;
    font-weight: 600;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    padding: 0.65rem 1.5rem !important;
    letter-spacing: 0.01em !important;
    transition: opacity 0.15s !important;
    box-shadow: 0 0 20px #6366F122 !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: #111827 !important;
    border-color: #1E293B !important;
    color: #E2E8F0 !important;
    border-radius: 8px !important;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: #6366F1 !important;
}

/* ── Divider ── */
hr { border-color: #1E293B !important; }

/* ── Warning / info ── */
.stAlert {
    border-radius: 8px !important;
    border: 1px solid #1E293B !important;
}
</style>
""", unsafe_allow_html=True)


# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <span style="font-size:1.6rem">🛒</span>
    <h1 class="page-title">O2R Recommendation Engine</h1>
</div>
<p class="page-subtitle">
    AI-powered product recommendations for retailer ordering intelligence.
    &nbsp;
    <span class="pill">Collaborative Filtering</span>
    <span class="pill">FP-Growth</span>
    <span class="pill">Regional Trends</span>
    <span class="pill">Popularity Scoring</span>
</p>
""", unsafe_allow_html=True)


# ── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <div style="font-size:1.1rem;font-weight:700;color:#E2E8F0;margin-bottom:0.25rem;">⚙️ Control Panel</div>
        <div style="font-size:0.78rem;color:#475569;">Configure retailer and engine settings</div>
    </div>
    """, unsafe_allow_html=True)

    customer_id = st.selectbox(
        "Retailer ID",
        sorted(retailer_features["customerId"].unique()),
        help="Select a retailer to load their profile and run recommendations."
    )

    st.markdown("<div style='margin-top:1.25rem;'></div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="sidebar-stat">Dataset size &nbsp;·&nbsp; <strong>{retailer_features.shape[0]} retailers</strong></div>
    <div class="sidebar-stat">Unique retailer IDs &nbsp;·&nbsp; <strong>{retailer_features["customerId"].nunique()}</strong></div>
    <div class="sidebar-stat">Feature dimensions &nbsp;·&nbsp; <strong>{retailer_features.shape[1]} columns</strong></div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:1.5rem;padding:0.85rem 1rem;background:#0F172A;border-radius:8px;border:1px solid #1E293B;font-size:0.78rem;color:#64748B;line-height:1.6;">
        Select a retailer ID above to load their purchase history, segment, and hub details.
    </div>
    """, unsafe_allow_html=True)


# ── Retailer Profile ────────────────────────────────────────────────────────────
profile = retailer_features[retailer_features["customerId"] == customer_id]

st.markdown('<div class="section-label">Retailer Profile</div>', unsafe_allow_html=True)
st.markdown('<div class="section-heading">👤 Profile & Statistics</div>', unsafe_allow_html=True)

with st.container():
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

st.markdown("<div style='margin: 1.75rem 0;'></div>", unsafe_allow_html=True)


# ── Recommendations ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Engine Output</div>', unsafe_allow_html=True)
st.markdown('<div class="section-heading">Generate Recommendations</div>', unsafe_allow_html=True)

if st.button("Run Recommendation Engine", type="primary", use_container_width=True):
    with st.spinner("Running hybrid recommendation engine..."):
        recs = hybrid_recommend(customer_id)
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

        # Top recommendation banner
        st.markdown(f"""
        <div class="top-rec-banner">
            <span style="font-size:1.4rem"></span>
            <div>
                <div class="top-rec-label">Top Recommendation</div>
                <div class="top-rec-name">{top_product}</div>
            </div>
            <div style="margin-left:auto;text-align:right;">
                <div class="top-rec-label">Score</div>
                <div style="font-family:'JetBrains Mono',monospace;color:#818CF8;font-size:1rem;font-weight:600;">{round(top_score, 3)}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Score normalisation for bar widths
        max_score = result_df["Score"].max()

        # ── Table header ──
        st.markdown("""
        <div style="display:grid;grid-template-columns:60px 1fr 220px;
                    padding:0.5rem 1rem;border-bottom:1px solid #1E293B;margin-top:0.5rem;">
            <span style="font-size:0.68rem;font-weight:700;letter-spacing:0.1em;
                         text-transform:uppercase;color:#475569;">Rank</span>
            <span style="font-size:0.68rem;font-weight:700;letter-spacing:0.1em;
                         text-transform:uppercase;color:#475569;">Product</span>
            <span style="font-size:0.68rem;font-weight:700;letter-spacing:0.1em;
                         text-transform:uppercase;color:#475569;">Score</span>
        </div>
        """, unsafe_allow_html=True)

        # ── One row per recommendation ──
        for _, row in result_df.iterrows():
            rank    = int(row["Rank"])
            product = row["Product"]
            score   = row["Score"]
            pct     = (score / max_score * 100) if max_score > 0 else 0

            if rank == 1:
                badge_bg, badge_color, badge_border = "#6366F1", "#fff", "#6366F1"
            elif rank in (2, 3):
                badge_bg, badge_color, badge_border = "#1E293B", "#818CF8", "#6366F1"
            else:
                badge_bg, badge_color, badge_border = "#0F172A", "#475569", "#1E293B"

            col_rank, col_product, col_score = st.columns([0.5, 4, 2])

            with col_rank:
                st.markdown(
                    f"""<div style="display:flex;align-items:center;height:48px;">
                        <span style="display:inline-flex;align-items:center;justify-content:center;
                                     width:28px;height:28px;border-radius:6px;
                                     background:{badge_bg};color:{badge_color};
                                     border:1px solid {badge_border};
                                     font-size:0.72rem;font-weight:700;
                                     font-family:'JetBrains Mono',monospace;">#{rank}</span>
                    </div>""",
                    unsafe_allow_html=True
                )

            with col_product:
                st.markdown(
                    f"""<div style="display:flex;align-items:center;height:48px;">
                        <span style="color:#E2E8F0;font-weight:500;font-size:0.875rem;">{product}</span>
                    </div>""",
                    unsafe_allow_html=True
                )

            with col_score:
                st.markdown(
                    f"""<div style="display:flex;align-items:center;gap:0.6rem;height:48px;">
                        <div style="flex:1;height:5px;background:#1E293B;border-radius:999px;overflow:hidden;">
                            <div style="width:{pct:.1f}%;height:100%;border-radius:999px;
                                        background:linear-gradient(90deg,#4F46E5,#818CF8);"></div>
                        </div>
                        <span style="font-family:'JetBrains Mono',monospace;font-size:0.78rem;
                                     color:#818CF8;white-space:nowrap;min-width:38px;">{score:.3f}</span>
                    </div>""",
                    unsafe_allow_html=True
                )

            st.markdown(
                "<div style='border-bottom:1px solid #0F172A;margin:0 0 0 0;'></div>",
                unsafe_allow_html=True
            )

    else:
        st.warning("No recommendations could be generated for this retailer.")

# ── Footer ──────────────────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:3rem;'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="border-top:1px solid #1E293B;padding-top:1rem;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:0.5rem;">
    <span style="font-size:0.75rem;color:#334155;font-family:'JetBrains Mono',monospace;">O2R Recommendation Engine</span>
    <span style="font-size:0.72rem;color:#1E293B;">
        Collaborative Filtering · FP-Growth · Regional Trends · Popularity Scoring
    </span>
</div>
""", unsafe_allow_html=True)