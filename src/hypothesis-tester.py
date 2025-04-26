import pandas as pd
import scipy.stats as stats

# Load the dataset
df = pd.read_csv("analysis_ready_data.csv")

# Check if necessary columns exist
if "skor" in df.columns and "fiyat_per_m2" in df.columns:
    subset = df[["skor", "fiyat_per_m2"]].dropna()

    # Perform the Spearman correlation test
    correlation, p_value = stats.spearmanr(subset["skor"], subset["fiyat_per_m2"])

    # Interpretation
    alpha = 0.05
    result_text = ""

    result_text += "--- Hypothesis Testing ---\n"
    result_text += f"Spearman Correlation Coefficient: {correlation:.4f}\n"
    result_text += f"p-value: {p_value:.4e}\n\n"

    if p_value < alpha:
        result_text += "Conclusion: We reject the null hypothesis.\n"
        result_text += "There is a statistically significant relationship between SEGE score and real estate prices.\n"
    else:
        result_text += "Conclusion: We fail to reject the null hypothesis.\n"
        result_text += "There is no statistically significant relationship between SEGE score and real estate prices.\n"

    # Save result to a text file
    with open("hypothesis_outputs/hypothesis_test_result.txt", "w", encoding="utf-8") as f:
        f.write(result_text)

    print(result_text)
else:
    print("The required columns 'skor' and 'fiyat_per_m2' are missing from the dataset.")