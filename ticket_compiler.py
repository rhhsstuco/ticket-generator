import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import config

def generate_tickets(csv_file=config.CSV_FILE, barcode_dir="barcodes", output_dir="tickets"):
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(csv_file)
    opts = config.TICKET_OPTIONS
    template = config.TEMPLATE_FILE

    try:
        font = ImageFont.truetype(opts["font_path"], opts["font_size"])
    except OSError:
        print("⚠️ Font not found, falling back to default.")
        font = ImageFont.load_default()

    for _, row in df.iterrows():
        name = str(row.get("Name", "")).strip()
        email = str(row.get("Email", "")).strip()
        code = str(row.get("Code", "")).strip()

        if not code:
            continue

        if os.path.exists(template):
            ticket = Image.open(template).convert("RGB")
            if ticket.size != tuple(opts["size"]):
                ticket = ticket.resize(tuple(opts["size"]))
        else:
            ticket = Image.new("RGB", tuple(opts["size"]), opts["background_color"])

        draw = ImageDraw.Draw(ticket)

        barcode_path = os.path.join(barcode_dir, f"{code}.png")
        if not os.path.exists(barcode_path):
            print(f"⚠️ Barcode for {code} not found, skipping")
            continue

        barcode_img = Image.open(barcode_path).convert("RGB")
        barcode_img = barcode_img.resize(tuple(opts["barcode_size"]))
        ticket.paste(barcode_img, tuple(opts["barcode_position"]))

        draw.text(tuple(opts["name_position"]), f"Name: {name}", font=font, fill=opts["text_color"])
        draw.text(tuple(opts["email_position"]), f"Email: {email}", font=font, fill=opts["text_color"])

        output_path = os.path.join(output_dir, f"{code}_ticket.png")
        ticket.save(output_path)

        print(f"✅ Ticket generated for {name} → {output_path}")

if __name__ == "__main__":
    generate_tickets()
