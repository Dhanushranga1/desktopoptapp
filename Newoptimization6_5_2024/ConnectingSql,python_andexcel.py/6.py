import matplotlib.pyplot as plt
import numpy as np

# Total length and width of the fabric
total_length = 103
total_width = 1.5
retain_ratio = 0.75
min_retain_length = total_length * retain_ratio
threshold = 23
max_gap = 3
max_removals = 3  # Maximum number of sections that can be removed

# Defect data
defects = [
    {"from": 7, "to": 7, "points": 1},
    {"from": 15, "to": 15, "points": 1},
    {"from": 15.3, "to": 18.5, "points": 'continuous'},
    {"from": 23, "to": 23, "points": 4},
    {"from": 25, "to": 25, "points": 1},
    {"from": 28, "to": 28, "points": 4},
    {"from": 30, "to": 30, "points": 1},
    {"from": 41, "to": 41, "points": 4},
    {"from": 50, "to": 52, "points": 1},
    {"from": 66, "to": 66, "points": 4},
    {"from": 68, "to": 68, "points": 4},
    {"from": 71, "to": 71, "points": 1},
    {"from": 76, "to": 76, "points": 4},
    {"from": 78, "to": 78, "points": 4},
    {"from": 79, "to": 79, "points": 4}
]

# Function to calculate defect density
def calculate_defect_density(defects, start, end, width):
    total_points = 0
    for defect in defects:
        if defect["to"] >= start and defect["from"] <= end:
            if defect["points"] == 'continuous':
                return float('inf')  # Continuous defect needs removal
            total_points += defect["points"]
    length = end - start
    defect_density = (total_points / (length * width)) * 100
    return defect_density

# Function to split sections based on continuous defects
def split_sections(defects, length):
    sections = []
    current_start = 0
    for defect in defects:
        if defect["points"] == 'continuous':
            if defect["from"] > current_start:
                sections.append((current_start, defect["from"]))
            current_start = defect["to"]
    if current_start < length:
        sections.append((current_start, length))
    return sections

# Separate continuous defects and normal defects
continuous_defects = [defect for defect in defects if defect["points"] == 'continuous']
normal_defects = [defect for defect in defects if defect["points"] != 'continuous']

# Get the initial sections after removing continuous defects
initial_sections = split_sections(continuous_defects, total_length)

# Function to split and remove sections based on density and minimum retain length
def split_and_remove_sections(sections, defects, width, threshold, min_length, max_removals):
    retained_sections = sections[:]
    removals = 0
    while total_defect_density(retained_sections, defects, width) > threshold and removals < max_removals:
        max_density = 0
        section_to_remove = None
        for section in retained_sections:
            density = calculate_defect_density(defects, section[0], section[1], width)
            if density > max_density:
                max_density = density
                section_to_remove = section
        if section_to_remove:
            retained_sections.remove(section_to_remove)
            removals += 1
            total_length_retained = sum(end - start for start, end in retained_sections)
            if total_length_retained < min_length:
                retained_sections.append(section_to_remove)
                break
    return retained_sections

# Calculate the total defect density for given sections
def total_defect_density(sections, defects, width):
    total_points = 0
    total_area = 0
    for start, end in sections:
        length = end - start
        area = length * width
        for defect in defects:
            if defect["to"] >= start and defect["from"] <= end:
                if defect["points"] == 'continuous':
                    return float('inf')  # Continuous defect needs removal
                total_points += defect["points"]
        total_area += area
    return (total_points / total_area) * 100

# Split and remove dense sections while ensuring minimum length and density threshold
final_sections = split_and_remove_sections(initial_sections, normal_defects, total_width, threshold, min_retain_length, max_removals)

# Visualize the sections using matplotlib
fig, ax = plt.subplots(figsize=(12, 6))
y = 1

for section in final_sections:
    density = calculate_defect_density(normal_defects, section[0], section[1], total_width)
    ax.plot([section[0], section[1]], [y, y], linewidth=6, label=f'{section[0]}-{section[1]}m, Density: {density:.2f}')
    y -= 1

# Calculate total retained fabric
total_retained_fabric = sum(end - start for start, end in final_sections)
total_retained_percentage = (total_retained_fabric / total_length) * 100

ax.set_yticks([])
ax.set_xlabel('Length (m)')
ax.set_title(f'Fabric Sections After Defect Removal (Retained: {total_retained_percentage:.2f}%)')
ax.legend()

plt.show()
