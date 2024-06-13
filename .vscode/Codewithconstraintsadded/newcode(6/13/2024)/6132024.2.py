import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns

def calculate_pphms(defects, total_length, width):
    total_defect_points = sum(d['points'] if isinstance(d['points'], int) else 0 for d in defects)
    return (total_defect_points * 100) / (width * total_length)

def remove_sections(defects, total_length, width, threshold_pphms):
    sections_to_remove = []
    good_sections = []
    current_start = 0

    for defect in defects:
        if isinstance(defect['points'], str) or defect['points'] == 4:
            sections_to_remove.append((defect['from'], defect['to']))
        elif defect['points'] > 0:
            if not sections_to_remove or defect['from'] > sections_to_remove[-1][1] + 1:
                sections_to_remove.append((defect['from'], defect['to']))
            else:
                sections_to_remove[-1] = (sections_to_remove[-1][0], defect['to'])

    combined_good_sections = []
    if sections_to_remove[0][0] > 0:
        combined_good_sections.append((0, sections_to_remove[0][0]))

    for i in range(1, len(sections_to_remove)):
        if sections_to_remove[i][0] > sections_to_remove[i - 1][1] + 1:
            combined_good_sections.append((sections_to_remove[i - 1][1] + 1, sections_to_remove[i][0]))

    if sections_to_remove[-1][1] < total_length:
        combined_good_sections.append((sections_to_remove[-1][1] + 1, total_length))

    return combined_good_sections, sections_to_remove

def calculate_section_pphms(defects, start, end, width):
    section_length = end - start
    section_points = sum(defect['points'] for defect in defects if defect['from'] >= start and defect['to'] <= end)
    return (section_points * 100) / (section_length * width)

def calculate_good_fabric_pphms(good_sections, defects, width, join_penalty):
    total_good_length = sum(end - start for start, end in good_sections)
    total_good_points = sum(calculate_section_pphms(defects, start, end, width) * (end - start) for start, end in good_sections) + join_penalty
    good_pphms = (total_good_points * 100) / (width * total_good_length)
    return good_pphms, total_good_length

def plot_fabric_sections(total_length, good_sections, removed_sections, width):
    fig, ax = plt.subplots(figsize=(12, 2))
    ax.set_xlim(0, total_length)
    ax.set_ylim(0, 1)

    for start, end in good_sections:
        ax.add_patch(patches.Rectangle((start, 0.25), end - start, 0.5, edgecolor='black', facecolor='green'))

    for start, end in removed_sections:
        ax.add_patch(patches.Rectangle((start, 0.25), end - start, 0.5, edgecolor='black', facecolor='red'))

    for defect in defects:
        ax.text(defect['from'], 0.75, f"{defect['points']}", color='black', ha='center', va='bottom', fontsize=8)

    plt.xlabel('Fabric Length (meters)')
    plt.title('Fabric Defect Map and Sections')
    plt.yticks([])
    plt.show()

def main(defects, total_length, width, threshold_pphms):
    original_pphms = calculate_pphms(defects, total_length, width)
    print(f"Original PPHMS: {original_pphms:.2f}")

    good_sections, removed_sections = remove_sections(defects, total_length, width, threshold_pphms)

    join_penalty = 4 * (len(good_sections) - 1)
    good_pphms, total_good_length = calculate_good_fabric_pphms(good_sections, defects, width, join_penalty)

    print(f"Final PPHMS after removal and joining: {good_pphms:.2f}")
    print(f"Total length of good fabric: {total_good_length:.2f} meters")
    print("Sections to remove:", removed_sections)
    print("Good sections:", good_sections)

    plot_fabric_sections(total_length, good_sections, removed_sections, width)

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

main(defects, total_length, width, threshold_pphms)
