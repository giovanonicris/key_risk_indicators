import pandas as pd
import os

kri_id = 102
url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=SUPDELISRM'

def fetch_supplier_deliveries():
    df = pd.read_csv(url, parse_dates=['DATE'])
    df = df.dropna()[['DATE', 'SUPDELISRM']]
    df["KEY_RISK_INDICATOR_ID"] = kri_id
    output_file = 'fred_supplier_deliveries_index/supplier_deliveries_data.csv'
    os.makedirs('supplier_deliveries_index', exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"ISM Supplier Deliveries data saved to {output_file}")

if __name__ == "__main__":
    fetch_supplier_deliveries()