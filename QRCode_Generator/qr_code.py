import qrcode
#Creating QR Code


website_link = 'https://youtu.be/xvFZjo5PgG0?feature=shared'

qr = qrcode.QRCode(version = 1, box_size = 5, border = 5)
qr.add_data(website_link)
qr.make()

img = qr.make_image(fill_color = 'black', back_color = 'white')
img.save('QR.png')



