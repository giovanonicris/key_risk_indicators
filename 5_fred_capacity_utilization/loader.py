from fredapi import Fred
import pandas as pd
import os
from dotenv import load_dotenv

kri_id = 5

load_dotenv()
os.makedirs("fred_supplier_deliveries_index", exist_ok=True)

fred_api_key = os.getenv("FRED_API_KEY")
fred = Fred(api_key=os.environ['FRED_API_KEY'])
cumfns_data = fred.get_series('CUMFNS')
cumfns_df = cumfns_data.reset_index()
cumfns_df.columns = ['DATE', 'VALUE']
cumfns_df["KRI_ID"] = kri_id
cumfns_df = cumfns_df[["KRI_ID", "VALUE", "DATE"]]
cumfns_df.to_csv("fred_supplier_deliveries_index/cumfns.csv", index=False)
print("Updated cumfns.csv")