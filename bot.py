import os
import subprocess
import sys

# Required libraries ko background mein install karna
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip" "install", package, "--quiet"])

try:
    import pandas as pd
except ImportError:
    install('pandas')
    install('openpyxl')
    import pandas as pd

# 1. Excel file ko read karna
excel_file = 'laptop.xlsx'
posts_html = ""
keywords_list = []

if os.path.exists(excel_file):
    xl = pd.ExcelFile(excel_file)
    # Excel ke saare sheets (tabs) par loop chalana
    for sheet_name in xl.sheet_names:
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        
        # Columns ke naam clean karna
        df.columns = [str(c).strip().lower() for c in df.columns]
        
        for index, row in df.iterrows():
            # Agar model khali hai toh skip karein
            if pd.isna(row.get('model')) or str(row.get('model')).strip() == "" or "model" in str(row.get('model')).lower():
                continue
                
            model = str(row.get('model', '')).strip()
            gen = str(row.get('gen', '')).strip()
            ram = str(row.get('ram', '')).strip()
            hdd = str(row.get('hdd', '')).strip()
            card = str(row.get('card', '')).strip()
            price = str(row.get('sell price', row.get('price', ''))).strip()
            
            if gen and gen != 'nan': model += f" ({gen})"
            
            # SEO Keywords generate karna
            keywords_list.append(f"{model} price in Pakistan, used laptop {model}")
            
            # Graphics card text setup
            card_info = f"<li><strong>GPU:</strong> {card}</li>" if card and card != 'nan' and card != '1' else ""
            
            # Har laptop ki post ka HTML design
            posts_html += f"""
            <div class="post-card">
                <h2>🔥 {model}</h2>
                <div class="specs">
                    <ul>
                        <li><strong>RAM:</strong> {ram if ram != 'nan' else '8'} GB</li>
                        <li><strong>Storage:</strong> {hdd if hdd != 'nan' else '256'} SSD/HDD</li>
                        {card_info}
                    </ul>
                </div>
                <div class="price-tag">Price: {price if price != 'nan' else 'Call'}</div>
                <a href="https://whatsapp.com/channel/0029VbCMtxgJ93wV9FOx7u1D" class="btn-join" target="_blank">Order on WhatsApp</a>
            </div>
            """
else:
    posts_html = "<p>No stock data found. Please check laptop.xlsx file.</p>"

seo_keywords = ", ".join(keywords_list[:20])

# 2. Main HTML Template with Auto SEO
html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BS Tech | Wholesale Laptop & Hardware Shop Pakistan</title>
    <meta name="description" content="Get the best deals on HP, Dell, Lenovo and core hardware laptops at BS Tech Pakistan. Fully verified stock updated daily.">
    <meta name="keywords" content="BS Tech, laptop prices Pakistan, wholesale laptop market, {seo_keywords}">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; background-color: #f4f6f9; color: #333; }}
        header {{ background-color: #111; color: white; padding: 30px 20px; text-align: center; }}
        .whatsapp-banner {{ background-color: #25D366; color: white; padding: 12px; text-align: center; font-weight: bold; font-size: 16px; position: sticky; top: 0; z-index: 1000; }}
        .whatsapp-banner a {{ color: white; text-decoration: underline; margin-left: 10px; }}
        .container {{ max-width: 900px; margin: 20px auto; padding: 0 20px; display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); grid-gap: 20px; }}
        .post-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); display: flex; flex-direction: column; justify-content: space-between; border-top: 4px solid #0076ff; }}
        .post-card h2 {{ margin-top: 0; font-size: 18px; color: #111; }}
        .specs ul {{ padding-left: 20px; margin: 10px 0; font-size: 14px; color: #555; }}
        .price-tag {{ font-size: 20px; font-weight: bold; color: #e67e22; margin: 10px 0; }}
        .btn-join {{ display: block; background-color: #25D366; color: white; padding: 10px; text-align: center; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 14px; }}
        .btn-join:hover {{ background-color: #1ebd58; }}
        footer {{ text-align: center; padding: 30px; color: #777; font-size: 14px; background: #111; margin-top: 5px; }}
    </style>
</head>
<body>
    <div class="whatsapp-banner">
        🔥 Daily Laptop Deals aur Stock Updates ke liye hamara WhatsApp Channel Join Karen! 
        <a href="https://whatsapp.com/channel/0029VbCMtxgJ93wV9FOx7u1D" target="_blank">Join Channel Now</a>
    </div>
    <header>
        <h1>BS Tech - Laptop Hub</h1>
        <p>Wholesale Prices & Premium Hardware Quality</p>
    </header>
    <div class="container">
        {posts_html}
    </div>
    <footer>
        <p style="color:white;">&copy; 2026 BS Tech. Automated System. All Rights Reserved.</p>
    </footer>
</body>
</html>"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("Website updated with SEO tags successfully!")
