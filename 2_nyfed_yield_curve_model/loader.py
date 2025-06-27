import pandas as pd
import os
import requests

url = "https://www.newyorkfed.org/medialibrary/media/research/capital_markets/allmonth.xls"
output_folder = "nyfed_yield_curve_model"
xls_path = os.path.join(output_folder, "allmonth.xls")
csv_path = os.path.join(output_folder, "recession_probabilities.csv")
kri_id = 2

def load_data():
    os.makedirs(output_folder, exist_ok=True)

    response = requests.get(url)
    with open(xls_path, "wb") as f:
        f.write(response.content)
    print("Downloaded allmonth.xls")

    df = pd.read_excel(xls_path)

    df = df.rename(columns={
        "Date": "DATE",
        "Rec_prob": "VALUE"
    })

    df = df.dropna(subset=["DATE", "VALUE"])

    df["VALUE"] = (
        df["VALUE"]
        .astype(str)
        .str.rstrip('%')
        .replace('', pd.NA)
        .astype(float) / 100.0
    )
    df["KRI_ID"] = kri_id
    df = df[["KRI_ID", "VALUE", "DATE"]]
    df.to_csv(csv_path, index=False)
    print(f"Saved to {csv_path}")
    return df

if __name__ == "__main__":
    load_data()
