import requests
import pandas as pd
from io import BytesIO

kri_id = 4
gscpi_url = 'https://www.newyorkfed.org/medialibrary/research/interactives/gscpi/downloads/gscpi_data.xlsx'

def download_gscpi_data():
    response = requests.get(gscpi_url)
    if response.status_code == 200:
        data = BytesIO(response.content)
        xls = pd.ExcelFile(data)
        sheet_name = 'GSCPI Monthly Data'
        df = pd.read_excel(xls, sheet_name=sheet_name)
        
        df = df.iloc[:, :2]
        df.columns = ["DATE", "VALUE"]
        df = df.dropna(how='all')
        df["KRI_ID"] = kri_id
        df = df[["KRI_ID", "VALUE", "DATE"]]

        output_file = 'gscpi/gscpi_data.csv'
        df.to_csv(output_file, index=False)
        print(f"GSCPI data successfully saved to {output_file}")
    else:
        print(f"GSCPI data failed to download: {response.status_code}")
        exit(1)

if __name__ == "__main__":
    download_gscpi_data()