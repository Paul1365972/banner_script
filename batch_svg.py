from typing import List, Tuple, Dict, Any
import numpy
from PIL import Image, ImageOps
from constants import *
import os
from pixart2svg import fill_block, generate_path


def convert(image: Image, defs_map: Dict[Any, Tuple[int, List[Tuple[int, int]]]]) -> List[Tuple[int, int, int, Tuple[int, int, int, int]]]:
    image = numpy.array(image)

    height, width, channels = image.shape
    if channels != 4:
        raise AssertionError("Image must be RGBA")

    g = []
    is_pixel_filled = numpy.zeros((height, width), dtype=bool)
    for x, y in sorted([(x, y) for y in range(height) for x in range(width)], key=lambda x: (x[0] + x[1], x[1], x[0])):
        if is_pixel_filled[y, x]:
            continue
        color_block = fill_block(image, is_pixel_filled, x, y)
        path = generate_path(color_block)
        
        if image[y, x, 3] == 0:
            continue
        
        minx, miny = map(min, zip(*path))
        normal_path = [(x - minx, y - miny) for x, y in path]
        key_path = tuple(sorted(normal_path))
        
        if defs_map.get(key_path) is None:
            defs_map[key_path] = (len(defs_map), normal_path)
        g.append((defs_map[key_path][0], minx, miny, image[y, x]))
    return g


def recreate():
    os.makedirs("data/", exist_ok=True)
    banner_atlas = Image.open("data/banner_atlas.png")
    
    gs = []
    defs_map = {}

    for index, pattern in enumerate(BANNER_DATA):
        for color in range(COLORS):
            pattern_img = banner_atlas.crop((BANNER_WIDTH * pattern.banner_atlas_index, BANNER_HEIGHT * color, BANNER_WIDTH * (pattern.banner_atlas_index + 1), BANNER_HEIGHT * (color + 1)))
            # Border with left, top, right, bottom (1, 3, 1, 3)
            pattern_img = ImageOps.expand(pattern_img, border=(2, 4, 3, 5), fill=(0, 0, 0, 0))
            codepoint = to_codepoint(index, color)
            g = convert(pattern_img, defs_map)
            gs.append((codepoint, g))
    
    with open("data/all.svg", 'w', encoding='UTF-8') as file:
        file.write('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1">\n')
        file.write('  <defs>\n')
        for index, path in defs_map.values():
            x1, y1 = path[0]
            path_string = f'M {x1},{y1}'
            for x2, y2 in path[1:]:
                if x1 == x2:
                    path_string += f' V {y2}'
                elif y1 == y2:
                    path_string += f' H {x2}'
                else:
                    raise AssertionError("This should not happen")
                x1, y1 = x2, y2
            path_string += ' Z'
            file.write(f'    <path id="{index}" d="{path_string}"/>\n')
        file.write('  </defs>\n')
        
        n = 0
        for codepoint, uses in gs:
            file.write(f'  <g id="uni{codepoint:X}">\n')
            for use in uses:
                index, x, y, color = use
                pixel_color = '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2])
                opacity = f"{(color[3] / 255):.3f}"
                file.write(f'    <use xlink:href="#{index}" x="{x + n // 16 * 30}" y="{y + n % 16 * 50}" fill="{pixel_color}" opacity="{opacity}"/>\n')
            file.write('  </g>\n')
            n += 1
        file.write('</svg>\n')


if __name__ == "__main__":
    recreate()
