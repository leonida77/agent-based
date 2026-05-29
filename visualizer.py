import numpy as np
import matplotlib.pyplot as plt


def render_model(model, step):
    image = np.ones((model.height, model.width, 3))

    for (x, y), value in model.discovered_map.items():
        row = model.height - 1 - y

        if value == "unknown":
            image[row, x] = [0.85, 0.85, 0.85]
        elif value == "obstacle":
            image[row, x] = [0.0, 0.0, 0.0]
        elif value == "dirty":
            image[row, x] = [1.0, 1.0, 1.0]
        elif value == "clean":
            image[row, x] = [0.4, 0.8, 0.4]

    rx, ry = model.robot.pos
    image[model.height - 1 - ry, rx] = [0.0, 0.2, 1.0]

    plt.imshow(image)
    plt.title(f"Robot Vacuum Simulation - Step {step}")
    plt.axis("off")
    plt.pause(0.05)
    plt.clf()