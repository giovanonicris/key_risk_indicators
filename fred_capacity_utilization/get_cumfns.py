from fredapi import Fred
import pandas as pd
import os
from dotenv import load_dotenv

kri_id = 103

#set up
load_dotenv()  # load variables from .env
os.makedirs("fred_supplier_deliveries_index", exist_ok=True)

fred_api_key = os.getenv("FRED_API_KEY")
fred = Fred(api_key=os.environ['FRED_API_KEY'])
isrm_data = fred.get_series('CUMFNS')
isrm_df = isrm_data.reset_index()
isrm_df.columns = ['DATE', 'CUMFNS']
isrm_df["KEY_RISK_INDICATOR_ID"] = kri_id
isrm_df.to_csv("fred_capacity_utilization/cumfns.csv", index=False)
print("Updated cumfns.csv")
