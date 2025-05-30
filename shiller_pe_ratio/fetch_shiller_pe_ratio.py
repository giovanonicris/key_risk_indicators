import requests
import pandas as pd
from bs4 import BeautifulSoup

#set appropriate KRI ID for this dataset
kri_id = 13

# URL from multpl.com Shiller P/E page
url = 'https://www.multpl.com/shiller-pe/table/by-year'

# function to grab and write data
def fetch_shiller_pe_data():
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # locate the table on the web page
        table = soup.find('table')
        if table:
            df = pd.read_html(str(table))[0]
            print(df.head())  # peek into data, if extracted correctly
            df.rename(columns={df.columns[1]: "Shiller PE Ratio"}, inplace=True)
            df["KEY_RISK_INDICATOR_ID"] = kri_id
            
            # write CSV
            output_file = 'shiller_pe_ratio/shiller_pe_data.csv'
            df.to_csv(output_file, index=False)
            print(f"Shiller P/E data saved to {output_file}")
        else:
            print("No table found on the webpage!")
            exit(1)
    else:
        print(f"Unable to retrieve data: {response.status_code}")
        exit(1)

if __name__ == "__main__":
    fetch_shiller_pe_data()
