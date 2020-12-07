import wget
from PIL import Image
import os


def getImage(url):
    filename = wget.download(url)
    img = Image.open(filename)
    size = 500, 400
    filename = 'resized-'+filename
    img = img.resize(size, Image.ANTIALIAS)
    img.save(filename, "BMP")
    print('Profile Image Successfully Downloaded And Edited\n')
    return filename

'''
image = Image.open(filename)
image.show()
'''