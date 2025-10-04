import os
import json
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

csv_file = config["csv_file"]
template_file = config["template_file"]
ticket_opts = config["ticket_options"]
barcode_dir = config["barcode_options"].get("output_dir", "barcodes")
output_dir = ticket_opts.get("output_dir", "tickets")
overwrite_existing = ticket_opts.get("overwrite_existing", False)

def generate_tickets():
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(csv_file, dtype={"Code": str})

    try:
        font = ImageFont.truetype(ticket_opts["font_path"], ticket_opts["font_size"])
    except OSError:
        print("Font not found, falling back to default.")
        font = ImageFont.load_default()

    for _, row in df.iterrows():
        name = str(row.get("Name", "")).strip()
        email = str(row.get("Email", "")).strip()
        code = str(row.get("Code", "")).strip()

        if not code:
            continue

        output_path = os.path.join(output_dir, f"{code}_ticket.png")
        if os.path.exists(output_path) and not overwrite_existing:
            print(f"Overwrite disables. Skipping {code}.")
            continue

        if os.path.exists(template_file):
            ticket = Image.open(template_file).convert("RGB")
            if ticket.size != tuple(ticket_opts["size"]):
                ticket = ticket.resize(tuple(ticket_opts["size"]))
        else:
            ticket = Image.new("RGB", tuple(ticket_opts["size"]), ticket_opts["background_color"])

        draw = ImageDraw.Draw(ticket)

        barcode_path = os.path.join(barcode_dir, f"{code}.png")
        if not os.path.exists(barcode_path):
            print(f"Barcode for {code} not found, skipping.")
            continue

        barcode_img = Image.open(barcode_path).convert("RGB")
        barcode_img = barcode_img.resize(tuple(ticket_opts["barcode_size"]))
        ticket.paste(barcode_img, tuple(ticket_opts["barcode_position"]))

        draw.text(tuple(ticket_opts["name_position"]), f"Name: {name}", font=font, fill=ticket_opts["text_color"])
        draw.text(tuple(ticket_opts["email_position"]), f"Email: {email}", font=font, fill=ticket_opts["text_color"])

        ticket.save(output_path)
        print(f"Ticket generated for {name} as {output_path}")

if __name__ == "__main__":
    generate_tickets()
