# Order Book Imbalance

**Author:** Dzandu Selorm (dzand-cmd)  
**Project Type:** Quantitative Trading  
**Language:** Python  
**Status:** Complete 

---

## Overview

This project implements an order book imbalance signal engine designed to analyze market microstructure data and extract predictive signals from bid-ask pressure. The model computes imbalance metrics across the order book and evaluates their relationship with short-term future price movements.

The goal is to study whether order book pressure can be used as a predictive signal for short-horizon price direction in liquid markets.

## Project Structure

order-book-imbalance/  
│  
├── order_book_imbalance.py   # Core imbalance computation and analysis  
├── .gitignore                     # Ignored files and cache settings  
├── README.md                      # Project documentation


## Methodology

- Parse high-frequency limit order book data
- Extract best bid and ask sizes over time
- Compute imbalance signal I(t)
- Align imbalance with forward returns
- Evaluate statistical relationship between imbalance and price movement


## Analysis  
- Correlation between imbalance and next-period returns
- Conditional return analysis (high vs low imbalance regimes)
- Simple predictive test of directional bias
- Visualization of imbalance vs price dynamics


## Assumptions  
- Order book snapshots are representative of near-term liquidity
- Short-term price movements respond to visible liquidity imbalance
- Market impact and hidden liquidity are not explicitly modeled


## Outputs  
- Time series of order book imbalance
- Correlation statistics with returns
- Regime-based return comparison
- Visual plots of imbalance vs price movement


## How to run

git clone https://github.com/dzand-cmd/order-book-imbalance.git  
cd order-book-imbalance  
pip install numpy pandas matplotlib  
python order_book_imbalance.py

