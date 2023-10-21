import math
import random

from GraphicFile import GraphicFile


def calculate_bits_count_required(number):
    if number <= 0:
        return 1
    return int(math.log2(number)) + 1


width = 50
height = 50
palette = [
    (0, 0, 0, 255),
    (255, 0, 0, 255),
    (0, 255, 0, 255),
    (0, 0, 255, 255),
    (255, 255, 255, 255),
]

pixels = []
for _ in range(width * height):
    pixels.append(random.randint(0, len(palette) - 1))

GraphicFile(width, height, calculate_bits_count_required(len(palette) - 1), len(palette), palette, pixels).\
    save('image1.gf')
