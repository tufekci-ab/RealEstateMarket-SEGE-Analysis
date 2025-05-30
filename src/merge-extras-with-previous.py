
import pandas as pd, re

df_main = pd.read_csv("analysis_ready_data.csv")
df_extra = pd.read_csv("extra-data.csv")
df = pd.merge(df_main, df_extra, on="ilan_id", how="inner")


df["bina_yasi"] = df["bina_yasi"].astype(str).str.extract(r"(\d+)").astype(float)

def parse_oda(x):
    try:
        o, s = x.split("+")
        return int(o), int(s)
    except:
        return None, None

df["oda_sayisi_yeni"], df["salon_sayisi"] = zip(*df["oda_sayisi"].apply(parse_oda))
df.drop(columns=["oda_sayisi"], inplace=True)

df["kat_sayisi"] = df["kat_sayisi"].astype(str).str.extract(r"(\d+)").astype(float)

def kat_enc(r):
    k = str(r["kat"]).strip().lower()
    ks = r["kat_sayisi"]
    if pd.isna(k): return None
    if any(x in k for x in ["bahçe", "zemin", "giriş"]): return 0
    if any(x in k for x in ["kot", "yüksek"]): return -1
    if "ara" in k: return int(round(ks / 2)) if not pd.isna(ks) else None
    if "en üst" in k: return int(ks) if not pd.isna(ks) else None


    m = re.match(r"(\d+)\.*\s*kat", k)
    if m: return int(m.group(1))

    return None

df["kat_sayisi_encoded"] = df.apply(kat_enc, axis=1)

cephe = df["cephe"].astype(str).str.lower()
df["cephe_kuzey"] = cephe.str.contains("kuzey").astype(int)
df["cephe_guney"] = cephe.str.contains("güney").astype(int)
df["cephe_dogu"] = cephe.str.contains("doğu").astype(int)
df["cephe_bati"] = cephe.str.contains("batı").astype(int)

df = df[~df["kat_sayisi_encoded"].isna()]


df.replace("", pd.NA, inplace=True)
df.dropna(inplace=True)

df.to_csv("detailed-listings-cleaned.csv", index=False, encoding="utf-8-sig")
print("merged: detailed-listings-cleaned.csv")
