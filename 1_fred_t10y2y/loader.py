from fredapi import Fred
import pandas as pd
import os
from dotenv import load_dotenv

kri_id = 1

def load_data():
    load_dotenv()
    os.makedirs("fred_t10y2y", exist_ok=True)

    fred_api_key = os.getenv("FRED_API_KEY")
    fred = Fred(api_key=os.environ['FRED_API_KEY'])
    t10y2y_data = fred.get_series('T10Y2Y')
    t10y2y_df = t10y2y_data.reset_index()
    t10y2y_df.columns = ['DATE', 'VALUE']
    t10y2y_df["KRI_ID"] = kri_id
    t10y2y_df = t10y2y_df[["KRI_ID", "VALUE", "DATE"]]
    t10y2y_df.to_csv("fred_t10y2y/t10y2y.csv", index=False)
    print("Updated t10y-2y_data.csv")
    return t10y2y_df

if __name__ == "__main__":
    load_data()
