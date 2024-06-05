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
cut_penalty = 4

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

# Function to maximize remaining length while keeping points per 100 sqm <= 23
def maximize_remaining_length_with_cut_penalty(defects, length, width, target_points_per_100_sqm, cut_penalty):
    total_points = sum(defect[2] for defect in defects)
    remaining_length = length
    remaining_defects = defects[:]
    
    points_per_100_sqm = (total_points * 100) / (remaining_length * width)
    cut_ranges = []

    while points_per_100_sqm > target_points_per_100_sqm and remaining_defects:
        # Sort defects by density (defect points / length) and pick the section with maximum density
        remaining_defects.sort(key=lambda x: x[2] / (x[1] - x[0] + 1), reverse=True)
        
        # Find the largest defect or the section that includes the most defects and cut it
        start, end, _ = remaining_defects.pop(0)
        
        # Ensure the section is greater than 1 meter
        if end - start < 1:
            continue

        cut_ranges.append((start, end))
        
        # Remove all defects in the cut range
        remaining_defects = [d for d in remaining_defects if d[1] < start or d[0] > end]
        
        total_points -= sum(d[2] for d in remaining_defects if start <= d[0] <= end or start <= d[1] <= end)
        total_points += cut_penalty  # Add cut penalty
        remaining_length -= (end - start + 1)
        points_per_100_sqm = (total_points * 100) / (remaining_length * width)

    cut_positions = [(start + end) / 2 for start, end in cut_ranges]
    
    return cut_positions, points_per_100_sqm, remaining_length, cut_ranges

# Initial points calculation
points_a, points_per_100_sqm_a = calculate_points_and_ratio(fabric_a_defects, fabric_a_length, fabric_width)
points_b, points_per_100_sqm_b = calculate_points_and_ratio(fabric_b_defects, fabric_b_length, fabric_width)

print(f"Fabric A: Total Points = {points_a}, Points per 100 sqm = {points_per_100_sqm_a}")
print(f"Fabric B: Total Points = {points_b}, Points per 100 sqm = {points_per_100_sqm_b}")

cut_positions_a, points_per_100_sqm_a, remaining_length_a, cut_ranges_a = maximize_remaining_length_with_cut_penalty(fabric_a_defects, fabric_a_length, fabric_width, 23, cut_penalty)
cut_positions_b, points_per_100_sqm_b, remaining_length_b, cut_ranges_b = maximize_remaining_length_with_cut_penalty(fabric_b_defects, fabric_b_length, fabric_width, 23, cut_penalty)

print(f"Fabric A after cuts: Points per 100 sqm = {points_per_100_sqm_a}, Remaining Length = {remaining_length_a}")
print("Fabric A cut ranges:", cut_ranges_a)

print(f"Fabric B after cuts: Points per 100 sqm = {points_per_100_sqm_b}, Remaining Length = {remaining_length_b}")
print("Fabric B cut ranges:", cut_ranges_b)

# If fabric A or B is still above the threshold, combine them
if points_per_100_sqm_a > 23:
    # Try to bring down Fabric A points by combining with Fabric B
    combined_length = remaining_length_a + remaining_length_b
    combined_points = sum(defect[2] for defect in fabric_a_defects if defect not in cut_ranges_a) + sum(defect[2] for defect in fabric_b_defects if defect not in cut_ranges_b) + cut_penalty  # Add penalty for combining
    combined_points_per_100_sqm = (combined_points * 100) / (combined_length * fabric_width)
    print(f"Combined Fabric (A+B): Length = {combined_length}, Points per 100 sqm = {combined_points_per_100_sqm}")
    if combined_length <= 80 and combined_points_per_100_sqm <= 23:
        print("Combined fabric meets the requirements.")
else:
    combined_length = remaining_length_a
    combined_points_per_100_sqm = points_per_100_sqm_a

if points_per_100_sqm_b > 23:
    # Try to bring down Fabric B points by combining with Fabric A
    combined_length = remaining_length_b + remaining_length_a
    combined_points = sum(defect[2] for defect in fabric_b_defects if defect not in cut_ranges_b) + sum(defect[2] for defect in fabric_a_defects if defect not in cut_ranges_a) + cut_penalty  # Add penalty for combining
    combined_points_per_100_sqm = (combined_points * 100) / (combined_length * fabric_width)
    print(f"Combined Fabric (B+A): Length = {combined_length}, Points per 100 sqm = {combined_points_per_100_sqm}")
    if combined_length <= 80 and combined_points_per_100_sqm <= 23:
        print("Combined fabric meets the requirements.")
else:
    combined_length = remaining_length_b
    combined_points_per_100_sqm = points_per_100_sqm_b

# Ensure the combined length is below 80 meters
if combined_length > 80:
    combined_length = 80

print(f"Final Combined Fabric: Length = {combined_length}, Points per 100 sqm = {combined_points_per_100_sqm}")

# Visualization of cuts and joined fabric
visualize_cuts_and_join(
    [fabric_a_length, fabric_b_length],
    [fabric_a_defects, fabric_b_defects],
    [cut_positions_a, cut_positions_b],
    "Fabric Cuts and Joined Fabric"
)
