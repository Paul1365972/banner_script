from PIL import Image, ImageOps
import pixart2svg
from constants import *
from glob import glob
import os
from pixels2svg import pixels2svg

def recreate():
    os.makedirs("data/svg", exist_ok=True)
    os.makedirs("data/png", exist_ok=True)
    for file in glob("data/svg/*.svg") + glob("data/png/*.png"):
        os.remove(file)

    banner_atlas = Image.open("data/banner_atlas.png")

    for index, pattern in enumerate(BANNER_DATA):
        for color in range(COLORS):
            pattern_img = banner_atlas.crop((BANNER_WIDTH * pattern.banner_atlas_index, BANNER_HEIGHT * color, BANNER_WIDTH * (pattern.banner_atlas_index + 1), BANNER_HEIGHT * (color + 1)))
            # Border with left, top, right, bottom
            pattern_img = ImageOps.expand(pattern_img, border=(1, 3, 1, 3), fill=(0, 0, 0, 0))
            # pattern_img = ImageOps.expand(pattern_img, border=(2, 4, 3, 5), fill=(0, 0, 0, 0))
            
            # TODO: Remove test dots
            # pattern_img.putpixel((0, 0), (255, 0, 0, 255))
            # pattern_img.putpixel((24, 0), (255, 0, 0, 255))
            # pattern_img.putpixel((0, 47), (255, 0, 0, 255))
            # pattern_img.putpixel((24, 47), (255, 0, 0, 255))
            
            codepoint = to_codepoint(index, color)
            pattern_img.save(f"data/png/{codepoint:x}.png")
            
            # pixart2svg.convert(pattern_img, f"data/svg/{codepoint:x}.svg")
            pixels2svg(f"data/png/{codepoint:x}.png", f"data/svg/{codepoint:x}.svg")


if __name__ == "__main__":
    recreate()
