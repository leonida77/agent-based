from model import VacuumModel

model = VacuumModel(10, 10)

for step in range(50):
    print(f"\nSTEP {step + 1}")
    model.step()

print("\nSimulation finished")
print(f"Remaining dirty cells: {len(model.dirty_cells)}")