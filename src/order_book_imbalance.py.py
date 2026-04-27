import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("../data/BTC-USD.csv.gz", compression ="gzip", nrows = 50000)
#print(data)

def compute_order_imbalance(dataframe):

    snapshots = []

    for timestamp, snapshot in dataframe.groupby('timestamp'):
        bids = snapshot[snapshot['side'] == 'bid']
        asks = snapshot[snapshot['side'] == 'ask']

        if bids.empty or asks.empty:
            continue

        best_bid_price = bids['price'].max()
        best_bid_size = bids.loc[bids['price'] == best_bid_price, 'amount'].sum()

        best_ask_price = asks['price'].min()
        best_ask_size = asks.loc[asks['price'] == best_ask_price, 'amount'].sum()

        imbalance = (best_bid_size - best_ask_size)/(best_bid_size + best_ask_size)
        if best_bid_size + best_ask_size == 0:
            continue

        snapshots.append((timestamp, imbalance))

    return pd.DataFrame(snapshots, columns = ['timestamp', 'imbalance'])

imbalance_dataframe = compute_order_imbalance(data)
imbalance_dataframe['datetime'] = pd.to_datetime(imbalance_dataframe['timestamp'], unit='us')
print(imbalance_dataframe.head())

plt.figure(figsize=(12,5))
plt.plot(imbalance_dataframe['datetime'], imbalance_dataframe['imbalance'], label='Imbalance')
plt.xlabel("Time")
plt.ylabel("Order Book Imbalance")
plt.title("BTC-USD Imbalance over Time")
plt.legend()
plt.show()
