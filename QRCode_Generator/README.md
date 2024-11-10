QR Code Generator in Python
A simple Python project for generating QR codes that link to any URL. This example creates a QR code for a YouTube video link, with customizable size and color options.

📂 Getting Started
Set Up Environment: Create a Python file, e.g., qr_code.py, in your editor (e.g., VS Code).

Install Dependencies:

pip install qrcode pillow
Import Libraries:

import qrcode

🖼️ Creating the QR Code
Define the Link:

website_link = 'https://youtu.be/xvFZjo5PgG0?feature=shared'

Customize the QR Code:

qr = qrcode.QRCode(version=1, box_size=5, border=5)
qr.add_data(website_link)
qr.make()

Generate and Save the Image:

img = qr.make_image(fill_color='black', back_color='white')
img.save('QRCode')
