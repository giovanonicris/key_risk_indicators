import requests
import pandas as pd
from io import BytesIO

kri_id = 6
gpr_url = 'https://www.matteoiacoviello.com/gpr_files/data_gpr_export.xls'

def load_data():
    response = requests.get(gpr_url)
    if response.status_code == 200:
        data = BytesIO(response.content)
        xls = pd.ExcelFile(data)
        print("Available sheets:", xls.sheet_names)
        sheet_name = xls.sheet_names[0]

        df = pd.read_excel(xls, sheet_name=sheet_name)
        df.columns.values[0] = "DATE"
        df.rename(columns={"GPR": "VALUE"}, inplace=True)
        df["KRI_ID"] = kri_id
        df = df[["KRI_ID", "VALUE", "DATE"]]
        output_file = 'gpr/gpr_data.csv'
        df.to_csv(output_file, index=False)
        print(f"GPR data successfully saved to {output_file}")
    else:
        print(f"GPR data failed to download:{response.status_code}")
        exit(1)
