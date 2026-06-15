import streamlit as st
import pandas as pd

from hybrid_engine import (
    hybrid_recommend,
    sku_dict,
    retailer_features
)

# 1. Page Config (Kept identical, added initial state for sidebar)
st.set_page_config(
    page_title="O2R Recommendation Engine",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- HEADER SECTION ---
st.title("🛒 O2R Retailer Recommendation Engine")

# Improved Typography: Inline code blocks for visual tags
st.markdown("""
**AI-powered product recommendations leveraging:** `Collaborative Filtering` • `FP-Growth Association Rules` • `Regional Trends` • `Product Popularity`
""")

# Use native divider instead of markdown("---")
st.divider()

# --- SIDEBAR SECTION ---
with st.sidebar:
    st.header("⚙️ Control Panel")
    # Added a help tooltip to the selectbox
    customer_id = st.selectbox(
        "Choose Retailer ID",
        sorted(retailer_features["customerId"].unique()),
        help="Select a retailer ID to view their profile and generate tailored recommendations."
    )
    
    st.info("Select a retailer above to load their profile data.")

profile = retailer_features[retailer_features["customerId"] == customer_id]

# --- MAIN CONTENT: RETAILER PROFILE ---
st.subheader("👤 Retailer Profile & Statistics")

# Using a container to group the metrics visually
with st.container():
    # CHANGED: Use 2 columns instead of 4 to give long text room to breathe
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Hub", profile["hub_name"].iloc[0])
        st.metric("Top Brand", profile["favorite_brand"].iloc[0])
        
    with col2:
        st.metric("Top Category", profile["favorite_category"].iloc[0])
        st.metric("Spend Segment", profile["spend_segment"].iloc[0])

    # Added a small spacer
    st.write("") 

    # Keep the numerical metrics in 3 columns since numbers are short
    col3, col4, col5 = st.columns(3)
    with col3:
        st.metric("Total Orders", f"{int(profile['total_orders'].iloc[0]):,}")
    with col4:
        st.metric("Unique Products", f"{int(profile['unique_products'].iloc[0]):,}")
    with col5:
        st.metric("Total Quantity", f"{int(profile['total_qty'].iloc[0]):,}")

st.divider()

# --- RECOMMENDATION ENGINE SECTION ---
st.subheader("Generate Insights")

# UI Enhancement: Changed button to 'primary' type so it stands out as the main call-to-action
if st.button("Generate Recommendations", type="primary", use_container_width=True):
    
    # Added a spinner so the user knows the AI is calculating
    with st.spinner("Running hybrid recommendation engine..."):
        recs = hybrid_recommend(customer_id)

        results = []
        for i, (sku, score) in enumerate(recs, start=1):
            results.append({
                "Rank": i,
                "Product": sku_dict.get(sku, sku),
                "Recommendation Score": round(score, 3)
            })

        result_df = pd.DataFrame(results)

        if len(result_df) > 0:
            # Highlight the top product immediately with a native success block
            top_product = result_df.iloc[0]["Product"]
            st.success(f"**Top Recommendation:** {top_product}")

            st.subheader("Recommended Products List")

            # UI Enhancement: Use column_config to turn the score into a visual progress bar
            max_score = float(result_df["Recommendation Score"].max()) if not result_df.empty else 1.0

            st.dataframe(
                result_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Rank": st.column_config.NumberColumn("Rank", format="%d"),
                    "Product": st.column_config.TextColumn("Product Name"),
                    "Recommendation Score": st.column_config.ProgressColumn(
                        "Recommendation Score",
                        help="Confidence score from the hybrid engine",
                        format="%.3f",
                        min_value=0,
                        max_value=max_score,
                    ),
                }
            )
        else:
            st.warning("No recommendations found for this retailer.")

st.divider()

# Footer
st.caption("Built using Collaborative Filtering + FP-Growth + Regional Trends + Popularity Scoring")