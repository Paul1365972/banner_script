#!/usr/bin/env python3

# Convert a pixel art to SVG file
# Copyright (C) 2021  Star Brilliant
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Source: https://gist.github.com/m13253/66284bc244deeff0f0f8863c206421c7
# Modified

from typing import List, Tuple
from PIL import Image
import numpy


def fill_block(image: numpy.ndarray, is_pixel_filled: numpy.ndarray, x: int, y: int) -> List[Tuple[int, int]]:
    # Flood fill algorithm
    pixel_color = image[y, x]
    color_block = [(x, y)]
    is_pixel_filled[y, x] = True 
    i = 0
    while i < len(color_block):
        x1, y1 = color_block[i]
        for x2, y2 in {(x1, y1 - 1), (x1 - 1, y1), (x1 + 1, y1), (x1, y1 + 1)}:
            if y2 < 0 or y2 >= image.shape[0] or x2 < 0 or x2 >= image.shape[1]:
                continue
            if is_pixel_filled[y2, x2]:
                continue
            if (image[y2, x2] == pixel_color).all():
                color_block.append((x2, y2))
                is_pixel_filled[y2, x2] = True
        i += 1
    if len(color_block) != len(set(color_block)):
        raise AssertionError("Duplicates found, this should not happen")
    return color_block


def generate_path(color_block: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    # Square tracing algorithm
    # http://www.imageprocessingplace.com/downloads_V3/root_downloads/tutorials/contour_tracing_Abeer_George_Ghuneim/alg.html
    x, y = sorted(color_block, key=lambda x: (x[0] + x[1], x[1], x[0]))[0]
    path = [(x, y)]
    x1, y1 = x, y
    dx, dy = 1, 0
    while (x1, y1) != (x, y) or len(path) == 1:
        x2, y2 = x1 + (dx + dy - 1) // 2, y1 + (dy - dx - 1) // 2  # Left pixel
        x3, y3 = x1 + (dx - dy - 1) // 2, y1 + (dx + dy - 1) // 2  # Right pixel
        if (x3, y3) in color_block:
            if (x2, y2) in color_block:
                path.append((x1, y1))
                dx, dy = dy, -dx  # Turn left
            else:
                pass  # Go straight
        else:
            path.append((x1, y1))
            dx, dy = -dy, dx  # Turn right
        x1, y1 = x1 + dx, y1 + dy
    return path


def convert(image: Image, output_file: str):
    image = numpy.array(image)

    height, width, channels = image.shape
    if channels != 4:
        raise AssertionError("Image must be RGBA")

    is_pixel_filled = numpy.zeros((height, width), dtype=bool)
    with open(output_file, 'w', encoding='UTF-8') as file:
        file.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
        file.write(f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">\n')
        file.write('  <g>\n')
        
        for x, y in sorted([(x, y) for y in range(height) for x in range(width)], key=lambda x: (x[0] + x[1], x[1], x[0])):
            if is_pixel_filled[y, x]:
                continue
            color_block = fill_block(image, is_pixel_filled, x, y)
            path = generate_path(color_block)
            
            pixel_color = '#{:02x}{:02x}{:02x}'.format(image[y, x, 0], image[y, x, 1], image[y, x, 2])
            opacity = f"{(image[y, x, 3] / 255):.3f}"
            if image[y, x, 3] == 0:
                continue
            
            x1, y1 = path[0]
            path_string = f'M {x1},{y1}'
            for x2, y2 in path[1:]:
                if x1 == x2:
                    path_string += f' V {y2}'
                elif y1 == y2:
                    path_string += f' H {x2}'
                else:
                    path_string += f' L {x2},{y2}'
                    raise AssertionError("This should not happen")
                x1, y1 = x2, y2
            path_string += ' Z'
            file.write(f'    <path fill="{pixel_color}" opacity="{opacity}" d="{path_string}"/>\n')
        file.write('  </g>\n')
        file.write('</svg>\n')
