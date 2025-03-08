import os
from PIL import Image


def trim_image(img, bg_color=(255, 255, 255)):
    if img.mode != "RGB":
        img = img.convert("RGB")

    width, height = img.size
    left, top, right, bottom = width, height, -1, -1

    for x in range(width):
        for y in range(height):
            if img.getpixel((x, y)) != bg_color:
                left = x
                break
        if left != width:
            break
    for y in range(height):
        for x in range(width):
            if img.getpixel((x, y)) != bg_color:
                top = y
                break
        if top != height:
            break

    for x in range(width - 1, -1, -1):
        for y in range(height):
            if img.getpixel((x, y)) != bg_color:
                right = x
                break
        if right != -1:
            break

    for y in range(height - 1, -1, -1):
        for x in range(width):
            if img.getpixel((x, y)) != bg_color:
                bottom = y
                break
        if bottom != -1:
            break

    if left == width and top == height and right == -1 and bottom == -1:
        return img
    else:
        cropped_img = img.crop((left, top, right + 1, bottom+1))
        return cropped_img


def resize_and_crop_png_images(folder_path, target_width, target_height):
    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            filepath = os.path.join(folder_path, filename)
            try:
                img = Image.open(filepath)
                img = trim_image(img).resize((target_width, target_height))
                img.save(filepath, "PNG")
            except Exception as e:
                print(f"Ошибка при обработке файла {filename}: {e}")
