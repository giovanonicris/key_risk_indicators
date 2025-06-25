import pandas as pd
import os
import requests

# set up
kri_id = 106
url = "https://www.newyorkfed.org/medialibrary/media/research/capital_markets/allmonth.xls"
download_path = "nyfed_yield_curve_model/allmonth.xls"
output_file = "nyfed_yield_curve_model/nyfed_yield_curve_prob.csv"
os.makedirs("nyfed_yield_curve_model", exist_ok=True)

# download Excel data
response = requests.get(url)
response.raise_for_status()
with open(download_path, "wb") as f:
    f.write(response.content)
print("Downloaded allmonth.xls")

# parse
df = pd.read_excel(download_path, skiprows=5)
df = df.dropna(subset=["YEAR", "MONTH", "PROBABILITY"])
latest = df.iloc[-1]

# format and save
year = int(latest["YEAR"])
month = int(latest["MONTH"])
prob = float(latest["PROBABILITY"])
date_label = f"{year}-{month:02}"

output_df = pd.DataFrame([{
    "DATE": date_label,
    "PROBABILITY": prob,
    "KEY_RISK_INDICATOR_ID": kri_id
}])

if os.path.isfile(output_file):
    output_df.to_csv(output_file, mode='a', index=False, header=False)
else:
    output_df.to_csv(output_file, index=False)

print(f"Saved NY Fed probability for {date_label} to {output_file}")
