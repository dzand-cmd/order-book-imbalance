import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =========================
# LOAD DATA
# =========================

data = pd.read_csv(r"C:\Users\dzand\quant-projects\order-book-imbalance\data\BTC-USD.csv.gz",compression="gzip",nrows=50000)

# =========================
# BUILD SNAPSHOTS
# =========================

def build_features(dataframe, levels=5):
    snapshots = []
    for timestamp, snapshot in dataframe.groupby("timestamp"):
        bids = snapshot[snapshot["side"] == "bid"]
        asks = snapshot[snapshot["side"] == "ask"]
        if bids.empty or asks.empty:
            continue

        bid_levels = (bids.groupby("price")["amount"].sum().sort_index(ascending=False).head(levels))
        ask_levels = (asks.groupby("price")["amount"].sum().sort_index().head(levels))

        bid_volume = bid_levels.sum()
        ask_volume = ask_levels.sum()

        total_volume = bid_volume + ask_volume

        if total_volume == 0:
            continue

        imbalance = (bid_volume - ask_volume) / total_volume

        best_bid = bid_levels.index[0]
        best_ask = ask_levels.index[0]

        midprice = (best_bid + best_ask) / 2

        snapshots.append((timestamp,imbalance,midprice))

    return pd.DataFrame(snapshots,columns=["timestamp","imbalance","midprice"])

df = build_features(data, levels=5)

df["datetime"] = pd.to_datetime(df["timestamp"],unit="us")

# =========================
# FUTURE RETURNS
# =========================

horizon = 10
df["future_midprice"] = df["midprice"].shift(-horizon)
df["future_return"] = (df["future_midprice"] - df["midprice"]) / df["midprice"]

df = df.dropna()

# =========================
# SIGNAL ANALYSIS
# =========================

correlation = df["imbalance"].corr(df["future_return"])

print("\nCorrelation:")
print(correlation)

# =========================
# BUCKET ANALYSIS
# =========================

bins = [-1, -0.5, 0, 0.5, 1]

labels = ["[-1,-0.5)","[-0.5,0)","[0,0.5)","[0.5,1]"]

df["bucket"] = pd.cut(df["imbalance"],bins=bins,labels=labels,include_lowest=True)

bucket_results = (df.groupby("bucket")["future_return"].mean())

print("\nAverage Future Return by Imbalance Bucket:")
print(bucket_results)

# =========================
# SIGNAL ACCURACY
# =========================

threshold = 0.3
df["signal"] = np.where(df["imbalance"] > threshold,1, np.where(df["imbalance"] < -threshold,-1,0))

active = df["signal"] != 0

signal_accuracy = (np.sign(df.loc[active, "future_return"]) == df.loc[active, "signal"]).mean()

print("\nSignal Accuracy:")
print(signal_accuracy)

# =========================
# SIMPLE STRATEGY
# =========================

df["strategy_return"] = (df["signal"] * df["future_return"])

df["cum_return"] = (1 + df["strategy_return"]).cumprod()

# =========================
# PERFORMANCE METRICS
# =========================

strategy_returns = df.loc[active,"strategy_return"]

if len(strategy_returns) > 1:
    mean_ret = strategy_returns.mean()
    std_ret = strategy_returns.std()

    sharpe = (mean_ret / std_ret if std_ret > 0 else np.nan)

    win_rate = (strategy_returns > 0).mean()

    running_max = (df["cum_return"].cummax())

    drawdown = (df["cum_return"]/ running_max - 1)

    max_drawdown = drawdown.min()

    print("\nStrategy Metrics")
    print("----------------")
    print("Sharpe Ratio:", sharpe)
    print("Win Rate:", win_rate)
    print("Max Drawdown:", max_drawdown)

# =========================
# ROLLING CORRELATION
# =========================

window = 500

df["rolling_corr"] = (df["imbalance"].rolling(window).corr(df["future_return"]))

# =========================
# VISUALIZATIONS
# =========================

plt.figure(figsize=(12,5))
plt.plot(df["datetime"],df["imbalance"])
plt.title("Order Book Imbalance")
plt.xlabel("Time")
plt.ylabel("Imbalance")
plt.show()

plt.figure(figsize=(8,5))
plt.scatter(df["imbalance"],df["future_return"],alpha=0.2)
plt.title("Imbalance vs Future Return")
plt.xlabel("Imbalance")
plt.ylabel("Future Return")
plt.show()

plt.figure(figsize=(8,5))
bucket_results.plot(kind="bar")
plt.title("Average Future Return by Imbalance Bucket")
plt.ylabel("Average Future Return")
plt.show()

plt.figure(figsize=(12,5))
plt.plot(df["datetime"],df["rolling_corr"])
plt.title("Rolling Correlation")
plt.xlabel("Time")
plt.ylabel("Correlation")
plt.show()

plt.figure(figsize=(12,5))
plt.plot(df["datetime"],df["cum_return"])
plt.title("Strategy Equity Curve")
plt.xlabel("Time")
plt.ylabel("Portfolio Value")
plt.show()