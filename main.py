import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime

ticker = "AAPL"
stock = yf.Ticker(ticker)

expirations = stock.options
print("Available expirations:", expirations)

today = datetime.utcnow()

all_data = []

for expiry in expirations[:5]:  # We start by taking only the first 5 maturities
    option_chain = stock.option_chain(expiry)
    calls = option_chain.calls

    expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
    T = max((expiry_date - today).days / 365, 0)

    for _, row in calls.iterrows():
        all_data.append({
            "strike": row["strike"],
            "impliedVol": row["impliedVolatility"],
            "maturity": T
        })

df = pd.DataFrame(all_data)

# Clean data
df = df[df["impliedVol"] > 0]
df = df[df["maturity"] > 0]

# Remove extreme strikes (optional but recommended)
lower_strike = df["strike"].quantile(0.05)
upper_strike = df["strike"].quantile(0.95)
df = df[(df["strike"] >= lower_strike) & (df["strike"] <= upper_strike)]

print("\nCleaned data sample:")
print(df.head())

import plotly.graph_objects as go

from scipy.interpolate import griddata

K = df["strike"].values
T = df["maturity"].values
IV = df["impliedVol"].values

K_lin = np.linspace(min(K), max(K), 50)
T_lin = np.linspace(min(T), max(T), 50)

K_grid, T_grid = np.meshgrid(K_lin, T_lin)

IV_grid = griddata(
    (K, T),
    IV,
    (K_grid, T_grid),
    method="cubic"
)

fig = go.Figure(data=[
    go.Surface(z=IV_grid, x=K_lin, y=T_lin)
])

fig.update_layout(
    title="Smoothed Implied Volatility Surface",
    scene=dict(
        xaxis_title="Strike",
        yaxis_title="Maturity (Years)",
        zaxis_title="Implied Volatility"
    ),
    width=900,
    height=700
)

fig.show()