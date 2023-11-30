from constants import *
from blackrenderer.render import renderText
import os
from glob import glob
from PIL import Image
import json

FONT_SIZE = 250

def test_all():
    images = []
    max_width = 0
    max_height = 0
    for index in range(len(BANNER_DATA)):
        for color in range(COLORS):
            codepoint = to_codepoint(index, color)
            text = chr(codepoint)
            path = f"data/test/{codepoint:x}.png"
            renderText("build/BannerScript.ttf", text, path, fontSize=FONT_SIZE, margin=20)
            image = Image.open(path)
            images.append(image)
            max_width = max(max_width, image.width)
            max_height = max(max_height, image.height)

    atlas = Image.new("RGBA", (max_width * len(BANNER_DATA), max_height * COLORS))
    for index, image in enumerate(images):
        atlas.paste(image, (index // COLORS * max_width, index % COLORS * max_height))

    atlas.save("data/test_all.png")


def test():
    os.makedirs("data/test", exist_ok=True)
    for file in glob("data/test/*.svg") + glob("data/test/*.png"):
        os.remove(file)
    test_all()
    test_specific()


if __name__ == "__main__":
    test()
