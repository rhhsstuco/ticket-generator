import pandas as pd
import random
import string
import os
import json

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

fields = config["generate_options"]["fields"]
code_length = config["generate_options"]["code_length"]
dummy_count = config["generate_options"]["dummy_count"]
csv_file = config["csv_file"]
overwrite_existing = config["generate_options"].get("overwrite_existing", False)


def generate_codes(count, length=code_length):
    seen = set()
    codes = []
    while len(codes) < count:
        code = ''.join(random.choices(string.digits, k=length))
        if code not in seen:
            seen.add(code)
            codes.append(code)
    return codes


def generate_random_field_value():
    return ''.join(random.choices(string.ascii_uppercase, k=4))


def generate_dummy_students(count=dummy_count):
    codes = generate_codes(count)
    data = []

    for i in range(count):
        row = {}
        for field in fields:
            lower = field.lower()
            if lower == "name":
                row[field] = f"Student{i+1}"
            elif lower == "email":
                row[field] = f"student{i+1}@example.com"
            elif lower == "code":
                row[field] = codes[i]
            else:
                row[field] = generate_random_field_value()
        data.append(row)
    return pd.DataFrame(data)


def main():
    file_exists = os.path.exists(csv_file)
    file_nonempty = file_exists and os.path.getsize(csv_file) > 0

    if overwrite_existing:
        print(f"Overwrite mode enabled. Regenerating {csv_file}.")
        df = generate_dummy_students()

    elif file_nonempty:
        df = pd.read_csv(csv_file)
        print(f"Loaded {csv_file} with {len(df)} rows.")

        for field in fields:
            if field not in df.columns:
                df[field] = None

        if "Code" not in df.columns:
            df["Code"] = None

        missing_mask = df["Code"].isna() | df["Code"].astype(str).str.strip().eq("")
        missing_count = missing_mask.sum()

        if missing_count > 0:
            print(f"Generating {missing_count} new codes.")
            new_codes = generate_codes(missing_count)
            df.loc[missing_mask, "Code"] = new_codes

    else:
        print(f"File {csv_file} not found or empty. Generating {dummy_count} dummy entries.")
        df = generate_dummy_students()

    df = df[fields]
    df.to_csv(csv_file, index=False)
    print(f"Updated {csv_file} with {len(df)} rows and columns: {', '.join(fields)}.")


if __name__ == "__main__":
    main()
