import os
from PIL import Image, ImageOps

def trim_image(img, border_size=5, bg_color=(255, 255, 255)):

    # Преобразуем изображение в режим RGB, если оно в другом режиме
    if img.mode != "RGB":
        img = img.convert("RGB")

    width, height = img.size
    left, top, right, bottom = width, height, -1, -1

    # Ищем самую левую границу
    for x in range(width):
        for y in range(height):
            if img.getpixel((x, y)) != bg_color:  # Если пиксель не фоновый
                left = x
                break
        if left != width:
            break

    # Ищем самую верхнюю границу
    for y in range(height):
        for x in range(width):
            if img.getpixel((x, y)) != bg_color:  # Если пиксель не фоновый
                top = y
                break
        if top != height:
            break

    # Ищем самую правую границу
    for x in range(width - 1, -1, -1):
        for y in range(height):
            if img.getpixel((x, y)) != bg_color:  # Если пиксель не фоновый
                right = x
                break
        if right != -1:
            break

    # Ищем самую нижнюю границу
    for y in range(height - 1, -1, -1):
        for x in range(width):
            if img.getpixel((x, y)) != bg_color:  # Если пиксель не фоновый
                bottom = y
                break
        if bottom != -1:
            break

    # Если границы не изменились, значит, изображение полностью фоновое
    if left == width and top == height and right == -1 and bottom == -1:
        return img

    # Обрезаем изображение
    cropped_img = img.crop((left, top, right + 1, bottom + 1))

    # Добавляем рамку
    cropped_width, cropped_height = cropped_img.size
    new_width = cropped_width + 2 * border_size
    new_height = cropped_height + 2 * border_size
    new_img = Image.new("RGB", (new_width, new_height), bg_color)  # Создаем новое изображение с цветом фона
    new_img.paste(cropped_img, (border_size, border_size))  # Вставляем обрезанное изображение в центр

    return new_img

def resize_and_crop_png_images(folder_path, target_width, target_height, crop_type='center'):

    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            filepath = os.path.join(folder_path, filename)
            try:
                img = Image.open(filepath)

                # Обрезаем изображение по крайним черным пикселям и добавляем рамку


                # Изменение размера с сохранением пропорций
                img = ImageOps.fit(img, (target_width, target_height), Image.LANCZOS, 0, (0.5, 0.5))
                img = trim_image(img)
                img = ImageOps.fit(img, (target_width, target_height), Image.LANCZOS, 0, (0.5, 0.5))
                img.save(filepath, "PNG")  # Перезаписываем исходный файл
                print(f"Изменен размер и обрезано изображение: {filename}")

            except Exception as e:
                print(f"Ошибка при обработке файла {filename}: {e}")

# Пример использования:
folder_path = "images"  # Замените на фактический путь к папке
target_width = 100
target_height = 100
resize_and_crop_png_images(folder_path, target_width, target_height)
