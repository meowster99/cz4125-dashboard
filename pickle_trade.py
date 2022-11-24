# ONLY RUN for pickling
# To create pickle file
import pickle
from src.trade.retrieve_trade import Retrieve

RAW_TRADE_DATA = "./data/trade_data/raw"
TRADE_DATA = './data/trade_data/trade_data.pkl'


def save_object(obj, filename):
  with open(filename, 'wb') as outp:  # Overwrites any existing file.
    pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)


r = Retrieve(RAW_TRADE_DATA)
r.retrieve()
s = r.stats
save_object(s, TRADE_DATA)
