from PIL import Image
from constants import *
import os


def reduce_image_by_4(image):
    # Remove border
    image = image.crop((0, 0, image.size[0] - 84, image.size[1]))
    width, height = image.size

    # Make sure dimensions are divisible by 4
    if width % 4 != 0 or height % 4 != 0:
        raise AssertionError(f"Dimensions of the image must be divisible by 4")

    if width // 4 != len(BANNER_DATA) * BANNER_WIDTH:
        raise AssertionError(f"Unexpected banner width, expected: {width // 4}, got { len(BANNER_DATA) * BANNER_WIDTH }")
    if height // 4 != 16 * BANNER_HEIGHT:
        raise AssertionError(f"Unexpected banner height, expected {height // 4}, got {16 * BANNER_HEIGHT}")

    # Create a new image with reduced dimensions
    new_img = Image.new("RGBA", (width//4, height//4))

    # Iterate through the original image in 4x4 blocks
    for x in range(0, width, 4):
        for y in range(0, height, 4):
            color = image.getpixel((x, y))

            # Fail in case colors inside a block differ
            for dx in range(4):
                for dy in range(4):
                    if image.getpixel((x + dx, y + dy)) != color:
                        raise AssertionError(f"Unable to scale down image, colors inside group not equal (Location: {x + dx}, {y + dy})")

            # Write pixel to new image
            new_img.putpixel((x // 4, y // 4), color)

    return new_img

def fix_first_entry(image):
    for color_index in range(16):
        color = image.getpixel((3 * BANNER_WIDTH // 2, (2 * color_index + 1) * BANNER_HEIGHT // 2))
        for y in range(BANNER_HEIGHT):
            for x in range(BANNER_WIDTH):
                image.putpixel((x, y + color_index * BANNER_HEIGHT), color)
    return image

def fix_gradient_entry(image, index):
    for color_index in range(COLORS):
        for y in range(BANNER_HEIGHT):
            avg = (0, 0, 0, 0)
            for x in range(BANNER_WIDTH):
                color = image.getpixel((x + index * BANNER_WIDTH, y + color_index * BANNER_HEIGHT))
                avg = tuple(map(lambda acc, val: acc + val, avg, color))
            color = tuple(c // BANNER_WIDTH for c in avg)
            for x in range(BANNER_WIDTH):
                image.putpixel((x + index * BANNER_WIDTH, y + color_index * BANNER_HEIGHT), color)
    return image

def fix_skull(image):
    head = set([(x,y) for x in range(6, 14) for y in range(12, 20)])
    face = set([(7, 16), (8, 16), (11, 16), (12, 16), (9, 17), (10, 17)] + [(x, 18) for x in range(7, 13)])
    pixels = head.difference(face)
    for color_index in range(COLORS):
        for y in range(BANNER_HEIGHT):
            avg = (0, 0, 0, 0)
            for x, y in pixels:
                color = image.getpixel((x + 31 * BANNER_WIDTH, y + color_index * BANNER_HEIGHT))
                avg = tuple(map(lambda acc, val: acc + val, avg, color))
            color = tuple(c // len(pixels) for c in avg)
            for x, y in pixels:
                image.putpixel((x + 31 * BANNER_WIDTH, y + color_index * BANNER_HEIGHT), color)
    return image

def create():
    image = Image.open('assets/mc_tools_bannersx4.png')
    image = reduce_image_by_4(image)
    image = fix_first_entry(image)
    image = fix_gradient_entry(image, 29)
    image = fix_gradient_entry(image, 36)
    image = fix_skull(image)
    os.makedirs("data/", exist_ok=True)
    image.save("data/banner_atlas.png")

if __name__ == "__main__":
    create()
