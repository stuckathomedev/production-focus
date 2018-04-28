from io import BytesIO

from flask import send_file, request

from . import routes

from PIL import Image


# By Hellbus under CC-SA 3.0
# https://commons.wikimedia.org/wiki/File:Z566M_digit_0.jpg & others

happy = list(map(Image.open, ["happiness.jpg",
                              "greathappiness.jpg",
                              "happiness2nd.jpg",
                              "uraniumsmile.jpg"]))

def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


@routes.route('/generate_happiness')
def users():
    pattern = request.args.get('percent')
    width, height = happy[0].size
    total_width = width * len(pattern)
    total_height = height

    for percent in happy:
        if percent >= ".80":
            percent = 1
        if percent >= .60 and percent < .80:
            percent = 2
        if percent >= .20 and percent < .60:
            percent = 0
        else:
            percent = 4

    return serve_pil_image(happy[percent])



    return serve_pil_image(collage)


