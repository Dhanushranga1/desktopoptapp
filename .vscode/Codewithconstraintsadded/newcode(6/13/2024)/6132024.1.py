import matplotlib.pyplot as plt

def calculate_pphms(defects, total_length, width):
    # Calculate the pphms for the original fabric
    total_defect_points = sum(d['points'] if isinstance(d['points'], int) else 0 for d in defects)
    original_pphms = (total_defect_points * 100) / (width * total_length)
    return original_pphms

def remove_bad_sections(defects, total_length, width):
    sections_to_remove = []
    current_length = 0
    good_sections = []

    for defect in defects:
        if defect['from'] > current_length:
            good_sections.append({"from": current_length, "to": defect['from'], "points": 0})

        if isinstance(defect['points'], str) or defect['points'] == 4:
            sections_to_remove.append(defect)
            current_length = defect['to']
        else:
            if defect['points'] > 0:
                good_sections[-1]['to'] = defect['to']
                good_sections[-1]['points'] += defect['points']

        current_length = max(current_length, defect['to'])

    if current_length < total_length:
        good_sections.append({"from": current_length, "to": total_length, "points": 0})

    return good_sections, sections_to_remove

def calculate_good_fabric_pphms(good_sections, width, join_penalty):
    total_good_length = sum(section['to'] - section['from'] for section in good_sections)
    total_good_points = sum(section['points'] for section in good_sections) + join_penalty
    good_pphms = (total_good_points * 100) / (width * total_good_length)
    return good_pphms, total_good_length

def plot_fabric_sections(defects, good_sections, sections_to_remove, total_length):
    fig, ax = plt.subplots(figsize=(12, 2))
    ax.set_xlim(0, total_length)
    ax.set_ylim(0, 1)

    for section in good_sections:
        ax.plot([section['from'], section['to']], [0.5, 0.5], color='green', lw=8, solid_capstyle='butt')

    for section in sections_to_remove:
        ax.plot([section['from'], section['to']], [0.5, 0.5], color='red', lw=8, solid_capstyle='butt')

    for defect in defects:
        ax.text(defect['from'], 0.55, f"{defect['points']}", color='black', ha='center', va='bottom', fontsize=8)

    plt.xlabel('Fabric Length (meters)')
    plt.title('Fabric Defect Map and Sections')
    plt.yticks([])
    plt.show()

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
pphms_threshold = 23
join_penalty = 4 * 3

original_pphms = calculate_pphms(defects, total_length, width)
good_sections, sections_to_remove = remove_bad_sections(defects, total_length, width)
good_pphms, total_good_length = calculate_good_fabric_pphms(good_sections, width, join_penalty)

# Display results
print(f"Original PPHMS: {original_pphms:.2f}")
print("Sections to remove:")
for section in sections_to_remove:
    print(section)
print("Good sections:")
for section in good_sections:
    print(section)
print(f"Final PPHMS after removal and joining: {good_pphms:.2f}")
print(f"Total length of good fabric: {total_good_length:.2f} meters")

# Plot the sections
plot_fabric_sections(defects, good_sections, sections_to_remove, total_length)
