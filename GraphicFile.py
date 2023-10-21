import math
import struct

from collections import deque


def calculate_bits_count_required(number):
    if number <= 0:
        return 1
    return int(math.log2(number)) + 1


class GraphicFile:
    def __init__(self, width=0, height=0, bits_per_pixel=0, palette_size=0, palette=None, pixels=None, file=None):
        if pixels is None:
            pixels = []
        if palette is None:
            palette = []
        self.width = width
        self.height = height
        self.bits_per_pixel = bits_per_pixel
        self.palette_size = palette_size
        self.palette = palette
        self.pixels = pixels

        if file is None:
            return

        with open(file, 'rb') as f:
            self.width, self.height, self.bits_per_pixel, self.palette_size = struct.unpack('>HHBH', f.read(7))

            for _ in range(self.palette_size):
                self.palette.append(struct.unpack('>BBBB', f.read(4)))

            processed = 0
            d = deque()
            for _ in range(math.ceil(self.width * self.height * self.bits_per_pixel / 8)):
                packed = struct.unpack('>B', f.read(1))[0]
                for _ in range(8):
                    d.append((packed & 0b10000000) >> 7)
                    packed <<= 1

                    if len(d) >= self.bits_per_pixel:
                        x = d.popleft()
                        for _ in range(self.bits_per_pixel - 1):
                            x <<= 1
                            x |= d.popleft()
                        self.pixels.append(x)
                        processed += 1

                    if processed == self.width * self.height:
                        break

    def upscale(self, vert, hor):
        width = self.width * hor
        height = self.height * vert
        bits_per_pixel = self.bits_per_pixel
        palette_size = self.palette_size
        palette = self.palette
        pixels = []

        for i in range(self.height):
            for _ in range(vert):
                for j in range(self.width):
                    for _ in range(hor):
                        pixels.append(self.pixels[i * self.width + j])

        return GraphicFile(width, height, bits_per_pixel, palette_size, palette, pixels)

    def save(self, file):
        pixel_size = calculate_bits_count_required(len(self.palette) - 1)

        width_bits = struct.pack('>H', self.width)
        height_bits = struct.pack('>H', self.height)

        bits_per_pixel_bits = struct.pack('>B', pixel_size)
        palette_size_bits = struct.pack('>H', len(self.palette))

        with open(file, 'wb') as f:
            f.write(width_bits)
            f.write(height_bits)
            f.write(bits_per_pixel_bits)
            f.write(palette_size_bits)

            for color in self.palette:
                for component in color:
                    component_bits = struct.pack('>B', component)
                    f.write(component_bits)

            pixel_bits = []
            for pixel in self.pixels:
                bits = format(pixel, '0{pixel_size}b'.format(pixel_size=pixel_size))
                pixel_bits.append(bits)
            binary = ''.join(pixel_bits)

            for i in range(0, len(binary), 8):
                byte = f'{binary[i:i + 8]:0<8}'
                integer = int(byte, 2)
                pixel_bits = struct.pack('>B', integer)
                f.write(pixel_bits)
