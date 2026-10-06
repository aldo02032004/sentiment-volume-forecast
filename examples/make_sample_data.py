# Bikin ulang examples/sample_export.xlsx: data palsu 120 hari dengan format export yang sama.
# Jalankan: python examples/make_sample_data.py
import numpy as np
import pandas as pd

rng = np.random.default_rng(7)
dates = pd.date_range("2026-05-01", periods=120, freq="D")
day = np.arange(len(dates))
rows = []
for sentiment, base, trend in (("positive", 90, 0.2), ("negative", 120, -0.1), ("neutral", 50, 0.0)):
    level = base + trend * day - 20 * (dates.dayofweek >= 5) + 15 * np.sin(day / 9)   # tren + akhir pekan sepi + gelombang
    level *= np.where(rng.random(len(day)) < 0.05, rng.uniform(2, 3.5, len(day)), 1)   # sesekali lonjakan isu
    for d, n in zip(dates, rng.poisson(np.clip(level, 5, None))):
        rows += [(d + pd.Timedelta(seconds=int(s)), sentiment, f"user_{a}")
                 for s, a in zip(rng.integers(0, 86400, n), rng.integers(0, 3000, n))]

df = pd.DataFrame(rows, columns=["Date", "Sentiment", "Author"]).sort_values("Date", ignore_index=True)
n = len(df)
df = df.assign(No=np.arange(1, n + 1), Type="Tweet", Headline="", Mentions="contoh postingan",
               Link="https://example.com", Media="Twitter", Followers=rng.integers(10, 50000, n),
               Retweeted=rng.integers(0, 100, n), Favourited=rng.integers(0, 300, n), Location="",
               Date=df["Date"].dt.strftime("%Y-%m-%d %H:%M:%S"))
cols = ["No", "Type", "Headline", "Mentions", "Date", "Link", "Media", "Sentiment",
        "Author", "Followers", "Retweeted", "Favourited", "Location"]
df[cols].to_excel("examples/sample_export.xlsx", index=False, startrow=1)   # baris 1 kosong, header di baris 2 (sama kayak export asli)
print(f"examples/sample_export.xlsx: {n:,} baris")
