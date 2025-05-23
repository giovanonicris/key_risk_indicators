import pandas as pd
import os

kri_id = 103
url = 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=T10Y2Y'

def fetch_yield_curve_spread():
    df = pd.read_csv(url, parse_dates=['DATE'])
    df = df.dropna()[['DATE', 'T10Y2Y']]
    df["KEY_RISK_INDICATOR_ID"] = kri_id
    output_file = 'fred_t10y2y_yield_curve/t10y2y_yield_curve_spread.csv'
    os.makedirs('yield_curve_spread', exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"Yield curve spread data saved to {output_file}")

if __name__ == "__main__":
    fetch_yield_curve_spread()
