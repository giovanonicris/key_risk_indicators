from fredapi import Fred
import pandas as pd
import os
from dotenv import load_dotenv

kri_id = 9

load_dotenv()
os.makedirs("fred_crude_oil_etf_volatility", exist_ok=True)

def load_data():
    fred_api_key = os.getenv("FRED_API_KEY")
    fred = Fred(api_key=fred_api_key)
    ovx_data = fred.get_series('OVXCLS')
    ovx_df = ovx_data.reset_index()
    ovx_df.columns = ['DATE', 'VALUE']
    ovx_df["KRI_ID"] = kri_id
    ovx_df = ovx_df[["KRI_ID", "VALUE", "DATE"]]
    ovx_df.to_csv("fred_crude_oil_etf_volatility/ovxcls.csv", index=False)
    print("Updated ovxcls.csv")
    return ovx_df
