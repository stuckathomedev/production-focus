from io import BytesIO

from flask import send_file, request

from . import routes

from PIL import Image


# By Hellbus under CC-SA 3.0
# https://commons.wikimedia.org/wiki/File:Z566M_digit_0.jpg & others

happy = list(map(Image.open, ["img/happiness.jpg",
                              "img/greathappiness.jpg",
                              "img/happiness2nd.jpg",
                              "img/uraniumsmile.jpg"]))


def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.convert('RGB').save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


@routes.route('/generate_happiness')
def happiness():
    percent = float(request.args.get('percent'))

    if percent >= .80:
        index = 1
    elif .60 <= percent < .80:
        index = 2
    elif .20 <= percent < .60:
        index = 0
    else:
        index = 3

    return serve_pil_image(happy[index])
