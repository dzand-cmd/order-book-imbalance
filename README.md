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
├── src/  
│   ├── order_book_imbalance.py   # Core imbalance computation and analysis  
├── .gitignore                     # Ignored files and cache settings  
├── README.md                      # Project documentation


## How to run

git clone https://github.com/dzand-cmd/order-book-imbalance.git  
cd order-book-imbalance  
pip install numpy pandas matplotlib  
python src/order_book_imbalance.py

