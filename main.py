import tkinter

from PIL import Image, ImageTk, ImageGrab
from GraphicFile import GraphicFile, calculate_bits_count_required


def draw(event):
    canvas.create_oval(event.x - 10,
                       event.y - 10,
                       event.x + 10,
                       event.y + 10,
                       fill='purple', outline='purple')


def save_action():
    x = root.winfo_rootx() + canvas.winfo_x()
    y = root.winfo_rooty() + canvas.winfo_y()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()
    image = ImageGrab.grab().crop((x, y, x1, y1))
    palette = []
    pixels = []
    for i in range(2, image.height - 2):
        for j in range(image.width):
            pixel = image.getpixel((j, i))
            if len(palette) > 32:
                pixels.append(33)
            else:
                color = (pixel[0], pixel[1], pixel[2], 255)
                if color not in palette:
                    palette.append(color)
                pixels.append(palette.index(color))
    GraphicFile(image.width,
                image.height - 4,
                calculate_bits_count_required(len(palette) - 1),
                len(palette),
                palette,
                pixels).save('image2.gf')


gf = GraphicFile(file='image2.gf').upscale(1, 1)
root = tkinter.Tk()
root.geometry(f'{gf.width}x{gf.height + 50}')
root.resizable(False, False)

bg_color = "#C4C4C4"

canvas = tkinter.Canvas(root, background=bg_color, height=gf.height, width=gf.width)
canvas.pack(anchor='nw', expand=1)
canvas.bind("<B1-Motion>", draw)

save_btn = tkinter.Button(root, text="Save as gf", width=10, command=save_action)
save_btn.pack(after=canvas, anchor='nw')

img = Image.new('RGBA', (gf.width, gf.height))
for i in range(gf.height):
    for j in range(gf.width):
        index = gf.pixels[i * gf.width + j]
        if index > gf.palette_size:
            color = (0, 0, 0, 0)
        else:
            color = gf.palette[index]
        img.putpixel((j, i), color)
imgtk = ImageTk.PhotoImage(img)
canvas.create_image((gf.width // 2, gf.height // 2 + 2), image=imgtk)

root.mainloop()
