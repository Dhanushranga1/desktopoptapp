import matplotlib.pyplot as plt

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
    defect_density = (total_points / (length * width)) * 100.0
    return defect_density

# Function to identify and remove sections based on defect density
def identify_and_remove_sections(defects, length, width, max_gap, max_removals):
    sections = [(0, length)]
    removed_sections = []

    for defect in defects:
        if defect["points"] == 'continuous':
            start = defect["from"]
            end = defect["to"]
            for section in sections[:]:
                if section[0] < start < section[1]:
                    sections.remove(section)
                    sections.append((section[0], start))
                    sections.append((end, section[1]))

    for _ in range(max_removals):
        max_density = 0
        section_to_remove = None
        for section in sections:
            density = calculate_defect_density(defects, section[0], section[1], width)
            if density > max_density:
                max_density = density
                section_to_remove = section
        if section_to_remove and max_density > threshold:
            sections.remove(section_to_remove)
            removed_sections.append(section_to_remove)

            # Split the section around dense defects within max_gap
            dense_defects = [
                defect for defect in defects
                if section_to_remove[0] <= defect["from"] <= section_to_remove[1]
                and defect["points"] != 'continuous'
            ]

            for defect in dense_defects:
                sections.append((section_to_remove[0], defect["from"]))
                section_to_remove = (defect["to"], section_to_remove[1])
            if section_to_remove[0] < section_to_remove[1]:
                sections.append(section_to_remove)

    return sections, removed_sections

# Identify and remove dense sections
good_sections, removed_sections = identify_and_remove_sections(defects, total_length, total_width, max_gap, max_removals)

# Function to calculate the total defect density for given sections
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

# Calculate the total defect density for the remaining good sections
total_density = total_defect_density(good_sections, defects, total_width)

# Visualize the sections using matplotlib
fig, ax = plt.subplots(figsize=(12, 6))
y = 1

for section in good_sections:
    density = calculate_defect_density(defects, section[0], section[1], total_width)
    ax.plot([section[0], section[1]], [y, y], linewidth=6, label=f'{section[0]}-{section[1]}m, Density: {density:.2f}')
    y -= 1

# Calculate total retained fabric
total_retained_fabric = sum(end - start for start, end in good_sections)
total_retained_percentage = (total_retained_fabric / total_length) * 100

ax.set_yticks([])
ax.set_xlabel('Length (m)')
ax.set_title(f'Fabric Sections After Defect Removal (Retained: {total_retained_percentage:.2f}%)')
ax.legend()

plt.show()
