from fredapi import Fred
import pandas as pd
import os
from dotenv import load_dotenv

kri_id = 9

load_dotenv()
os.makedirs("fred_ovxcls", exist_ok=True)

fred_api_key = os.getenv("FRED_API_KEY")
fred = Fred(api_key=os.environ['FRED_API_KEY'])
ovx_data = fred.get_series('OVXCLS')
ovx_df = ovx_data.reset_index()
ovx_df.columns = ['DATE', 'VALUE']
ovx_df["KRI_ID"] = kri_id
ovx_df = ovx_df[["KRI_ID", "VALUE", "DATE"]]
ovx_df.to_csv("fred_crude_oil_etf_volatility/ovxcls.csv", index=False)
print("Updated ovxcls.csv")