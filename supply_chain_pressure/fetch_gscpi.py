import requests
import pandas as pd
from io import BytesIO

# URL of the GSCPI data file
gscpi_url = 'https://www.newyorkfed.org/medialibrary/research/interactives/gscpi/downloads/gscpi_data.xlsx'

# function to grab gscpi data
def download_gscpi_data():
    response = requests.get(gscpi_url)
    if response.status_code == 200:
        data = BytesIO(response.content)
        
        # load and inspect Excel file
        xls = pd.ExcelFile(data)
        sheet_name = 'GSCPI Monthly Data'
        df = pd.read_excel(xls, sheet_name=sheet_name)
        
        # rename cols, drop empty
        df = df.iloc[:, :2]
        df.columns = ["Date", "GSCPI"]
        df = df.dropna(how='all')
        
        # write CSV file to repo
        output_file = 'supply_chain_pressure/gscpi_data.csv'
        df.to_csv(output_file, index=False)
        print(f"GSCPI data successfully saved to {output_file}")
    else:
        print(f"GSCPI data failed to download: {response.status_code}")
        exit(1)

if __name__ == "__main__":
    download_gscpi_data()
