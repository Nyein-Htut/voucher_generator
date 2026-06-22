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
    
    # Process multiple incoming structural items
    items = request.form.getlist('item[]')
    qtys = request.form.getlist('qty[]')
    prices = request.form.getlist('price[]')  
    delivery = int(request.form['delivery'])

    # Build dynamically parsed line item dataset mapping array
    invoice_rows = []
    subtotal = 0
    
    for i in range(len(items)):
        qty_val = int(qtys[i])
        unit_price_val = int(prices[i])
        
        # AUTOMATIC CALCULATION: Multiply unit price by quantity
        row_total = qty_val * unit_price_val
        subtotal += row_total
        
        invoice_rows.append((
            items[i], 
            str(qty_val), 
            f"{unit_price_val:,} MMK", 
            f"{row_total:,} MMK"
        ))

    # Append structural transport line item block safely
    invoice_rows.append(("车费 (Delivery)", "1", f"{delivery:,} MMK", f"{delivery:,} MMK"))
    total = subtotal + delivery

    # ----------------------------------------------------
    # FIRST PASS: Calculate Dynamic Frame Height Exactly
    # ----------------------------------------------------
    # Trace the exact placement of text layout structures
    logo_w, logo_h = 600, 400 # Default fallback safe boundaries estimation
    try:
        with Image.open("static/logo.jpg") as temp_logo:
            orig_w, orig_h = temp_logo.size
            logo_h = int((600 / orig_w) * orig_h)
    except:
        pass

    calculated_y = 100 + logo_h + 80  # After logo positioning 
    calculated_y += (65 * 3) + 42 + 20 # Height of meta data details lines 
    calculated_y += 40 + 50            # First separator spacing
    calculated_y += 65 + 45            # Header column metrics labels spacing
    calculated_y += len(invoice_rows) * 70 # Dynamically appended items density height
    calculated_y += 20 + 50 + 60 + 100 # Total block section room + bottom padding margins

    canvas_width = 1200
    canvas_height = calculated_y  # Flawless variable container height resolution

    img = Image.new("RGB", (canvas_width, canvas_height), "white")  
    draw = ImageDraw.Draw(img)

    # ----------------------------------------------------
    # TYPOGRAPHY & COLORS (Premium Charcoal Palette Config)
    # ----------------------------------------------------
    TEXT_COLOR = "#1C1B1A"
    MUTED_COLOR = "#6E6D6A"
    BORDER_COLOR = "#E0DDD5"  

    font_path = "static/fonts/NotoSansSC-Regular.ttf"
    font_sm = ImageFont.truetype(font_path, 26)
    font_reg = ImageFont.truetype(font_path, 28)
    font_med = ImageFont.truetype(font_path, 32)
    font_lg = ImageFont.truetype(font_path, 38)  

    # Luxury Dynamic Framing Architecture System
    draw.rectangle([40, 40, canvas_width - 40, canvas_height - 40], outline=BORDER_COLOR, width=1)
    draw.rectangle([50, 50, canvas_width - 50, canvas_height - 50], outline=BORDER_COLOR, width=2)

    # Centered Brand Logo processing pipeline tracking elements
    logo = Image.open("static/logo.jpg")
    orig_w, orig_h = logo.size
    
    target_width = 600  
    target_height = int((target_width / orig_w) * orig_h)
    logo = logo.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    logo_x = (canvas_width - target_width) // 2
    img.paste(logo, (logo_x, 100))

    y = 100 + target_height + 80

    # Two-Column Meta Data Layout Rendering System
    label_col_x = 120  
    val_col_x = 420    

    meta_items = [
        ("TELEPHONE", "09684875920 / 09261244508"),
        ("ADDRESS", "F-20/ Shwe Sapal 2 Street/ FMI City/\nHlaing Thar Yar Township/ Yangon"),
        ("DATE / TIME", datetime.now().strftime("%d %B %Y — %H:%M:%S")),
        ("CLIENT", customer.upper())  
    ]

    for label, val in meta_items:
        draw.text((label_col_x, y), label, fill=MUTED_COLOR, font=font_sm)
        
        if "\n" in val:
            lines = val.split("\n")
            for line in lines:
                draw.text((val_col_x, y), line, fill=TEXT_COLOR, font=font_reg)
                y += 42
            y += 20
        else:
            draw.text((val_col_x, y), val, fill=TEXT_COLOR, font=font_reg)
            y += 65

    y += 40
    draw.line((100, y, canvas_width - 100, y), fill=BORDER_COLOR, width=1)
    y += 50

    # Structural Transaction Data Metric Columns Grid 
    col_item_x = 100
    col_unit_x = 550
    col_price_x = 750   
    col_total_x = 1100  

    draw.text((col_item_x, y), "ITEM DESCRIPTION", fill=MUTED_COLOR, font=font_sm)
    draw.text((col_unit_x, y), "QTY", fill=MUTED_COLOR, font=font_sm)
    draw.text((col_price_x, y), "UNIT PRICE", fill=MUTED_COLOR, font=font_sm)
    
    total_header_txt = "TOTAL AMOUNT"
    w_th = draw.textlength(total_header_txt, font=font_sm)
    draw.text((col_total_x - w_th, y), total_header_txt, fill=MUTED_COLOR, font=font_sm)

    y += 65
    draw.line((100, y, canvas_width - 100, y), fill=BORDER_COLOR, width=1)
    y += 45

    # Variable Multi-Item Row Array Iterator Engine
    for r_item, r_qty, r_price, r_total in invoice_rows:
        draw.text((col_item_x, y), r_item, fill=TEXT_COLOR, font=font_med)
        draw.text((col_unit_x, y), r_qty, fill=TEXT_COLOR, font=font_reg)
        draw.text((col_price_x, y), r_price, fill=TEXT_COLOR, font=font_reg)
        
        w_tr = draw.textlength(r_total, font=font_reg)
        draw.text((col_total_x - w_tr, y), r_total, fill=TEXT_COLOR, font=font_reg)
        y += 70

    y += 20
    draw.line((100, y, canvas_width - 100, y), fill=TEXT_COLOR, width=1)
    y += 50

    # Premium Summary Total Component block
    draw.text((col_item_x, y), "总计(Total)", fill=TEXT_COLOR, font=font_lg)
    
    grand_total_str = f"{total:,} MMK"
    w_gt = draw.textlength(grand_total_str, font=font_lg)
    draw.text((col_total_x - w_gt, y), grand_total_str, fill=TEXT_COLOR, font=font_lg)

    filename = f"{uuid.uuid4()}.jpg"
    filepath = os.path.join(GENERATED_FOLDER, filename)
    img.save(filepath, quality=95)

    return send_file(
        filepath,
        mimetype="image/jpeg",
        as_attachment=True,
        download_name="voucher.jpg"
    )

if __name__ == '__main__':
    app.run(debug=True)
