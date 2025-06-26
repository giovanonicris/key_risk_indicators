import pandas as pd
import os

kri_id = 3
url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=VIXCLS'

def fetch_vix_data():
    df = pd.read_csv(url)
    df.columns = [col.strip().upper() for col in df.columns]
    df.rename(columns={"OBSERVATION_DATE": "DATE", "VIXCLS": "VALUE"}, inplace=True)
    df = df.dropna(subset=["VALUE"])
    df["DATE"] = pd.to_datetime(df["DATE"])
    df["KRI_ID"] = kri_id
    df = df[["KRI_ID", "VALUE", "DATE"]]
    os.makedirs('fred_vix', exist_ok=True)
    df.to_csv('fred_vix/vix_data.csv', index=False)
    print("VIX data saved to fred_vix/vix_data.csv")

if __name__ == "__main__":
    fetch_vix_data()