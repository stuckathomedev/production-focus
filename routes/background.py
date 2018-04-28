from io import BytesIO

from flask import send_file, request

from . import routes

from PIL import Image

background = Image.open("img/background.jpg")


def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.convert('RGB').save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


@routes.route('/background')
def give_background():
    return serve_pil_image(background)

