# Bikin data contoh (palsu) dengan format export yang sama, buat nyoba notebook tanpa data asli.
# Jalankan:  python examples/make_sample_data.py
# Hasil:     examples/sample_export.xlsx -> upload ke Google Drive, share "Anyone with the link", tempel linknya di SOURCES
import numpy as np
import pandas as pd

DAYS = 120          # panjang data (hari)
START = "2026-05-01"
SEED = 7            # ganti angka ini buat dapat data contoh lain

rng = np.random.default_rng(SEED)
dates = pd.date_range(START, periods=DAYS, freq="D")
weekend = (dates.dayofweek >= 5).astype(float)

rows = []
for sentiment, base, trend in (("positive", 90, 0.2), ("negative", 120, -0.1), ("neutral", 50, 0.0)):
    # rata-rata harian = dasar + tren pelan - efek akhir pekan + gelombang + sesekali lonjakan isu
    level = base + trend * np.arange(DAYS) - 20 * weekend + 15 * np.sin(np.arange(DAYS) / 9)
    level *= np.where(rng.random(DAYS) < 0.05, rng.uniform(2, 3.5, DAYS), 1)
    for day, n in zip(dates, rng.poisson(np.clip(level, 5, None))):
        for _ in range(n):
            rows.append({"Date": day + pd.Timedelta(seconds=int(rng.integers(0, 86400))),
                         "Sentiment": sentiment, "Author": f"user_{rng.integers(0, 3000)}"})

df = pd.DataFrame(rows).sort_values("Date").reset_index(drop=True)
df.insert(0, "No", np.arange(1, len(df) + 1))
df["Type"] = "Tweet"
df["Headline"] = ""
df["Mentions"] = [f"contoh postingan {i}" for i in df["No"]]
df["Link"] = [f"https://example.com/post/{i}" for i in df["No"]]
df["Media"] = "Twitter"
df["Followers"] = rng.integers(10, 50000, len(df))
df["Retweeted"] = rng.integers(0, 100, len(df))
df["Favourited"] = rng.integers(0, 300, len(df))
df["Location"] = ""
df["Date"] = df["Date"].dt.strftime("%Y-%m-%d %H:%M:%S")
df = df[["No", "Type", "Headline", "Mentions", "Date", "Link", "Media", "Sentiment",
         "Author", "Followers", "Retweeted", "Favourited", "Location"]]

# file export asli punya 1 baris judul di atas header, jadi header ditaruh di baris ke-2
with pd.ExcelWriter("examples/sample_export.xlsx") as writer:
    pd.DataFrame([["Sample export (synthetic data)"]]).to_excel(writer, index=False, header=False)
    df.to_excel(writer, index=False, startrow=1)
print(f"examples/sample_export.xlsx: {len(df):,} baris, {DAYS} hari")
