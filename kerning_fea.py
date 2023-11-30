from constants import *
import os
from itertools import product


def write_fea():
    os.makedirs("build/", exist_ok=True)
    base_list = [to_codepoint(0, color_index) for color_index in range(COLORS)]
    pattern_list = [to_codepoint(pattern, color_index) for color_index, pattern in product(range(COLORS), range(1, len(BANNER_DATA)))]

    with open("build/BannerScript.fea", 'w', encoding='UTF-8') as file:
        file.write((
            "languagesystem DFLT dflt;\n"
            "languagesystem latn dflt;\n"
            "\n"
            "feature ccmp {\n"
            "} ccmp;\n"
            "\n"
            f"@BASE = [{' '.join([hex(x)[2:] for x in base_list])}];\n"
            f"@PATTERN = [{' '.join([hex(x)[2:] for x in pattern_list])}];\n"
            "feature kern {\n"
            "    pos [@BASE @PATTERN] @PATTERN -800;\n"
            "} kern;\n"
            ))


if __name__ == "__main__":
    write_fea()
