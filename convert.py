import sys
import re
from constants import *

mapping = {}
for index, banner in enumerate(BANNER_DATA):
    mapping[banner.mc_code] = index


def extract_char_and_num(word):
    pattern = re.compile(r'([a-zA-Z]+)(\d+)')
    match = pattern.search(word)
    if match:
        char_part = match.group(1)
        num_part = int(match.group(2))
        return (char_part, num_part)
    else:
        return None


def translate_text(text):
    words = text.split()
    translated_words = []

    for word in words:
        token = extract_char_and_num(word.lower())
        if token is not None and token[1] in range(COLORS):
            index = mapping.get(token[0])
            if index is not None:
                word = chr(to_codepoint(index, token[1]))
        translated_words.append(word)

    return ' '.join(translated_words)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide text to translate.")
        sys.exit(1)

    # Parse all remaining command line arguments and join them to handle spaces
    text = ' '.join(sys.argv[1:])

    translated_text = translate_text(text)
    print(f"Translated Text: {translated_text}")
