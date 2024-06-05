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

# Function to visualize the cut sections and joining
def visualize_cuts_and_join(lengths, defects, cut_positions, title):
    plt.figure(figsize=(15, 8))
    
    for i, (length, defect_list, cuts) in enumerate(zip(lengths, defects, cut_positions)):
        x = np.linspace(0, length, 1000)
        y = np.zeros_like(x)
        for defect in defect_list:
            start = int((defect[0] / length) * 1000)
            end = int((defect[1] / length) * 1000)
            y[start:end+1] = defect[2]
        
        plt.subplot(len(lengths), 1, i + 1)
        plt.plot(x, y, label=f'Fabric {i + 1} Defects')
        for pos in cuts:
            plt.axvline(x=pos, color='r', linestyle='--', label='Cut')
        plt.title(f'Fabric {i + 1}')
        plt.xlabel('Meters')
        plt.ylabel('Defect Points')
        plt.legend()
        plt.grid()

    plt.tight_layout()
    plt.suptitle(title, y=1.02)
    plt.show()

# Initial points calculation
points_a, points_per_100_sqm_a = calculate_points_and_ratio(fabric_a_defects, fabric_a_length, fabric_width)
points_b, points_per_100_sqm_b = calculate_points_and_ratio(fabric_b_defects, fabric_b_length, fabric_width)

print(f"Fabric A: Total Points = {points_a}, Points per 100 sqm = {points_per_100_sqm_a}")
print(f"Fabric B: Total Points = {points_b}, Points per 100 sqm = {points_per_100_sqm_b}")

# Function to maximize remaining length while keeping points per 100 sqm <= 23
def maximize_remaining_length(defects, length, width, target_points_per_100_sqm):
    total_points = sum(defect[2] for defect in defects)
    remaining_length = length
    remaining_defects = defects[:]
    
    points_per_100_sqm = (total_points * 100) / (remaining_length * width)
    cut_ranges = []
    
    while points_per_100_sqm > target_points_per_100_sqm and remaining_defects:
        # Find the defect with the highest points and remove it
        max_defect = max(remaining_defects, key=lambda x: x[2])
        remaining_defects.remove(max_defect)
        
        total_points -= max_defect[2]
        cut_ranges.append((max_defect[0], max_defect[1]))
        
        points_per_100_sqm = (total_points * 100) / (remaining_length * width)
    
    cut_positions = [(defect[0] + defect[1]) / 2 for defect in defects if defect not in remaining_defects]
    remaining_length -= sum(end - start + 1 for start, end in cut_ranges)
    
    return cut_positions, points_per_100_sqm, remaining_length, cut_ranges

cut_positions_a, points_per_100_sqm_a, remaining_length_a, cut_ranges_a = maximize_remaining_length(fabric_a_defects, fabric_a_length, fabric_width, 23)
cut_positions_b, points_per_100_sqm_b, remaining_length_b, cut_ranges_b = maximize_remaining_length(fabric_b_defects, fabric_b_length, fabric_width, 23)

print(f"Fabric A after cuts: Points per 100 sqm = {points_per_100_sqm_a}, Remaining Length = {remaining_length_a}")
print("Fabric A cut ranges:", cut_ranges_a)

print(f"Fabric B after cuts: Points per 100 sqm = {points_per_100_sqm_b}, Remaining Length = {remaining_length_b}")
print("Fabric B cut ranges:", cut_ranges_b)

# Ensure the combined length is at least 80 meters
if remaining_length_a + remaining_length_b < 80:
    print("Combined length after cuts is less than 80 meters. Further optimization needed.")
else:
    combined_length = remaining_length_a + remaining_length_b
    combined_points = points_a + points_b - sum(defect[2] for defect in fabric_a_defects if (defect[0] + defect[1]) / 2 in cut_positions_a) - sum(defect[2] for defect in fabric_b_defects if (defect[0] + defect[1]) / 2 in cut_positions_b)
    combined_points_per_100_sqm = (combined_points * 100) / (combined_length * fabric_width)
    print(f"Combined Fabric: Length = {combined_length}, Points per 100 sqm = {combined_points_per_100_sqm}")

# Visualization of cuts and joined fabric
visualize_cuts_and_join(
    [fabric_a_length, fabric_b_length],
    [fabric_a_defects, fabric_b_defects],
    [cut_positions_a, cut_positions_b],
    "Fabric Cuts and Joined Fabric"
)
