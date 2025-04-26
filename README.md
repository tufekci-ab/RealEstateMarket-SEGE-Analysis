# SEGE Score and Real Estate Price Analysis

## Project Overview

This project investigates whether there is a significant relationship between the Socio-Economic Development Index (SEGE) scores of districts and the real estate prices within those districts in Turkey. SEGE provides a comparative socio-economic ranking of regions, and understanding its correlation with real estate values could offer valuable insights for investment decisions and urban development planning.

## Motivation

Socio-economic development directly influences property demand, pricing trends, and investment potential. Higher SEGE scores often correspond to better infrastructure, education, healthcare, and employment opportunities, which in turn may affect real estate prices. This project aims to explore and quantify this potential relationship.

## Research Questions

- **Null Hypothesis (H₀):** There is no statistically significant relationship between SEGE scores and real estate prices.
- **Alternative Hypothesis (H₁):** There is a statistically significant relationship between SEGE scores and real estate prices.

## Data Sources

- **Hepsiemlak.com:** Property listings scraped from various districts. Due to Cloudflare protections, scraping was challenging. Data was collected using multiple parallel Azure-based client instances to bypass rate limits and anti-bot measures. Approximately 150,000 raw listings were initially collected.

- **SEGE Scores:** Official Socio-Economic Development rankings for Turkish regions.

The real estate dataset was enriched by merging scraped property listings with corresponding SEGE scores for each district.

### Data Cleaning and Filtering

- Listings were **filtered by title deed (tapu) status**. Only properties with either "Kat İrtifakı" (floor servitude) or "Kat Mülkiyeti" (floor ownership) were retained. Properties without official title deed status were excluded to ensure legal certainty and comparability across listings.
- **New buildings (Sıfır Bina)** were subsequently filtered out. Since newly constructed properties often have inflated prices that do not yet reflect true market dynamics, they were excluded to maintain market consistency.
- **Outlier Removal:** Data was filtered between the 1st and 99th percentiles for price and area variables to eliminate extreme values.
- As a result of these cleaning steps, approximately **two-thirds of the original 150,000 listings were removed**. The final analysis was based on around 50,000 high-quality and comparable listings.

## Methods

- Web scraping of real estate listings.
- Data cleaning, preprocessing, and merging with SEGE data.
- Exploratory Data Analysis (EDA)
- Normality Testing (KS-Lilliefors, Anderson-Darling)
- Non-parametric Hypothesis Testing (Spearman's Rank Correlation)

## Exploratory Data Analysis (EDA)

A thorough exploratory data analysis was conducted to better understand the underlying distribution of the variables:

- **Histograms:** To observe the distribution and skewness of variables such as property price, area, and SEGE scores.
- **Boxplots:** To detect outliers and visualize the spread of property prices and SEGE scores.
- **Q-Q Plots:** To assess the normality of the data distributions.
- **Normality Testing:** KS-Lilliefors and Anderson-Darling tests were applied, revealing that the variables do not follow a normal distribution.
- **Correlation Matrix:** To explore linear relationships between key variables.
- **Log and Box-Cox Transformations:** Applied to achieve distributions closer to normality when necessary.
- **Outlier Removal:** Data was filtered between the 1st and 99th percentiles to eliminate extreme values that could skew analysis.

## Key Results

- The data did not follow a normal distribution, as verified through normality tests.
- Spearman's correlation analysis showed:
  - **Spearman Correlation Coefficient:** ~0.4371
  - **p-value:** < 0.001
- **Conclusion:** The null hypothesis (H₀) was rejected. There is a statistically significant positive relationship between SEGE scores and real estate prices.

## Project Structure

```
RealEstateMarket-SEGE-Analysis/
├── data/                      # Raw scraped data and SEGE scores
├── eda_outputs/              # EDA outputs: histograms, QQ plots, summaries
├── hypothesis_outputs/       # Result of hypothesis test
├── src/                      # All Python scripts (EDA, PDF, Hypothesis, etc.)
├── analysis_ready_data.csv   # Final cleaned dataset
├── EDA_Report.pdf            # Final PDF report with all visuals
├── run_all.bat               # One-click execution script
├── requirements.txt          # Python dependencies
├── .gitignore
└── README.md
```

## How to Run

1. Ensure your cleaned dataset is named `analysis_ready_data.csv`.
2. Generate EDA outputs:
    ```bash
    python src/EDA-Calculator.py
    ```
3. Create the EDA PDF report:
    ```bash
    python src/PDF-Maker.py
    ```
4. Perform hypothesis testing:
    ```bash
    python src/hypothesis_test_student.py
    ```

## Requirements

Install necessary libraries:
```bash
pip install -r requirements.txt
```

## Limitations

- Data scraping was challenged by anti-bot measures (Cloudflare); bypassing required multiple parallel cloud instances.
- Dataset matching between SEGE scores and property data involved assumptions based on district names.
- Only residential real estate was considered.
- Temporal factors (seasonality, economic conditions) were not included.

## Future Work

- Implement predictive modeling (e.g., Random Forest, XGBoost) to estimate property prices.
- Apply Deep Learning models for advanced feature extraction and prediction.
- Extend dataset to include commercial properties, rental prices, and additional socio-economic indicators.

---

This project lays the foundation for understanding socio-economic impacts on real estate pricing and sets the stage for more advanced modeling efforts.

