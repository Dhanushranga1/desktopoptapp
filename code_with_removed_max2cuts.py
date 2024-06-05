import matplotlib.pyplot as plt
import numpy as np

# Defect data for fabric rolls
# fabric_a_defects = [
#     (7, 7, 4), (15, 15, 1), (23, 23, 5), (25, 25, 1), (28, 28, 4),
#     (30, 30, 1), (41, 41, 4), (41, 41, 4), (52, 52, 1), (66, 66, 4),
#     (68, 68, 4), (71, 71, 1), (76, 76, 4)
# ]
fabric_a_defects = [
    (2, 2, 4), (5, 5, 4), (10, 10, 1), (22, 22, 4), 
    (23, 23, 4), (28, 28, 4), (35, 35, 2), (39, 39, 4), 
    (46, 46, 2), (70, 70, 2)
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
def visualize_cuts_and_join(lengths, defects, cut_positions, title, cut_ranges):
    plt.figure(figsize=(15, 8))
    
    for i, (length, defect_list, cuts, cut_range) in enumerate(zip(lengths, defects, cut_positions, cut_ranges)):
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
        
        for start, end in cut_range:
            plt.axvspan(start, end, color='y', alpha=0.3, label='Cut Range')

        plt.title(f'Fabric {i + 1}')
        plt.xlabel('Meters')
        plt.ylabel('Defect Points')
        plt.legend()
        plt.grid()

    plt.tight_layout()
    plt.suptitle(title, y=1.02)
    plt.show()

# Function to maximize remaining length while keeping points per 100 sqm <= 23 with max 2 cuts
def maximize_remaining_length_with_cut_penalty(defects, length, width, target_points_per_100_sqm, cut_penalty, min_remaining_length_ratio):
    total_points = sum(defect[2] for defect in defects)
    remaining_length = length
    remaining_defects = defects[:]
    
    points_per_100_sqm = (total_points * 100) / (remaining_length * width)
    cut_ranges = []

    # Function to find high-density sections
    def find_high_density_sections(defects):
        sections = []
        start = defects[0][0]
        end = defects[0][1]
        total_points = defects[0][2]

        for i in range(1, len(defects)):
            if defects[i][0] <= end + 1:  # Continuous or overlapping defects
                end = max(end, defects[i][1])
                total_points += defects[i][2]
            else:
                if end - start >= 1:  # Section length should be greater than 1 meter
                    sections.append((start, end, total_points))
                start = defects[i][0]
                end = defects[i][1]
                total_points = defects[i][2]

        if end - start >= 1:  # Add the last section
            sections.append((start, end, total_points))
        
        return sections

    while points_per_100_sqm > target_points_per_100_sqm and remaining_defects and remaining_length > min_remaining_length_ratio * length:
        # Sort defects by start point
        remaining_defects.sort()

        # Find high-density sections
        high_density_sections = find_high_density_sections(remaining_defects)

        # Sort sections by density (defect points / length) and pick the section with maximum density
        high_density_sections.sort(key=lambda x: x[2] / (x[1] - x[0] + 1), reverse=True)
        
        # Remove the section with the highest density
        # start, end, _ = high_density_sections.pop(0)
        if high_density_sections:
            start, end, _ = high_density_sections.pop(0)
        else:
            break

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

# Min remaining length ratio (75% of original length)
min_remaining_length_ratio = 0.75

# Maximize remaining length for Fabric A
cut_positions_a, points_per_100_sqm_a, remaining_length_a, cut_ranges_a = maximize_remaining_length_with_cut_penalty(fabric_a_defects, fabric_a_length, fabric_width, 23, cut_penalty, min_remaining_length_ratio)
print(f"Fabric A after cuts: Points per 100 sqm = {points_per_100_sqm_a}, Remaining Length = {remaining_length_a}")
print("Fabric A cut ranges:", cut_ranges_a)

# Maximize remaining length for Fabric B
cut_positions_b, points_per_100_sqm_b, remaining_length_b, cut_ranges_b = maximize_remaining_length_with_cut_penalty(fabric_b_defects, fabric_b_length, fabric_width, 23, cut_penalty, min_remaining_length_ratio)
print(f"Fabric B after cuts: Points per 100 sqm = {points_per_100_sqm_b}, Remaining Length = {remaining_length_b}")
print("Fabric B cut ranges:", cut_ranges_b)

# If fabric A or B is still above the threshold, combine them
combined_length = 0
combined_points_per_100_sqm = 0

if points_per_100_sqm_a > 23 or points_per_100_sqm_b > 23:
    # Try to bring down Fabric A and B points by combining
    combined_length = remaining_length_a + remaining_length_b
    combined_points = sum(defect[2] for defect in fabric_a_defects if defect not in cut_ranges_a) + sum(defect[2] for defect in fabric_b_defects if defect not in cut_ranges_b) + cut_penalty  # Add penalty for combining
    combined_points_per_100_sqm = (combined_points * 100) / (combined_length * fabric_width)
    print(f"Combined Fabric (A+B): Length = {combined_length}, Points per 100 sqm = {combined_points_per_100_sqm}")
    if combined_length >= 80 and combined_points_per_100_sqm <= 23:
        print("Combined fabric meets the requirements.")
else:
    combined_length = remaining_length_a if points_per_100_sqm_a <= 23 else remaining_length_b
    combined_points_per_100_sqm = points_per_100_sqm_a if points_per_100_sqm_a <= 23 else points_per_100_sqm_b

# Ensure the combined length is at least 80 meters and points per 100 sqm is below 23
if combined_length < 80:
    if points_per_100_sqm_a <= 23:
        combined_length += remaining_length_b
        combined_points_per_100_sqm = (points_a + points_b + cut_penalty) * 100 / (combined_length * fabric_width)
    elif points_per_100_sqm_b <= 23:
        combined_length += remaining_length_a
        combined_points_per_100_sqm = (points_a + points_b + cut_penalty) * 100 / (combined_length * fabric_width)

print(f"Final Combined Fabric: Length = {combined_length}, Points per 100 sqm = {combined_points_per_100_sqm}")

# Visualize the cuts and joining
visualize_cuts_and_join(
    [fabric_a_length, fabric_b_length],
    [fabric_a_defects, fabric_b_defects],
    [cut_positions_a, cut_positions_b],
    "Fabric Cuts and Joined Fabric",
    [cut_ranges_a, cut_ranges_b]
)
