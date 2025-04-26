import pandas as pd

# Read the CSV file
file_path = "hepsiemlak_500k+.txt"
df = pd.read_csv(file_path)

# Check if the columns match the expected ones
expected_columns = ["ilan_id", "ilan_linki", "ilan_tarihi", "ilan_tipi", "metrekare", "bina_yasi", "kat", "konum", "fiyat", "para_birimi"]

if list(df.columns) != expected_columns:
    raise ValueError(f"Columns do not match. Current columns: {list(df.columns)}")

# Clean the 'fiyat' column and convert to Int64
df['fiyat'] = df['fiyat'].astype(str).str.replace('.', '').str.replace(',', '')
df['fiyat'] = df['fiyat'].astype('Int64')

# Remove rows where 'konum' contains 'Kıbrıs'
rows_before_kibris = len(df)
df = df[~df['konum'].str.contains("Kıbrıs", na=False)]
rows_after_kibris = len(df)

# Sort by 'fiyat' ascending
df = df.sort_values(by='fiyat', ascending=True)

# Drop duplicate rows
rows_before_dups = len(df)
df = df.drop_duplicates()
rows_after_dups = len(df)

# Save to new CSV file
output_path = "hepsiemlak_500k_sorted.csv"
df.to_csv(output_path, index=False)

print(f"Rows removed that include (kıbrıs) {rows_before_kibris - rows_after_kibris}")
print(f"Duplicates removed: {rows_before_dups - rows_after_dups}")
print(f"Cleaned file saved to: {output_path}")
