import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Messy 15-day weather log (+1 duplicated row = 16 raw rows)
dates = [f"2026-06-{d:02d}" for d in range(1, 16)]
city = ["islamabad", "Islamabad ", " ISLAMABAD", "Islamabad", "islamabad ",
        "Islamabad", " islamabad", "ISLAMABAD", "Islamabad ", "islamabad",
        "Islamabad", " Islamabad", "ISLAMABAD ", "islamabad", "Islamabad"]
temp = ["32C", "27C", "29C", "35C", "36C", "26C", "34C", "37C",
        "30C", "28C", "33C", "38C", "25C", "35C", "31C"]
hum = [45, 78, np.nan, 40, 38, 82, 50, np.nan,
       65, 72, 55, 35, np.nan, 42, 60]
cond = ["sunny", " Rainy", "CLOUDY ", "sunny", "Sunny", "rainy ", "Cloudy",
        "SUNNY", "cloudy", " Rainy", "Sunny", "sunny ", "RAINY", "Sunny", "cloudy"]

raw = pd.DataFrame({"Date": dates, "City": city, "Temperature": temp,
                    "Humidity": hum, "Condition": cond})
raw = pd.concat([raw, raw.iloc[[2]]], ignore_index=True)   # duplicated row

df = raw.copy()

# (a) Cleaning
df["City"] = df["City"].str.strip().str.title()
df["Condition"] = df["Condition"].str.strip().str.title()
df["Temperature"] = pd.to_numeric(df["Temperature"].str.replace("C", "", regex=False),
                                  errors="coerce")
df["Date"] = pd.to_datetime(df["Date"])
df = df.drop_duplicates().reset_index(drop=True)
print("Rows after dropping duplicates:", len(df))
median_h = df["Humidity"].median()
df["Humidity"] = df["Humidity"].fillna(median_h)
print("Missing Humidity filled with median:", median_h)

# (b) One-hot encoding
encoded = pd.get_dummies(df, columns=["Condition"], dtype=int)
print(encoded.filter(like="Condition_").head())

# (d) correlation
corr = df["Temperature"].corr(df["Humidity"])
print("Correlation (Temperature, Humidity):", round(corr, 2))

# (e) counts
counts = df["Condition"].value_counts()
print("Condition counts:")
print(counts)

# (c, d, e, f) 2x2 dashboard
fig, axes = plt.subplots(2, 2, figsize=(12, 9))

axes[0, 0].plot(df["Date"], df["Temperature"], marker="o", color="tomato")
axes[0, 0].set_title("Temperature over Date")
axes[0, 0].set_xlabel("Date")
axes[0, 0].set_ylabel("Temperature (°C)")
axes[0, 0].tick_params(axis="x", rotation=45)
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].scatter(df["Temperature"], df["Humidity"], color="darkorange", s=60)
axes[0, 1].set_title(f"Temperature vs. Humidity (r = {corr:.2f})")
axes[0, 1].set_xlabel("Temperature (°C)")
axes[0, 1].set_ylabel("Humidity (%)")
axes[0, 1].grid(True, alpha=0.3)

axes[1, 0].pie(counts.values, labels=counts.index, autopct="%1.1f%%", startangle=90)
axes[1, 0].set_title("Days per Condition")

axes[1, 1].hist(df["Temperature"], bins=5, color="seagreen", edgecolor="white")
axes[1, 1].set_title("Temperature Distribution")
axes[1, 1].set_xlabel("Temperature (°C)")
axes[1, 1].set_ylabel("Number of Days")

fig.suptitle("Weather Overview", fontsize=16)
plt.tight_layout()
plt.savefig("weather_dashboard.png")
plt.show()
print("Saved weather_dashboard.png")
