# Order Book Imbalance Alpha Signals

**Author:** dzand-cmd  
**Project Type:** Quantitative Research / Algorithmic Trading  
**Language:** Python  
**Status:** In Progress  

---

## Overview

This project implements an order book imbalance signal engine designed to analyze market microstructure data and extract predictive signals from bid-ask pressure. The model computes imbalance metrics across the order book and evaluates their relationship with short-term future price movements.

The goal is to study whether order book pressure can be used as a predictive signal for short-horizon price direction in liquid markets.

## Project Structure

order-book-imbalance/
│
├── order_book_imbalance.py     # Main implementation of imbalance calculation
├── data/                       # Market data (L2 order book snapshots or trades)
├── results/                    # Output metrics, plots, and analysis
├── notebooks/                  # (Optional) Exploratory analysis
└── README.md                   # Project documentation


## How to run

git clone https://github.com/your/repo
cd order-book-imbalance
pip install -r requirements.txt
python src/order_book_imbalance.py
