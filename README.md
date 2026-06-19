# 🛒 O2R Recommendation Engine

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data-150458.svg)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Recommender-orange.svg)

**AI-powered product recommendations for retailer ordering intelligence.**

O2R Recommendation Engine is a specialized application designed to help B2B retailers and distributors optimize their product ordering process. By leveraging a state-of-the-art hybrid recommendation system, this tool provides hyper-personalized product suggestions based on purchasing history, regional trends, and overall item popularity.

---

## 🌟 Key Features

- **📊 Comprehensive Retailer Profiles:** Instantly view retailer statistics including their hub, top purchased brands, favorite categories, spend segment, and overall lifetime metrics.
- **🧠 Hybrid Recommendation Algorithm:** A sophisticated engine that blends multiple signals to generate the most accurate product suggestions:
  - **Collaborative Filtering (60%):** Identifies similar retailers and recommends what they are buying.
  - **Regional Trends (25%):** Factors in trending products based on the retailer's specific Hub and Shop Type.
  - **Popularity Scoring (15%):** Ensures universally high-demand products are always in the mix.
- **⚡ High-Performance Data Processing:** Built on `.parquet` files for rapid data loading and minimal memory footprint.
- **🖥️ Interactive Dashboard:** A sleek, dark-mode optimized Streamlit UI for seamless interaction and clean data visualization.

---

## 🏗️ Project Architecture

```text
O2R-recommender/
│
├── app.py                   # Main Streamlit dashboard application
├── hybrid_engine.py         # Core recommendation logic & algorithms
├── config.py                # Data paths and system configuration
│
├── data/
│   ├── raw/                 # Raw input datasets (e.g., orders_50k.xlsx)
│   └── processed/           # Optimized .parquet datasets
│       ├── retailer_features.parquet
│       ├── product_features.parquet
│       ├── interaction_matrix.parquet
│       ├── similarity_matrix.parquet
│       └── ...
│
└── models/                  # Saved machine learning models (.pkl)
```

---

## 🚀 Getting Started

### Prerequisites

Ensure you have Python installed, along with the necessary libraries. It is recommended to use a virtual environment.

```bash
# Clone the repository
git clone https://github.com/rizzit17/O2R-recommender.git
cd O2R-recommender

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install streamlit pandas pyarrow fastparquet
```

### Running the App

To launch the recommendation dashboard locally:

```bash
streamlit run app.py
```

This will open the application in your default web browser at `http://localhost:8501`.

---

## ⚙️ How the Engine Works

1. **User Selection:** The user selects a specific `Retailer ID` via the sidebar.
2. **Profile Loading:** The app queries `retailer_features.parquet` to load the retailer's historical data, total orders, and unique product counts.
3. **Recommendation Generation:** 
   - `hybrid_engine.py` calculates a similarity score against other users using the pre-computed `similarity_matrix.parquet`.
   - It filters out products the retailer has already purchased.
   - It cross-references Regional Trends and Global Popularity scores.
   - A final weighted score is generated, ranking the top products visually in the UI with dynamic progress bars.

---

## 📝 Important Note on Data Privacy

For confidentiality and data privacy reasons, the proprietary datasets (`.parquet`, `.xlsx`) and pre-trained machine learning models (`.pkl`) are not included in this repository. 

These files are located in `data/` and `models/` and have been intentionally excluded via `.gitignore` to prevent exposing sensitive information. If you are cloning this repository to test the application, you will need to provide your own datasets following the structure outlined in the notebooks, and run the processing scripts to generate the required `.parquet` and `.pkl` files.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/rizzit17/O2R-recommender/issues).
