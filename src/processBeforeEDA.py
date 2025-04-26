import pandas as pd

# 1. Load the data
df = pd.read_csv("data/hepsiemlak_500k_with_sege.csv")

# 2–3. Filter for TL currency and exclude new buildings
df = df[df['para_birimi'] == "TL"]
df = df[df['bina_yasi'] != "Sıfır Bina"]

# 4. Clean the area column correctly
df['metrekare'] = (
    df['metrekare']
      .str.replace(" m²", "", regex=False)
      .str.replace(".",  "", regex=False)
      .str.replace(",",  ".", regex=False)
      .astype(float)
)

# 5. Convert price to int64
df['fiyat'] = df['fiyat'].astype('int64')

# 6. Clean invalid data
df = df[(df['fiyat'] > 0) & (df['metrekare'] > 0)]

# 7. Calculate price per square meter and round to 2 decimal places
df['fiyat_per_m2'] = (df['fiyat'] / df['metrekare']).round(2)

# 8. Save the cleaned data
df.to_csv("analysis_ready_data.csv", index=False, encoding="utf-8")
print("Cleaned dataset saved as: analysis_ready_data.csv")