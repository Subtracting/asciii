import random
import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np

mapping = [".", ";", "/", "}", "%", "#", "$"]

# size = 16
# font_scale = 20


def create_gif(image_paths, output_gif_path, duration=60):
    images = [Image.open(image_path) for image_path in image_paths]
    images[0].save(
        output_gif_path,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0,
    )


def draw_img(size, bgColor):
    image = Image.new("RGB", size, bgColor)
    return image


def draw_char(image, coords, character, font, fontColor):
    x, y = coords
    draw = ImageDraw.Draw(image)
    draw.text((x, y), character, fill=fontColor, font=font)


def process_image(input_path, size, mapping, output_path, font_scale):
    font = ImageFont.truetype("arial.ttf", font_scale)

    img = cv2.imread(f"{input_path}", 0)
    img2 = cv2.imread(f"{input_path}", 1)

    bg_color = tuple(map(int, np.min(img2, axis=(0, 1))))

    v = np.median(img)
    sigma = 0.33

    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edges = cv2.Canny(img, lower, upper, apertureSize=3)

    width = len(img[0])
    height = len(img)

    image = draw_img((width, height), bg_color)

    for y in range(0, height, size):
        for x in range(0, width, size):
            avg_arr = set()
            for s in range(size):
                try:
                    avg_arr.add(img[y][x + s])
                    avg_arr.add(img[y + s][x])
                    avg_arr.add(img[y + s][x + s])
                except:
                    pass

            avg = sum(avg_arr) / len(avg_arr)
            idx = int(avg // (355 / len(mapping)))

            red = img2[y][x][2]
            green = img2[y][x][1]
            blue = img2[y][x][0]

            color = (red, green, blue)
            char = mapping[idx]

            draw_char(
                image,
                (x, y),
                char,
                font,
                color,
            )

    for y in range(0, height, size // 2):
        for x in range(0, width, size // 2):
            if edges[y][x] != 0:
                char = random.sample([".", ","], 1)[0]
                red = img2[y][x][2]
                green = img2[y][x][1]
                blue = img2[y][x][0]

                color = (red, green, blue)
                color = (80, 50, 50)
                draw_char(
                    image,
                    (x, y),
                    char,
                    font,
                    color,
                )

    image.save(output_path, "PNG")


# if gif == 1:
#     vidcap = cv2.VideoCapture("input/recall.mp4")
#     success, image = vidcap.read()
#     count = 0
#     k = 0
#     images = []

#     while success:
#         cv2.imwrite(f"frames/frame{count:02d}.jpg", image)
#         success, image = vidcap.read()
#         print("Read a new frame: ", success, count)
#         process_image(
#             f"frames/frame{count:02d}.jpg", size=size, mapping=mapping, count=count
#         )
#         images.append(f"output/image_{count:02d}.png")
#         count += 1

#     create_gif(images, "output/recall.gif")
