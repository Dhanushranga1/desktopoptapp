import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns

def calculate_pphms(defects, total_length, width):
    total_defect_points = sum(d['points'] if isinstance(d['points'], int) else 0 for d in defects)
    return (total_defect_points * 100) / (width * total_length)

def calculate_section_pphms(defects, start, end, width):
    section_length = end - start
    section_points = sum(defect['points'] if isinstance(defect['points'], int) else 0 for defect in defects if defect['from'] >= start and defect['to'] <= end)
    if section_length == 0 or width == 0:
        return 0  # or any other default value you want to return
    return (section_points * 100) / (section_length * width)

def find_sections_to_remove(defects, total_length, width, threshold_pphms, max_gap):
    sections_to_remove = []
    current_start = 0
    current_end = 0

    for defect in defects:
        if isinstance(defect['points'], str) or defect['points'] == 4:
            if current_end == 0:
                current_start = defect['from']
                current_end = defect['to']
            elif defect['from'] <= current_end + max_gap:
                current_end = defect['to']
            else:
                sections_to_remove.append((current_start, current_end))
                current_start = defect['from']
                current_end = defect['to']
    if current_end != 0:
        sections_to_remove.append((current_start, current_end))

    return sections_to_remove

def calculate_good_fabric(defects, total_length, width, sections_to_remove):
    good_sections = []
    last_end = 0

    for start, end in sections_to_remove:
        if last_end < start:
            good_sections.append((last_end, start))
        last_end = end
    if last_end < total_length:
        good_sections.append((last_end, total_length))

    join_penalty = 4 * (len(good_sections) - 1)
    total_good_length = sum(end - start for start, end in good_sections)
    total_good_points = sum(calculate_section_pphms(defects, start, end, width) * (end - start) for start, end in good_sections) + join_penalty
    good_pphms = (total_good_points * 100) / (width * total_good_length)
    return good_pphms, total_good_length, good_sections

def plot_fabric_sections(total_length, good_sections, removed_sections, width):
    fig, ax = plt.subplots(figsize=(12, 2))
    ax.set_xlim(0, total_length)
    ax.set_ylim(0, 1)

    for start, end in good_sections:
        ax.add_patch(patches.Rectangle((start, 0.25), end - start, 0.5, edgecolor='black', facecolor='green'))

    for start, end in removed_sections:
        ax.add_patch(patches.Rectangle((start, 0.25), end - start, 0.5, edgecolor='black', facecolor='red'))

    plt.xlabel('Fabric Length (meters)')
    plt.title('Fabric Defect Map and Sections')
    plt.yticks([])
    plt.show()

def main(defects, total_length, width, threshold_pphms, min_acceptable_length_ratio, max_gap):
    original_pphms = calculate_pphms(defects, total_length, width)
    print(f"Original PPHMS: {original_pphms:.2f}")

    sections_to_remove = find_sections_to_remove(defects, total_length, width, threshold_pphms, max_gap)
    good_pphms, total_good_length, good_sections = calculate_good_fabric(defects, total_length, width, sections_to_remove)

    while good_pphms > threshold_pphms or total_good_length < min_acceptable_length_ratio * total_length:
        max_defect_section = max(sections_to_remove, key=lambda x: calculate_section_pphms(defects, x[0], x[1], width), default=None)
        if max_defect_section in sections_to_remove:
            sections_to_remove.remove(max_defect_section)
        good_pphms, total_good_length, good_sections = calculate_good_fabric(defects, total_length, width, sections_to_remove)

    print(f"Final PPHMS after removal and joining: {good_pphms:.2f}")
    print(f"Total length of good fabric: {total_good_length:.2f} meters")
    print("Sections to remove:", sections_to_remove)
    print("Good sections:", good_sections)

    plot_fabric_sections(total_length, good_sections, sections_to_remove, width)

# Data
defects = [
    {"from": 7, "to": 7, "points": 1},
    {"from": 15, "to": 15, "points": 1},
    {"from": 15.3, "to": 18.5, "points": "continuous defect"},
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

total_length = 103
width = 1.5
threshold_pphms = 23
min_acceptable_length_ratio = 0.85
max_gap = 5

main(defects, total_length, width, threshold_pphms, min_acceptable_length_ratio, max_gap)
