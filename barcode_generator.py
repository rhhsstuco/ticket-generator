import os
import pandas as pd
import barcode
from barcode.writer import ImageWriter
import json

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

csv_file = config["csv_file"]
barcode_format = config["barcode_format"]
barcode_options = config.get("barcode_options", {})
output_dir = barcode_options.get("output_dir", "barcodes")
overwrite_existing = barcode_options.get("overwrite_existing", False)

def generate_barcodes(csv_file=csv_file, output_dir=output_dir):
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(csv_file):
        print(f"Error: CSV file '{csv_file}' not found.")
        return

    df = pd.read_csv(csv_file, dtype={"Code": str})

    if "Code" not in df.columns:
        raise ValueError("CSV must contain a 'Code' column.")

    barcode_class = barcode.get_barcode_class(barcode_format)

    existing_files = os.listdir(output_dir)
    if existing_files and not overwrite_existing:
        print(f"Existing barcodes detected in '{output_dir}'.")
        print("Set 'overwrite_existing' to true in config.json to replace them.")
        return

    for _, row in df.iterrows():
        code = str(row["Code"]).strip()
        if not code:
            continue

        filename = os.path.join(output_dir, f"{code}")
        my_barcode = barcode_class(code, writer=ImageWriter())

        valid_options = {
            k: v
            for k, v in barcode_options.items()
            if k not in ["output_dir", "overwrite_existing"]
        }

        my_barcode.save(filename, valid_options)
        print(f"Generated barcode for {code} as {filename}.png")


if __name__ == "__main__":
    generate_barcodes()