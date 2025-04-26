import pandas as pd

# Read the real estate listings data
listings = pd.read_csv("hepsiemlak_500k_sorted.csv")

# Read the SEGE scores data
sege = pd.read_csv("sege_scores.csv")

# Convert SEGE column names to lowercase and replace spaces with underscores
sege.columns = sege.columns.str.lower().str.replace(' ', '_')

# Convert 'kademe' column to string (to avoid potential issues during merging)
sege['kademe'] = sege['kademe'].astype(str)

# Split the 'konum' column into 'il' (city) and 'ilce' (district)
listings['il'] = listings['konum'].apply(lambda x: x.split('/')[0].strip())
listings['ilce'] = listings['konum'].apply(lambda x: x.split('/')[1].strip() if len(x.split('/')) > 1 else None)

# Perform the merge operation
merged = listings.merge(sege, on=["il", "ilce"], how="left")

# Save the merged dataset
merged.to_csv("hepsiemlak_500k_with_sege.csv", index=False, encoding="utf-8")

print("Datasets merged successfully.")