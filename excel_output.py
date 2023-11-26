import pandas as pd
import os

def create_excel(results, url):
    df = pd.DataFrame(results, columns=['URL', 'Result'])
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    filename = "output.xlsx"
    filepath = os.path.join(output_dir, filename)
    df.to_excel(filepath, index=False)
    return filename
