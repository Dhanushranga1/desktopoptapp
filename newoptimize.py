import matplotlib.pyplot as plt
import numpy as np

# Defect data for fabric rolls
fabric_a_defects = [
    (7, 7, 4), (15, 15, 1), (23, 23, 5), (25, 25, 1), (28, 28, 4),
    (30, 30, 1), (41, 41, 4), (41, 41, 4), (52, 52, 1), (66, 66, 4),
    (68, 68, 4), (71, 71, 1), (76, 76, 4)
]
fabric_b_defects = [
    (3, 3, 2), (27, 27, 4), (37, 37, 4), (46, 46, 4), (48, 48, 4),
    (54, 54, 4), (58, 58, 1), (67, 67, 4), (75, 75, 4), (76, 76, 4)
]

# Fabric dimensions
fabric_a_length = 88.7
fabric_b_length = 81.1
fabric_width = 1.5

# Function to calculate total points and points per 100 sqm
def calculate_points_and_ratio(defects, length, width):
    total_points = sum(defect[2] for defect in defects)
    points_per_100_sqm = (total_points * 100) / (length * width)
    return total_points, points_per_100_sqm

# Function to visualize the cut sections
def visualize_cuts(length, defects, cut_positions, title):
    x = np.linspace(0, length, 1000)
    y = np.zeros_like(x)
    for defect in defects:
        start = int((defect[0] / length) * 1000)
        end = int((defect[1] / length) * 1000)
        y[start:end+1] = defect[2]
    
    plt.figure(figsize=(15, 2))
    plt.plot(x, y, label='Defects')
    for pos in cut_positions:
        plt.axvline(x=pos, color='r', linestyle='--', label='Cut')
    plt.title(title)
    plt.xlabel('Meters')
    plt.ylabel('Defect Points')
    plt.legend()
    plt.grid()
    plt.show()

# Initial points calculation
points_a, points_per_100_sqm_a = calculate_points_and_ratio(fabric_a_defects, fabric_a_length, fabric_width)
points_b, points_per_100_sqm_b = calculate_points_and_ratio(fabric_b_defects, fabric_b_length, fabric_width)

print(f"Fabric A: Total Points = {points_a}, Points per 100 sqm = {points_per_100_sqm_a}")
print(f"Fabric B: Total Points = {points_b}, Points per 100 sqm = {points_per_100_sqm_b}")

# Cutting logic to achieve points per 100 sqm <= 23
# For simplicity, assume we cut at the midpoint of defects with major points to reduce total points

cut_positions_a = []
cut_positions_b = []

if points_per_100_sqm_a > 23:
    # Sort defects by points descending
    fabric_a_defects.sort(key=lambda x: -x[2])
    total_removed_points = 0
    for defect in fabric_a_defects:
        if points_per_100_sqm_a - (defect[2] * 100) / (fabric_a_length * fabric_width) <= 23:
            break
        cut_positions_a.append((defect[0] + defect[1]) / 2)
        total_removed_points += defect[2]
        points_per_100_sqm_a = ((points_a - total_removed_points) * 100) / (fabric_a_length * fabric_width)

if points_per_100_sqm_b > 23:
    # Sort defects by points descending
    fabric_b_defects.sort(key=lambda x: -x[2])
    total_removed_points = 0
    for defect in fabric_b_defects:
        if points_per_100_sqm_b - (defect[2] * 100) / (fabric_b_length * fabric_width) <= 23:
            break
        cut_positions_b.append((defect[0] + defect[1]) / 2)
        total_removed_points += defect[2]
        points_per_100_sqm_b = ((points_b - total_removed_points) * 100) / (fabric_b_length * fabric_width)

print(f"Fabric A after cuts: Points per 100 sqm = {points_per_100_sqm_a}")
print(f"Fabric B after cuts: Points per 100 sqm = {points_per_100_sqm_b}")

# Visualization of cuts
visualize_cuts(fabric_a_length, fabric_a_defects, cut_positions_a, "Fabric A Cut Positions")
visualize_cuts(fabric_b_length, fabric_b_defects, cut_positions_b, "Fabric B Cut Positions")
