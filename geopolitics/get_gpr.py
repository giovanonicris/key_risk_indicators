import requests
import pandas as pd
from io import BytesIO

# URL of the GPR data file
gpr_url = 'https://www.matteoiacoviello.com/gpr_files/data_gpr_export.xls'

def download_gpr_data():
    response = requests.get(gpr_url)
    
    if response.status_code == 200:
        data = BytesIO(response.content)
        xls = pd.ExcelFile(data)
        print("Available sheets:", xls.sheet_names) # to help debug
        sheet_name = xls.sheet_names[0]  # grab first sheet

        # read and write file
        df = pd.read_excel(xls, sheet_name=sheet_name)
        df.columns.values[0] = "Date" # rename 'month' for consistency across other data
        output_file = 'geopolitics/gpr_data.csv'
        df.to_csv(output_file, index=False)
        print(f"GPR data successfully saved to {output_file}")
    
    else:
        print(f"GPR data failed to download:{response.status_code}")
        exit(1)

if __name__ == "__main__":
    download_gpr_data()
