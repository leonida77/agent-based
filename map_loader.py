from PIL import Image


def load_floorplan_as_grid(image_path, grid_width=80, grid_height=50, threshold=180):
    image = Image.open(image_path).convert("L")
    image = image.resize((grid_width, grid_height))

    real_map = {}

    for img_y in range(grid_height):
        for x in range(grid_width):
            pixel = image.getpixel((x, img_y))

            mesa_y = grid_height - 1 - img_y
            position = (x, mesa_y)

            if pixel < threshold:
                real_map[position] = "obstacle"
            else:
                real_map[position] = "dirty"

    return real_map