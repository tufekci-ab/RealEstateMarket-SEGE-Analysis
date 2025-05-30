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
- As a result of these cleaning steps, approximately **a third of the original 150,000 listings were removed**. The final analysis was based on around 100,000 high-quality and comparable listings.

## Extra Data Collection

To enhance the analytical depth and prepare for future modeling tasks, we developed a second-stage scraper that collects additional features directly from each listing’s detail page, rather than from the summary listing page. This approach enabled the extraction of seven new variables such as heating type, number of bathrooms, number of floors, and property orientation—information that is not consistently available in the listing previews.

This secondary scraper resulted in the addition of over 10,000 new rows of data, significantly enriching the dataset. Due to increased ban risks when accessing listing pages individually, we were not able to revisit the entire dataset. Nonetheless, the extra data serves as a valuable augmentation for subsequent predictive modeling efforts and will be utilized in later phases of the project.

To safely scale the scraping process, the new scraper was executed across multiple Azure-based client machines in parallel, similar to the initial scraping setup. However, these deployment configurations are infrastructure-specific and not tightly coupled with the scraper code itself, so they are not included in the repository. Only the scraper logic is pushed as a single consolidated script to maintain codebase clarity.


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
- SEGE scores are moderately and positively associated with real estate prices.
- Districts with higher socio-economic development tend to have more expensive properties, controlling for basic listing features.


## Machine Learning Phase

In the final stage of the project, a machine learning model was developed to predict real estate prices using both SEGE scores and enriched listing-level attributes collected via a detail-page scraper.

### Models Tried

- **Random Forest Regressor**  
  Initially used for its interpretability and strong performance on structured data.  
  **Observation:** Tended to overfit the training data despite parameter tuning efforts. Performance degraded on unseen data.

- **XGBoost Regressor**  
  Chosen as the final model due to better generalization and robustness to overfitting.

### Features Used

- SEGE score  
- Net area (m²)  
- Number of rooms  
- Number of bathrooms  
- Heating type  
- Building age  
- Total number of floors  
- Orientation (e.g., south-facing)

### Scripts

- **Model training:** `src/final_model.py`  
- **Hyperparameter tuning:** `src/hyperopt.py`  
- **Evaluation output:** `ML Model Insights.html`  
- **Serialized model file:** `trained_model.pkl`

## Project Structure

```
RealEstateMarket-SEGE-Analysis/
├── data/                          # Raw data, SEGE scores
├── eda_outputs/                  # Histograms, plots
├── hypothesis_outputs/           # Hypothesis test results
├── src/                          # All Python scripts (EDA, PDF, Modeling, etc.)
│   ├── EDA-Calculator.py
│   ├── final_model.py
│   ├── hyperopt.py
│   ├── hypothesis-tester.py
│   ├── PDF-Maker.py
│   ├── processBeforeEDA.py
│   └── merge-extras-with-previous.py
├── analysis_ready_data.csv       # Cleaned dataset for modeling
├── trained_model.pkl             # Serialized trained XGBoost model
├── ML Model Insights.html        # Summary + visualizations of model performance
├── EDA_Report.html               # EDA report with plots and summaries
├── run_all.bat                   # One-click script to execute pipeline
├── requirements.txt              # Python packages
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

- **Retrain with enriched data:** Incorporate the 10,000+ listings enriched via the detail-page scraper, which includes 7 additional features (e.g., heating type, bathroom count, orientation) to improve model complexity and accuracy.

- **Extend modeling efforts:** Evaluate and compare advanced machine learning models (e.g., Random Forest, XGBoost, LightGBM) using a wider set of listing-level and regional features. Focus on generalization and cross-validation stability.

- **Control for time effects:** Introduce temporal data (e.g., date of listing, inflation, interest rates) to study market dynamics over time and detect temporal patterns in price changes.

## GPU Support

If you wish to train models using GPU acceleration, ensure that the appropriate CUDA drivers and toolkit (e.g., CUDA 11.7+) are installed on your system. The code will automatically utilize the GPU if available.


## AI Assistance Disclaimer

GenAI tools were occasionally used to support writing and analysis. All final decisions and implementations were made by the project team.


---
---

This project lays the foundation for understanding socio-economic impacts on real estate pricing and sets the stage for more advanced modeling efforts.

