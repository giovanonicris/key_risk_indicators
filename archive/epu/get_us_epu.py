import pandas as pd
import urllib.request
import os
import io

kri_id = 101
url = 'https://www.policyuncertainty.com/media/US_Policy_Uncertainty_Data.csv'

def fetch_epu_data():
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            csv_data = response.read().decode('utf-8')
        df = pd.read_csv(io.StringIO(csv_data)) #convert raw csv and load
    except Exception as e:
        print(f"Failed to fetch EPU data: {e}")
        return

    # combine Year and Month into DATE column
    df["DATE"] = pd.to_datetime(df["Year"].astype(str) + "-" + df["Month"].astype(str) + "-01")

    # rename the EPU index column
    df = df.rename(columns={"News_Based_Policy_Uncert_Index": "US_EPU_INDEX"})

    #keep cols that we need
    df = df[["DATE", "US_EPU_INDEX"]].dropna()
    df["KEY_RISK_INDICATOR_ID"] = kri_id

    os.makedirs('epu_index', exist_ok=True)
    output_file = 'epu/epu_us.csv'
    df.to_csv(output_file, index=False)
    print(f"EPU data saved to {output_file}")

if __name__ == "__main__":
    fetch_epu_data()