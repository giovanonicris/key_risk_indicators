from fredapi import Fred
import pandas as pd
import os
from dotenv import load_dotenv

kri_id = 104

#set up
load_dotenv()  # load variables from .env
os.makedirs("fred_t10y2y_yield_curve", exist_ok=True)

fred_api_key = os.getenv("FRED_API_KEY")
fred = Fred(api_key=os.environ['FRED_API_KEY'])
ovx_data = fred.get_series('T10Y2Y')
ovx_df = ovx_data.reset_index()
ovx_df.columns = ['DATE', 'T10Y2Y']
ovx_df["KEY_RISK_INDICATOR_ID"] = kri_id
ovx_df.to_csv("fred_t10y2y_yield_curve/yield_curve_spread.csv", index=False)
print("Updated yield_curve_spread.csv")
