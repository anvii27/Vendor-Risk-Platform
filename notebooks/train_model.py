import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../backend"))
import pandas as pd
from model import train_model

df = pd.read_csv("../data/vendors.csv")
train_model(df)