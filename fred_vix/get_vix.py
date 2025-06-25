import pandas as pd
import os

kri_id = 106
url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=VIXCLS'

def fetch_vix_data():
    df = pd.read_csv(url)
    df.columns = [col.strip().upper() for col in df.columns]
    df.rename(columns={"OBSERVATION_DATE": "DATE"}, inplace=True)
    # drop missing values and filter columns
    df = df.dropna(subset=["VIXCLS"])
    df["DATE"] = pd.to_datetime(df["DATE"])
    df["KEY_RISK_INDICATOR_ID"] = kri_id
    df = df[["DATE", "VIXCLS", "KEY_RISK_INDICATOR_ID"]]
    #prep to write
    os.makedirs('fred_vix', exist_ok=True)
    df.to_csv('fred_vix/vix_data.csv', index=False)
    print("VIX data saved to fred_vix/vix_data.csv")

if __name__ == "__main__":
    fetch_vix_data()
