import matplotlib.pyplot as plt

from model import VacuumModel
from visualizer import render_model


model = VacuumModel(
    image_path="assets/floorplan.png",
    width=80,
    height=50
)

plt.figure(figsize=(12, 8))
for step in range(5000):
    model.step()

    if step % 5 == 0:
        render_model(model, step)

    if model.finished:
        plt.close()
        print("\n===================================")
        print("FINISHED CLEANING")
        print("Robot returned to charging station")
        print("===================================")
        break

model.print_statistics()