import csv
from dataclasses import dataclass

@dataclass
class BannerPatternVariant:
    mc_in_game_name: str
    mc_pattern_name: str
    clong_name: str
    mc_code: str
    banner_atlas_index: int

def to_codepoint(index: int, color_index: int) -> int:
    assert index in range(len(BANNER_DATA))
    assert color_index in range(COLORS)
    # Maybe use 0xF600 - 0xF8FF
    codepoint = 0xE000 + color_index + index * 16
    # assert codepoint in range(0xF600, 0xF900)
    return codepoint

BANNER_WIDTH = 20
BANNER_HEIGHT = 39

COLORS = 16

COLOR_NAMES = {
    'white': 0,
    'orange': 1,
    'magenta': 2,
    'light blue': 3,
    'yellow': 4,
    'lime': 5,
    'pink': 6,
    'gray': 7,
    'light gray': 8,
    'cyan': 9,
    'purple': 10,
    'blue': 11,
    'brown': 12,
    'green': 13,
    'red': 14,
    'black': 15,
}

BANNER_DATA: list[BannerPatternVariant] = []

with open('assets/banner.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    # Skip the header
    next(csv_reader, None)
    # Read each row into the array
    for row in csv_reader:
        BANNER_DATA.append(BannerPatternVariant(row[0], row[1], row[2], row[3], int(row[4])))
