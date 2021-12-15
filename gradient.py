import telebot
from PIL import Image, ImageFilter
import math
from random import randint
import os
width, height = 700, 700
bot = telebot.TeleBot("YOUR API")
im = Image.new('RGB', (width, height))
ld = im.load()
way = "/opt/random_palette/grad/" + "grad.png"
chat_id = "YOIR chad id"

heatmap = [
    [0.0, (randint(0, 100) * 0.01, randint(0, 100)
           * 0.01, randint(0, 100) * 0.01)],
    [randint(0, 100) * 0.01, (randint(0, 100) * 0.01,
                              randint(0, 100) * 0.01, randint(0, 100) * 0.01)],
    [1.00, (randint(0, 100) * 0.01, randint(0, 100)
            * 0.01, randint(0, 100) * 0.01)],
]


def gaussian(x, a, b, c, d=0):
    return a * math.exp(-(x - b)**2 / (2 * c**2)) + d


def pixel(x, width=100, map=[], spread=1):
    width = float(width)
    r = sum([gaussian(x, p[1][0], p[0] * width, width/(spread*len(map)))
             for p in map])
    g = sum([gaussian(x, p[1][1], p[0] * width, width/(spread*len(map)))
             for p in map])
    b = sum([gaussian(x, p[1][2], p[0] * width, width/(spread*len(map)))
             for p in map])
    return min(1.0, r), min(1.0, g), min(1.0, b)


def paintx():
    for x in range(im.size[0]):
        r, g, b = pixel(x, width=im.size[0], map=heatmap)
        r, g, b = [int(256*v) for v in (r, g, b)]
        for y in range(im.size[1]):
            ld[x, y] = r, g, b


def painty():
    for x in range(im.size[0]):
        r, g, b = pixel(x, width=im.size[0], map=heatmap)
        r, g, b = [int(256*v) for v in (r, g, b)]
        for y in range(im.size[1]):
            ld[y, x] = r, g, b


c = randint(0, 1)
if c == 1:
    paintx()
else:
    painty()

blured_im = im.filter(ImageFilter.GaussianBlur(5))
blured_im.save(way)
photo = open(way, 'rb')
bot.send_photo(chat_id, photo)
os.remove(way)
