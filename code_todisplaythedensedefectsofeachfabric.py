import matplotlib.pyplot as plt
import numpy as np

# Defect data for fabric rolls
fabric_a_defects = [
    (2, 2, 4), (5, 5, 4), (10, 10, 1), (22, 22, 4), 
    (23, 23, 4), (28, 28, 4), (35, 35, 2), (39, 39, 4), 
    (46, 46, 2), (70, 70, 2)
]
fabric_a_length = 88.7
fabric_width = 1.5
cut_penalty = 4


def calculate_points_and_ratio(defects, length, width):
    total_points = sum(defect[2] for defect in defects)
    points_per_100_sqm = (total_points * 100) / (length * width)
    return total_points, points_per_100_sqm


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




min_remaining_length_ratio = 0.65
cut_positions_a, points_per_100_sqm_a, remaining_length_a, cut_ranges_a = maximize_remaining_length_with_cut_penalty(fabric_a_defects, fabric_a_length, fabric_width, 23, cut_penalty, min_remaining_length_ratio)


