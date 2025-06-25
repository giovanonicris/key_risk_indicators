import pandas as pd
import os

kri_id = 106
url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=VIXCLS'

def fetch_vix_data():
    df = pd.read_csv(url)
    df = df[df['VIXCLS'] != '.']  # remove missing values
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['VIXCLS'] = df['VIXCLS'].astype(float)
    df = df[['DATE', 'VIXCLS']]
    df["KEY_RISK_INDICATOR_ID"] = kri_id
    output_file = 'fred_vix/vix_data.csv'
    os.makedirs('fred_vix', exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"VIX data saved to {output_file}")

if __name__ == "__main__":
    fetch_vix_data()
