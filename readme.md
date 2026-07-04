# Telangana PDS Analytics

## Project Overview
This project analyse the Telangana fair price shop across the state
using the data from 2023-2025. Here we use the given data to analyse 
policy impact analysis, fraud prevention, logistic optimization. 

## Datasets Used
From Telangana open data portal download 
1. Transaction Data https://data.telangana.gov.in/dataset/telangana-state-civil-supplies-distribution-fp-shop-wise-transactions-data
2. Card Status Data https://data.telangana.gov.in/dataset/telangana-state-civil-supplies-distribution-fair-price-shop-card-status-data
3. FPS location https://data.telangana.gov.in/dataset/telangana-state-civil-supplies-distribution-fair-price-shop-status-latitude-and-longitude

## Features Engineered
4 Feature Engineering has been done
1. utilization_ratio -- How many LOCAL families actually came to collect ration?

   utilization_ratio = (Total transactions - Outside visitors) / Total ration cards

3. portability_rate -- What % of total visitors are from OUTSIDE this shop's area?

   portability_rate = Outside visitors / Total transactions

5. rice_per_card -- On average, how much rice (kg) does each ration card holder get?

   total_rice = riceafsc + ricefsc + riceaap

   rice_per_card = Total rice distributed / Total ration cards

7. shop_volatility -- How CONSISTENT is this shop month to month?

   shop_volatility = Standard deviation of transactions across 29 months

## Dimensionality Reduction (PCA)
- Reduced 4 features to 2 components
- PC1 explains 62.87% variance
- PC2 explains 24.41% variance
- Total: 87.27% information retained

## Clustering Results
The data is aggregated, scaled using standard scaler. 

Elbow method is used to find the number of clusters.

k-means = 5

The shops are clustered into 5 groups.

Clusters are grouped using the feature engineering.

Cluster summary shows
- cluster 0 and 4 -- stable local hubs with trans_volatility less
- cluster 1 -- suspicious because of high trans_volatility
- cluster 2 and 3 --may be urban hubs with more moving population

## Model Evaluation
- Silhouette Score: 0.38 (reasonable clustering for real-world data)
- Optimal K selected using Elbow Method

## Anomaly Detection (DBSCAN)
- eps=0.5, min_samples=5
- 147 shops flagged as NOISE (anomalies)
- Most suspicious shop: 1599003 (Ranga Reddy)
  - trans_volatility = 1240 (73x higher than normal!)

## How to Run
1. Clone the repository
2. Install dependencies:
   pip install -r requirements.txt
3. Run the dashboard:
   streamlit run app/app.py
4. Open browser at http://localhost:8501

## Key Insights
1. Portability transactions increased ~20% from 2023-2025
   indicating growing adoption of One Nation One Ration Card policy

2. Perfect correlation (1.00) between ration cards and transactions
   showing shops serve proportional beneficiaries

3. PDS transactions show no seasonality (~440-450/month)
   confirming ration is a basic necessity

4. Rice distribution uniform across all districts (21-23kg/card)
   confirming rice as primary staple food in Telangana

5. 147 anomalous shops detected requiring investigation
   especially in Ranga Reddy and Hyderabad districts
