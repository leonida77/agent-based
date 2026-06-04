import numpy as np
import matplotlib.pyplot as plt


def render_model(model, step):
    image = np.ones((model.height, model.width, 3))

    for (x, y), value in model.discovered_map.items():
        row = model.height - 1 - y

        if value == "unknown":
            # Сиво = непознато
            image[row, x] = [0.85, 0.85, 0.85]

        elif value == "obstacle":
            # Црно = ѕид
            image[row, x] = [0.0, 0.0, 0.0]

        elif value == "dirty":
            # Бело = откриено но неисчистено
            image[row, x] = [1.0, 1.0, 1.0]

        elif value == "clean":
            # Зелено = исчистено
            image[row, x] = [0.4, 0.8, 0.4]

    # Робот
    rx, ry = model.robot.pos
    image[model.height - 1 - ry, rx] = [0.0, 0.2, 1.0]

    # Фаза
    phase_text = ""

    if model.robot.phase == "explore":
        phase_text = "SCANNING"

    elif model.robot.phase == "clean":
        phase_text = "CLEANING"

    elif model.robot.phase == "return_home":
        phase_text = "RETURNING HOME"

    # Coverage %
    discovered_cells = sum(
        1
        for value in model.discovered_map.values()
        if value != "unknown"
    )

    coverage = (
        discovered_cells
        / len(model.discovered_map)
        * 100
    )

    plt.imshow(image)

    plt.title(
        f"{phase_text} | Step: {step} | Coverage: {coverage:.1f}%"
    )

    plt.axis("off")

    plt.pause(0.05)
    plt.clf()