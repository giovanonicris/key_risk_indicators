import pandas as pd
import os

kri_id = 105
url = 'https://www.newyorkfed.org/medialibrary/media/research/capital_markets/Prob_Rec.csv'

def fetch_nyfed_yield_curve_prob():
    df = pd.read_csv(url, skiprows=4)
    df = df.rename(columns=lambda x: x.strip())
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
    df = df.dropna(subset=['DATE', 'P(REC)'])
    df = df[['DATE', 'P(REC)']]
    df["KEY_RISK_INDICATOR_ID"] = kri_id
    output_file = 'nyfed_yield_curve_model/nyfed_yield_curve_prob.csv'
    os.makedirs('nyfed_yield_curve_model', exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"NY Fed yield curve model data saved to {output_file}")

if __name__ == "__main__":
    fetch_nyfed_yield_curve_prob()
