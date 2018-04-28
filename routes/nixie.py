from io import BytesIO

from flask import send_file, request

from . import routes

from PIL import Image

# By Hellbus under CC-SA 3.0
# https://commons.wikimedia.org/wiki/File:Z566M_digit_0.jpg & others

nixies = list(map(Image.open, ["img/0.jpg",
                          "img/1.jpg",
                          "img/2.jpg",
                          "img/3.jpg",
                          "img/4.jpg",
                          "img/5.jpg",
                          "img/6.jpg",
                          "img/7.jpg",
                          "img/8.jpg",
                          "img/9.jpg",
                          "img/decimal.jpg"]))


def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


@routes.route('/generate_nixie')
def users():
    pattern = request.args.get('pattern')
    width, height = nixies[0].size
    total_width = width * len(pattern)
    total_height = height

    collage = Image.new('RGB', (total_width, total_height))
    x_offset = 0
    for num in pattern:
        if num == '.':
            num = 10 # index of decimal
        else:
            num = int(num)
        collage.paste(nixies[num], (x_offset, 0))
        x_offset += width

    return serve_pil_image(collage)