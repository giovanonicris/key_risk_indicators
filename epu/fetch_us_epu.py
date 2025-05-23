import pandas as pd
import os

kri_id = 101
url = 'https://www.policyuncertainty.com/media/US_Policy_Uncertainty_Data.csv'

def fetch_epu_data():
    df = pd.read_csv(url)
    df = df.rename(columns=lambda x: x.strip())
    df = df[['DATE', 'US_EPU_INDEX']].dropna()
    df["KEY_RISK_INDICATOR_ID"] = kri_id
    output_file = 'epu/epu_us.csv'
    os.makedirs('epu_index', exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"EPU data saved to {output_file}")

if __name__ == "__main__":
    fetch_epu_data()