import numpy as np
import pandas as pd
import yfinance as yf
import time
from datetime import datetime

tickers = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA", "META"]

all_data = []

for ticker in tickers:

    stock = yf.Ticker(ticker)
    expirations = stock.options

    for expiry in expirations:

        option_chain = stock.option_chain(expiry)
        calls = option_chain.calls

expirations = stock.options
print("Available expirations:", expirations)

today = datetime.utcnow()

all_data = []
for expiry in expirations:

    time.sleep(1)
    option_chain = stock.option_chain(expiry)
    calls = option_chain.calls

    expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
    T = max((expiry_date - today).days / 365, 0)

    if 0.02 < T < 1.0:
        for _, row in calls.iterrows():
            all_data.append({
                "strike": row["strike"],
                "impliedVol": row["impliedVolatility"],
                "maturity": T
            })

df = pd.DataFrame(all_data)
S0 = stock.history(period="1d")["Close"].iloc[-1]
print("Current price:", S0)
df["moneyness"] = df["strike"] / S0
print("Number of rows:", len(df))
print(df.head())

# Clean data
df = df[df["impliedVol"] > 0]
df = df[df["impliedVol"] < 2] 
df = df[df["maturity"] > 0]

# Remove extreme strikes (optional but recommended)
lower_strike = df["strike"].quantile(0.05)
upper_strike = df["strike"].quantile(0.95)
df = df[(df["strike"] >= lower_strike) & (df["strike"] <= upper_strike)]

print("\nCleaned data sample:")
print(df.head())

# Add maturity in days and months (for interpretation only)
df["maturity_days"] = df["maturity"] * 365
df["maturity_months"] = df["maturity"] * 12

print("\nWith maturity in days:")
print(df[["maturity", "maturity_days", "maturity_months"]].head())

import plotly.graph_objects as go

from scipy.interpolate import griddata

K = df["moneyness"].values 
T = df["maturity"].values
IV = df["impliedVol"].values

K_lin = np.linspace(min(K), max(K), 50)
T_lin = np.linspace(min(T), max(T), 50)

K_grid, T_grid = np.meshgrid(K_lin, T_lin)

IV_grid = griddata(
    (K, T),
    IV,
    (K_grid, T_grid),
    method="linear"
)
IV_grid = np.nan_to_num(IV_grid, nan=np.nanmean(IV))
fig = go.Figure(data=[
    go.Surface(z=IV_grid, x=K_lin, y=T_lin)
])

fig.update_layout(
    title="Smoothed Implied Volatility Surface",
    scene=dict(
        xaxis_title="Moneyness (K/S)",
        yaxis_title="Maturity (Years)",
        zaxis_title="Implied Volatility"
    ),
    width=1000,
    height=750
)

fig.show()
import matplotlib.pyplot as plt

# Choose a maturity close to 3 months
target_maturity = 0.03

subset = df[np.abs(df["maturity"] - target_maturity) < 0.02]

plt.scatter(subset["moneyness"], subset["impliedVol"])

plt.xlabel("Moneyness (K/S)")
plt.ylabel("Implied Volatility")
plt.title("Volatility Smile (3M maturity)")
print("Smile data points:", len(subset))

plt.show()

import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# -------------------------
# Volatility Smile
# -------------------------

target_maturity = df["maturity"].median()
subset = df[np.abs(df["maturity"] - target_maturity) < 0.01]

print("Smile data points:", len(subset))

# -------------------------
# Skew calculation
# -------------------------

atm_subset = subset[(subset["moneyness"] > 0.9) & (subset["moneyness"] < 1.1)]

X = atm_subset["moneyness"].values.reshape(-1,1)
y = atm_subset["impliedVol"].values

model = LinearRegression()
model.fit(X, y)

skew = model.coef_[0]

print("Volatility skew:", skew)

# -------------------------
# Smile fit
# -------------------------

x = subset["moneyness"].values
y = subset["impliedVol"].values

coeffs = np.polyfit(x, y, 2)
poly = np.poly1d(coeffs)

x_fit = np.linspace(min(x), max(x), 200)
y_fit = poly(x_fit)

# -------------------------
# Plot
# -------------------------

plt.scatter(x, y, label="Market data")
plt.plot(x_fit, y_fit, color="red", linewidth=2, label="Fitted smile")

plt.xlabel("Moneyness (K/S)")
plt.ylabel("Implied Volatility")
plt.title("Volatility Smile with Fit")
plt.legend()

plt.show()