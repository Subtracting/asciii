import cv2
from PIL import Image, ImageDraw, ImageFont

mapping = [".", ";", "/", "}", "%", "#", "$"]
# mapping = ["/", "#", "$", "9", "0"]

size = 40
gif = 0

font = ImageFont.truetype("arial.ttf", size)


def change_contrast(img, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))

    def contrast(c):
        return 128 + factor * (c - 128)

    return img.point(contrast)


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
    change_contrast(image, 100)
    return image


def draw_char(image, coords, character, fontColor):
    x, y = coords
    draw = ImageDraw.Draw(image)
    draw.text((x, y), character, fill=fontColor, font=font)


def process_image(input_path, size, mapping, count):
    img = cv2.imread(f"{input_path}", 0)
    img2 = cv2.imread(f"{input_path}", 1)

    width = len(img[0])
    height = len(img)

    image = draw_img((width, height), "black")

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

            draw_char(image, (x, y), mapping[idx], tuple(img2[y][x]))

    image.save(f"output/image_{count:02d}.png", "PNG")
    # ges = cv2.Canny(img, 100, 200)
    # print(ges)


process_image("input/test.png", size=size, mapping=mapping, count=9999999)


if gif == 1:
    vidcap = cv2.VideoCapture("recall.mp4")
    success, image = vidcap.read()
    count = 0
    k = 0
    images = []

    while success:
        cv2.imwrite(f"frames/frame{count:02d}.jpg", image)
        success, image = vidcap.read()
        print("Read a new frame: ", success, count)
        process_image(
            f"frames/frame{count:02d}.jpg", size=size, mapping=mapping, count=count
        )
        images.append(f"output/image_{count:02d}.png")
        count += 1

    create_gif(images, "recall.gif")
