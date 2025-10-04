CODE_LENGTH = 8
DUMMY_COUNT = 50
CSV_FILE = "tickets.csv"
TEMPLATE_FILE = "template.png"

BARCODE_FORMAT = "code128"
BARCODE_OPTIONS = {    
    "module_width": 0.5,
    "module_height": 10,
    "font_size": 12,
    "text_distance": 6,
    "quiet_zone": 2,
    "foreground": "#000000",
    "background": "#ffffff",
    "font_color": "#ff0000"
}

TICKET_OPTIONS = {
    "size": (2000, 1429),
    "background_color": "white",
    "font_path": "arial.ttf",
    "font_size": 50,
    "text_color": "black",

    "barcode_size": (1000, 300),
    "barcode_position": (500, 400),
    "name_position": (200, 800),
    "email_position": (200, 900),
}