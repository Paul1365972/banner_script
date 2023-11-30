from constants import *
from blackrenderer.render import renderText
import os
from glob import glob
from PIL import Image

FONT_SIZE = 250


def test_specific():
    texts = ["", ""]
    images = []
    max_width = 0
    max_height = 0
    for index, text in enumerate(texts):
        path = f"data/test/specific_{index}.png"
        renderText("build/BannerScript.ttf", text, path, fontSize=2000, margin=20)
        renderText("build/BannerScript.ttf", text, f"data/test/specific_{index}.svg", fontSize=2000, margin=20)
        image = Image.open(path)
        images.append(image)
        max_width = max(max_width, image.width)
        max_height = max(max_height, image.height)

    atlas = Image.new("RGBA", (max_width, max_height * len(images)))
    for index, image in enumerate(images):
        atlas.paste(image, (0, index * max_height))

    atlas.save("data/test_specific.png")


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
