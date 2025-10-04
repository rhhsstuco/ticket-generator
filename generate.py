import pandas as pd
import random
import string
import os
import config

def generate_codes(count, length=config.CODE_LENGTH):
    seen = set()
    codes = []
    while len(codes) < count:
        code = ''.join(random.choices(string.digits, k=length))
        if code not in seen:
            seen.add(code)
            codes.append(code)
    return codes

def generate_dummy_students(count=config.DUMMY_COUNT):
    codes = generate_codes(count, config.CODE_LENGTH)
    students = []
    for i in range(count):
        name = f"Student{i+1}"
        email = f"student{i+1}@example.com"
        students.append({"Name": name, "Email": email, "Code": codes[i]})
    return pd.DataFrame(students)

def main():
    file_path = config.CSV_FILE

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)

        if df.empty:
            print(f"File {file_path} is empty, generating dummy data.")
            df = generate_dummy_students()
        else:
            if "Code" not in df.columns:
                df["Code"] = None

            for i in range(len(df)):
                if pd.isna(df.loc[i, "Code"]) or not str(df.loc[i, "Code"]).strip():
                    df.loc[i, "Code"] = generate_codes()

    else:
        print(f"File {file_path} not found, generating dummy data.")
        df = generate_dummy_students()

    df.to_csv(file_path, index=False)
    print(f"Updated {file_path} with {len(df)} rows")

if __name__ == "__main__":
    main()
