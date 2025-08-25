from PIL import Image

def convert_to_png_and_remove_white(image_path, output_path):
    img = Image.open(image_path)
    img = img.convert("RGBA")

    datas = img.getdata()

    new_data = []
    for item in datas:
        # change all white (also shades of whites)
        # pixels to transparent
        if item[0] in list(range(200, 256)):
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)
    img.save(output_path, "PNG")

# Convert and remove white portions for both images
convert_to_png_and_remove_white("./frontend/static/solution/deforestation1.png", "./frontend/static/solution/deforestation1.png")
convert_to_png_and_remove_white("./frontend/static/solution/deforestation2.png", "./frontend/static/solution/deforestation2.png")