import os
import pandas as pd
import barcode
from barcode.writer import ImageWriter
import config

def generate_barcodes(csv_file=config.CSV_FILE, output_dir="barcodes"):
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(csv_file, dtype={"Code": str})

    if "Code" not in df.columns:
        raise ValueError("CSV must contain a 'Code' column.")

    for _, row in df.iterrows():
        code = str(row["Code"]).strip()

        if not code:
            continue

        barcode_class = barcode.get_barcode_class(config.BARCODE_FORMAT)
        filename = os.path.join(output_dir, f"{code}")

        my_barcode = barcode_class(code, writer=ImageWriter())

        # Use BARCODE_OPTIONS only if defined and not empty
        if hasattr(config, "BARCODE_OPTIONS") and config.BARCODE_OPTIONS:
            my_barcode.save(filename, config.BARCODE_OPTIONS)
        else:
            my_barcode.save(filename)

        print(f"Generated barcode for {code} as {filename}.png")

if __name__ == "__main__":
    generate_barcodes()