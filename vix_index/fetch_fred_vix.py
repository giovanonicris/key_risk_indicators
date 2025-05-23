import pandas as pd
import os

kri_id = 106
url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=VIXCLS'

def fetch_vix_data():
    df = pd.read_csv(url, parse_dates=['DATE'])
    df = df.dropna()[['DATE', 'VIXCLS']]
    df["KEY_RISK_INDICATOR_ID"] = kri_id
    output_file = 'vix_index/vix_data.csv'
    os.makedirs('vix_index', exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"VIX data saved to {output_file}")

if __name__ == "__main__":
    fetch_vix_data()
