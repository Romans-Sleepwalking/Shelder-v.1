import wget
from PIL import Image


def getImage(url):  # called from the Cuttie.registerProfile method

    filename = wget.download(url)  # downloads the image from URL

    # opens image, resizes, renames, reformats, saves copy
    img = Image.open(filename)
    filename = 'resized-' + filename
    size = 500, 400
    img = img.resize(size, Image.ANTIALIAS)
    img.save(filename, "BMP")  # BEWARE OF THE IMAGE CACHE

    return filename  # returns the copy path
