from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os
import uuid

app = Flask(__name__)

GENERATED_FOLDER = "generated"

if not os.path.exists(GENERATED_FOLDER):
    os.makedirs(GENERATED_FOLDER)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():

    customer = request.form['customer']
    item = request.form['item']
    qty = request.form['qty']
    price = int(request.form['price'])
    delivery = int(request.form['delivery'])

    total = price + delivery

    # White background
    img = Image.new("RGB", (1080, 1500), "white")
    draw = ImageDraw.Draw(img)

    # Fonts
    title_font = ImageFont.truetype(
        "static/fonts/NotoSansSC-Regular.ttf", 60)

    normal_font = ImageFont.truetype(
        "static/fonts/NotoSansSC-Regular.ttf", 34)

    bold_font = ImageFont.truetype(
        "static/fonts/NotoSansSC-Regular.ttf", 44)

    total_font = ImageFont.truetype(
        "static/fonts/NotoSansSC-Regular.ttf", 60)

    # Logo
    logo = Image.open("static/logo.jpg")
    logo = logo.resize((520, 520))
    img.paste(logo, (280, 20))

    y = 560

    # Header information
    draw.text((150, y), "Tel", fill="black", font=normal_font)
    draw.text(
        (450, y),
        "09684875920 / 09261244508",
        fill="black",
        font=normal_font
    )

    y += 60

    draw.text((150, y), "Address", fill="black", font=normal_font)
    draw.text(
        (450, y),
        "F-20 Shwe Sapal 2 Street\nFMI City, Hlaing Thar Yar\nYangon",
        fill="black",
        font=normal_font
    )

    y += 130

    draw.text((150, y), "Voucher Date", fill="black", font=normal_font)

    draw.text(
        (450, y),
        datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        fill="black",
        font=normal_font
    )

    y += 60

    draw.text((150, y), "Customer", fill="black", font=normal_font)

    draw.text(
        (450, y),
        customer,
        fill="black",
        font=normal_font
    )

    y += 80

    draw.line((50, y, 1030, y), fill="black", width=3)

    y += 40

    # Table Header
    draw.text((60, y), "Item", fill="black", font=bold_font)
    draw.text((450, y), "Unit", fill="black", font=bold_font)
    draw.text((620, y), "Price", fill="black", font=bold_font)
    draw.text((860, y), "Total", fill="black", font=bold_font)

    y += 90

    # Item row
    draw.text((60, y), item, fill="black", font=normal_font)

    draw.text((470, y), qty, fill="black", font=normal_font)

    draw.text(
        (600, y),
        f"{price:,} MMK",
        fill="black",
        font=normal_font
    )

    draw.text(
        (850, y),
        f"{price:,} MMK",
        fill="black",
        font=normal_font
    )

    y += 70

    # Delivery row
    draw.text((60, y), "车费", fill="black", font=normal_font)

    draw.text((470, y), "1", fill="black", font=normal_font)

    draw.text(
        (600, y),
        f"{delivery:,} MMK",
        fill="black",
        font=normal_font
    )

    draw.text(
        (850, y),
        f"{delivery:,} MMK",
        fill="black",
        font=normal_font
    )

    y += 120

    draw.line((50, y, 1030, y), fill="black", width=4)

    y += 60

    draw.text(
        (60, y),
        "总计",
        fill="black",
        font=total_font
    )

    draw.text(
        (600, y),
        f"{total:,} MMK",
        fill="black",
        font=total_font
    )

    filename = f"{uuid.uuid4()}.jpg"

    filepath = os.path.join(
        GENERATED_FOLDER,
        filename
    )

    img.save(filepath, quality=95)

    return send_file(
        filepath,
        mimetype="image/jpeg",
        as_attachment=True,
        download_name="voucher.jpg"
    )


if __name__ == '__main__':
    app.run(debug=True)