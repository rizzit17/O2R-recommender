# 🛒 O2R Retailer Recommendation Engine

An AI-powered recommendation system designed to help retailers discover relevant products based on historical purchasing behavior, regional demand patterns, and product popularity.

## Problem Statement

Retailers using the O2R platform have access to hundreds of products but often:

* Miss relevant products
* Reorder only familiar items
* Miss cross-selling opportunities
* Lack personalized recommendations

This project aims to provide intelligent product recommendations using machine learning and data-driven insights.

---

## Key Features

* Personalized retailer recommendations
* Collaborative Filtering using Cosine Similarity
* Association Rule Mining using FP-Growth
* Regional Trend Analysis
* Product Popularity Scoring
* Hybrid Recommendation Engine
* Interactive Streamlit Dashboard

---

## System Architecture

```text
Retailer Orders
       │
       ▼
Data Cleaning
       │
       ▼
Feature Engineering
       │
 ┌─────┼─────┐
 ▼     ▼     ▼
Retailer Product Region
Features Features Trends
       │
       ▼
Recommendation Models
       │
 ┌─────┼─────┬─────┐
 ▼     ▼     ▼
Collaborative Filtering
FP-Growth Association Rules
Regional Trends
Popularity Scoring
       │
       ▼
Hybrid Recommendation Engine
       │
       ▼
Streamlit Dashboard
```

---

## Dataset

### Current Development Dataset

* 100,000 retailer transactions

### Final Production Dataset

* 609,724 retailer transactions

### Data Fields

* Customer ID
* SKU Number
* Product Name
* Quantity
* Hub
* Shop Type
* Brand
* Category
* Transaction Date

---

## Data Processing Pipeline

### Data Cleaning

* Missing value analysis
* Duplicate removal
* Data type correction
* SKU validation
* Customer validation
* Product mapping validation
* Quantity validation
* Memory optimization using Parquet files

### Feature Engineering

#### Retailer Features

* Total Orders
* Total Quantity
* Unique Products
* Favorite Brand
* Favorite Category
* Spend Segment
* Hub
* Shop Type

#### Product Features

* Popularity Score
* Purchase Frequency

#### Region Features

* Hub-wise Product Rankings

---

## Machine Learning Components

### 1. Collaborative Filtering

Uses cosine similarity on retailer-product interaction matrices to identify retailers with similar purchasing behavior.

### 2. FP-Growth Association Rule Mining

Discovers products frequently purchased together.

Example:

```text
Rajnigandha → TZ
```

Generated:

* 125 association rules (100K dataset)

### 3. Regional Trend Recommendation

Captures local demand patterns across hubs and shop types.

### 4. Popularity-Based Recommendation

Ranks products based on overall sales performance.

---

## Hybrid Recommendation Engine

Final recommendation score:

```text
Final Score =
0.60 × Collaborative Filtering
+
0.25 × Regional Trend Score
+
0.15 × Popularity Score
```

Products are ranked based on the final hybrid score.

---

## Project Workflow

### Notebook 1

Data Cleaning & EDA

### Notebook 2

Retailer-Product Interaction Matrix

### Notebook 3

Retailer Feature Engineering

### Notebook 4

Product Feature Engineering

### Notebook 5

Regional Trend Analysis

### Notebook 6

FP-Growth Association Rules

### Notebook 7

Similarity Matrix Generation

### Notebook 8

Hybrid Recommendation Engine

### Notebook 9

Testing & Validation

---

## Streamlit Dashboard

Features:

* Retailer Selection
* Retailer Profile Analysis
* Recommendation Generation
* Recommendation Score Visualization
* Business Insights

---

## Current Results

* 100,000 transactions processed
* Thousands of retailers analyzed
* 125 association rules generated
* Retailer similarity matrix created
* Hybrid recommendation engine deployed
* Interactive Streamlit dashboard operational

---

## Tech Stack

### Data Processing

* Python
* Pandas
* NumPy

### Machine Learning

* Scikit-Learn
* Cosine Similarity
* FP-Growth

### Storage

* Parquet

### Dashboard

* Streamlit

---

## Future Enhancements

* FP-Growth integration into hybrid scoring
* Demand forecasting
* Inventory prediction
* Cross-sell recommendation module
* FastAPI deployment
* Real-time recommendation service

---

## Key Concepts Demonstrated

* Recommendation Systems
* Collaborative Filtering
* Association Rule Mining
* Feature Engineering
* Similarity Learning
* Hybrid Ranking Systems
* Streamlit Deployment
* Retail Analytics
