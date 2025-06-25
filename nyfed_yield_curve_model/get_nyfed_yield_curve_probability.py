import pandas as pd
import os
import requests

url = "https://www.newyorkfed.org/medialibrary/media/research/capital_markets/allmonth.xls"
output_folder = "nyfed_yield_curve_model"
xls_path = os.path.join(output_folder, "allmonth.xls")
csv_path = os.path.join(output_folder, "recession_probabilities.csv")
kri_id = 108

def fetch_nyfed_yield_curve_prob():
    os.makedirs(output_folder, exist_ok=True)

    # download the .xls file
    response = requests.get(url)
    with open(xls_path, "wb") as f:
        f.write(response.content)
    print("Downloaded allmonth.xls")

    # read and parse the file
    df = pd.read_excel(xls_path)

    df = df.rename(columns={
        "Date": "DATE",
        "Rec_prob": "PROBABILITY"
    })

    # drop rows with missing probability
    df = df.dropna(subset=["DATE", "PROBABILITY"])

    # clean percentage and convert
    df["PROBABILITY"] = (
        df["PROBABILITY"]
        .astype(str)
        .str.rstrip('%')
        .replace('', pd.NA)
        .astype(float) / 100.0
    )
    df["KEY_RISK_INDICATOR_ID"] = kri_id
    df = df[["DATE", "PROBABILITY", "KEY_RISK_INDICATOR_ID"]]
    #write
    df.to_csv(csv_path, index=False)
    print(f"Saved to {csv_path}")

if __name__ == "__main__":
    fetch_nyfed_yield_curve_prob()
