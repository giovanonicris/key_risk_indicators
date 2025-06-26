import os
from pathlib import Path
import importlib.util
import pandas as pd

#find parent loader file
base_dir = Path(__file__).resolve().parent
#output file
output_file = base_dir / "fact_kri_data.csv"

#fx to load and execute each py script "loader.py"
def load_from_loader(loader_path):
    spec = importlib.util.spec_from_file_location("loader", loader_path)
    loader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loader)
    return loader.load_data()

#fx to loop through directories
def run_and_collect():
    all_dfs = []

    for subdir in sorted(base_dir.iterdir()):
        #find subdirectory with standard prefix
        if subdir.is_dir() and subdir.name[0].isdigit():
            loader_path = subdir / "loader.py"
            if loader_path.exists():
                try:
                    print(f"Running {loader_path}")
                    #run loader fx
                    df = load_from_loader(loader_path)
                    #safety check to make sure union is properly executed
                    if set(df.columns) >= {"KRI_ID", "VALUE", "DATE"}:
                        all_dfs.append(df)
                        print(f"Collected from {loader_path}")
                except Exception as e:
                    print(f"Error in {subdir.name}: {e}")

    if all_dfs:
        final_df = pd.concat(all_dfs, ignore_index=True)
        final_df.to_csv(output_file, index=False)
        print(f"Fact table written to: {output_file}")
    else:
        print("No data collected.")

if __name__ == "__main__":
    run_and_collect()