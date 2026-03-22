# 3D Implied Volatility Surface Modeling

This project focuses on the construction and analysis of an implied volatility surface using real option market data. It combines financial theory, quantitative modeling, and data analysis to study volatility dynamics across strike prices and maturities.

## Theoretical Framework

The project is based on the Black–Scholes model, where the underlying asset follows a geometric Brownian motion:

dS_t = μS_t dt + σS_t dW_t

European call options are priced using:

C(S_t, K, T) = S_t Φ(d1) − K e^{-r(T−t)} Φ(d2)

The implied volatility is extracted by inverting this formula from observed market prices.

## Features

- Option data collection using `yfinance`
- Data cleaning and filtering (removal of arbitrage inconsistencies)
- Implied volatility computation
- 2D interpolation across strike and maturity dimensions
- Construction of a smooth 3D volatility surface
- Interactive visualization using Plotly

## Volatility Surface Analysis

The resulting surface highlights key stylized facts observed in financial markets:

- Volatility smile (dependence on moneyness)
- Term structure of volatility
- Asymmetric risk expectations

These findings illustrate the limitations of the constant volatility assumption in Black–Scholes.

## Technologies Used

- Python
- NumPy / Pandas
- SciPy
- Plotly
- yfinance

## Project Structure

- `main.py` — core implementation
- `requirements.txt` — dependencies
- `README.md` — project description

## Academic Context

This project was developed as part of an independent study in quantitative finance, focusing on volatility modeling and derivative pricing.

A full theoretical report (including model derivations and economic interpretation) is available upon request.

## Future Improvements

- Implementation of stochastic volatility models (Heston)
- Local volatility calibration
- Real-time market data integration