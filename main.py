import matplotlib.pyplot as plt

from model import VacuumModel
from visualizer import render_model


model = VacuumModel(
    image_path="assets/floorplan.png",
    width=80,
    height=50
)

plt.figure(figsize=(12, 8))

for step in range(2000):
    model.step()

    if step % 5 == 0:
        render_model(model, step)

    if model.finished:
        break

plt.close()

print("\nSimulation finished")
print(f"Remaining dirty cells: {len(model.dirty_cells)}")
model.print_statistics()