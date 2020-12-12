import wget
from PIL import Image
import requests
import json


def getImage(url):  # called from the Cuttie.registerProfile method

    filename = wget.download(url)  # downloads the image from URL

    # opens image, resizes, renames, reformats, saves copy
    img = Image.open(filename)
    filename = 'resized-' + filename
    size = 500, 400
    img = img.resize(size, Image.ANTIALIAS)
    img.save(filename, "BMP")  # BEWARE OF THE IMAGE CACHE

    return filename  # returns the copy path


def MorePictures(segment):
    APIs = {'doggies': {'URL': "https://dog.ceo/api/breeds/image/random",
                        'key': "message"},
            'kitties': {'URL': "http://aws.random.cat//meow",
                        'key': "file"}}

    r = requests.get(APIs[segment]['URL'])
    filename = wget.download(r.json()[APIs[segment]['key']])  # downloads the image from URL

    img = Image.open(filename)
    img.show()


